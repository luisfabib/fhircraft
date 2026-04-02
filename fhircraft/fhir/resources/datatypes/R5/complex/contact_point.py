from typing import Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from ..primitive import *
from fhircraft.fhir.resources.datatypes.R5.complex import Element, Period

class ContactPoint(Element):
    """
    Details of a Technology mediated contact point (phone, fax, email, etc.)
    """

    _type = "ContactPoint"

    system: Optional[Code] = Field(
        description="phone | fax | email | pager | url | sms | other",
        default=None,
    )
    value: Optional[String] = Field(
        description="The actual contact point details",
        default=None,
    )
    use: Optional[Code] = Field(
        description="home | work | temp | old | mobile - purpose of this contact point",
        default=None,
    )
    rank: Optional[PositiveInt] = Field(
        description="Specify preferred order of use (1 = highest)",
        default=None,
    )
    period: Optional[Period] = Field(
        description="Time period when the contact point was/is in use",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_cpt_2_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="value.empty() or system.exists()",
            human="A system is required if a value is provided.",
            key="cpt-2",
            severity="error",
        )
