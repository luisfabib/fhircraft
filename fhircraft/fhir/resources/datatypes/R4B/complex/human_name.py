from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
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
    use_ext: Optional[Element] = Field(
        description="Placeholder element for use extensions",
        default=None,
        alias="_use",
    )
    text: Optional[String] = Field(
        description="Text representation of the full name",
        default=None,
    )
    text_ext: Optional[Element] = Field(
        description="Placeholder element for text extensions",
        default=None,
        alias="_text",
    )
    family: Optional[String] = Field(
        description="Family name (often called \u0027Surname\u0027)",
        default=None,
    )
    family_ext: Optional[Element] = Field(
        description="Placeholder element for family extensions",
        default=None,
        alias="_family",
    )
    given: Optional[List[String]] = Field(
        description="Given names (not always \u0027first\u0027). Includes middle names",
        default=None,
    )
    given_ext: Optional[List[Optional[Element]]] = Field(
        description="Placeholder element for given extensions",
        default=None,
        alias="_given",
    )
    prefix: Optional[List[String]] = Field(
        description="Parts that come before the name",
        default=None,
    )
    prefix_ext: Optional[List[Optional[Element]]] = Field(
        description="Placeholder element for prefix extensions",
        default=None,
        alias="_prefix",
    )
    suffix: Optional[List[String]] = Field(
        description="Parts that come after the name",
        default=None,
    )
    suffix_ext: Optional[List[Optional[Element]]] = Field(
        description="Placeholder element for suffix extensions",
        default=None,
        alias="_suffix",
    )
    period: Optional[Period] = Field(
        description="Time period when name was/is in use",
        default=None,
    )
