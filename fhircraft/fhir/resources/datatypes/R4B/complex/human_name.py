from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from ..primitive import *
from fhircraft.fhir.resources.datatypes.R4B.complex import Element, Period

class HumanName(Element):
    """
    Name of a human - parts and usage
    """

    _type = "HumanName"

    use: Optional[Code] = Field(
        description="usual | official | temp | nickname | anonymous | old | maiden",
        default=None,
    )
    text: Optional[String] = Field(
        description="Text representation of the full name",
        default=None,
    )
    family: Optional[String] = Field(
        description="Family name (often called \u0027Surname\u0027)",
        default=None,
    )
    given: Optional[List[String]] = Field(
        description="Given names (not always \u0027first\u0027). Includes middle names",
        default=None,
    )
    prefix: Optional[List[String]] = Field(
        description="Parts that come before the name",
        default=None,
    )
    suffix: Optional[List[String]] = Field(
        description="Parts that come after the name",
        default=None,
    )
    period: Optional[Period] = Field(
        description="Time period when name was/is in use",
        default=None,
    )
