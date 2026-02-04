from typing import TYPE_CHECKING, Optional
from fhircraft.fhir.mapper.engine.exceptions import (
    MappingError,
    SourceAssertionError,
    SourceProcessingError,
    SourceConditionError,
    SourceTypeError,
)
from fhircraft.fhir.path import engine as fhirpath
from fhircraft.fhir.path import fhirpath as fhirpath_parser
import logging

from fhircraft.fhir.path.engine.core import FHIRPath


logger = logging.getLogger(__name__)

if TYPE_CHECKING:

    from fhircraft.fhir.resources.datatypes.R4.core import (
        StructureMapGroupRuleSource as R4_StructureMapGroupRuleSource,
    )
    from fhircraft.fhir.resources.datatypes.R4B.core import (
        StructureMapGroupRuleSource as R4B_StructureMapGroupRuleSource,
    )
    from fhircraft.fhir.resources.datatypes.R5.core import (
        StructureMapGroupRuleSource as R5_StructureMapGroupRuleSource,
    )
    from fhircraft.fhir.mapper.engine.scope import MappingScope


class RuleSource:

    def __init__(
        self,
        source: "R4_StructureMapGroupRuleSource | R4B_StructureMapGroupRuleSource | R5_StructureMapGroupRuleSource",
        parent_rule: "MappingRule",
    ):
        """
        Initializes a RuleSource instance from a StructureMapGroupRuleSource.

        Args:
            source: The StructureMapGroupRuleSource to initialize from.
        Raises:
            SourceProcessingError: If required fields are missing.
        """
        self.definition = source
        if self.definition.context is None:
            raise SourceProcessingError("Source context is required")
        self.parent_rule = parent_rule
        self.variable = source.variable or f"source_{id(source)}"
        self.resolved_path: Optional[FHIRPath] = None
        self.iteration_count = 0
        self.parsed_condition = (
            fhirpath_parser.parse(source.condition)
            if source.condition
            else fhirpath.Literal(True)
        )
        self.parsed_assertion = (
            fhirpath_parser.parse(source.check)
            if source.check
            else fhirpath.Literal(True)
        )

    def process(
        self,
        scope: "MappingScope",
    ) -> None:
        """
        Processes the source within the given mapping scope.
        """
        self.resolved_path = scope.resolve_fhirpath(self.definition.context)  # type: ignore
        if self.resolved_path is None:
            raise SourceProcessingError(
                f"Source context {self.definition.context} not found"
            )

        # Apply element path if specified
        if self.definition.element:
            self.resolved_path = self.resolved_path._invoke(
                fhirpath.Element(self.definition.element)
            )
        # Apply list mode if specified
        self._apply_list_mode()

        # Store source FHIRPath in scope
        scope.define_variable(self.variable, self.resolved_path)
        # Store resolved path and calculate iteration count
        self.iteration_count = self.resolved_path.count(scope.get_instances()) or 0

        # Evaluate conditions
        if not self._check_type_condition(scope):
            raise SourceTypeError(
                f"Source type condition not met for source {self.variable}"
            )
        if not self._check_where_condition(scope):
            raise SourceConditionError(
                f"Source condition not met for source {self.variable}"
            )
        if not self._check_assertion_condition(scope):
            raise SourceAssertionError(
                f"Source assertion failed for source {self.variable}"
            )
        if not self._validate_cardinality():
            raise SourceProcessingError("Cardinality constraints violated")

    def _check_type_condition(self, scope: "MappingScope") -> bool:
        """Check type condition."""
        if not self.definition.type:
            return True
        if not self.resolved_path:
            raise SourceProcessingError("Source path not resolved")
        condition_fhirpath = self.resolved_path._invoke(
            fhirpath.LegacyIs(fhirpath.TypeSpecifier(self.definition.type.title()))
        )
        return bool(condition_fhirpath.single(scope.get_instances()))

    def _check_where_condition(self, scope: "MappingScope") -> bool:
        """Check where condition."""
        condition_fhirpath = self._replace_mapping_scope_elements(
            self.parsed_condition, scope
        )
        return bool(condition_fhirpath.single(scope.get_instances()))

    def _check_assertion_condition(self, scope: "MappingScope") -> bool:
        """Check assertion condition."""
        assertion_fhirpath = self._replace_mapping_scope_elements(
            self.parsed_assertion, scope
        )
        return bool(assertion_fhirpath.single(scope.get_instances()))

    def _validate_cardinality(self) -> bool:
        """Validate cardinality constraints."""
        min_card = getattr(self.definition, "min", None)
        max_card = getattr(self.definition, "max", None)

        if min_card is not None and self.iteration_count < min_card:
            return False

        if (
            max_card is not None
            and max_card != "*"
            and self.iteration_count > int(max_card)
        ):
            return False

        return True

    def _apply_list_mode(self) -> None:
        if (list_mode := self.definition.listMode) and self.resolved_path is not None:
            match list_mode:
                case "first":
                    self.resolved_path = self.resolved_path._invoke(fhirpath.First())
                case "not_first":
                    self.resolved_path = self.resolved_path._invoke(fhirpath.Tail())
                case "last":
                    self.resolved_path = self.resolved_path._invoke(fhirpath.Last())
                case "only_one":
                    self.resolved_path = self.resolved_path._invoke(fhirpath.Single())
                case "not_last":
                    self.resolved_path = self.resolved_path._invoke(
                        fhirpath.Exclude(self.resolved_path._invoke(fhirpath.Last()))
                    )
                case _:
                    raise SourceProcessingError(
                        f"Unsupported listMode '{self.definition.listMode}' in source {self.variable}"
                    )

    def _replace_mapping_scope_elements(self, path, scope: "MappingScope"):
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
