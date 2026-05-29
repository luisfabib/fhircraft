"""
Index-based FHIR type registry.

Provides a per-release :class:`TypeRegistry` that maps type names and canonical
URLs to Python classes, backed by the existing ``.manifest.json`` definition index.
"""

from __future__ import annotations

import importlib
import re
from pathlib import Path
from threading import Lock
from typing import Any, Literal, overload, TYPE_CHECKING

from fhircraft.fhir.resources.indexer import Manifest, ManifestEntry
from fhircraft.utils import to_snake_case, capitalize

if TYPE_CHECKING:
    from fhircraft.fhir.resources.base import FHIRBaseModel

# Supported FHIR releases that have a definitions manifest
SUPPORTED_RELEASES = ("R4", "R4B", "R5")

# Definitions directory: …/fhircraft/fhir/resources/definitions/
_DEFINITIONS_DIR = Path(__file__).parent.parent / "definitions"

# ---------------------------------------------------------------------------
# TypeRegistry
# ---------------------------------------------------------------------------


class TypeRegistry:
    """Per-release index mapping FHIR type names and canonical URLs to Python types.

    All classes are imported lazily on first access.

    Args:
        release: FHIR release string, e.g. ``"R4B"``.
    """

    def __init__(self, release: str) -> None:
        self.release = release
        self._manifest: Manifest = Manifest.load(
            _DEFINITIONS_DIR / release / ".manifest.json"
        )
        # name → Python type  (both PascalCase and manifest camelCase for primitives)
        self._by_name: dict[str, type[FHIRBaseModel]] = {}
        # canonical url → Python type
        self._by_url: dict[str, type[FHIRBaseModel]] = {}
        self._lock = Lock()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_by_name(self, name: str) -> type[FHIRBaseModel] | None:
        """Return the Python type for a FHIR type *name*, or ``None``.

        Accepts both the Python PascalCase name used in the datatypes modules
        (``"Boolean"``, ``"Observation"``) and the manifest camelCase name used
        for primitive types (``"boolean"``, ``"dateTime"``).
        """
        if name in self._by_name:
            return self._by_name[name]

        # Resolve via manifest: try exact name first, then case-insensitive scan
        urls = self._manifest.by_name.get(name)
        if not urls:
            lower = name.lower()
            for manifest_name, manifest_urls in self._manifest.by_name.items():
                if manifest_name.lower() == lower:
                    urls = manifest_urls
                    break
        if not urls:
            return None

        entry = self._manifest.definitions.get(self._manifest.by_url.get(urls[0], ""))
        if entry is None:
            return None

        python_type = self._load_type(entry)
        if python_type is not None:
            with self._lock:
                self._by_name[name] = python_type
                self._by_url[entry.url] = python_type
        return python_type

    def get_by_url(self, url: str) -> type[FHIRBaseModel] | None:
        """Return the Python type for a canonical FHIR URL, or ``None``.

        The factory singleton's ``construction_cache`` is checked first so that
        profiled resources built via :class:`~fhircraft.fhir.resources.factory.FHIRModelFactory`
        are also reachable by their canonical URL alongside built-in types.
        """
        # Factory construction_cache has priority (includes runtime-profiled resources)
        factory_type = self._check_factory_cache(url)
        if factory_type is not None:
            return factory_type

        if url in self._by_url:
            return self._by_url[url]

        filename = self._manifest.by_url.get(url)
        if not filename:
            return None
        entry = self._manifest.definitions.get(filename)
        if entry is None:
            return None

        python_type = self._load_type(entry)
        if python_type is not None:
            with self._lock:
                self._by_url[url] = python_type
                self._by_name[entry.name] = python_type
        return python_type

    def get_entry(self, url: str) -> ManifestEntry | None:
        """Return the :class:`ManifestEntry` for a canonical URL without loading the class.

        Useful for inspecting metadata (``kind``, ``fhir_version``, ``has_snapshot``,
        etc.) cheaply, without triggering a module import.
        """
        filename = self._manifest.by_url.get(url)
        if not filename:
            return None
        return self._manifest.definitions.get(filename)

    def all_urls(self, kind: str | None = None) -> list[str]:
        """Return all canonical URLs known to this registry.

        Args:
            kind: Optional filter — one of ``"primitive-type"``, ``"complex-type"``,
                  ``"resource"``.  When ``None`` all URLs are returned.
        """
        if kind is None:
            return list(self._manifest.by_url.keys())
        return [
            entry.url
            for entry in self._manifest.definitions.values()
            if entry.kind == kind
        ]

    def all_names(self, kind: str | None = None) -> list[str]:
        """Return all type names known to this registry.

        Args:
            kind: Optional filter — same values as :meth:`all_urls`.
        """
        if kind is None:
            return list(self._manifest.by_name.keys())
        return [
            entry.name
            for entry in self._manifest.definitions.values()
            if entry.kind == kind
        ]

    def __repr__(self) -> str:  # pragma: no cover
        return f"TypeRegistry(release={self.release!r}, entries={len(self._manifest.definitions)})"

    def _load_type(self, entry: ManifestEntry) -> type[FHIRBaseModel] | None:
        """Load the Python class for a :class:`ManifestEntry`, returning ``None`` on failure."""

        # Complex types and resources: derive module path from PascalCase name
        try:
            module = importlib.import_module(self._build_module_path(entry))
            obj: type = getattr(module, capitalize(entry.name))
            # Trigger Pydantic model rebuild if forward refs are unresolved.
            # We must pass an explicit namespace so that forward references like
            # "Extension" (which only appear under TYPE_CHECKING in element.py)
            # can be resolved regardless of which frame calls model_rebuild.
            if not getattr(obj, "__pydantic_complete__", True):
                complex_pkg = importlib.import_module(
                    f"fhircraft.fhir.resources.datatypes.{self.release}.complex"
                )
                prim_pkg = importlib.import_module(
                    f"fhircraft.fhir.resources.datatypes.{self.release}.primitive"
                )
                obj.model_rebuild(  # type: ignore[union-attr]
                    _types_namespace={**vars(prim_pkg), **vars(complex_pkg)}
                )
            return obj
        except (ImportError, AttributeError):
            return None

    def _build_module_path(self, entry: ManifestEntry) -> str:
        """Derive the dotted module import path for a complex type or resource."""
        snake = to_snake_case(entry.name)
        match entry.kind:
            case "primitive-type":
                tier = "primitive"
            case "complex-type":
                tier = "complex"
            case "resource":
                tier = "core"
            case _:
                raise ValueError(f"Unknown entry kind: {entry.kind}")
        return f"fhircraft.fhir.resources.datatypes.{self.release}.{tier}.{snake}"

    @staticmethod
    def _check_factory_cache(url: str) -> type | None:
        """Check the factory singleton's ``construction_cache`` for *url*."""
        try:
            # Lazy import to avoid circular dependency (factory → datatypes → registry)
            from fhircraft.fhir.resources import (
                factory as _factory_module,
            )  # noqa: PLC0415

            return _factory_module.factory.construction_cache.get(url)  # type: ignore[return-value]
        except (ImportError, AttributeError):
            return None


# ---------------------------------------------------------------------------
# Module-level per-release singletons
# ---------------------------------------------------------------------------

_registry_cache: dict[str, TypeRegistry] = {}
_registry_lock = Lock()


def get_registry(release: str = "R4B") -> TypeRegistry:
    """Return the :class:`TypeRegistry` singleton for the given FHIR *release*.

    Registries are constructed lazily on first access and then reused.

    Args:
        release: FHIR release string — one of ``"R4"``, ``"R4B"``, ``"R5"``.

    Returns:
        The singleton :class:`TypeRegistry` for the requested release.
    """
    if release not in _registry_cache:
        with _registry_lock:
            if release not in _registry_cache:
                _registry_cache[release] = TypeRegistry(release)
    return _registry_cache[release]


@overload
def get_fhir_type(
    type_str: str, release: str, fail_if_not_found: Literal[True] = True
) -> type[FHIRBaseModel]: ...


@overload
def get_fhir_type(
    type_str: str, release: str, fail_if_not_found: Literal[False] = False
) -> type[FHIRBaseModel] | None: ...


def get_fhir_type(
    type_str: str, release: str, fail_if_not_found: bool = True
) -> type[FHIRBaseModel] | None:
    """
    Get the FHIR type (primitive, complex, or resource) by its string name.

    Args:
        type_str (str): The FHIR type name.
        release (str): The FHIR release version, e.g. `"R4B"`.
        fail_if_not_found (bool): Whether to raise an error if the type is not found (default: True).

    Returns:
        The corresponding FHIR type class, or None if not found and fail_if_not_found is False.

    Raises:
        AttributeError: If the type is not found and `fail_if_not_found` is True.
    """
    result = get_registry(release).get_by_name(type_str)
    if fail_if_not_found and result is None:
        raise AttributeError(f"No FHIR {release} type found for name: {type_str}")
    return result


@overload
def get_fhir_type_by_url(
    url: str, release: str, fail_if_not_found: Literal[True] = True
) -> type[FHIRBaseModel]: ...


@overload
def get_fhir_type_by_url(
    url: str, release: str, fail_if_not_found: Literal[False] = False
) -> type[FHIRBaseModel] | None: ...


def get_fhir_type_by_url(
    url: str, release: str, fail_if_not_found: bool = True
) -> type[FHIRBaseModel] | None:
    """Return the FHIR type (primitive, complex, or resource) for a canonical URL.

    Args:
        url: The canonical FHIR URL, e.g. `"http://hl7.org/fhir/StructureDefinition/Observation"`.
        release: The FHIR release version, e.g. `"R4B"`.
        fail_if_not_found: Whether to raise an error if the type is not found (default: True).

    Returns:
        The corresponding Python type class.

    Raises:
        AttributeError: If no type is found for the given URL and `fail_if_not_found` is ``True``.
    """
    result = get_registry(release).get_by_url(url)
    if fail_if_not_found and result is None:
        raise AttributeError(f"No FHIR {release} type found for URL: {url}")
    return result
