from typing import TYPE_CHECKING, List, Optional, Sequence
from fhircraft.fhir.mapper.engine.abstract import FHIRMappingEngineComponent
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


class Group(FHIRMappingEngineComponent):
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
        self.name = (
            str(definition.name) if definition.name else f"group-{id(definition)}"
        )
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
        # Store the name of the group this group extends, resolved lazily at process() time
        self.extends_name: Optional[str] = (
            str(definition.extends) if definition.extends else None
        )

    def _collect_rules(self, scope: "MappingScope") -> "List[Rule]":
        """
        Collect the full ordered rule list for this group, prepending rules
        inherited from the extended group chain (deepest ancestor first).

        Resolved lazily at process() time via scope so forward references and
        cross-map extends are supported.
        """
        if not self.extends_name:
            return list(self.rules)
        parent = scope.resolve_group(self.extends_name)
        return parent._collect_rules(scope) + self.rules

    def _check_extends_compatibility(
        self, parent_group: "Group", scope: "MappingScope"
    ) -> None:
        """
        Validate that this group's inputs are compatible with the parent group's inputs.

        Called from process() once the scope is available so that type names can be
        resolved via scope.get_type().

        Per the FHIR spec the extending group SHALL have all of the parent's inputs
        with the same name, mode, and type (when the parent specifies one). It MAY
        add extra inputs.

        Raises:
            MappingError: If a required parent input is absent, or has a mismatched
                mode or type.
        """
        parent_by_name = {str(inp.name): inp for inp in parent_group.inputs}
        child_by_name = {str(inp.name): inp for inp in self.inputs}

        for pname, pinp in parent_by_name.items():
            cinp = child_by_name.get(pname)
            if cinp is None:
                raise MappingError(
                    f"Group '{self.name}' extends '{parent_group.name}' but is "
                    f"missing required input '{pname}'."
                )
            if str(cinp.mode) != str(pinp.mode):
                raise MappingError(
                    f"Group '{self.name}' input '{pname}' has mode '{cinp.mode}', "
                    f"but parent group '{parent_group.name}' requires mode '{pinp.mode}'."
                )
            if pinp.type:
                # Use the scope to resolve the required type (ensures it exists)
                pinp_type = str(pinp.type)
                cinp_type = str(cinp.type) if cinp.type else None
                try:
                    scope.get_type(pinp_type)
                except MappingError:
                    pass  # type not registered in scope; still enforce name match
                if cinp_type != pinp_type:
                    raise MappingError(
                        f"Group '{self.name}' input '{pname}' has type '{cinp_type}', "
                        f"but parent group '{parent_group.name}' requires type '{pinp_type}'."
                    )

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
                    scope.get_type(str(input.type))
                except MappingError:
                    raise MappingError(
                        f"Input '{input.name}' in group '{self.name}' has unknown type '{input.type}'."
                    )
            if not input.name:
                raise MappingError(
                    f"A {input.mode} input in group '{self.name}' is missing a name."
                )

            scope.define_variable(str(input.name), parameter)

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

        # Resolve extends chain: validate compatibility and collect inherited rules
        if self.extends_name:
            parent = scope.resolve_group(self.extends_name)
            self._check_extends_compatibility(parent, group_scope)
            all_rules = parent._collect_rules(scope) + self.rules
        else:
            all_rules = self.rules

        # Process each rule (inherited first, then own)
        for rule in all_rules:
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
