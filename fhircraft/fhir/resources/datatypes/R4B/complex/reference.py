from typing import Optional, TYPE_CHECKING

from pydantic import Field, field_validator, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R4B.complex import Element

if TYPE_CHECKING:
    from fhircraft.fhir.resources.datatypes.R4B.complex import Identifier


class Reference(Element):
    """
    A reference from one resource to another
    """

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
        description='Type the reference refers to (e.g. "Patient")',
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

    @field_validator(
        *(
            "display",
            "identifier",
            "type",
            "reference",
            "extension",
        ),
        mode="after",
        check_fields=None,
    )
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*("extension",), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ref_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="reference.startsWith('#').not() or (reference.substring(1).trace('url') in %rootResource.contained.id.trace('ids')) or (reference='#' and %rootResource!=%resource)",
            human="SHALL have a contained resource if a local reference is provided",
            key="ref-1",
            severity="error",
        )
