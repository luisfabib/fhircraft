"""
FHIR Mapping Language Engine

This module provides the core FHIR Mapping Language execution engine that processes
StructureMap resources to transform FHIR data from source to target structures.
"""

import enum
import logging
from collections import OrderedDict
from typing import Dict, Type

from pydantic import BaseModel, ConfigDict

import fhircraft.fhir.path.engine as fhirpath

from fhircraft.fhir.resources.datatypes.R4 import core as R4_models
from fhircraft.fhir.resources.datatypes.R4B import core as R4B_models
from fhircraft.fhir.resources.datatypes.R5 import core as R5_models

from fhircraft.fhir.path.parser import fhirpath as fhirpath_parser
from fhircraft.fhir.resources.definitions.registry import StructureDefinitionRegistry
from fhircraft.fhir.resources.factory import ResourceFactory
from fhircraft.fhir.resources.repository import CompositeStructureDefinitionRepository

from .exceptions import (
    MappingError,
)
from .scope import MappingScope
from .group import Group

logger = logging.getLogger(__name__)


class ArbitraryModel(BaseModel):
    """
    A dynamic Pydantic model that accepts arbitrary fields.

    This is used for arbitrary target structures in mappings where no
    specific structure definition is provided. Unlike plain dicts, this
    model is compatible with the FHIRPath engine's update mechanisms,
    allowing complex nested path creation and array operations.
    """

    model_config = ConfigDict(extra="allow")


class StructureMapTargetListMode(str, enum.Enum):
    """Enumeration of StructureMap model modes."""

    FIRST = "first"
    LAST = "last"
    SHARED = "shared"
    SINGLE = "single"


class StructureMapModelMode(str, enum.Enum):
    """Enumeration of StructureMap model modes."""

    SOURCE = "source"
    TARGET = "target"
    QUERIED = "queried"
    PRODUCED = "produced"


class FHIRMappingEngine:
    """
    FHIRMappingEngine is responsible for executing FHIR StructureMap-based transformations between FHIR resources.

    This engine validates, processes, and applies mapping rules defined in a StructureMap to transform source FHIR resources into target resources, supporting complex mapping logic, rule dependencies, and FHIRPath-based expressions.

    Attributes:
        repository (StructureDefinitionRegistry): Registry for FHIR StructureDefinitions.
        factory (ResourceFactory): Factory for constructing FHIR resource models.
        transformer (MappingTransformer): Executes FHIRPath-based transforms.
    """

    def __init__(
        self,
        repository: StructureDefinitionRegistry | None = None,
        factory: ResourceFactory | None = None,
        fhir_release: str = "R5",
    ):
        self.repository = repository or StructureDefinitionRegistry(
            fhir_release=fhir_release
        )
        self.factory = factory or ResourceFactory(
            registry=self.repository, fhir_release=fhir_release
        )

    def execute(
        self,
        structure_map: (
            R4_models.StructureMap | R4B_models.StructureMap | R5_models.StructureMap
        ),
        sources: tuple[BaseModel | dict],
        targets: tuple[BaseModel | dict] | None = None,
        group: str | None = None,
    ) -> tuple[BaseModel | dict, ...]:
        """
        Executes a FHIR StructureMap transformation using the provided sources and optional targets.

        This method resolves structure definitions, validates input data, sets up the mapping scope,
        binds source and target instances to group parameters, and processes the entrypoint group
        to produce the mapped target instances.

        Args:
            structure_map: The StructureMap resource defining the transformation rules.
            sources: Source data to be mapped, as a tuple of Pydantic models or dictionaries.
            targets: Optional target instances to populate. If not provided, new instances are created as needed.
            group: The name of the entrypoint group to execute. If not specified, the first group is used.

        Returns:
            tuple: A tuple of resulting target instances after the transformation, which can be a mixture of BaseModel instances and/or dictionaries.

        Raises:
            NotImplementedError: If StructureMap imports are present (not supported).
            ValueError: If a constant in the StructureMap is missing a name or conflicts with a model name.
            RuntimeError: If the number of provided sources or targets does not match the group parameters, or if required targets are missing.
            TypeError: If provided sources or targets do not match the expected types for the group parameters.
        """

        # Ensure sources is a tuple
        if not isinstance(sources, tuple):
            sources = (sources,)

        if structure_map.import_:
            raise NotImplementedError("StructureMap imports are not implemented yet")

        # Resolve structure definitions
        source_models = self._resolve_structure_definitions(
            structure_map, StructureMapModelMode.SOURCE
        )
        target_models = self._resolve_structure_definitions(
            structure_map, StructureMapModelMode.TARGET
        )
        queried_models = self._resolve_structure_definitions(
            structure_map, StructureMapModelMode.QUERIED
        )
        produced_models = self._resolve_structure_definitions(
            structure_map, StructureMapModelMode.PRODUCED
        )

        # Validate source data
        validated_sources = self._validate_source_data(sources, source_models)

        # Create the global mapping scope
        global_scope = MappingScope(
            name="global",
            types={
                **source_models,
                **target_models,
                **queried_models,
                **produced_models,
            },
            groups=OrderedDict(
                [(str(group.name), Group(group)) for group in structure_map.group or []]  # type: ignore
            ),
            concept_maps={
                str(map.id): map
                for map in (structure_map.contained or [])
                if isinstance(
                    map,
                    (R4_models.ConceptMap, R4B_models.ConceptMap, R5_models.ConceptMap),
                )
                and map.id
            },
        )

        # Build default mapping group registry
        self._build_default_group_registry(structure_map, global_scope)

        # Parse and validate constants
        for const in getattr(structure_map, "const", None) or []:
            if not const.name:
                raise ValueError("Constant must have a name")
            if const.name in source_models or const.name in target_models:
                raise ValueError(
                    f"Constant name '{const.name}' conflicts with existing source or target model"
                )
            # Add the constant as a variable in the global scope
            global_scope.define_variable(const.name, fhirpath_parser.parse(const.value))

        # Determine the entrypoint group
        target_group = (global_scope.groups.get(group) if group else None) or list(
            global_scope.groups.values()
        )[0]

        # Validate the group parameters
        expected_sources = len(
            [
                input
                for input in (target_group.inputs)
                if input.mode == StructureMapModelMode.SOURCE
            ]
        )
        if len(validated_sources) != expected_sources:
            raise RuntimeError(
                f"Entrypoint group {target_group.name} expected {expected_sources} sources, got {len(validated_sources)}."
            )

        # Validate targets if provided
        if targets:
            expected_targets = len(
                [
                    input
                    for input in target_group.inputs
                    if input.mode
                    in (StructureMapModelMode.TARGET, StructureMapModelMode.PRODUCED)
                ]
            )
            if len(targets) != expected_targets:
                raise RuntimeError(
                    f"Entrypoint group {target_group.name} expected {expected_targets} targets, got {len(targets)}."
                )

        # Bind source and target instances to group parameters
        parameters = []
        for input in target_group.inputs:
            if not input.name:
                raise ValueError(
                    f"Input in group '{target_group.name}' is missing a name."
                )
            if input.mode == StructureMapModelMode.SOURCE:

                if input.type:
                    # Explicit type specified - match by type
                    source_instance = validated_sources.get(input.type)
                    if not source_instance:
                        raise TypeError(
                            f"Invalid source provided. None of the source arguments matches the '{input.name}' parameter of type {input.type} for the entrypoint group '{target_group.name}'."
                        )
                else:
                    # No type specified - use first available source or match by parameter name
                    source_instance = (
                        validated_sources.get(input.name)
                        or validated_sources.get("source")
                        or next(iter(validated_sources.values()), None)
                    )
                    if source_instance is None:
                        raise TypeError(
                            f"No source data available for parameter '{input.name}'."
                        )
                source_instance_id = f"source_{id(source_instance)}"
                global_scope.source_instances[source_instance_id] = source_instance  # type: ignore
                parameters.append(fhirpath.Element(source_instance_id))

            if input.mode == StructureMapModelMode.TARGET:
                target_type = global_scope.types.get(input.type) if input.type else None

                if target_type is not None:
                    # Type specified and model available - create or find typed instance
                    if not targets:
                        target_instance = target_type.model_construct()
                    else:
                        target_instance = next(
                            (
                                target
                                for target in targets
                                if isinstance(target, target_type)
                            ),
                            None,
                        )
                        if not target_instance:
                            raise TypeError(
                                f"Invalid target provided. None of the target arguments matches the {input.name} parameters of type {input.type} for the entrypoint group '{target_group.name}'."
                            )
                else:
                    # No type or type not resolved - use arbitrary target
                    if targets:
                        target_instance = targets[0]
                    else:
                        # Create ArbitraryModel instance for arbitrary target
                        # This allows FHIRPath engine to work properly with nested paths
                        target_instance = ArbitraryModel()

                target_instance_id = f"source_{id(target_instance)}"
                global_scope.target_instances[target_instance_id] = target_instance  # type: ignore
                parameters.append(fhirpath.Element(target_instance_id))

        # Process the entrypoint group
        target_group.process(scope=global_scope, parameters=parameters)

        # Return the resulting target instances
        return tuple(
            [
                # Convert ArbitraryModel to dict for user consumption
                (
                    instance.model_dump()
                    if isinstance(instance, ArbitraryModel)
                    # Validate other BaseModel instances
                    else (
                        instance.model_validate(instance.model_dump())
                        if isinstance(instance, BaseModel)
                        # Pass through non-BaseModel instances (shouldn't happen)
                        else instance
                    )
                )
                for instance in global_scope.target_instances.values()
            ]
        )

    def _build_default_group_registry(
        self,
        structure_map: (
            R4_models.StructureMap | R4B_models.StructureMap | R5_models.StructureMap
        ),
        global_scope: MappingScope,
    ):
        """
        Builds a registry of default mapping groups based on typeMode.
        Groups with typeMode 'types' or 'type-and-types' are considered default mapping groups.
        """
        default_groups = {}
        for group in structure_map.group or []:
            if group.typeMode in ["types", "type-and-types"]:
                # Build a key based on input/output types
                if group.input and len(group.input) >= 2:
                    source_type = group.input[0].type or "Any"
                    target_type = group.input[1].type or "Any"
                    key = f"{source_type}->{target_type}"
                    default_groups[key] = group

        # Store the default groups registry in global scope
        global_scope.default_groups = default_groups

    def _resolve_structure_definitions(
        self,
        structure_map: (
            R4_models.StructureMap | R4B_models.StructureMap | R5_models.StructureMap
        ),
        mode: StructureMapModelMode,
    ) -> Dict[str, type[BaseModel] | type[ArbitraryModel]]:
        """
        Resolves and constructs resource models for the specified mode from the given StructureMap.

        If no structures are defined for the given mode, returns an empty dict, allowing
        arbitrary data to be used without predefined models. If a structure URL cannot be
        resolved, logs a warning and continues without that model.

        Args:
            structure_map (StructureMap): The structure map containing structure definitions to resolve.
            mode (StructureMapModelMode): The mode (e.g., source or target) to filter structures by.

        Returns:
            Dict[str, type[BaseModel] | None]: A dictionary mapping structure aliases to model classes,
                or None for structures that couldn't be resolved. Empty if no structures defined for this mode.
        """
        if not structure_map.structure:
            return {}

        resolved = {}
        for s in structure_map.structure:
            if s.mode != mode:
                continue
            if not (canonical_url := s.url):
                logger.warning(
                    f"Structure definition for mode {mode} is missing URL. "
                    f"Data for this structure will be treated as arbitrary."
                )
                resolved[s.alias or "arbitrary"] = ArbitraryModel
                continue
            # Handle core FHIR types with known canonical URLs to avoid unnecessary repository lookups
            if canonical_url.startswith("http://hl7.org/fhir/StructureDefinition/"):
                from fhircraft.fhir.resources.datatypes import get_fhir_type

                core_type = canonical_url.removeprefix(
                    "http://hl7.org/fhir/StructureDefinition/"
                )
                try:
                    resolved[s.alias or core_type] = get_fhir_type(
                        core_type, self.factory.fhir_release
                    )
                    return resolved
                except AttributeError:
                    pass
            try:
                structure_def = self.repository.get(canonical_url)
                model = self.factory.build(structure_def)
                resolved[s.alias or structure_def.name] = model
            except (KeyError, ValueError, AttributeError) as e:
                # If StructureDefinition not found, log warning but continue
                logger.warning(
                    f"Could not resolve structure definition for {canonical_url}: {e}. "
                    f"Data for this structure will be treated as arbitrary."
                )
                # Mark as no model validation available
                resolved[s.alias or canonical_url] = ArbitraryModel

        return resolved

    def _validate_source_data(
        self,
        source_data: tuple[BaseModel | dict, ...],
        source_models: Dict[str, Type[BaseModel] | None],
    ) -> dict[str, BaseModel | dict]:
        """
        Validates and maps source data entries to their corresponding models when available.

        For entries with defined models, performs Pydantic validation.
        For entries without models (model is None or empty dict), passes through as-is.

        Args:
            source_data (tuple[BaseModel | dict, ...]): A tuple containing source data entries, which can be Pydantic model instances, dictionaries, or objects with a `__dict__` attribute.
            source_models (Dict[str, Type[BaseModel] | None]): A dictionary mapping string aliases to Pydantic model classes, or None for arbitrary data.

        Returns:
            dict[str, BaseModel | dict]: A dictionary mapping aliases to validated Pydantic model instances or raw data.

        Raises:
            MappingError: If any entry in `source_data` does not match any of the provided source models.
        """
        if not source_models:
            # No models defined - treat all source data as arbitrary
            # Use generic keys for the data
            if len(source_data) == 1:
                return {"source": source_data[0]}
            return {f"source{i}": data for i, data in enumerate(source_data)}

        validated_entries = {}
        matched_indices = set()

        def _validate_entry(entry: BaseModel | dict, entry_idx: int) -> bool:
            """Try to validate entry against available models. Returns True if matched."""
            for alias, source_model in source_models.items():
                if source_model is None:
                    # No model - accept arbitrary data
                    if alias not in validated_entries:
                        validated_entries[alias] = entry
                        return True
                    continue

                try:
                    if isinstance(entry, source_model):
                        validated_entries[alias] = entry
                        return True
                    elif isinstance(entry, dict):
                        validated_entries[alias] = source_model(**entry)
                        return True
                    elif hasattr(entry, "__dict__"):
                        validated_entries[alias] = source_model(**entry.__dict__)
                        return True
                except Exception as e:
                    print(e)
                    continue
            return False

        for idx, entry in enumerate(source_data):
            if not _validate_entry(entry, idx):
                raise MappingError(
                    f"Source data entry of type {type(entry)} does not match any source model. "
                    f"Available models: {list(source_models.keys())}"
                )
            matched_indices.add(idx)

        return validated_entries


mapper = FHIRMappingEngine()
