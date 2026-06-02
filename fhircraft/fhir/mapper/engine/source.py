from typing import TYPE_CHECKING, Optional
from fhircraft.fhir.mapper.engine.abstract import FHIRMappingEngineComponent
from fhircraft.exceptions import (
    MapperDigestionError,
    MapperException,
    MapperExecutionError,
    MapperSourceProcessingError,
)
from fhircraft.fhir.path import engine as fhirpath
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
    from fhircraft.fhir.mapper.engine.rule import Rule


class RuleSource(FHIRMappingEngineComponent):

    def __init__(
        self,
        source: "R4_StructureMapGroupRuleSource | R4B_StructureMapGroupRuleSource | R5_StructureMapGroupRuleSource",
        parent_rule: "Rule",
    ):
        """
        Initializes a RuleSource instance from a StructureMapGroupRuleSource.

        Args:
            source: The StructureMapGroupRuleSource to initialize from.
        Raises:
            MapperDigestionError: If required fields are missing.
        """
        self.definition = source
        if self.definition.context is None:
            raise MapperDigestionError("Source context is required")
        self.parent_rule = parent_rule
        self.variable = (
            str(source.variable) if source.variable else f"source-{id(source)}"
        )
        self.resolved_path: Optional[FHIRPath] = None
        self.iteration_count = 0
        self.condition = (
            source.condition if source.condition else fhirpath.Literal(True)
        )
        self.assertion = source.check if source.check else fhirpath.Literal(True)

    def process(
        self,
        scope: "MappingScope",
    ) -> None:
        """
        Processes the source within the given mapping scope.
        """
        self.resolved_path = scope.resolve_fhirpath(self.definition.context)  # type: ignore
        if self.resolved_path is None:
            raise MapperSourceProcessingError(
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
            raise MapperSourceProcessingError(
                f"Source type condition not met for source {self.variable}"
            )
        if not self._check_where_condition(scope):
            raise MapperSourceProcessingError(
                f"Source condition not met for source {self.variable}"
            )
        if not self._check_assertion_condition(scope):
            raise MapperSourceProcessingError(
                f"Source assertion failed for source {self.variable}"
            )
        if not self._validate_cardinality():
            raise MapperSourceProcessingError("Cardinality constraints violated")

    def _check_type_condition(self, scope: "MappingScope") -> bool:
        """Check type condition."""
        if not self.definition.type:
            return True
        if not self.resolved_path:
            raise MapperSourceProcessingError("Source path not resolved")
        condition_fhirpath = self.resolved_path._invoke(
            fhirpath.LegacyIs(fhirpath.TypeSpecifier(self.definition.type.title()))
        )
        return bool(condition_fhirpath.single(scope.get_instances()))

    def _check_where_condition(self, scope: "MappingScope") -> bool:
        """Check where condition."""
        if not isinstance(self.condition, FHIRPath):
            condition_fhirpath = self.resolve_fhirpath_within_context(
                str(self.condition), scope
            )
        else:
            condition_fhirpath = self.condition
        return bool(condition_fhirpath.single(scope.get_instances()))

    def _check_assertion_condition(self, scope: "MappingScope") -> bool:
        """Check assertion condition."""
        if not isinstance(self.assertion, FHIRPath):
            assertion_fhirpath = self.resolve_fhirpath_within_context(
                str(self.assertion), scope
            )
        else:
            assertion_fhirpath = self.assertion
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
                    raise MapperSourceProcessingError(
                        f"Unsupported listMode '{self.definition.listMode}' in source {self.variable}"
                    )
