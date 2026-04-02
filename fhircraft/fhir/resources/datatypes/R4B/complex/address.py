from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.base import FHIRBaseModel
from ..primitive import *
from fhircraft.fhir.resources.datatypes.R4B.complex.element import Element
from typing import TYPE_CHECKING

from fhircraft.fhir.resources.datatypes.R4B.complex import Element, Period

class Address(Element):
    """
    An address expressed using postal conventions (as opposed to GPS or other location definition formats)
    """

    _type = "Address"

    use: Optional[Code] = Field(
        description="home | work | temp | old | billing - purpose of this address",
        default=None,
    )
    type: Optional[Code] = Field(
        description="postal | physical | both",
        default=None,
    )
    text: Optional[String] = Field(
        description="Text representation of the address",
        default=None,
    )
    line: Optional[List[String]] = Field(
        description="Street name, number, direction \u0026 P.O. Box etc.",
        default=None,
    )
    city: Optional[String] = Field(
        description="Name of city, town etc.",
        default=None,
    )
    district: Optional[String] = Field(
        description="District name (aka county)",
        default=None,
    )
    state: Optional[String] = Field(
        description="Sub-unit of country (abbreviations ok)",
        default=None,
    )
    postalCode: Optional[String] = Field(
        description="Postal code for area",
        default=None,
    )
    country: Optional[String] = Field(
        description="Country (e.g. can be ISO 3166 2 or 3 letter code)",
        default=None,
    )
    period: Optional[Period] = Field(
        description="Time period when address was/is in use",
        default=None,
    )
