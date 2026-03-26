"""
FHIRModelFactory — the top-level façade for building Pydantic models from FHIR ``StructureDefinition`` objects.

This is the main public entry point; the rest of the pipeline (resolver,
assembler, builders, validators) is invoked from here.
"""

import re
import keyword
from typing import Any, Literal, Sequence, TYPE_CHECKING

from pydantic import BaseModel

from fhircraft.fhir.resources.base import (
    FHIRBaseModel,
    FhirBaseModelKind,
)
from fhircraft.fhir.resources.factory.assembler import ModelAssembler
from fhircraft.fhir.resources.factory.context import BuildContext
from fhircraft.fhir.resources.factory.resolver import SnapshotResolver
from fhircraft.fhir.resources.definitions.registry import StructureDefinitionRegistry
from fhircraft.fhir.resources.datatypes.registry import get_fhir_type_by_url
from fhircraft.utils import get_FHIR_release_from_version, capitalize

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


class FHIRModelFactory:
    """
    FHIRModelFactory constructs Pydantic model classes from FHIR StructureDefinitions.

    The factory manages a registry of StructureDefinitions, supports loading FHIR packages, and
    caches constructed models to optimise performance.

    Attributes:
        fhir_release (str): The FHIR release version (e.g. "R4", "R5") used by the factory.
        definition_registry (StructureDefinitionRegistry): Registry for storing and retrieving
            StructureDefinitions.
        construction_cache (dict[str, type[BaseModel]]): Cache mapping canonical URLs to
            constructed Pydantic model classes.
    """

    def __init__(
        self, fhir_release: str, registry: StructureDefinitionRegistry | None = None
    ) -> None:

        self.fhir_release: str = fhir_release
        if registry and registry.fhir_release != fhir_release:
            raise ValueError(
                f"Provided registry FHIR release '{registry.fhir_release}' does not match factory FHIR release '{fhir_release}'."
            )
        self.definition_registry = registry or StructureDefinitionRegistry(fhir_release)
        # Global cache: canonical URL → built Pydantic model
        self.construction_cache: dict[str, type[BaseModel]] = {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def build(
        self,
        structure_definition: Any = None,
        *,
        canonical_url: str | None = None,
        mixins: Sequence[type] | None = None,
        mode: Literal["auto", "snapshot", "differential"] = "auto",
    ) -> type[BaseModel]:
        """
        Constructs and returns a Pydantic model class based on a FHIR StructureDefinition.

        Args:
            structure_definition (Any, optional): The FHIR StructureDefinition object to build the model from.
            canonical_url (str, optional): The canonical URL of the StructureDefinition to retrieve from the registry.
            mixins (Sequence[type], optional): Additional mixin classes to include in the generated model.
            mode (Literal["auto", "snapshot", "differential"], optional): The mode for building the model.
                "auto" selects the best mode automatically, "snapshot" uses the snapshot representation,
                and "differential" uses the differential representation.

        Returns:
            type[BaseModel]: The constructed Pydantic model class.

        Raises:
            KeyError: If neither structure_definition nor canonical_url is provided, or if the canonical_url is not found in the registry.

        Notes:
            - Uses a cache to avoid rebuilding models for the same StructureDefinition URL.
            - If both structure_definition and canonical_url are provided, structure_definition takes precedence.
        """

        if structure_definition:
            structure_definition = self._normalise_structure_definition(
                self.definition_registry, structure_definition
            )
        elif canonical_url:
            structure_definition = self.definition_registry.get(canonical_url)
        # Cache check
        if structure_definition.url in self.construction_cache:
            return self.construction_cache[structure_definition.url]

        return self._build(structure_definition, mixins=mixins, mode=mode)

    def register_package(
        self,
        package_name: str,
        version: str,
        skip_invalid: bool = False,
        include_dependencies: bool = True,
    ) -> None:
        """
        Download and register all StructureDefinitions from a FHIR npm package.

        Args:
            package_name: Package identifier (e.g. ``"hl7.fhir.us.mcode"``).
            version: Package version string (e.g. ``"1.0.0"``).
            skip_invalid: Whether to skip invalid StructureDefinitions.
            include_dependencies: Whether to include dependencies when downloading the package.
        """
        self.definition_registry.download_package(
            package_name, version, skip_invalid, include_dependencies
        )

    def register(
        self,
        sd: "R4_StructureDefinition | R4B_StructureDefinition | R5_StructureDefinition | dict",
    ) -> "R4_StructureDefinition | R4B_StructureDefinition | R5_StructureDefinition":
        """
        Register a StructureDefinition with the factory.

        Accepts a typed StructureDefinition model instance or a plain dict.  The
        normalised, validated SD instance is returned so callers can inspect it.

        Args:
            sd: A StructureDefinition model instance or a ``dict`` representation.

        Returns:
            The normalised StructureDefinition instance that was stored.

        Raises:
            ValueError: If *sd* is neither a dict nor a StructureDefinition instance.
        """
        if isinstance(sd, dict):
            return self.definition_registry.from_dict(sd)
        elif getattr(sd, "_resource_type", None) == "StructureDefinition":
            self.definition_registry.add(sd)
            return sd
        else:
            raise ValueError(
                "Input must be a dict or a StructureDefinition model instance."
            )

    def unregister(self, url: str) -> None:
        """
        Remove a StructureDefinition from the registry and evict it from the cache.

        If *url* is not registered, the call is a no-op.

        Args:
            url: The canonical URL of the StructureDefinition to remove.
        """
        self.definition_registry.structure_definitions_by_url.pop(url, None)
        self.evict(url)

    def reset_cache(self) -> None:
        """Discard the entire construction cache."""
        self.construction_cache.clear()

    def has_registered_definition(self, url: str) -> bool:
        """Return ``True`` if *url* is present in the definition registry."""
        return url in self.definition_registry

    def get_registered_definition(
        self, url: str
    ) -> "R4_StructureDefinition | R4B_StructureDefinition | R5_StructureDefinition":
        """
        Retrieve a registered StructureDefinition by canonical URL.

        Args:
            url: The canonical URL of the StructureDefinition.

        Returns:
            The StructureDefinition instance stored in the registry.

        Raises:
            KeyError: If *url* is not registered.
        """
        return self.definition_registry.get(url)

    def list_registered_definitions(self, kind: str | None = None) -> list[str]:
        """
        Return all canonical URLs registered in the definition registry.

        Args:
            kind: When provided, only URLs whose StructureDefinition has a matching
                ``kind`` field (e.g. ``"resource"``, ``"complex-type"``) are returned.

        Returns:
            Sorted list of canonical URL strings.
        """
        sds = self.definition_registry.structure_definitions_by_url
        if kind is None:
            return sorted(sds)
        return sorted(
            url for url, sd in sds.items() if getattr(sd, "kind", None) == kind
        )

    def is_built(self, url: str) -> bool:
        """Return ``True`` if a model for *url* is present in the construction cache."""
        return url in self.construction_cache

    def list_built(self) -> list[str]:
        """Return all canonical URLs whose models are currently cached."""
        return list(self.construction_cache)

    def evict(self, url: str) -> None:
        """
        Remove a single entry from the construction cache.

        If *url* is not cached, the call is a no-op.

        Args:
            url: Canonical URL of the model to evict.
        """
        self.construction_cache.pop(url, None)

    def rebuild(
        self,
        url: str,
        *,
        mixins: Sequence[type] | None = None,
        mode: Literal["auto", "snapshot", "differential"] = "auto",
    ) -> type[BaseModel]:
        """
        Evict *url* from the cache and build a fresh model.

        Useful when the underlying StructureDefinition has changed after the
        initial build (e.g. after calling :meth:`register` again with an updated SD).

        Args:
            url: Canonical URL of the StructureDefinition to rebuild.
            mixins: Optional mixin classes forwarded to :meth:`build`.
            mode: Build mode forwarded to :meth:`build`.

        Returns:
            The newly constructed Pydantic model class.
        """
        self.evict(url)
        return self.build(canonical_url=url, mixins=mixins, mode=mode)

    def enable_internet_access(self) -> None:
        """Allow the definition registry to resolve unknown URLs from the internet."""
        self.definition_registry.enable_internet_access()

    def disable_internet_access(self) -> None:
        """Prevent the definition registry from making any outgoing HTTP requests."""
        self.definition_registry.disable_internet_access()

    # ------------------------------------------------------------------
    # Internal build pipeline
    # ------------------------------------------------------------------

    def _build(
        self,
        structure_def: "R4_StructureDefinition | R4B_StructureDefinition | R5_StructureDefinition",
        mixins: Sequence[type] | None = None,
        mode: Literal["auto", "snapshot", "differential"] = "auto",
    ) -> type[BaseModel]:
        """Internal build method, assumes input is already normalised and validated."""

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
        # Resolve base model/class
        # ------------------------------------------------------------------
        base_model: type = FHIRBaseModel
        if base_canonical := structure_def.baseDefinition:
            # Try directly from registry of built-in types first
            resolved = get_fhir_type_by_url(
                base_canonical, fhir_release, fail_if_not_found=False
            )
            if (
                resolved is not None
                and isinstance(resolved, type)
                and issubclass(resolved, FHIRBaseModel)
            ):
                base_model = resolved
            else:
                base_model = self.build(canonical_url=base_canonical)

        # ------------------------------------------------------------------
        # Produce the complete DefinitionIndex
        # ------------------------------------------------------------------
        resolver = SnapshotResolver(self.definition_registry)
        definition_index = resolver.resolve(structure_def, mode=mode)

        # ------------------------------------------------------------------
        # Assemble the Pydantic model
        # ------------------------------------------------------------------
        base_classes: tuple[type, ...] = (base_model,)
        if mixins:
            base_classes = (base_model, *mixins)

        assembler = ModelAssembler(
            index=definition_index,
            ctx=BuildContext(
                fhir_release=self.fhir_release,
                fhir_version=fhir_version,
                registry=self.definition_registry,
                resource_name=sanitized_name,
                factory=self,
                base=base_model,
            ),
            resource_name=sanitized_name,
        )
        model = assembler.assemble(sanitized_name, base=base_classes)

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

    def _normalise_structure_definition(
        self,
        registry: StructureDefinitionRegistry,
        sd: Any,
    ) -> "R4_StructureDefinition | R4B_StructureDefinition | R5_StructureDefinition":
        """Normalizes a StructureDefinition input to a standard StructureDefinition object."""

        if getattr(sd, "_resource_type", None) == "StructureDefinition":
            registry.add(sd)
            return sd

        elif isinstance(sd, dict):
            return registry.from_dict(sd)

        elif isinstance(sd, str):
            return registry.get(sd)

        return sd

    @staticmethod
    def _sanitize_name(name: str) -> str:
        """Produce a valid Python class name from a FHIR resource name."""
        sanitized = "".join(ch for ch in name if ch.isalnum())
        sanitized = "".join(
            capitalize(word) for word in re.split("[^a-zA-Z]", name) if word
        )

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
