from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
import fhircraft.fhir.resources.datatypes.R5.primitive as fhir
from fhircraft.fhir.resources.datatypes.R5.complex import DataType, Element, Period

class HumanName(DataType):
    """
    Name of a human or other living entity - parts and usage
    """

    _type = "HumanName"

    use: Optional[fhir.code] = Field(
        description="usual | official | temp | nickname | anonymous | old | maiden",
        default=None,
    )
    text: Optional[fhir.string] = Field(
        description="Text representation of the full name",
        default=None,
    )
    family: Optional[fhir.string] = Field(
        description="Family name (often called \u0027Surname\u0027)",
        default=None,
    )
    given: Optional[List[fhir.string]] = Field(
        description="Given names (not always \u0027first\u0027). Includes middle names",
        default=None,
    )
    prefix: Optional[List[fhir.string]] = Field(
        description="Parts that come before the name",
        default=None,
    )
    suffix: Optional[List[fhir.string]] = Field(
        description="Parts that come after the name",
        default=None,
    )
    period: Optional[Period] = Field(
        description="time period when name was/is in use",
        default=None,
    )
