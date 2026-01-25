from typing import Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R4.complex import Element, Period


class ContactPoint(Element):
    """
    Details of a Technology mediated contact point (phone, fax, email, etc.)
    """

    _type = "ContactPoint"

    system: Optional[Code] = Field(
        description="phone | fax | email | pager | url | sms | other",
        default=None,
    )
    system_ext: Optional[Element] = Field(
        description="Placeholder element for system extensions",
        default=None,
        alias="_system",
    )
    value: Optional[String] = Field(
        description="The actual contact point details",
        default=None,
    )
    value_ext: Optional[Element] = Field(
        description="Placeholder element for value extensions",
        default=None,
        alias="_value",
    )
    use: Optional[Code] = Field(
        description="home | work | temp | old | mobile - purpose of this contact point",
        default=None,
    )
    use_ext: Optional[Element] = Field(
        description="Placeholder element for use extensions",
        default=None,
        alias="_use",
    )
    rank: Optional[PositiveInt] = Field(
        description="Specify preferred order of use (1 = highest)",
        default=None,
    )
    rank_ext: Optional[Element] = Field(
        description="Placeholder element for rank extensions",
        default=None,
        alias="_rank",
    )
    period: Optional["Period"] = Field(
        description="Time period when the contact point was/is in use",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "period",
                "rank",
                "use",
                "value",
                "system",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ext_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("extension",),
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_cpt_2_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="value.empty() or system.exists()",
            human="A system is required if a value is provided.",
            key="cpt-2",
            severity="error",
        )
