"""
FHIR Structure Mapper

High-level public API for FHIR StructureMap-based data transformation.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple, Union, TYPE_CHECKING

from pydantic import BaseModel

from fhircraft.exceptions import FhircraftException, MapperExecutionError, MapperParsingError
from fhircraft.fhir.mapper.engine.core import FHIRMappingEngine
from fhircraft.fhir.mapper.engine.registry import StructureMapRegistry
from fhircraft.fhir.mapper.parser import FHIRMappingLanguageParser, StructureMapUnion
from fhircraft.fhir.resources.definitions.registry import StructureDefinitionRegistry
from fhircraft.fhir.resources import get_fhir_type

__all__ = ["FHIRStructureMapper"]

if TYPE_CHECKING:
    from fhircraft.fhir.resources.datatypes.R4.core.structure_definition import (
        StructureDefinition as R4_StructureDefinition,
    )
    from fhircraft.fhir.resources.datatypes.R4B.core.structure_definition import (
        StructureDefinition as R4B_StructureDefinition,
    )
    from fhircraft.fhir.resources.datatypes.R5.core.structure_definition import (
        StructureDefinition as R5_StructureDefinition,
    )
    from fhircraft.fhir.resources.datatypes.R4.core.structure_map import (
        StructureMap as R4_StructureMap,
    )
    from fhircraft.fhir.resources.datatypes.R4B.core.structure_map import (
        StructureMap as R4B_StructureMap,
    )
    from fhircraft.fhir.resources.datatypes.R5.core.structure_map import (
        StructureMap as R5_StructureMap,
    )


class FHIRStructureMapper:
    """
    High-level interface for FHIR StructureMap-based data transformation.

    Combines parsing, resource registration, and mapping execution into a
    single cohesive API, mirroring the conventions of
    :class:`~fhircraft.fhir.resources.factory.FHIRModelFactory`.

    Example::

        mapper = FHIRStructureMapper()

        result = mapper.map(
            "map 'http://example.org' = 'demo' "
            "group main(source src, target tgt) { src.name -> tgt.fullName; }",
            source_data={"name": "John Doe"},
        )
    """

    def __init__(
        self,
        fhir_release: str = "R5",
        structure_definition_registry: StructureDefinitionRegistry | None = None,
        structure_map_registry: StructureMapRegistry | None = None,
    ) -> None:
        """
        Initialise the mapper.

        Args:
            fhir_release: FHIR version to target (``"R4"``, ``"R4B"``, or ``"R5"``).
            structure_definition_registry: Pre-built definition registry. A new one
                is created automatically when omitted.
            structure_map_registry: Pre-built StructureMap registry. A new one is
                created automatically when omitted.
        """
        self.fhir_release = fhir_release
        self._engine = FHIRMappingEngine(
            fhir_release=fhir_release,
            structure_definition_registry=structure_definition_registry,
            structure_map_registry=structure_map_registry,
        )
        self._parser = FHIRMappingLanguageParser()

    # ------------------------------------------------------------------
    # Core mapping operation
    # ------------------------------------------------------------------

    def map(
        self,
        structure_map: "Union[str, R4_StructureMap, R4B_StructureMap, R5_StructureMap, Dict[str, Any]]",
        source_data: Union[
            BaseModel, Dict[str, Any], Tuple[Union[BaseModel, dict], ...]
        ],
        target_data: Optional[
            Union[BaseModel, Dict[str, Any], Tuple[Union[BaseModel, dict], ...]]
        ] = None,
        group: Optional[str] = None,
    ) -> tuple[BaseModel | dict, ...]:
        """
        Execute a StructureMap transformation.

        Args:
            structure_map: The mapping to apply. Accepts:

                - A FHIR mapping language script string.
                - Any StructureMap model instance (R4, R4B, or R5).
                - A raw dictionary conforming to the StructureMap schema.

            source_data: Source data to transform — a single object
                (BaseModel or dict) or a tuple for multi-source mappings.
            target_data: Optional pre-existing target object(s). When
                omitted, targets are constructed automatically.
            group: Name of the entrypoint group. Defaults to the first
                group defined in the mapping.

        Returns:
            A tuple of transformed target instances.

        Raises:
            ValueError: If *structure_map* is of an unsupported type.
            MapperExecutionError: If execution fails.
        """
        structure_map = self._resolve_mapping(structure_map)
        sources = source_data if isinstance(source_data, tuple) else (source_data,)
        targets: tuple | None = None
        if target_data is not None:
            targets = target_data if isinstance(target_data, tuple) else (target_data,)
        try:
            return self._engine.execute(
                structure_map=structure_map,
                sources=sources,  # type: ignore[arg-type]
                targets=targets,  # type: ignore[arg-type]
                group=group,
            )
        except Exception as e:
            raise MapperExecutionError(f"Mapping execution failed: {e}") from e

    # ------------------------------------------------------------------
    # Parsing helpers
    # ------------------------------------------------------------------

    def parse(self, script: str) -> StructureMapUnion:
        """
        Parse a FHIR mapping language script into a StructureMap model.

        Args:
            script: FHIR mapping language script (short syntax).

        Returns:
            A validated StructureMap model instance.

        Raises:
            MapperParsingError: If the script contains syntax errors.
        """
        try:
            return self._parser.parse(script, fhir_release=self.fhir_release)
        except Exception as e:
            raise MapperParsingError(f"Failed to parse mapping script: {e}") from e

    def list_groups(
        self,
        mapping: "Union[str, R4_StructureMap, R4B_StructureMap, R5_StructureMap, Dict[str, Any]]",
    ) -> List[str]:
        """
        Return the names of all groups defined in a mapping.

        Args:
            mapping: StructureMap, mapping language script, or raw dict.

        Returns:
            List of group name strings.
        """
        structure_map = self._resolve_mapping(mapping)
        return [str(g.name) for g in (structure_map.group or []) if g.name]

    # ------------------------------------------------------------------
    # StructureDefinition registry
    # ------------------------------------------------------------------

    def register_definition(
        self,
        sd: "R4_StructureDefinition | R4B_StructureDefinition | R5_StructureDefinition | dict",
        fail_if_exists: bool = False,
    ) -> "R4_StructureDefinition | R4B_StructureDefinition | R5_StructureDefinition":
        """
        Register a StructureDefinition for use in mappings.

        Args:
            sd: A StructureDefinition model instance or a raw dictionary.
            fail_if_exists: Raise :exc:`ValueError` if the canonical URL is
                already registered.

        Returns:
            The registered StructureDefinition instance.
        """
        registry = self._engine.structure_definition_registry
        if isinstance(sd, dict):
            return registry.from_dict(sd, fail_if_exists=fail_if_exists)
        registry.add(sd, fail_if_exists=fail_if_exists)
        return sd

    def has_registered_definition(self, canonical_url: str) -> bool:
        """
        Return ``True`` if *canonical_url* is present in the definition registry.

        Args:
            canonical_url: Canonical URL of the StructureDefinition.
        """
        return canonical_url in self._engine.structure_definition_registry

    def get_registered_definition(
        self, canonical_url: str
    ) -> "R4_StructureDefinition | R4B_StructureDefinition | R5_StructureDefinition":
        """
        Retrieve a registered StructureDefinition by its canonical URL.

        Args:
            canonical_url: Canonical URL (optionally suffixed with ``|version``).

        Raises:
            StructureDefinitionNotFoundError: If the URL is not registered.
        """
        return self._engine.structure_definition_registry.get(canonical_url)

    def list_registered_definitions(self, kind: str | None = None) -> list[str]:
        """
        Return canonical URLs of all known StructureDefinitions.

        Covers both in-memory definitions added at runtime and the built-in
        local definitions shipped with the selected FHIR release.

        Args:
            kind: Optional kind filter — e.g. ``"resource"``,
                ``"complex-type"``, ``"primitive-type"``. When omitted all
                definitions are returned.

        Returns:
            Sorted list of canonical URL strings.
        """
        reg = self._engine.structure_definition_registry
        urls: set[str] = set()

        # In-memory definitions added at runtime
        for url, sd in reg.structure_definitions_by_url.items():
            if kind is None or getattr(sd, "kind", None) == kind:
                urls.add(url)

        # File-backed local manifest
        manifest = reg.local_manifest
        for url, filename in manifest.by_url.items():
            if url in urls:
                continue
            entry = manifest.definitions.get(filename)
            if kind is None or (entry and entry.kind == kind):
                urls.add(url)

        return sorted(urls)

    def register_package(self, package_name: str, package_version: str) -> None:
        """
        Download a FHIR npm package and register all its StructureDefinitions.

        Args:
            package_name: Package identifier (e.g. ``"hl7.fhir.us.core"``).
            package_version: Package version string.

        Raises:
            RuntimeError: If internet access is disabled.
        """
        self._engine.structure_definition_registry.download_package(
            package_name, package_version
        )

    # ------------------------------------------------------------------
    # StructureMap registry
    # ------------------------------------------------------------------

    def register_map(
        self,
        sm: "R4_StructureMap | R4B_StructureMap | R5_StructureMap | dict",
        fail_if_exists: bool = False,
    ) -> "R4_StructureMap | R4B_StructureMap | R5_StructureMap":
        """
        Register a StructureMap so it can be resolved by ``imports`` directives.

        Args:
            sm: A StructureMap model instance or a raw dictionary.
            fail_if_exists: Raise :exc:`ValueError` if the canonical URL is
                already registered.

        Returns:
            The registered StructureMap instance.
        """
        registry = self._engine.structure_map_registry
        if isinstance(sm, dict):
            return registry.from_dict(sm, fail_if_exists=fail_if_exists)
        registry.add(sm, fail_if_exists=fail_if_exists)
        return sm

    def has_registered_map(self, canonical_url: str) -> bool:
        """
        Return ``True`` if *canonical_url* is present in the StructureMap registry.

        Args:
            canonical_url: Canonical URL of the StructureMap.
        """
        return canonical_url in self._engine.structure_map_registry

    def get_registered_map(
        self, canonical_url: str
    ) -> "R4_StructureMap | R4B_StructureMap | R5_StructureMap":
        """
        Retrieve a registered StructureMap by its canonical URL.

        Args:
            canonical_url: Canonical URL (optionally suffixed with ``|version``).

        Raises:
            MapperRegistryNotFoundError: If the URL is not registered.
        """
        return self._engine.structure_map_registry.get(canonical_url)

    def list_registered_maps(self) -> list[str]:
        """
        Return canonical URLs of all registered StructureMaps.

        Returns:
            Sorted list of canonical URL strings.
        """
        return sorted(self._engine.structure_map_registry.structure_maps_by_url.keys())

    # ------------------------------------------------------------------
    # Internet access
    # ------------------------------------------------------------------

    def enable_internet_access(self) -> None:
        """Allow both registries to resolve unknown resources from the internet."""
        self._engine.structure_definition_registry.enable_internet_access()
        self._engine.structure_map_registry.enable_internet_access()

    def disable_internet_access(self) -> None:
        """Prevent both registries from making outgoing HTTP requests."""
        self._engine.structure_definition_registry.disable_internet_access()
        self._engine.structure_map_registry.disable_internet_access()

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _resolve_mapping(
        self,
        mapping: "Union[str, R4_StructureMap, R4B_StructureMap, R5_StructureMap, Dict[str, Any]]",
    ) -> StructureMapUnion:
        if isinstance(mapping, str):
            return self.parse(mapping)
        if isinstance(mapping, dict):            
            StructureMap = get_fhir_type("StructureMap", self.fhir_release)
            return StructureMap.model_validate(mapping)
        if isinstance(mapping, BaseModel):
            return mapping  # type: ignore[return-value]
        raise ValueError(f"Unsupported mapping type: {type(mapping)}")
