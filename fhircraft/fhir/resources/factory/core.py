"""
ProfileFactory — the top-level façade for building Pydantic models from FHIR
``StructureDefinition`` objects.

This is the main public entry point; the rest of the pipeline (resolver,
assembler, builders, validators) is invoked from here.

Usage::

    factory = ProfileFactory(repository)
    factory.register_sd_dict(my_profile_dict)   # pre-register dependency
    model = factory.build(sd=my_profile_sd)
"""

from __future__ import annotations

import inspect
import keyword
import warnings
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Sequence, TYPE_CHECKING

from pydantic import BaseModel, Field, create_model

from fhircraft.fhir.resources.base import (
    FHIRBaseModel,
    FHIRSliceModel,
    FhirBaseModelKind,
)
from fhircraft.fhir.resources.datatypes.utils import get_complex_FHIR_type
from fhircraft.fhir.resources.factory.assembler import ModelAssembler
from fhircraft.fhir.resources.factory.context import BuildContext
from fhircraft.fhir.resources.factory.exceptions import (
    DefinitionResolutionError,
)
from fhircraft.fhir.resources.factory.index import DefinitionIndex
from fhircraft.fhir.resources.factory.resolver import SnapshotResolver
from fhircraft.fhir.resources.repository import CompositeStructureDefinitionRepository
from fhircraft.utils import get_FHIR_release_from_version

if TYPE_CHECKING:
    from fhircraft.fhir.resources.datatypes.R4.core import (
        StructureDefinition as R4_StructureDefinition,
    )
    from fhircraft.fhir.resources.datatypes.R4B.core import (
        StructureDefinition as R4B_StructureDefinition,
    )
    from fhircraft.fhir.resources.datatypes.R5.core import (
        StructureDefinition as R5_StructureDefinition,
    )


class FHIRStructureFactory:
    """
    Builds Pydantic models from FHIR ``StructureDefinition`` objects.

    **Pipeline** (per call to :meth:`build`):

    1. Normalise the input (dict → Pydantic SD object, URL → fetch from repo).
    2. Cache-check (return cached model if already built).
    3. Detect FHIR version → create a :class:`BuildContext` with a
       :class:`TypeRegistry`.
    4. Resolve ``baseDefinition`` → obtain *base_model* and *base_index*.
    5. :class:`SnapshotResolver` → fully resolved :class:`DefinitionIndex`.
    6. :class:`ModelAssembler` → Pydantic model class.
    7. Post-build: set ``meta.profile`` default, attach ``_fhir_release`` etc.
    8. Cache under canonical URL; return.

    To build a profile that depends on another profile, register the dependency
    first via :meth:`register`::

        factory.register(base_sd)        # builds + registers base
        model = factory.build(profile_sd)  # base is now in TypeRegistry

    Args:
        repository: A :class:`CompositeStructureDefinitionRepository`.  A
            default instance is created when omitted.
        internet_enabled: Whether to enable internet access in the repository.
        enable_packages: Whether to enable FHIR-package support.
        registry_base_url: Override for the FHIR package registry URL.
        timeout: HTTP request timeout for package downloads.
    """

    def __init__(
        self,
        repository: CompositeStructureDefinitionRepository | None = None,
        internet_enabled: bool = True,
        enable_packages: bool = True,
        registry_base_url: str | None = None,
        timeout: float = 30.0,
    ) -> None:
        if repository is None:
            self.repository = CompositeStructureDefinitionRepository(
                internet_enabled=internet_enabled,
                enable_packages=enable_packages,
                registry_base_url=registry_base_url,
                timeout=timeout,
            )
        else:
            self.repository = repository

        # Global cache: canonical URL → built Pydantic model
        self.construction_cache: dict[str, type[BaseModel]] = {}

    # ------------------------------------------------------------------
    # Main entry points
    # ------------------------------------------------------------------

    def build(
        self,
        structure_definition: Any = None,
        *,
        canonical_url: str | None = None,
        mixins: Sequence[type] | None = None,
    ) -> type[BaseModel]:
        """
        Build and return a Pydantic model for the given ``StructureDefinition``.

        Args:
            structure_definition: The ``StructureDefinition`` to build from.  Accepted forms:

                * A parsed ``R4 / R4B / R5 StructureDefinition`` Pydantic object
                * A ``dict`` (will be validated as a ``StructureDefinition``)
                * A file path string (``*.json`` / ``*.yaml``)
                * A canonical URL string (fetched from the repository)
                * ``None`` — requires *canonical_url* to be set

            canonical_url: Canonical URL to look up when *sd* is ``None``.
            mixins: Optional extra base classes added to the constructed model
                (e.g. ``(FHIRSliceModel,)``).

        Returns:
            A Pydantic model class representing the FHIR resource / profile.

        Raises:
            ValueError: For invalid / missing inputs.
            DefinitionResolutionError: When the differential cannot be resolved.
            UnregisteredTypeError: When a required type is not in the registry.
        """
        structure_definition = self._normalise_sd(structure_definition, canonical_url)
        # Cache check
        if structure_definition.url in self.construction_cache:
            return self.construction_cache[structure_definition.url]

        return self._build(structure_definition, mixins=mixins)

    # ------------------------------------------------------------------
    # Internal build pipeline
    # ------------------------------------------------------------------

    def _build(
        self,
        structure_def: "R4_StructureDefinition | R4B_StructureDefinition | R5_StructureDefinition",
        mixins: Sequence[type] | None = None,
        mode: Literal["auto", "snapshot", "differential"] = "auto",
    ) -> type[BaseModel]:

        sd_url = structure_def.url or ""
        sd_name = structure_def.name or ""
        fhir_version = structure_def.fhirVersion or ""

        if not sd_name:
            raise ValueError("StructureDefinition must have a valid 'name'.")
        if not fhir_version:
            raise ValueError(
                "StructureDefinition must specify 'fhirVersion'. "
                "Set it explicitly if building from a dict."
            )

        fhir_release = get_FHIR_release_from_version(fhir_version)
        sanitized_name = self._sanitize_name(sd_name)

        # ------------------------------------------------------------------
        # Resolve base definition
        # ------------------------------------------------------------------
        base_canonical = structure_def.baseDefinition
        base_model: type = FHIRBaseModel

        if base_canonical:
            # Try directly from registry / datatypes first (fast path)
            resolved = ctx.resolve_type_safe(base_canonical)
            if resolved is not None and issubclass(resolved, FHIRBaseModel):
                base_model = resolved
            else:
                # Try to build from repository
                try:
                    base_model = self.build(canonical_url=base_canonical)
                except Exception as exc:
                    warnings.warn(
                        f"Could not resolve base definition '{base_canonical}' for "
                        f"'{sd_name}': {exc}.  Using FHIRBaseModel as fallback."
                    )
                    base_model = FHIRBaseModel

            # Obtain the base snapshot for differential resolution
            base_definition = self.repository.get(base_canonical, fhir_version)
            if base_definition.snapshot and base_definition.snapshot.element:
                base_index = DefinitionIndex.from_elements(
                    base_definition.snapshot.element
                )
            else:
                raise DefinitionResolutionError(
                    f"Base definition '{base_canonical}' for '{sd_name}' has no snapshot or elements."
                )

        # ------------------------------------------------------------------
        # Produce the complete DefinitionIndex
        # ------------------------------------------------------------------
        resolver = SnapshotResolver(self.repository, fhir_version=fhir_version)
        definition_index = resolver.resolve(structure_def, base_index, mode=mode)

        # ------------------------------------------------------------------
        # Assemble the Pydantic model
        # ------------------------------------------------------------------
        base_classes: tuple[type, ...] = (base_model,)
        if mixins:
            base_classes = (base_model, *mixins)

        assembler = ModelAssembler(
            index=definition_index,
            ctx=BuildContext(
                fhir_release=fhir_release,
                fhir_version=fhir_version,
                repository=self.repository,
                factory=self,
                base=base_model,
            ),
            resource_name=sanitized_name,
        )
        model = assembler.assemble(sanitized_name, base=base_classes)

        # ------------------------------------------------------------------
        # Override / inject meta.profile default
        # ------------------------------------------------------------------
        if sd_url:
            has_meta = "meta" in model.model_fields or (
                issubclass(base_model, BaseModel) and "meta" in base_model.model_fields
            )
            if has_meta:
                try:
                    Meta = get_complex_FHIR_type("Meta", fhir_release)
                    meta_field: tuple = (
                        Optional[Meta],
                        Field(
                            title="Meta",
                            description="Metadata about the resource.",
                            default=Meta(profile=[sd_url]),
                        ),
                    )
                    model = create_model(
                        sanitized_name,
                        meta=meta_field,
                        __base__=model,
                    )
                except Exception:
                    pass  # non-fatal

        # ------------------------------------------------------------------
        # Attach structural class metadata
        # ------------------------------------------------------------------
        if issubclass(model, FHIRBaseModel):
            model._fhir_release = fhir_release
            model._canonical_url = structure_def.url
            model._kind = (
                FhirBaseModelKind(structure_def.kind)
                if structure_def.kind
                else FhirBaseModelKind.LOGICAL
            )
            model._type = structure_def.type or sd_name
            abstract = structure_def.abstract
            if abstract is not None:
                model._abstract = bool(abstract)
            elif issubclass(base_model, FHIRBaseModel) and hasattr(
                base_model, "_abstract"
            ):
                model._abstract = base_model._abstract
            else:
                model._abstract = False

        # ------------------------------------------------------------------
        # Cache and register
        # ------------------------------------------------------------------
        if sd_url:
            self.construction_cache[sd_url] = model
        return model

    # ------------------------------------------------------------------
    # Input normalisation
    # ------------------------------------------------------------------

    def _normalise_sd(
        self,
        sd: Any,
        canonical_url: str | None,
    ) -> "R4_StructureDefinition | R4B_StructureDefinition | R5_StructureDefinition":
        """
        Normalise *sd* (dict / str / Pydantic SD / ``None``) to a validated
        ``StructureDefinition`` Pydantic object, fetching from the repository
        when necessary.
        """

        if getattr(sd, "_resource_type", None) == "StructureDefinition":
            self.repository.add(sd)
            return sd

        if isinstance(sd, dict):
            self.repository.load_from_definitions(sd)
            url = sd.get("url", "")
            if url:
                return self.repository.get(url)
            else:
                raise ValueError(
                    "No URL found in the provided StructureDefinition dictionary."
                )

        if isinstance(sd, str) and sd.startswith("http"):
            # Canonical URL
            return self.repository.get(sd)

        if isinstance(sd, str):
            # File path
            loaded = self.repository.load_from_files(Path(sd))
            if loaded:
                return loaded[0] if isinstance(loaded, list) else loaded

            raise ValueError(
                "No StructureDefinition provided. Pass a parsed SD object, a dict, "
                "a file path, or a canonical URL."
            )

        if sd is None and canonical_url:
            return self.repository.get(canonical_url)

        return sd

    # ------------------------------------------------------------------
    # Name sanitisation (carried over from legacy factory)
    # ------------------------------------------------------------------

    @staticmethod
    def _sanitize_name(name: str) -> str:
        """Produce a valid Python class name from a FHIR resource name."""
        sanitized = "".join(ch for ch in name if ch.isalnum())
        if not sanitized:
            raise ValueError(
                f"FHIR resource name '{name}' has no alphanumeric characters."
            )
        while sanitized[0].isdigit():
            sanitized = sanitized[1:]
        sanitized = sanitized[0].upper() + sanitized[1:]
        if keyword.iskeyword(sanitized):
            sanitized = f"{sanitized}_"
        return sanitized

    # ------------------------------------------------------------------
    # Repository management helpers (mirrors legacy ResourceFactory API)
    # ------------------------------------------------------------------

    def configure_repository(
        self,
        directory: str | Path | None = None,
        files: list[str | Path] | None = None,
        definitions: list[dict] | None = None,
        packages: list[str | tuple[str, str]] | None = None,
        internet_enabled: bool = True,
        registry_base_url: str | None = None,
    ) -> None:
        """Configure the repository in one call."""
        self.repository.set_internet_enabled(internet_enabled)
        if registry_base_url and hasattr(self.repository, "set_registry_base_url"):
            self.repository.set_registry_base_url(registry_base_url)
        if directory:
            self.load_definitions_from_directory(directory)
        if files:
            self.load_definitions_from_files(*files)
        if definitions:
            self.load_definitions_from_list(*definitions)
        if packages:
            for pkg in packages:
                if isinstance(pkg, str):
                    self.load_package(pkg)
                elif isinstance(pkg, tuple) and len(pkg) == 2:
                    self.load_package(pkg[0], pkg[1])

    def disable_internet_access(self) -> None:
        self.repository.set_internet_enabled(False)

    def enable_internet_access(self) -> None:
        self.repository.set_internet_enabled(True)

    def load_definitions_from_directory(self, directory_path: str | Path) -> None:
        if hasattr(self.repository, "load_from_directory"):
            self.repository.load_from_directory(directory_path)
        else:
            raise NotImplementedError(
                "Repository does not support loading from directory"
            )

    def load_definitions_from_files(self, *file_paths: str | Path) -> None:
        if hasattr(self.repository, "load_from_files"):
            self.repository.load_from_files(*file_paths)
        else:
            raise NotImplementedError("Repository does not support loading from files")

    def load_definitions_from_list(self, *definitions: dict) -> None:
        if hasattr(self.repository, "load_from_definitions"):
            self.repository.load_from_definitions(*definitions)
        else:
            raise NotImplementedError(
                "Repository does not support loading from definitions"
            )

    def load_package(self, package_name: str, version: str | None = None) -> None:
        if hasattr(self.repository, "load_package"):
            self.repository.load_package(package_name, version)
        else:
            raise NotImplementedError("Repository does not support package loading")

    def get_loaded_packages(self) -> dict[str, str]:
        if hasattr(self.repository, "get_loaded_packages"):
            return self.repository.get_loaded_packages()
        return {}

    def has_package(self, package_name: str, version: str | None = None) -> bool:
        if hasattr(self.repository, "has_package"):
            return self.repository.has_package(package_name, version)
        return False

    def remove_package(self, package_name: str, version: str | None = None) -> None:
        if hasattr(self.repository, "remove_package"):
            self.repository.remove_package(package_name, version)

    def set_registry_base_url(self, base_url: str) -> None:
        if hasattr(self.repository, "set_registry_base_url"):
            self.repository.set_registry_base_url(base_url)
        else:
            raise NotImplementedError(
                "Repository does not support registry configuration"
            )

    def clear_package_cache(self) -> None:
        if hasattr(self.repository, "clear_package_cache"):
            self.repository.clear_package_cache()

    def resolve_structure_definition(
        self, canonical_url: str, version: str | None = None
    ) -> Any:
        if sd := self.repository.get(canonical_url, version):
            return sd
        raise ValueError(f"Could not resolve structure definition: {canonical_url}")

    def clear_cache(self) -> None:
        """Clear the construction cache."""
        self.construction_cache.clear()
