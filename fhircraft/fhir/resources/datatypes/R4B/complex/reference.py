from typing import Optional, TYPE_CHECKING

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
import fhircraft.fhir.resources.datatypes.R4B.primitive as fhir
from fhircraft.fhir.resources.datatypes.R4B.complex import Element

if TYPE_CHECKING:
    from fhircraft.fhir.resources.datatypes.R4B.complex import Identifier

class Reference(Element):
    """
    A reference from one resource to another
    """

    _type = "Reference"

    reference: Optional[fhir.string] = Field(
        description="Literal reference, Relative, internal or absolute URL",
        default=None,
    )
    type: Optional[fhir.uri] = Field(
        description='Type the reference refers to (e.g. "Patient")',
        default=None,
    )
    identifier: Optional["Identifier"] = Field(
        description="Logical reference, when literal reference is not known",
        default=None,
    )
    display: Optional[fhir.string] = Field(
        description="Text alternative for the resource",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ref_1_constraint_validator(self):
        if not self._root_resource or not self._resource:
            return self
        return fhir_validators.validate_model_constraint(
            self,
            expression="reference.startsWith('#').not() or (reference.substring(1).trace('url') in %rootResource.contained.id.trace('ids')) or (reference='#' and %rootResource!=%resource)",
            human="SHALL have a contained resource if a local reference is provided",
            key="ref-1",
            severity="error",
        )
