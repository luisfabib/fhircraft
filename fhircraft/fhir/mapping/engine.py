"""
FHIR Mapping Language Engine

This module provides the core FHIR Mapping Language execution engine that processes
StructureMap resources to transform FHIR data from source to target structures.
"""

import enum
import logging
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
from fhircraft.fhir.path.exceptions import FHIRPathError
from fhircraft.fhir.resources.factory import ResourceFactory
from fhircraft.fhir.resources.repository import (
    CompositeStructureDefinitionRepository,
    StructureDefinitionNotFoundError,
)

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


class MappingContext:
    """
    Context object that maintains state during mapping execution.

    This class tracks variables, source data, target models, and provides
    utilities for rule processing.
    """

    source_models: Dict[str, type[BaseModel]]
    """Mapping of aliases to source models"""

    target_models: Dict[str, type[BaseModel]]
    """Mapping of aliases to target models"""

    source_instances: Dict[str, BaseModel]
    """The source instances being constructed"""

    target_instances: Dict[str, BaseModel]
    """The target instances being constructed"""

    variables: Dict[str, Any]
    """Mapping variables for the current context"""

    group_stack: List[str]
    """Stack of group contexts"""

    processing_rules: Set[str]
    """Set of currently processing rules"""

    def __init__(
        self,
        source_models: Dict[str, Type[BaseModel]],
        target_models: Dict[str, Type[BaseModel]],
        source_instances: Dict[str, BaseModel],
        target_instances: Dict[str, BaseModel] | None = None,
        variables: Optional[Dict[str, Any]] = None,
    ):
        self.source_instances = source_instances
        self.target_instances = target_instances or {
            alias: target_model.model_construct()
            for alias, target_model in target_models.items()
        }
        self.source_models = source_models
        self.target_models = target_models
        self.variables = variables or {}
        self.group_stack = []
        self.processing_rules = set()

    def get_variable(self, name: str) -> Any:
        """Get a variable value by name."""
        return self.variables.get(name)

    def set_variable(self, name: str, value: Any) -> None:
        """Set a variable value."""
        self.variables[name] = value

    def push_group(self, group_name: str) -> None:
        """Enter a new group context."""
        self.group_stack.append(group_name)

    def pop_group(self) -> Optional[str]:
        """Exit the current group context."""
        return self.group_stack.pop() if self.group_stack else None

    def is_processing_rule(self, rule_name: str) -> bool:
        """Check if a rule is currently being processed (cycle detection)."""
        return rule_name in self.processing_rules

    def start_processing_rule(self, rule_name: str) -> None:
        """Mark a rule as being processed."""
        self.processing_rules.add(rule_name)

    def finish_processing_rule(self, rule_name: str) -> None:
        """Mark a rule as finished processing."""
        self.processing_rules.discard(rule_name)


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

        context = MappingContext(
            source_instances=validated_sources,
            source_models=source_models,
            target_models=target_models,
        )

        # Step 4: Apply mapping rules
        for group in structure_map.group or []:
            context = self.process_group(group, context)

        # Step 5: Return output resource
        return tuple(
            [
                instance.model_validate(instance.model_dump())
                for instance in context.target_instances.values()
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
        self, group: StructureMapGroup, context: MappingContext
    ) -> MappingContext:
        group_name = group.name or f"group_{id(group)}"

        # Create local context for the group
        group_source_models = {}
        group_target_models = {}
        group_source_instances = {}
        group_target_instances = {}
        for input in group.input or []:
            if input.mode == StructureMapModelMode.SOURCE:
                if input.type in context.source_models:
                    group_source_models[input.name] = context.source_models[input.type]
                    group_source_instances[input.name] = context.source_instances.get(
                        input.type
                    )

            elif input.mode == StructureMapModelMode.TARGET:
                if input.type in context.target_models:
                    group_target_models[input.name] = context.target_models[input.type]
                    group_target_instances[input.name] = context.target_instances.get(
                        input.type
                    )

        group_context = MappingContext(
            source_instances=group_source_instances,
            target_instances=group_target_instances,
            source_models=group_source_models,
            target_models=group_target_models,
        )

        for rule in group.rule or []:
            group_context = self.process_rule(rule, group_context)

        context.target_instances.update(group_context.target_instances)
        return context

    def process_rule(
        self,
        rule: StructureMapRule,
        context: MappingContext,
        rule_variables: Dict[str, Any] = {},
    ) -> MappingContext:
        rule_name = rule.name or f"rule_{id(rule)}"

        # Check for cycles
        if context.is_processing_rule(rule_name):
            logger.warning(f"Cycle detected in rule {rule_name}, skipping")
            return context

        context.start_processing_rule(rule_name)
        rule_variables.update(context.source_instances)
        rule_variables.update(context.target_instances)
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
                        return context

            # Process targets
            for target in rule.target or []:
                assert target.element and target.context
                target_instance = context.target_instances.get(target.context)
                if not target_instance:
                    raise RuleProcessingError(
                        f"Target context {target.context} not found for rule {rule_name}"
                    )
                value = self.process_target(target, rule_variables)
                setattr(target_instance, target.element, value)

                if target.variable:
                    rule_variables[target.variable] = value

            # Process dependent rules
            for dependent in rule.dependent or []:
                self._process_dependent(dependent, context, rule_variables)

            # Process nested rules
            for nested_rule in rule.rule or []:
                self.process_rule(nested_rule, context)

        finally:
            context.finish_processing_rule(rule_name)
        return context

    def process_source(
        self, source: StructureMapSource, rule_variables: Dict[str, Any]
    ) -> Any:
        source_item = rule_variables.get(source.context)
        # Apply element path if specified
        if source.element:
            try:
                # Parse and evaluate FHIRPath manually
                values = getattr(source_item, source.element)

                if source.listMode == "first":
                    return values[0] if values else None
                elif source.listMode == "last":
                    return values[-1] if values else None
                elif source.listMode == "only":
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
        transform = target.transform or "copy"
        if transform == "copy":
            if (
                not target.parameter
                or len(target.parameter) != 1
                or not target.parameter[0].valueId
            ):
                raise RuleProcessingError(
                    "Copy transform requires exactly one parameter of type Id"
                )
            return rule_variables.get(target.parameter[0].valueId)
        elif transform == "create":
            raise NotImplementedError("Create transform not implemented yet")
        elif transform == "evaluate":
            raise NotImplementedError("Evaluate transform not implemented yet")
        elif transform == "translate":
            raise NotImplementedError("Translate transform not implemented yet")
        else:
            raise RuntimeError(f"Unsupported transform: {transform}")

    def _process_dependent(
        self,
        dependent: StructureMapDependent,
        context: MappingContext,
        rule_variables: Dict[str, Any],
    ) -> None:
        """Process a dependent rule reference."""
        if dependent.name:
            # Find and execute the dependent rule
            target_rule = self._find_rule_by_name(dependent.name)
            if target_rule:
                self.process_rule(target_rule, context, rule_variables)
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
