"""
FHIR Mapping Language Engine

This module provides the core FHIR Mapping Language execution engine that processes
StructureMap resources to transform FHIR data from source to target structures.
"""

import enum
import logging
import uuid 
import re
from dataclasses import dataclass, field
from collections import OrderedDict
from typing import Any, Dict, List, Optional, Set, Type
from pydantic import BaseModel

import fhircraft.fhir.path.engine as fhirpath
from fhircraft.fhir.mapping.StructureMap import (
    StructureMap,
    StructureMapDependent,
    StructureMapGroup,
    StructureMapParameter,
    StructureMapRule,
    StructureMapSource,
    StructureMapTarget,
)
from fhircraft.fhir.mapping.ConceptMap import ConceptMap
from fhircraft.fhir.path import fhirpath as fhirpath_parser
from fhircraft.fhir.path.engine.core import FHIRPath, FHIRPathCollection, Literal
from fhircraft.fhir.path.exceptions import FHIRPathError
from fhircraft.fhir.resources.factory import ResourceFactory
from fhircraft.fhir.resources.datatypes.R4B.complex_types import (
    CodeableConcept, 
    Coding, 
    Quantity, 
    Identifier, 
    ContactPoint,
)
from fhircraft.fhir.resources.repository import (
    CompositeStructureDefinitionRepository,
    StructureDefinitionNotFoundError,
)
from fhircraft.utils import is_list_field

logger = logging.getLogger(__name__)


class MappingError(Exception):
    """Base exception for mapping engine errors."""

    pass


class ValidationError(MappingError):
    """Raised when input data validation fails."""

    pass


class RuleProcessingError(MappingError):
    """Raised when rule processing fails."""

    pass


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


@dataclass
class MappingScope:
    """
    A scope defines the visibility and accessibility of identifiers (variables, types, etc.)
    """

    name: str
    """Name of the scope"""

    types: Dict[str, type[BaseModel]] = field(default_factory=dict)
    """Mapping of types"""

    source_instances: Dict[str, BaseModel] = field(default_factory=dict)
    """The source instances being mapped"""

    target_instances: Dict[str, BaseModel] = field(default_factory=dict)
    """The target instances being mapped"""

    concept_maps: Dict[str, ConceptMap] = field(default_factory=dict)

    groups: OrderedDict[str, StructureMapGroup] = field(default_factory=OrderedDict)
    """The groups defined on this scope"""

    variables: Dict[str, FHIRPath] = field(default_factory=dict)
    """Mapping variables names to resolved FHIRPaths"""

    processing_rules: Set[str] = field(default_factory=set)
    """Set of currently processing rules"""

    parent: Optional["MappingScope"] = None
    """Parent mapping scope"""

    def define(self, variable: str, value: FHIRPath) -> None:
        """Define a new variable in this scope"""
        if not isinstance(value, FHIRPath):
            raise ValueError("Variables can only be assigned to a FHIRPath instance")
        self.variables[variable] = value

    def get_instances(self) -> Dict[str, BaseModel]:
        return {
            **(self.parent.get_instances() if self.parent else {}),
            **self.target_instances,
            **self.source_instances,
        }


    def get_concept_map(self, identifier: str) -> Optional[ConceptMap]:
        """Get a concept map by its identifier"""
        return self.concept_maps.get(identifier) or (
            self.parent.get_concept_map(identifier) if self.parent else None
        )
    
    def get_target_instance(self, identifier: str) -> Optional[BaseModel]:
        """Get a target instance by its identifier"""
        instance = self.target_instances.get(identifier) or (
            self.parent.get_target_instance(identifier) if self.parent else None
        )
        if not instance:
            raise MappingError(f"Target instance '{identifier}' not found in current or parent scopes.")
        return instance

    def get_source_instance(self, identifier: str) -> Optional[BaseModel]:
        """Get a source instance by its identifier"""
        instance = self.source_instances.get(identifier) or (
            self.parent.get_source_instance(identifier) if self.parent else None
        )
        if not instance:
            raise MappingError(f"Source instance '{identifier}' not found in current or parent scopes.")
        return instance

    def get_type(self, identifier: str) -> Optional[type[BaseModel]]:
        """Get a type by its identifier"""
        type_ = self.types.get(identifier) or (
            self.parent.get_type(identifier) if self.parent else None
        )
        if not type_:
            raise MappingError(f"Type '{identifier}' not found in current or parent scopes.")
        return type_

    def lookup(self, identifier: str) -> Optional[Any]:
        """Look up a variable, checking parent scopes if not found locally"""
        if identifier in self.variables:
            return self.variables[identifier]
        elif identifier in self.types:
            return self.types[identifier]
        elif identifier in self.groups:
            return self.groups[identifier]
        elif self.parent:
            return self.parent.lookup(identifier)
        return None

    def exists(self, identifier: str) -> bool:
        """Check if identifier exists in this scope or any parent scope"""
        return self.lookup(identifier) is not None

    def exists_local(self, identifier: str) -> bool:
        """Check if identifier exists in the current scope only"""
        return identifier in self.variables or identifier in self.types

    def get_all_symbols(self) -> Dict[str, Any]:
        """Get all symbols visible from this scope (including inherited)"""
        all_symbols = {}
        if self.parent:
            all_symbols.update(self.parent.get_all_symbols())
        all_symbols.update(self.variables)
        return all_symbols

    def get_path(self) -> List[str]:
        """Get the path from root to this scope"""
        if self.parent:
            return self.parent.get_path() + [self.name]
        return [self.name]

    def is_processing_rule(self, rule_name: str) -> bool:
        """Check if a rule is currently being processed (cycle detection)."""
        return rule_name in self.processing_rules

    def start_processing_rule(self, rule_name: str) -> None:
        """Mark a rule as being processed."""
        self.processing_rules.add(rule_name)

    def finish_processing_rule(self, rule_name: str) -> None:
        """Mark a rule as finished processing."""
        self.processing_rules.discard(rule_name)

    def __str__(self) -> str:
        return f"Scope({self.name}, variables: {list(self.variables.keys())}, types: {list(self.types.keys())})"

    def __repr__(self) -> str:
        return f"Scope(name='{self.name}', parent={self.parent.name if self.parent else None}, variables={list(self.variables.keys())}, types={list(self.types.keys())})"


class FHIRMappingEngine:
    """
    Main FHIR Mapping Language execution engine.

    This engine processes StructureMap resources to transform FHIR data
    from source structures to target structures following the FHIR Mapping
    Language specification.
    """

    def __init__(
        self,
        repository: CompositeStructureDefinitionRepository | None = None,
        factory: ResourceFactory | None = None,
    ):
        """
        Initialize the mapping engine.

        Args:
            repository (CompositeStructureDefinitionRepository | None): Structure definition repository for resolving canonical URLs. If `None`, a default empty repository will be created.
        """
        self.repository = repository or CompositeStructureDefinitionRepository()
        self.factory = factory or ResourceFactory(repository=self.repository)

    def execute(
        self,
        structure_map: StructureMap,
        sources: tuple[BaseModel | dict, ...],
        targets: tuple[BaseModel | dict, ...] | None = None,
        group: str | None = None
    ) -> tuple[BaseModel, ...]:
        
        if not isinstance(sources, tuple):
            sources = (sources,)

        source_models = self._resolve_structure_definitions(
            structure_map, StructureMapModelMode.SOURCE
        )
        target_models = self._resolve_structure_definitions(
            structure_map, StructureMapModelMode.TARGET
        )

        validated_sources = self._validate_source_data(sources, source_models)

        global_scope = MappingScope(
            name="global",
            types={**source_models, **target_models},
            groups=OrderedDict([(group.name, group) for group in structure_map.group or []]),
            concept_maps={map.name: map for map in (structure_map.contained or []) if map.resourceType == "ConceptMap"}
        )

        target_group = global_scope.groups.get(group) or list(global_scope.groups.values())[0]

        # Validate the group parameters
        expected_sources = len([input for input in (target_group.input or []) if input.mode == StructureMapModelMode.SOURCE])
        if len(validated_sources) != expected_sources:
            raise RuntimeError(f'Entrypoint group {target_group.name} expected {expected_sources} sources, got {len(sources)}.')
        if targets:
            expected_targets = len([input for input in (target_group.input or []) if input.mode == StructureMapModelMode.TARGET])
            if len(targets) != expected_targets:
                raise RuntimeError(f'Entrypoint group {target_group.name} expected {expected_sources} targets, got {len(sources)}.')
        parameters = []
        for input in target_group.input:
            if input.mode == StructureMapModelMode.SOURCE:
                if input.type:
                    source_instance = validated_sources.get(input.type)
                    if not source_instance:
                        raise TypeError(f"Invalid source provided. None of the source arguments matches the '{input.name}' parameter of type {input.type} for the entrypoint group '{target_group.name}'.")
                else:
                    source_instance = sources.pop(0) 
                source_instance_id = f"source_{id(source_instance)}"
                global_scope.source_instances[source_instance_id] = source_instance
                parameters.append(fhirpath.Element(source_instance_id))
                    
            if input.mode == StructureMapModelMode.TARGET:
                if input.type and (target_type := global_scope.types.get(input.type)):
                    if not targets:
                        target_instance = target_type.model_construct()
                    else:
                        target_instance = next((target for target in targets if isinstance(target, target_type)), None)
                        if not target_instance:
                            raise TypeError(f"Invalid target provided. None of the target arguments matches the {input.name} parameters of type {input.type} for the entrypoint group '{target_group.name}'.")
                else:
                    if targets:
                        target_instance = targets.pop(0)
                    else:
                        raise RuntimeError(f"Entrypoint group '{target_group.name}' parameter {input.name} does not specify any type and no target instances have been provided.")                                        

                target_instance_id = f"source_{id(target_instance)}"
                global_scope.target_instances[target_instance_id] = target_instance
                parameters.append(fhirpath.Element(target_instance_id))

        self.process_group(target_group, parameters, global_scope)

        return tuple(
            [
                instance.model_validate(instance.model_dump())
                for instance in global_scope.target_instances.values()
            ]
        )

    def _resolve_structure_definitions(
        self, structure_map: StructureMap, mode: StructureMapModelMode
    ) -> Dict[str, type[BaseModel]]:
        """
        Resolve source and target structure definitions from the repository.

        Args:
            structure_map (StructureMap): The structure map containing structure references

        Returns:
            Dict[str, StructureDefinition]: Mapping of structure aliases to resolved structure definitions

        Raises:
            StructureDefinitionNotFoundError: If structure definitions canonical URLs cannot be resolved within the repository
            ValidationError: If input validation fails
        """
        if not structure_map.structure:
            raise ValidationError("Structure map does not specify any structures")

        return {
            s.alias
            or s.url: self.factory.construct_resource_model(
                structure_definition=self.repository.get(s.url)
            )
            for s in structure_map.structure
            if s.mode == mode
        }

    def _validate_source_data(
        self,
        source_data: tuple[BaseModel | dict, ...],
        source_models: Dict[str, Type[BaseModel]],
    ) -> dict[str, BaseModel]:
        """
        Validate input data against source structure.

        Args:
            source_data (tuple[BaseModel | dict, ...]): Tuple of source data object
            source_models (Dict[str, Type[BaseModel]]): Mapping of structure aliases to Pydantic model classes for validation

        Returns:
            (dict[str, BaseModel]): Mapping of aliases to validated source data instances
        """
        validated_entries = {}

        def _validate_entry(entry: BaseModel | dict) -> None:
            for alias, source_model in source_models.items():
                try:
                    if isinstance(entry, source_model):
                        validated_entries[alias] = entry
                    elif isinstance(entry, dict):
                        validated_entries[alias] = source_model(**entry)
                    elif hasattr(entry, "__dict__"):
                        validated_entries[alias] = source_model(**entry.__dict__)
                    return None
                except ValidationError:
                    continue
            else:
                raise ValidationError(
                    f"Source data entry of type {type(entry)} does not match any source model"
                )

        for entry in source_data:
            _validate_entry(entry)

        return validated_entries

    def validate_structure_map(self, structure_map: StructureMap) -> List[str]:
        """
        Validate a structure map for common issues.

        Args:
            structure_map: The structure map to validate

        Returns:
            List of validation warnings/errors
        """
        issues = []

        # Check basic structure
        if not structure_map.group:
            issues.append("StructureMap has no groups defined")

        if not structure_map.structure:
            issues.append("StructureMap has no structure declarations")

        # Check structure declarations
        source_structures = [
            s for s in structure_map.structure or [] if s.mode == "source"
        ]
        target_structures = [
            s for s in structure_map.structure or [] if s.mode == "target"
        ]

        if not source_structures:
            issues.append("No source structures defined")
        if not target_structures:
            issues.append("No target structures defined")

        # Check groups and rules
        for group in structure_map.group or []:
            if not group.rule:
                issues.append(f"Group {group.name} has no rules")

            for rule in group.rule or []:
                self._validate_rule(rule, issues)

        return issues

    def _validate_rule(self, rule: StructureMapRule, issues: List[str]) -> None:
        """Validate a single rule."""
        rule_name = rule.name or f"unnamed_rule_{id(rule)}"

        if not rule.source:
            issues.append(f"Rule {rule_name} has no source elements")

        if not rule.target:
            issues.append(f"Rule {rule_name} has no target elements")

        # Check for potential cycles in dependent rules
        if rule.dependent:
            for dep in rule.dependent:
                if dep.name == rule.name:
                    issues.append(f"Rule {rule_name} depends on itself")

        # Validate nested rules
        for nested_rule in rule.rule or []:
            self._validate_rule(nested_rule, issues)
        # Validate nested rules
        for nested_rule in rule.rule or []:
            self._validate_rule(nested_rule, issues)

    def process_group(
        self, group: StructureMapGroup, parameters: list[FHIRPath] | tuple[FHIRPath], scope: MappingScope
    ):
        group_name = group.name or f"group_{id(group)}"

        # Construct local group scope
        group_scope = MappingScope(
            name=group_name,
            parent=scope,
        )

        # Validate input parameters
        if len(group.input) != len(parameters):
            raise MappingError(f"Invalid number of parameters provided for group '{group_name}'. Expected {len(group.input)}, got {len(parameters)}.")
        for input, parameter in zip(group.input, parameters):
            group_scope.define(input.name, parameter)
        
        # Process rules in order, handling 'first' and 'last' list modes
        rules = [] 
        first_rule, last_rule = None, None
        for rule in group.rule or []:   
            if rule.target and (targetMode := next((target.listMode for target in rule.target if target.listMode), [None])[0]):
                if targetMode == StructureMapTargetListMode.FIRST:
                    if first_rule:
                        raise RuntimeError('Only one rule with "first" target list mode is allowed per group.')
                    first_rule = rule
                elif targetMode == StructureMapTargetListMode.LAST:
                    if last_rule:
                        raise RuntimeError('Only one rule with "last" target list mode is allowed per group.')
                    last_rule = rule
                else:
                    raise NotImplementedError("Only 'first' and 'last' target list modes are implemented so far. Mode '{}' not implemented")
            else:
                rules.append(rule)
        rules = ([first_rule] if first_rule else []) + rules + ([last_rule] if last_rule else [])

        # Process each rule
        for rule in rules:
            self.process_rule(rule, group_scope)


    def process_rule(self, rule: StructureMapRule, scope: MappingScope) -> MappingScope:
        rule_name = rule.name or f"rule_{id(rule)}"

        # Check for cycles
        if scope.is_processing_rule(rule_name):
            logger.warning(f"Cycle detected in rule {rule_name}, skipping")
            return scope
        scope.start_processing_rule(rule_name)

        try:
            logger.debug(f"Processing rule: {rule_name}")

            # Process sources first to determine iteration
            source_iterations = {}

            for source in rule.source or []:
                var_name = self.process_source(source, scope)
                source_fhirpath = scope.lookup(var_name)

                # Where condition
                if source.condition:
                    condition_fhirpath = fhirpath_parser.parse(source.condition)
                    condition_fhirpath = _replace_mapping_scope_elements(
                        condition_fhirpath, scope
                    )

                    if not bool(condition_fhirpath.single(scope.get_instances())):
                        logger.debug(f"Source condition not met for rule {rule_name}")
                        return scope

                # Check condition
                if source.check:
                    condition_fhirpath = fhirpath_parser.parse(source.check)
                    condition_fhirpath = _replace_mapping_scope_elements(
                        condition_fhirpath, scope
                    )

                    if not bool(condition_fhirpath.single(scope.get_instances())):
                        raise RuleProcessingError(
                            f"Source check failed for rule {rule_name}"
                        )

                # Collect source values for iteration
                if source_fhirpath is None:
                    raise RuleProcessingError(f"Source variable {var_name} not found")
                source_iterations[var_name] = source_fhirpath.count(scope.get_instances())
            
            for source_var, iterations in source_iterations.items():
                for source_iteration in range(iterations):

                    logger.debug(
                        f"Processing iteration {source_iteration} for rule {rule_name}"
                    )
                    # Create iteration scope
                    iteration_scope = MappingScope(
                        name=f"{scope.name}_iter_{source_iteration}",
                        source_instances=scope.source_instances.copy(),
                        target_instances=scope.target_instances.copy(),
                        types=scope.types.copy(),
                        variables=scope.variables.copy(),  # Copy existing variables
                        parent=scope.parent,
                    )
                    
                    # Set the source variable to an indexed FHIRPath
                    iteration_scope.define(source_var, scope.lookup(source_var)._invoke(fhirpath.Index(source_iteration)))

                    # Process targets for this iteration
                    for target in rule.target or []:
                        self.process_target(target, iteration_scope)

                    # Process dependent rules for this iteration
                    for dependent in rule.dependent or []:
                        dependent_group = iteration_scope.lookup(dependent.name)
                        parameters = [iteration_scope.lookup(param.valueId) for param in dependent.parameter]
                        self.process_group(dependent_group, parameters, iteration_scope)

                    # Process nested rules for this iteration
                    for nested_rule in rule.rule or []:
                        self.process_rule(nested_rule, iteration_scope)

                    # Merge back iteration results to main scope
                    scope.target_instances.update(iteration_scope.target_instances)

        finally:
            scope.finish_processing_rule(rule_name)
        return scope

    def process_source(self, source: StructureMapSource, scope: MappingScope) -> str:
        path = scope.lookup(source.context)
        if path is None:
            raise RuleProcessingError(f"Source context {source.context} not found")

        # Apply element path if specified
        if source.element:
            path = path._invoke(fhirpath.Element(source.element))

        # Apply list-option condition if specified
        if source.listMode == "first":
            path = path._invoke(fhirpath.First())
        elif source.listMode == "not_first":
            path = path._invoke(fhirpath.Tail())
        elif source.listMode == "not_last":
            path = path._invoke(fhirpath.Exclude(path._invoke(fhirpath.Last())))
        elif source.listMode == "last":
            path = path._invoke(fhirpath.Last())
        elif source.listMode == "only_one":
            path = path._invoke(fhirpath.Single())

        # Store source FHIRPath
        var_name = source.variable or f"source_{id(source)}"
        scope.define(var_name, path)
        return var_name

    def process_target(
        self,
        target: StructureMapTarget,
        scope: MappingScope,
        ) -> Any:
        if not target.context:
            raise RuleProcessingError("Target context is required")
        path = scope.lookup(target.context)
        if path is None:
            raise RuleProcessingError(f"Target context {target.context} not found")

        # Apply element path if specified
        if target.element:
            path = path._invoke(fhirpath.Element(target.element))

        insert_index = path.count(scope.get_instances())
        path = path._invoke(fhirpath.Index(insert_index))

        # Store target FHIRPath
        var_name = target.variable or f"target_{id(target)}"
        scope.define(var_name, path)

        transform = target.transform
        if transform:
            if transform == "copy":
                transformed_value = self._copy_transform(scope, target.parameter)
            elif transform == "create":
                transformed_value = self._create_transform(scope, target.parameter)
            elif transform == "truncate":
                transformed_value = self._truncate_transform(scope, target.parameter)
            elif transform == "escape":
                raise NotImplementedError("Escape transform not implemented yet")
            elif transform == "cast":
                transformed_value = self._cast_transform(scope, target.parameter)
            elif transform == "append":
                transformed_value = self._append_transform(scope, target.parameter)
            elif transform == "reference":
                transformed_value = self._reference_transform(scope, target.parameter)
            elif transform == "dateOp":
                raise NotImplementedError("DateOp transform not implemented yet")
            elif transform == "uuid":
                transformed_value = self._uuid_transform(scope, target.parameter)
            elif transform == "pointer":
                raise NotImplementedError("Pointer transform not implemented yet")
            elif transform == "translate":
                transformed_value = self._translate_transform(scope, target.parameter)
            elif transform == "evaluate":
                transformed_value = self._evaluate_transform(scope, target.parameter)
            elif transform == "cc":
                transformed_value = self._cc_transform(scope, target.parameter)
            elif transform == "c":
                transformed_value = self._c_transform(scope, target.parameter)
            elif transform == "qty":
                transformed_value = self._qty_transform(scope, target.parameter)
            elif transform == "id":
                transformed_value = self._id_transform(scope, target.parameter)
            elif transform == "cp":
                transformed_value = self._cp_transform(scope, target.parameter)
            else:
                raise RuntimeError(
                    f"Invalid FHIR Mapping Language transform: {transform}"
                )

            # Update the target structure
            path.update_single(scope.get_instances(), transformed_value)


    @staticmethod
    def _copy_transform(scope: MappingScope, parameters: List[StructureMapParameter]) -> Any:
        if (
            not parameters or len(parameters) != 1
            or not (
                (source := parameters[0].valueId)
                or 
                (literal := parameters[0].value) 
            )
        ):
            raise RuleProcessingError(
                "Copy transform requires exactly one parameter of type Id or a literal value."
            )
        # Just copy the source value or use the literal
        if source:
            source_fhirpath = scope.lookup(source)
            if not source_fhirpath:
                raise RuleProcessingError(f"Source variable {source} not found")
            # Just copy the source value
            return source_fhirpath.single(scope.get_instances())
        elif literal:
            # Just use the literal value
            return literal

    @staticmethod
    def _create_transform(scope: MappingScope, parameters: List[StructureMapParameter]) -> BaseModel:
        if (
            not parameters or len(parameters) != 1
            or not (create_type := parameters[0].value)
        ):
            raise RuleProcessingError(
                "The 'create' transform requires exactly one parameter of type String"
            )
        return scope.get_type(create_type).model_construct()


    @staticmethod
    def _truncate_transform(scope: MappingScope, parameters: List[StructureMapParameter]) -> str:
        if (
            not parameters
            or len(parameters) != 2
            or not (source := parameters[0].valueId)
            or not (length := parameters[1].valueInteger)
        ):
            raise RuleProcessingError(
                "The 'truncate' transform requires exactly two parameters of type Id and Integer"
            )
        source_fhirpath = scope.lookup(source)
        if not source_fhirpath:
            raise RuleProcessingError(f"Source variable {source} not found")
        return source_fhirpath._invoke(
            fhirpath.Substring(0, int(length))
        ).single(scope.get_instances())


    @staticmethod
    def _cast_transform(scope: MappingScope, parameters: List[StructureMapParameter]) -> Any:
        if (
            not parameters
            or len(parameters) < 1
            or len(parameters) > 2
            or not (source := parameters[0].valueId)
            or not (
                to_type := (
                    parameters[1].valueString
                    if len(parameters) == 2
                    else None
                )
            )
        ):
            raise RuleProcessingError(
                "The 'cast' transform requires at least one parameter of type Id and optionally a second parameter of type String"
            )
        if not to_type:
            raise RuleProcessingError(
                "Implicit type casting if not supported for the 'cast' transform. Please specify the target type explicitly."
            )
        source_fhirpath = scope.lookup(source)
        if not source_fhirpath:
            raise RuleProcessingError(f"Source variable {source} not found")
        return source_fhirpath._invoke(
            getattr(fhirpath, f"To{to_type.title()}")()
        ).single(scope.get_instances())


    @staticmethod
    def _append_transform(scope: MappingScope, parameters: List[StructureMapParameter]) -> str:
        if (
            not parameters
            or len(parameters) < 1
        ):
            raise RuleProcessingError(
                "The 'append' transform requires at least one parameter of type Id and String"
            )
        strings = []
        for parameter in parameters:
            if parameter.valueId:
                source_fhirpath = scope.lookup(parameter.valueId)
                if not source_fhirpath:
                    raise RuleProcessingError(f"Source variable {parameter.valueId} not found")
                strings.append(str(source_fhirpath.single(scope.get_instances())))
            elif parameter.valueString:
                strings.append(parameter.valueString)
            else:
                raise RuleProcessingError("Invalid parameter type for 'append' transform")
        return ''.join(strings)

    @staticmethod
    def _reference_transform(scope: MappingScope, parameters: List[StructureMapParameter]) -> str:
        if (
            not parameters
            or len(parameters) != 1
            or not (source := parameters[0].valueId)
        ):
            raise RuleProcessingError(
                "The 'reference' transform requires exactly one parameter of type Id"
            )
        source_fhirpath = scope.lookup(source)
        if not source_fhirpath:
            raise RuleProcessingError(f"Source variable {source} not found")
        resource_type = source_fhirpath._invoke(
            fhirpath.Element('resourceType')
        ).single(scope.get_instances())
        resource_id = source_fhirpath._invoke(
            fhirpath.Element('id')
        ).single(scope.get_instances())
        return f"{resource_type}/{resource_id}"
    
    @staticmethod
    def _uuid_transform(scope: MappingScope, parameters: List[StructureMapParameter]) -> str:
        if parameters:
            raise RuleProcessingError(
                "The 'uuid' transform does not take any parameters"
            )
        return str(uuid.uuid4())

    @staticmethod
    def _translate_transform(scope: MappingScope, parameters: List[StructureMapParameter]) -> str:
        if (
            not parameters
            or len(parameters) != 3
            or not (source := parameters[0].valueId)
            or not (map_name := parameters[1].valueString)
            or not (output := parameters[2].valueString)
        ):
            raise RuleProcessingError(
                "The 'translate' transform requires exactly two parameters of type Id and Integer"
            )
        
        source_code = scope.lookup(source).single(scope.get_instances())
        concept_map = scope.get_concept_map(map_name.lstrip('#'))
        if not concept_map:
            raise MappingError(f"Concept map '{map_name}' could not be resolved.")
        for group in concept_map.group:
            for element in group.element:
                for element_target in element.target:
                    if element.code == source_code:
                        if output == 'code':
                            return element_target.code
                        else:
                            raise NotImplementedError(f"Output mode '{output}' for translate operation is not yet implemented.")
        else:
            raise MappingError(f"Could not map source code '{source_code}' using concept map '{map_name}'.")

    @staticmethod
    def _evaluate_transform(scope: MappingScope, parameters: List[StructureMapParameter]) -> str:
        if len(parameters) == 1:
            raise NotImplementedError(
                "The evaluate transforms with implicit FHIRPath context is not supported."
            )   
        if (len(parameters) != 2
            or not (source := parameters[0].valueId)
            or not (evaluate_fhirpath := parameters[1].valueString)
        ):
            raise RuleProcessingError(
                "The 'evaluate' transform requires exactly two parameters of type Id and String"
            )
        context = scope.lookup(source).single(scope.get_instances())
        if not context:
            raise MappingError(f"Context '{context}' could not be resolved.")
        transformed_values =  fhirpath_parser.parse(evaluate_fhirpath).values(context)
        if transformed_values and len(transformed_values) > 1:
            raise MappingError(f"Currently, the evaluate transform only supports FHIRPath expressions that yield a single value. It returned {len(transformed_values)}")
        return transformed_values[0] if transformed_values else None

    @staticmethod
    def _cc_transform(scope: MappingScope, parameters: List[StructureMapParameter]) -> CodeableConcept:
        if not parameters or len(parameters)>3 or len(parameters)<1:
            raise RuleProcessingError(
                "The 'cc' transform either one parameter of type String or two parameters of type String and String"
            )        
        if len(parameters) == 1:
            return CodeableConcept(text=parameters[0].valueString)
        else:
            return CodeableConcept(coding=[Coding(
                code=parameters[0].valueString,
                system=parameters[1].valueString,
                display=parameters[2].valueString if len(parameters) == 3 else None,
            )])

    @staticmethod
    def _c_transform(scope: MappingScope, parameters: List[StructureMapParameter]) -> Coding:
        if not parameters or len(parameters)>3 or len(parameters)<2:
            raise RuleProcessingError(
                "The 'c' transform takes two or three parameters of type String"
            )       
        return Coding(
            code=parameters[0].valueString,
            system=parameters[1].valueString,
            display=parameters[2].valueString if len(parameters) == 3 else None,
        )

    @staticmethod
    def _qty_transform(scope: MappingScope, parameters: List[StructureMapParameter]) -> Quantity:
        if not parameters or len(parameters)>4 or len(parameters)<1:
            raise RuleProcessingError(
                "The 'qty' transform takes at least one or two parameters of type String"
            )       
        if len(parameters) == 1:
            matches = re.search(r"(<|<=|>=|>|ad)?(\d+((\.|\,)\d+)?) (.*)", parameters[0].valueString)
            if not matches:
                raise RuleProcessingError(
                    "The 'qty' transform single parameter must be of the form '[<|<=|>=|>|ad]<number> <unit>'"
                )
            
            return Quantity(
                comparator=matches.group(1) if matches.group(1) else None,
                value=float(matches.group(2).replace(',', '.')),
                unit=matches.group(5),
                system=None,
                code=None,
            )
        else:
            return Quantity(
                value=float(parameters[0].valueString),
                unit=parameters[1].valueString,
                system=parameters[2].valueString if len(parameters) > 2 else None,
                code=parameters[3].valueString if len(parameters) > 2 else None,
            )

    @staticmethod
    def _id_transform(scope: MappingScope, parameters: List[StructureMapParameter]) -> Identifier:
        if not parameters or len(parameters)>3 or len(parameters)<2:
            raise RuleProcessingError(
                "The 'id' transform takes at least two or three parameters of type String"
            )       
        return Identifier(
            system=parameters[0].valueString,
            value=parameters[1].valueString,
            type=CodeableConcept(
                coding=[Coding(
                    code=parameters[2].valueString, 
                    system='http://hl7.org/fhir/ValueSet/identifier-type'
            )]) if len(parameters) == 3 else None,
        )

    @staticmethod
    def _cp_transform(scope: MappingScope, parameters: List[StructureMapParameter]) -> ContactPoint:
        if not parameters or len(parameters)>2 or len(parameters)<1:
            raise RuleProcessingError(
                "The 'cp' transform takes at least one or two parameters of type String"
            )       
        if len(parameters) == 1:
            raise NotImplementedError(
                "The 'cp' transform with a single parameter is not yet implemented"
            )
        return ContactPoint(
            system=parameters[0].valueString,
            value=parameters[1].valueString,
        )

def _replace_mapping_scope_elements(path, scope: MappingScope):
    """
    Replace FHIRPath Element references with context Element references.

    This is used to adjust FHIRPath expressions to the current mapping context.
    """
    if isinstance(path, fhirpath.Element):
        if scope_fhirpath := scope.lookup(path.label):
            return scope_fhirpath
        return fhirpath.Element(f"{path.label}")
    elif isinstance(path, (fhirpath.Invocation)):
        left = _replace_mapping_scope_elements(path.left, scope)
        right = _replace_mapping_scope_elements(path.right, scope)
        return fhirpath.Invocation(left, right)
    elif isinstance(path, fhirpath.FHIRComparisonOperator):
        left = _replace_mapping_scope_elements(path.left, scope)
        right = _replace_mapping_scope_elements(path.right, scope)
        return path.__class__(left, right)
    return path
