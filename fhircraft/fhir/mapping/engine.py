"""
FHIR Mapping Language Engine

This module provides the core FHIR Mapping Language execution engine that processes
StructureMap resources to transform FHIR data from source to target structures.
"""

import enum
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Type

from pydantic import BaseModel

from fhircraft.fhir.mapping.StructureMap import (
    StructureMap,
    StructureMapDependent,
    StructureMapGroup,
    StructureMapRule,
    StructureMapSource,
    StructureMapTarget,
)
from fhircraft.fhir.path import fhirpath
from fhircraft.fhir.path.engine.core import FHIRPath
from fhircraft.fhir.path.exceptions import FHIRPathError
from fhircraft.fhir.resources.factory import ResourceFactory
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


class StructureMapModelMode(str, enum.Enum):
    """Enumeration of StructureMap model modes."""

    SOURCE = "source"  #
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
    """The source instances being constructed"""

    target_instances: Dict[str, BaseModel] = field(default_factory=dict)
    """The target instances being constructed"""

    variables: Dict[str, FHIRPath] = field(default_factory=dict)
    """Mapping variables names to resolved FHIRPaths"""

    processing_rules: Set[str] = field(default_factory=set)
    """Set of currently processing rules"""

    parent: Optional["MappingScope"] = None
    """Parent mapping scope"""

    def define(self, variable: str, value: FHIRPath) -> None:
        """Define a new variable in this scope"""
        self.variables[variable] = value

    def lookup(self, identifier: str) -> Optional[Any]:
        """Look up a variable, checking parent scopes if not found locally"""
        if identifier in self.variables:
            return self.variables[identifier]
        elif identifier in self.types:
            return self.types[identifier]
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
        data: tuple[BaseModel | dict, ...] | BaseModel | dict,
    ) -> tuple[BaseModel, ...]:
        """
        Execute a structure map transformation.

        Args:
            structure_map: The StructureMap resource defining the transformation
            data: The source data to transform
        Returns:
            The transformed target resource

        Raises:
            StructureDefinitionNotFoundError: If required structure definitions cannot be resolved
            ValidationError: If input validation fails
            MappingError: If transformation fails
        """
        if not isinstance(data, tuple):
            data = (data,)

        source_models = self._resolve_structure_definitions(
            structure_map, StructureMapModelMode.SOURCE
        )
        target_models = self._resolve_structure_definitions(
            structure_map, StructureMapModelMode.TARGET
        )

        validated_sources = self._validate_source_data(data, source_models)

        global_scope = MappingScope(
            name="global",
            source_instances=validated_sources,
            types={**source_models, **target_models},
        )

        # Step 4: Apply mapping rules
        for group in structure_map.group or []:
            global_scope = self.process_group(group, global_scope)

        # Step 5: Return output resource
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
        self, group: StructureMapGroup, context: MappingScope
    ) -> MappingScope:
        group_name = group.name or f"group_{id(group)}"

        # Create local context for the group
        group_source_models = {}
        group_target_models = {}
        group_source_instances = {}
        group_target_instances = {}
        for input in group.input or []:
            if input.mode == StructureMapModelMode.SOURCE:
                if input.type in context.types:
                    group_source_models[input.name] = context.types[input.type]
                    group_source_instances[input.name] = context.source_instances.get(
                        input.type
                    )

            elif input.mode == StructureMapModelMode.TARGET:
                if input.type in context.types:
                    group_target_models[input.name] = context.types[input.type]
                    group_target_instances[input.name] = context.target_instances.get(
                        input.type
                    )

        group_context = MappingScope(
            name=group_name,
            source_instances=group_source_instances,
            target_instances=group_target_instances,
            parent=context,
        )

        for rule in group.rule or []:
            group_context = self.process_rule(rule, group_context)

        context.target_instances.update(group_context.target_instances)
        return context

    def process_rule(
        self,
        rule: StructureMapRule,
        scope: MappingScope,
        rule_variables: Dict[str, Any] = {},
    ) -> MappingScope:
        rule_name = rule.name or f"rule_{id(rule)}"

        # Check for cycles
        if scope.is_processing_rule(rule_name):
            logger.warning(f"Cycle detected in rule {rule_name}, skipping")
            return scope

        scope.start_processing_rule(rule_name)
        rule_variables.update(scope.source_instances)
        rule_variables.update(scope.target_instances)
        try:
            logger.debug(f"Processing rule: {rule_name}")

            # Process sources
            for source in rule.source or []:
                source_value = self.process_source(source, rule_variables)

                # Store source value
                var_name = source.variable or f"source_{id(source)}"
                rule_variables[var_name] = source_value

                # Check source condition
                if source.condition:
                    if not bool(
                        fhirpath.parse(source.condition).single(rule_variables)
                    ):
                        logger.debug(f"Source condition not met for rule {rule_name}")
                        return scope

            # Process targets
            for target in rule.target or []:
                assert target.element and target.context
                target_instance = scope.target_instances.get(target.context)
                if not target_instance:
                    raise RuleProcessingError(
                        f"Target context {target.context} not found for rule {rule_name}"
                    )
                value = self.process_target(target, rule_variables)

                if isinstance(value, list):
                    if not is_list_field(
                        target_instance.__class__.model_fields[target.element]
                    ):
                        if len(value) > 1:
                            raise RuleProcessingError(
                                f"Multiple values returned for non-list field {target.element} in rule {rule_name}"
                            )
                        value = value[0] if value else None
                setattr(target_instance, target.element, value)

                if target.variable:
                    rule_variables[target.variable] = value

            # Process dependent rules
            for dependent in rule.dependent or []:
                self._process_dependent(dependent, scope, rule_variables)

            # Process nested rules
            for nested_rule in rule.rule or []:
                self.process_rule(nested_rule, scope)

        finally:
            scope.finish_processing_rule(rule_name)
        return scope

    def process_source(
        self, source: StructureMapSource, rule_variables: Dict[str, Any]
    ) -> Any:
        source_item = rule_variables.get(source.context)
        # Apply element path if specified
        if source.element:
            try:
                # Parse and evaluate FHIRPath manually
                if isinstance(source_item, list):
                    values = [
                        getattr(list_item, source.element) for list_item in source_item
                    ]
                else:
                    values = getattr(source_item, source.element)

                if source.listMode == "first":
                    return values[0] if values else None
                elif source.listMode == "not_first":
                    return values[1] if len(values) > 1 else None
                elif source.listMode == "not_last":
                    return values[:-1] if values else None
                elif source.listMode == "last":
                    return values[-1] if values else None
                elif source.listMode == "only_one":
                    if len(values) != 1:
                        raise RuleProcessingError(
                            f"Expected exactly one value for {source.element}, got {len(values)}"
                        )
                    return values[0]
                else:
                    return values

            except (FHIRPathError, IndexError) as e:
                logger.warning(
                    f"Failed to extract source element {source.element}: {e}"
                )
                return None

        return source_item

    def process_target(
        self,
        target: StructureMapTarget,
        rule_variables: Dict[str, Any],
    ) -> Any:
        """
        Process a target element to create or update target data.

        Args:
            target: The target element to process
            source_value: The value from source processing
            available_vars: Available variables in current scope
        """
        transform = target.transform
        if not transform:
            return None
        if transform == "copy":
            if (
                not target.parameter
                or len(target.parameter) != 1
                or not (source := target.parameter[0].valueId)
            ):
                raise RuleProcessingError(
                    "Copy transform requires exactly one parameter of type Id"
                )
            return rule_variables.get(source)

        elif transform == "create":
            raise NotImplementedError("Create transform not implemented yet")
        elif transform == "truncate":
            if (
                not target.parameter
                or len(target.parameter) != 2
                or not (source := target.parameter[0].valueId)
                or not (length := target.parameter[1].valueInteger)
            ):
                raise RuleProcessingError(
                    "The 'copy' transform requires exactly two parameters of type Id and Integer"
                )
            return fhirpath.parse(f"{source}.substring(0,{length})").single(
                rule_variables
            )

        elif transform == "escape":
            raise NotImplementedError("Escape transform not implemented yet")

        elif transform == "cast":
            if (
                not target.parameter
                or len(target.parameter) < 1
                or len(target.parameter) > 2
                or not (source := target.parameter[0].valueId)
                or not (
                    to_type := (
                        target.parameter[1].valueString
                        if len(target.parameter) == 2
                        else None
                    )
                )
            ):
                raise RuleProcessingError(
                    "The 'copy' transform requires exactly two parameters of type Id and Integer"
                )
            if not to_type:
                raise RuleProcessingError(
                    "The 'cast' transform requires a type parameter of type String"
                )
            return fhirpath.parse(f"{source}.to{to_type.title()}()").single(
                rule_variables
            )

        elif transform == "append":
            raise NotImplementedError("Append transform not implemented yet")
        elif transform == "translate":
            raise NotImplementedError("Translate transform not implemented yet")
        elif transform == "reference":
            raise NotImplementedError("Reference transform not implemented yet")
        elif transform == "dateOp":
            raise NotImplementedError("DateOp transform not implemented yet")
        elif transform == "uuid":
            raise NotImplementedError("UUID transform not implemented yet")
        elif transform == "pointer":
            raise NotImplementedError("Pointer transform not implemented yet")
        elif transform == "translate":
            raise NotImplementedError("Translate transform not implemented yet")
        elif transform == "evaluate":
            raise NotImplementedError("Evaluate transform not implemented yet")
        elif transform == "cc":
            raise NotImplementedError("cc transform not implemented yet")
        elif transform == "c":
            raise NotImplementedError("c transform not implemented yet")
        elif transform == "qty":
            raise NotImplementedError("qty transform not implemented yet")
        elif transform == "id":
            raise NotImplementedError("id transform not implemented yet")
        elif transform == "cp":
            raise NotImplementedError("cp transform not implemented yet")
        else:
            raise RuntimeError(f"Invalid FHIR Mapping Language transform: {transform}")

    def _process_dependent(
        self,
        dependent: StructureMapDependent,
        scope: MappingScope,
        rule_variables: Dict[str, Any],
    ) -> None:
        """Process a dependent rule reference."""
        if dependent.name:
            # Find and execute the dependent rule
            target_rule = self._find_rule_by_name(dependent.name)
            if target_rule:
                self.process_rule(target_rule, scope, rule_variables)
            else:
                logger.warning(f"Dependent rule not found: {dependent.name}")

    def _find_rule_by_name(self, rule_name: str) -> Optional[StructureMapRule]:
        """Find a rule by name in the structure map."""
        # for group in self.structure_map.group or []:
        #     for rule in group.rule or []:
        #         if rule.name == rule_name:
        #             return rule
        #         # Check nested rules recursively
        #         nested = self._find_rule_in_nested(rule, rule_name)
        #         if nested:
        #             return nested
        # return None

    def _find_rule_in_nested(
        self, parent_rule: StructureMapRule, rule_name: str
    ) -> Optional[StructureMapRule]:
        """Recursively find a rule in nested rules."""
        # for nested_rule in parent_rule.rule or []:
        #     if nested_rule.name == rule_name:
        #         return nested_rule
        #     deeper = self._find_rule_in_nested(nested_rule, rule_name)
        #     if deeper:
        #         return deeper
        # return None
