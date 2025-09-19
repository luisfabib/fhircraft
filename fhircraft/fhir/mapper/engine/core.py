"""
FHIR Mapping Language Engine

This module provides the core FHIR Mapping Language execution engine that processes
StructureMap resources to transform FHIR data from source to target structures.
"""

import enum
import logging
from collections import OrderedDict
from typing import Any, Dict, List, Type

from pydantic import BaseModel

import fhircraft.fhir.path.engine as fhirpath
from fhircraft.fhir.resources.datatypes.R5.resources.structure_map import (
    StructureMap,
    StructureMapGroup,
    StructureMapGroupRule,
    StructureMapGroupRuleSource,
    StructureMapGroupRuleTarget,
)
from fhircraft.fhir.path.parser import fhirpath as fhirpath_parser
from fhircraft.fhir.path.engine.core import FHIRPath
from fhircraft.fhir.resources.factory import ResourceFactory
from fhircraft.fhir.resources.repository import CompositeStructureDefinitionRepository

from .exceptions import MappingError, RuleProcessingError
from .scope import MappingScope
from .transformer import MappingTransformer

logger = logging.getLogger(__name__)


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
        repository (CompositeStructureDefinitionRepository): Repository for FHIR StructureDefinitions.
        factory (ResourceFactory): Factory for constructing FHIR resource models.
        transformer (MappingTransformer): Executes FHIRPath-based transforms.
    """

    def __init__(
        self,
        repository: CompositeStructureDefinitionRepository | None = None,
        factory: ResourceFactory | None = None,
    ):
        self.repository = repository or CompositeStructureDefinitionRepository()
        self.factory = factory or ResourceFactory(repository=self.repository)
        self.transformer = MappingTransformer()

    def execute(
        self,
        structure_map: StructureMap,
        sources: tuple[BaseModel | dict],
        targets: tuple[BaseModel | dict] | None = None,
        group: str | None = None,
    ) -> tuple[BaseModel, ...]:
        """
        Executes a FHIR StructureMap transformation using the provided sources and optional targets.

        This method resolves structure definitions, validates input data, sets up the mapping scope,
        binds source and target instances to group parameters, and processes the entrypoint group
        to produce the mapped target instances.

        Args:
            structure_map (StructureMap): The StructureMap resource defining the transformation rules.
            sources (tuple[BaseModel | dict]): Source data to be mapped, as a tuple of Pydantic models or dictionaries.
            targets (tuple[BaseModel | dict] | None, optional): Optional target instances to populate. If not provided, new instances are created as needed.
            group (str | None, optional): The name of the entrypoint group to execute. If not specified, the first group is used.

        Returns:
            tuple[BaseModel, ...]: A tuple of resulting target instances after the transformation.

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
                [(group.name, group) for group in structure_map.group or []]
            ),
            concept_maps={
                map.name: map
                for map in (structure_map.contained or [])
                if map.resourceType == "ConceptMap" and map.name
            },
        )

        # Parse and validate constants
        for const in structure_map.const or []:
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
                for input in (target_group.input or [])
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
                    for input in (target_group.input or [])
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
        for input in target_group.input:
            if input.mode == StructureMapModelMode.SOURCE:
                if input.type:
                    source_instance = validated_sources.get(input.type)
                    if not source_instance:
                        raise TypeError(
                            f"Invalid source provided. None of the source arguments matches the '{input.name}' parameter of type {input.type} for the entrypoint group '{target_group.name}'."
                        )
                else:
                    source_instance = sources[0]
                source_instance_id = f"source_{id(source_instance)}"
                global_scope.source_instances[source_instance_id] = source_instance  # type: ignore
                parameters.append(fhirpath.Element(source_instance_id))

            if input.mode == StructureMapModelMode.TARGET:
                if input.type and (target_type := global_scope.types.get(input.type)):
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
                    if targets:
                        target_instance = targets[0]
                    else:
                        raise RuntimeError(
                            f"Entrypoint group '{target_group.name}' parameter {input.name} does not specify any type and no target instances have been provided."
                        )

                target_instance_id = f"source_{id(target_instance)}"
                global_scope.target_instances[target_instance_id] = target_instance  # type: ignore
                parameters.append(fhirpath.Element(target_instance_id))

        # Process the entrypoint group
        self.process_group(target_group, parameters, global_scope)

        # Return the resulting target instances
        return tuple(
            [
                instance.model_validate(instance.model_dump())
                for instance in global_scope.target_instances.values()
            ]
        )

    def process_group(
        self,
        group: StructureMapGroup,
        parameters: list[FHIRPath] | tuple[FHIRPath],
        scope: MappingScope,
    ):
        """
        Processes a StructureMap group by validating input parameters, constructing a local mapping scope,
        and executing the group's rules in the correct order, handling special list modes ('first' and 'last').

        Args:
            group (StructureMapGroup): The group definition containing mapping rules and input definitions.
            parameters (list[FHIRPath] | tuple[FHIRPath]): The input parameters to be mapped, corresponding to the group's input definitions.
            scope (MappingScope): The parent mapping scope to use as the basis for the group's local scope.

        Raises:
            MappingError: If the number of provided parameters does not match the group's input definitions.
            RuntimeError: If more than one rule with 'first' or 'last' target list mode is found in the group.
            NotImplementedError: If a target list mode other than 'first' or 'last' is encountered.

        """
        group_name = group.name or f"group_{id(group)}"

        # Construct local group scope
        group_scope = MappingScope(
            name=group_name,
            parent=scope,
        )

        # Validate input parameters
        if len(group.input) != len(parameters):
            raise MappingError(
                f"Invalid number of parameters provided for group '{group_name}'. Expected {len(group.input)}, got {len(parameters)}."
            )
        for input, parameter in zip(group.input, parameters):
            group_scope.define_variable(input.name, parameter)

        # Process rules in order, handling 'first' and 'last' list modes
        rules = []
        first_rule, last_rule = None, None
        for rule in group.rule or []:
            if rule.target and (
                targetMode := next(
                    (target.listMode for target in rule.target if target.listMode),
                    [None],
                )[0]
            ):
                if targetMode == StructureMapTargetListMode.FIRST:
                    if first_rule:
                        raise RuntimeError(
                            'Only one rule with "first" target list mode is allowed per group.'
                        )
                    first_rule = rule
                elif targetMode == StructureMapTargetListMode.LAST:
                    if last_rule:
                        raise RuntimeError(
                            'Only one rule with "last" target list mode is allowed per group.'
                        )
                    last_rule = rule
                else:
                    raise NotImplementedError(
                        "Only 'first' and 'last' target list modes are implemented so far. Mode '{}' not implemented"
                    )
            else:
                rules.append(rule)
        rules = (
            ([first_rule] if first_rule else [])
            + rules
            + ([last_rule] if last_rule else [])
        )

        # Process each rule
        for rule in rules:
            self.process_rule(rule, group_scope)

    def process_rule(self, rule: StructureMapGroupRule, scope: MappingScope) -> MappingScope:
        """
        Processes a single StructureMap rule within the given mapping scope.

        This method handles the evaluation and execution of a StructureMapGroupRule, including:
        - Cycle detection to prevent infinite recursion.
        - Source processing to determine iteration counts and validate type, condition, and check constraints.
        - Iterative processing for each source instance, including:
            - Creating an iteration-specific mapping scope.
            - Setting indexed FHIRPath variables for the current iteration.
            - Processing target mappings, dependent rules/groups, and nested rules.
            - Merging results from each iteration back into the main scope.

        Args:
            rule (StructureMapGroupRule): The rule to process.
            scope (MappingScope): The current mapping scope.

        Returns:
            MappingScope: The updated mapping scope after processing the rule.

        Raises:
            RuleProcessingError: If any rule constraints (such as cardinality, type, or checks) are violated,
                or if required variables or dependent groups are not found.
        """
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
                source_fhirpath = scope.resolve_fhirpath(var_name)

                if source.type:
                    condition_fhirpath = source_fhirpath._invoke(
                        getattr(fhirpath, f"Is{source.type.title()}")
                    )
                    if not bool(condition_fhirpath.single(scope.get_instances())):
                        logger.debug(
                            f"Source type condition not met for rule {rule_name}"
                        )
                        return scope

                # Where condition
                if source.condition:
                    condition_fhirpath = fhirpath_parser.parse(source.condition)
                    condition_fhirpath = self._replace_mapping_scope_elements(
                        condition_fhirpath, scope
                    )

                    if not bool(condition_fhirpath.single(scope.get_instances())):
                        logger.debug(f"Source condition not met for rule {rule_name}")
                        return scope

                # Check condition
                if source.check:
                    condition_fhirpath = fhirpath_parser.parse(source.check)
                    condition_fhirpath = self._replace_mapping_scope_elements(
                        condition_fhirpath, scope
                    )

                    if not bool(condition_fhirpath.single(scope.get_instances())):
                        raise RuleProcessingError(
                            f"Source check failed for rule {rule_name}"
                        )

                # Collect source values for iteration
                if source_fhirpath is None:
                    raise RuleProcessingError(f"Source variable {var_name} not found")
                source_iterations[var_name] = source_fhirpath.count(
                    scope.get_instances()
                )
                if source.min is not None and source_iterations[var_name] < source.min:
                    raise RuleProcessingError(
                        f"Source minimum cardinality not met for rule {rule_name}"
                    )
                if (
                    source.max is not None
                    and source.max != "*"
                    and source_iterations[var_name] > int(source.max)
                ):
                    raise RuleProcessingError(
                        f"Source maximum cardinality exceeded for rule {rule_name}"
                    )

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
                    if (rule_source := scope.resolve_fhirpath(source_var)) is None:
                        raise RuleProcessingError(
                            f"Source variable {source_var} not found"
                        )
                    iteration_scope.define_variable(
                        source_var,
                        rule_source._invoke(fhirpath.Index(source_iteration)),
                    )

                    # Process targets for this iteration
                    for target in rule.target or []:
                        self.process_target(target, iteration_scope)

                    # Process dependent rules for this iteration
                    for dependent in rule.dependent or []:
                        dependent_group = iteration_scope.resolve_symbol(dependent.name)
                        if not dependent_group:
                            raise RuleProcessingError(
                                f"Dependent group or rule '{dependent.name}' not found"
                            )
                        if not isinstance(dependent_group, StructureMapGroup):
                            raise RuleProcessingError(
                                f"Dependent '{dependent.name}' is not a group"
                            )
                        parameters = [
                            iteration_scope.resolve_fhirpath(param.value)
                            for param in dependent.parameter
                        ]
                        self.process_group(dependent_group, parameters, iteration_scope)

                    # Process nested rules for this iteration
                    for nested_rule in rule.rule or []:
                        self.process_rule(nested_rule, iteration_scope)

                    # Merge back iteration results to main scope
                    scope.target_instances.update(iteration_scope.target_instances)

        finally:
            scope.finish_processing_rule(rule_name)
        return scope

    def process_source(self, source: StructureMapGroupRuleSource, scope: MappingScope) -> str:
        """
        Processes a StructureMapGroupRuleSource object within a given MappingScope and returns the variable name
        associated with the resolved FHIRPath expression.

        This method resolves the FHIRPath context from the source, applies any specified element path,
        and modifies the path according to the listMode option (e.g., first, last, not_first, not_last, only_one).
        The resulting FHIRPath expression is stored in the scope under a variable name, which is either
        provided by the source or generated uniquely.

        Args:
            source (StructureMapGroupRuleSource): The source mapping definition containing context, element, listMode, and variable.
            scope (MappingScope): The current mapping scope used to resolve FHIRPath and store variables.

        Returns:
            str: The variable name under which the resolved FHIRPath expression is stored in the scope.
        """
        path = scope.resolve_fhirpath(source.context)
        # Apply element path if specified
        if source.element:
            path = path._invoke(fhirpath.Element(source.element))

        # Apply list-option condition if specified
        if source.listMode == "first":
            path = path._invoke(fhirpath.First())
        elif source.listMode == "not_first":
            path = path._invoke(fhirpath.Tail())
        elif source.listMode == "not_last":
            path = path._invoke(
                fhirpath.Exclude(
                    path._invoke(fhirpath.Last()).single(scope.get_instances())
                )
            )
        elif source.listMode == "last":
            path = path._invoke(fhirpath.Last())
        elif source.listMode == "only_one":
            path = path._invoke(fhirpath.Single())

        # Store source FHIRPath
        var_name = source.variable or f"source_{id(source)}"
        scope.define_variable(var_name, path)
        return var_name

    def process_target(
        self,
        target: StructureMapGroupRuleTarget,
        scope: MappingScope,
    ) -> Any:
        """
        Processes a StructureMapGroupRuleTarget within the given mapping scope.

        This method resolves the FHIRPath context for the target, applies any specified element path,
        determines the appropriate insertion index, and stores the resulting FHIRPath in the scope as a variable.
        If a transform is specified on the target, it executes the transform with the provided parameters and
        updates the target structure with the transformed value.

        Args:
            target (StructureMapGroupRuleTarget): The mapping target to process, containing context, element, variable,
                transform, and parameters.
            scope (MappingScope): The current mapping scope, used for resolving FHIRPath contexts and managing variables.

        Returns:
            Any: The result of processing the target, typically the updated FHIRPath or transformed value.

        Raises:
            RuleProcessingError: If the target context is not specified.
        """
        if not target.context:
            raise RuleProcessingError("Target context is required")
        path = scope.resolve_fhirpath(target.context)
        # Apply element path if specified
        if target.element:
            path = path._invoke(fhirpath.Element(target.element))

        insert_index = path.count(scope.get_instances())
        path = path._invoke(fhirpath.Index(insert_index))

        # Store target FHIRPath
        var_name = target.variable or f"target_{id(target)}"
        scope.define_variable(var_name, path)

        transform = target.transform
        if transform:
            target.parameter = target.parameter or []
            # Execute the transform
            transformed_value = self.transformer.execute(
                transform, scope, target.parameter
            )
            # Update the target structure
            path.update_single(scope.get_instances(), transformed_value)

    def validate_structure_map(self, structure_map: StructureMap) -> List[str]:
        """
        Validates the structure and content of a given StructureMap instance.

        This method checks for the presence of required groups and structure declarations,
        ensures that both source and target structures are defined, and verifies that each
        group contains rules. It also delegates rule-specific validation to the _validate_rule method.

        Args:
            structure_map (StructureMap): The StructureMap object to validate.

        Returns:
            List[str]: A list of validation issue messages. The list is empty if no issues are found.
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

    def _resolve_structure_definitions(
        self, structure_map: StructureMap, mode: StructureMapModelMode
    ) -> Dict[str, type[BaseModel]]:
        """
        Resolves and constructs resource models for the specified mode from the given StructureMap.

        Args:
            structure_map (StructureMap): The structure map containing structure definitions to resolve.
            mode (StructureMapModelMode): The mode (e.g., source or target) to filter structures by.

        Returns:
            Dict[str, type[BaseModel]]: A dictionary mapping structure aliases or URLs to their corresponding resource model classes.

        Raises:
            MappingError: If the structure map does not specify any structures.
        """
        if not structure_map.structure:
            raise MappingError("Structure map does not specify any structures")

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
        Validates and maps a tuple of source data entries to their corresponding Pydantic models.

        Each entry in `source_data` is checked against the provided `source_models`. If an entry matches a model (either as an instance, a dict, or an object with a `__dict__`), it is validated and added to the result dictionary under the model's alias. If an entry does not match any model, a `MappingError` is raised.

        Args:
            source_data (tuple[BaseModel | dict, ...]): A tuple containing source data entries, which can be Pydantic model instances, dictionaries, or objects with a `__dict__` attribute.
            source_models (Dict[str, Type[BaseModel]]): A dictionary mapping string aliases to Pydantic model classes.

        Returns:
            dict[str, BaseModel]: A dictionary mapping aliases to validated Pydantic model instances.

        Raises:
            MappingError: If any entry in `source_data` does not match any of the provided source models.
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
                except MappingError:
                    continue
            else:
                raise MappingError(
                    f"Source data entry of type {type(entry)} does not match any source model"
                )

        for entry in source_data:
            _validate_entry(entry)

        return validated_entries

    def _validate_rule(self, rule: StructureMapGroupRule, issues: List[str]) -> None:
        """
        Validates a StructureMapGroupRule object and appends any issues found to the provided issues list.

        This method checks for the following:
            - The rule has at least one source element.
            - The rule has at least one target element.
            - The rule does not depend on itself (to prevent cycles).
            - Recursively validates any nested rules.

        Args:
            rule (StructureMapGroupRule): The rule to validate.
            issues (List[str]): A list to which validation issue messages will be appended.

        Returns:
            None
        """
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

    def _replace_mapping_scope_elements(self, path, scope: MappingScope):
        """
        Recursively replaces elements in a FHIRPath expression tree with their corresponding values from the given mapping scope.

        Args:
            path: A FHIRPath expression node, which can be an instance of fhirpath.Element, fhirpath.Invocation, fhirpath.FHIRComparisonOperator, or other supported types.
            scope (MappingScope): The mapping scope used to resolve FHIRPath element labels.

        Returns:
            The FHIRPath expression tree with elements replaced according to the mapping scope.

        Raises:
            MappingError: If a FHIRPath element label cannot be resolved in the mapping scope.

        Notes:
            - If a fhirpath.Element cannot be resolved in the scope, a new fhirpath.Element with the same label is returned.
            - The function processes Invocation and FHIRComparisonOperator nodes recursively.
        """
        if isinstance(path, fhirpath.Element):
            try:
                return scope.resolve_fhirpath(path.label)
            except MappingError:
                return fhirpath.Element(f"{path.label}")
        elif isinstance(path, (fhirpath.Invocation)):
            left = self._replace_mapping_scope_elements(path.left, scope)
            right = self._replace_mapping_scope_elements(path.right, scope)
            return fhirpath.Invocation(left, right)
        elif isinstance(path, fhirpath.FHIRComparisonOperator):
            left = self._replace_mapping_scope_elements(path.left, scope)
            right = self._replace_mapping_scope_elements(path.right, scope)
            return path.__class__(left, right)
        return path


mapper = FHIRMappingEngine()
