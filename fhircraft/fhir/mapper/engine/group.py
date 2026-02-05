from typing import TYPE_CHECKING, List, Sequence
from fhircraft.fhir.mapper.engine.exceptions import (
    MappingDigestionError,
    MappingError,
)
import logging

from fhircraft.fhir.path.engine.core import FHIRPath


logger = logging.getLogger(__name__)

from fhircraft.fhir.mapper.engine.scope import MappingScope
from fhircraft.fhir.mapper.engine.rule import Rule

if TYPE_CHECKING:

    from fhircraft.fhir.resources.datatypes.R4.core import (
        StructureMapGroup as R4_StructureMapGroup,
    )
    from fhircraft.fhir.resources.datatypes.R4B.core import (
        StructureMapGroup as R4B_StructureMapGroup,
    )
    from fhircraft.fhir.resources.datatypes.R5.core import (
        StructureMapGroup as R5_StructureMapGroup,
    )


class Group:
    """
    Represents a StructureMap Group with its own processing logic.
    """

    def __init__(
        self,
        definition: "R4_StructureMapGroup | R4B_StructureMapGroup | R5_StructureMapGroup",
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
        self.name = definition.name or f"group_{id(definition)}"
        self.parent_group = parent_group
        self.rules: List[Rule] = [
            Rule(rule, parent_group=self) for rule in definition.rule or []
        ]
        self._organize_rules()
        # Parse inputs
        if not self.definition.input:
            raise MappingDigestionError(
                f"Group '{self.name}' has no input definitions."
            )
        self.inputs = self.definition.input

    def bind_parameters(
        self, scope: "MappingScope", parameters: Sequence[FHIRPath], is_dependent: bool
    ) -> None:
        """Bind input parameters to the group scope."""
        if len(parameters) != len(self.inputs):
            raise MappingError(
                f"Expected {len(self.inputs)} parameters, got {len(parameters)}"
            )

        for input, parameter in zip(self.inputs, parameters):
            if input.mode == "target" and not is_dependent:
                if not input.type:
                    raise MappingError(
                        f"Target input '{input.name}' in group '{self.name}' must have a type specified."
                    )

            if input.type:
                try:
                    scope.get_type(input.type)
                except MappingError:
                    raise MappingError(
                        f"Input '{input.name}' in group '{self.name}' has unknown type '{input.type}'."
                    )
            if not input.name:
                raise MappingError(
                    f"A {input.mode} input in group '{self.name}' is missing a name."
                )

            scope.define_variable(input.name, parameter)

    def process(
        self,
        scope: "MappingScope",
        parameters: Sequence[FHIRPath],
        is_dependent: bool = False,
    ):
        """
        Processes a StructureMap group by validating input parameters, constructing a local mapping scope,
        and executing the group's rules in the correct order, handling special list modes ('first' and 'last').

        Args:
            parameters: The input parameters to be mapped, corresponding to the group's input definitions.
            scope: The parent mapping scope to use as the basis for the group's local scope.

        Raises:
            MappingError: If the number of provided parameters does not match the group's input definitions.
            RuntimeError: If more than one rule with 'first' or 'last' target list mode is found in the group.
            NotImplementedError: If a target list mode other than 'first' or 'last' is encountered.
        """
        # Construct local group scope
        group_scope = MappingScope(
            name=self.name,
            parent=scope,
        )

        self.bind_parameters(group_scope, parameters, is_dependent)

        # Process each rule
        for rule in self.rules:
            rule.process(group_scope)

    def _organize_rules(self):
        """Organizes rules based on 'first' and 'last' target list modes."""

        # Create rule objects
        first_rule = None
        last_rule = None
        regular_rules = []
        for rule in self.rules:
            # Check for list mode ordering
            if rule.has_first_target:
                if first_rule:
                    raise MappingDigestionError(
                        "Only one rule with 'first' target list mode allowed"
                    )
                first_rule = rule
            elif rule.has_last_target:
                if last_rule:
                    raise MappingDigestionError(
                        "Only one rule with 'last' target list mode allowed"
                    )
                last_rule = rule
            else:
                regular_rules.append(rule)

        # Combine in proper order
        self.rules = []
        if first_rule:
            self.rules.append(first_rule)
        self.rules.extend(regular_rules)
        if last_rule:
            self.rules.append(last_rule)
