from typing import TYPE_CHECKING, Optional
from fhircraft.fhir.mapper.engine.abstract import FHIRMappingEngineComponent
from fhircraft.exceptions import (
    MapperDigestionError,
    MapperException,
    MapperExecutionError,
    MapperSourceProcessingError,
)
from fhircraft.fhir.mapper.engine import transforms as tf
from fhircraft.fhir.path import engine as fhirpath
import logging

from fhircraft.fhir.path.engine.core import FHIRPath


logger = logging.getLogger(__name__)

if TYPE_CHECKING:

    from fhircraft.fhir.resources.datatypes.R4.core import (
        StructureMapGroupRuleTarget as R4_StructureMapGroupRuleTarget,
    )
    from fhircraft.fhir.resources.datatypes.R4B.core import (
        StructureMapGroupRuleTarget as R4B_StructureMapGroupRuleTarget,
    )
    from fhircraft.fhir.resources.datatypes.R5.core import (
        StructureMapGroupRuleTarget as R5_StructureMapGroupRuleTarget,
    )
    from fhircraft.fhir.mapper.engine.scope import MappingScope
    from fhircraft.fhir.mapper.engine.rule import Rule


class RuleTarget(FHIRMappingEngineComponent):

    def __init__(
        self,
        source: "R4_StructureMapGroupRuleTarget | R4B_StructureMapGroupRuleTarget | R5_StructureMapGroupRuleTarget",
        parent_rule: "Rule",
    ):
        """
        Initializes a RuleSource instance from a StructureMapGroupRuleTarget.

        Args:
            source: The StructureMapGroupRuleTarget to initialize from.
        Raises:
            SourceProcessingError: If required fields are missing.
        """
        self.definition = source
        if self.definition.context is None:
            raise MappingDigestionError("Source context is required")
        self.parent_rule = parent_rule
        self.variable = (
            str(source.variable) if source.variable else f"target-{id(source)}"
        )
        self.resolved_path: Optional[FHIRPath] = None
        self.transform = self._resolve_transform(
            str(self.definition.transform) if self.definition.transform else None,
            self.definition.parameter,
        )

    def process(
        self,
        scope: "MappingScope",
    ) -> None:
        """Process the target, creating path and executing transforms."""
        # Resolve target path
        self.resolved_path = scope.resolve_fhirpath(self.definition.context)  # type: ignore
        # Apply element path if specified
        if self.definition.element:
            self.resolved_path = self.resolved_path._invoke(
                fhirpath.Element(self.definition.element)
            )

        # Determine insertion index
        insert_index = self.resolved_path.count(scope.get_instances())
        self.resolved_path = self.resolved_path._invoke(fhirpath.Index(insert_index))

        # Apply transform if specified
        if self.transform:
            self.definition.parameter = self.definition.parameter or []  # type: ignore
            # Execute the transform
            transformed_value = self.transform.process(scope)
            # Update the target structure
            self.resolved_path.update_single(scope.get_instances(), transformed_value)

        # Define variable in scope
        scope.define_variable(self.variable, self.resolved_path)

    def _resolve_transform(self, transform_name: str | None, parameters):
        """Resolves the transform specified in the target definition."""
        match transform_name:
            case "id":
                return tf.Identifier(parameters)
            case "cp":
                return tf.ContactPoint(parameters)
            case "copy":
                return tf.Copy(parameters)
            case "create":
                return tf.Create(parameters)
            case "c":
                return tf.Coding(parameters)
            case "cc":
                return tf.CodeableConcept(parameters)
            case "qty":
                return tf.Quantity(parameters)
            case "truncate":
                return tf.Truncate(parameters)
            case "cast":
                return tf.Cast(parameters)
            case "append":
                return tf.Append(parameters)
            case "uuid":
                return tf.UUID(parameters)
            case "translate":
                return tf.Translate(parameters)
            case "evaluate":
                return tf.Evaluate(parameters)
            case "reference":
                return tf.Reference(parameters)
            case None:
                return None
            case _:
                raise SourceProcessingError(f"Unsupported transform: {transform_name}")

    def has_list_mode(self, mode: str) -> bool:
        """Check if this target has a specific list mode."""
        target_mode = getattr(self.definition, "listMode", None)
        if isinstance(target_mode, list):
            return mode in target_mode
        return target_mode == mode
