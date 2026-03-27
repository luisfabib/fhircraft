from typing import TYPE_CHECKING, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R5.complex import DataType, Element

if TYPE_CHECKING:
    from fhircraft.fhir.resources.datatypes.R5.complex import Identifier


class Reference(DataType):
    """
    A reference from one resource to another
    """

    _type = "Reference"

    reference: Optional[String] = Field(
        description="Literal reference, Relative, internal or absolute URL",
        default=None,
    )
    reference_ext: Optional[Element] = Field(
        description="Placeholder element for reference extensions",
        default=None,
        alias="_reference",
    )
    type: Optional[Uri] = Field(
        description='Type the reference refers to (e.g. "Patient") - must be a resource in resources',
        default=None,
    )
    type_ext: Optional[Element] = Field(
        description="Placeholder element for type extensions",
        default=None,
        alias="_type",
    )
    identifier: Optional["Identifier"] = Field(
        description="Logical reference, when literal reference is not known",
        default=None,
    )
    display: Optional[String] = Field(
        description="Text alternative for the resource",
        default=None,
    )
    display_ext: Optional[Element] = Field(
        description="Placeholder element for display extensions",
        default=None,
        alias="_display",
    )

    @model_validator(mode="after")
    def FHIR_ref_1_constraint_validator(self):
        if not self._root_resource or not self._resource:
            return self
        return fhir_validators.validate_model_constraint(
            self,
            expression="reference.exists()  implies (reference.startsWith('#').not() or (reference.substring(1).trace('url') in %rootResource.contained.id.trace('ids')) or (reference='#' and %rootResource!=%resource))",
            human="SHALL have a contained resource if a local reference is provided",
            key="ref-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ref_2_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="reference.exists() or identifier.exists() or display.exists() or extension.exists()",
            human="At least one of reference, identifier and display SHALL be present (unless an extension is provided).",
            key="ref-2",
            severity="error",
        )
