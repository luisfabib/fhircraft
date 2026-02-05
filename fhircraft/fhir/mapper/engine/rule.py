from typing import TYPE_CHECKING, List
from fhircraft.fhir.mapper.engine.exceptions import (
    RuleProcessingError,
    SourceAssertionError,
    SourceConditionError,
    SourceTypeError,
    MappingDigestionError,
)
from fhircraft.fhir.mapper.engine import transforms as tf
from fhircraft.fhir.mapper.engine.source import RuleSource
from fhircraft.fhir.mapper.engine.target import RuleTarget
from fhircraft.fhir.mapper.engine.scope import MappingScope
from fhircraft.fhir.path import engine as fhirpath
import logging


logger = logging.getLogger(__name__)

if TYPE_CHECKING:

    from fhircraft.fhir.resources.datatypes.R4.core import (
        StructureMapGroupRule as R4_StructureMapGroupRule,
        StructureMapGroupRuleDependent as R4_StructureMapGroupRuleDependent,
    )
    from fhircraft.fhir.resources.datatypes.R4B.core import (
        StructureMapGroupRule as R4B_StructureMapGroupRule,
        StructureMapGroupRuleDependent as R4B_StructureMapGroupRuleDependent,
    )
    from fhircraft.fhir.resources.datatypes.R5.core import (
        StructureMapGroupRule as R5_StructureMapGroupRule,
        StructureMapGroupRuleDependent as R5_StructureMapGroupRuleDependent,
    )
    from fhircraft.fhir.mapper.engine.group import Group


class Rule:
    """
    Represents a StructureMap Rule with iteration and condition logic.

    A Rule contains Sources and Targets, manages iteration over source collections,
    and handles conditions and dependencies.
    """

    def __init__(
        self,
        definition: "R4_StructureMapGroupRule | R4B_StructureMapGroupRule| R5_StructureMapGroupRule",
        parent_group=None,
    ):
        """
        Initializes a Rule instance from a StructureMapGroupRuleTarget.

        Args:
            source: The StructureMapGroupRuleTarget to initialize from.
        Raises:
            SourceProcessingError: If required fields are missing.
        """
        self.definition = definition
        self.name = definition.name or f"rule_{id(definition)}"
        self.parent_group = parent_group
        self.sources: List[RuleSource] = []
        self.targets: List[RuleTarget] = []
        self.nested_rules: List[Rule] = []
        self.dependents: List[
            "R4_StructureMapGroupRuleDependent | R4B_StructureMapGroupRuleDependent | R5_StructureMapGroupRuleDependent"
        ] = []

        # Create source objects
        for source_def in self.definition.source or []:
            self.sources.append(RuleSource(source_def, self))

        # Create target objects
        for target_def in self.definition.target or []:
            self.targets.append(RuleTarget(target_def, self))

        # Create nested rules
        for nested_def in self.definition.rule or []:
            self.nested_rules.append(Rule(nested_def, self.parent_group))

        # Extract dependents
        for dependent in self.definition.dependent or []:
            if not dependent.name:
                raise MappingDigestionError("Dependent rule or group must have a name")
            self.dependents.append(dependent)

    def process(
        self,
        scope: "MappingScope",
    ):
        """
        Processes the rule within the given mapping scope.

        Args:
            scope: The current mapping scope.
        """

        # Check for cycles
        if scope.is_processing_rule(self.name):
            logger.warning(f"Cycle detected in rule {self.name}, skipping")
            return scope
        scope.start_processing_rule(self.name)

        try:
            logger.debug(f"Processing rule: {self.name}")

            # Process sources first to determine iteration
            source_iterations = {}

            for source in self.sources:
                try:
                    source.process(scope)
                except (SourceTypeError, SourceConditionError):
                    logger.debug(
                        f"Source type or condition violated in rule {self.name}. Skipping rule."
                    )
                    return scope
                except SourceAssertionError:
                    raise SourceAssertionError(
                        f"Source assertion failed for rule {self.name}"
                    )
                source_iterations[source.variable] = source.iteration_count

            for source_var, iterations in source_iterations.items():
                for source_iteration in range(iterations):
                    logger.debug(
                        f"Processing iteration {source_iteration} for rule {self.name}"
                    )
                    # Create local iteration scope
                    iteration_scope = MappingScope(
                        name=f"{scope.name}_iter_{source_iteration}",
                        source_instances=scope.source_instances.copy(),
                        target_instances=scope.target_instances.copy(),
                        types=scope.types.copy(),
                        variables=scope.variables.copy(),
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
                    for target in self.targets:
                        target.process(iteration_scope)

                    # Process dependent rules for this iteration
                    for dependent in self.dependents:
                        self._process_dependent_group(dependent, iteration_scope)

                    # Process nested rules for this iteration
                    for nested_rule in self.nested_rules:
                        nested_rule.process(iteration_scope)

                    # Merge back iteration results to main scope
                    scope.target_instances.update(iteration_scope.target_instances)

        finally:
            scope.finish_processing_rule(self.name)
        return scope

    def _process_dependent_group(self, dependent, iteration_scope: "MappingScope"):
        from fhircraft.fhir.mapper.engine.group import Group

        dependent_group = iteration_scope.resolve_symbol(dependent.name)
        if not dependent_group:
            raise RuleProcessingError(
                f"Dependent group or rule '{dependent.name}' not found"
            )
        if not isinstance(dependent_group, Group):
            raise RuleProcessingError(f"Dependent '{dependent.name}' is not a group")
        # R5-specific logic
        if _parameters := getattr(dependent, "parameter", None):
            parameters = [
                iteration_scope.resolve_fhirpath(param.value)
                for param in _parameters or []
            ]
        # R4 and R4B-specific logic
        elif _variables := getattr(dependent, "variable", None):
            parameters = [
                iteration_scope.resolve_fhirpath(var) for var in _variables or []
            ]
        dependent_group.process(
            iteration_scope,
            parameters,
            is_dependent=True,
        )

    @property
    def has_first_target(self) -> bool:
        """Check if this rule has a target with 'first' list mode."""
        return any(target.has_list_mode("first") for target in self.targets)

    @property
    def has_last_target(self) -> bool:
        """Check if this rule has a target with 'last' list mode."""
        return any(target.has_list_mode("last") for target in self.targets)
