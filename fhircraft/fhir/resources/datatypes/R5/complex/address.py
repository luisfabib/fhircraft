from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R5.complex import Element, Period


class Address(Element):
    """
    An address expressed using postal conventions (as opposed to GPS or other location definition formats)
    """

    _type = "Address"

    use: Optional[Code] = Field(
        description="home | work | temp | old | billing - purpose of this address",
        default=None,
    )
    use_ext: Optional[Element] = Field(
        description="Placeholder element for use extensions",
        default=None,
        alias="_use",
    )
    type: Optional[Code] = Field(
        description="postal | physical | both",
        default=None,
    )
    type_ext: Optional[Element] = Field(
        description="Placeholder element for type extensions",
        default=None,
        alias="_type",
    )
    text: Optional[String] = Field(
        description="Text representation of the address",
        default=None,
    )
    text_ext: Optional[Element] = Field(
        description="Placeholder element for text extensions",
        default=None,
        alias="_text",
    )
    line: Optional[List[String]] = Field(
        description="Street name, number, direction \u0026 P.O. Box etc.",
        default=None,
    )
    line_ext: Optional[List[Optional[Element]]] = Field(
        description="Placeholder element for line extensions",
        default=None,
        alias="_line",
    )
    city: Optional[String] = Field(
        description="Name of city, town etc.",
        default=None,
    )
    city_ext: Optional[Element] = Field(
        description="Placeholder element for city extensions",
        default=None,
        alias="_city",
    )
    district: Optional[String] = Field(
        description="District name (aka county)",
        default=None,
    )
    district_ext: Optional[Element] = Field(
        description="Placeholder element for district extensions",
        default=None,
        alias="_district",
    )
    state: Optional[String] = Field(
        description="Sub-unit of country (abbreviations ok)",
        default=None,
    )
    state_ext: Optional[Element] = Field(
        description="Placeholder element for state extensions",
        default=None,
        alias="_state",
    )
    postalCode: Optional[String] = Field(
        description="Postal code for area",
        default=None,
    )
    postalCode_ext: Optional[Element] = Field(
        description="Placeholder element for postalCode extensions",
        default=None,
        alias="_postalCode",
    )
    country: Optional[String] = Field(
        description="Country (e.g. may be ISO 3166 2 or 3 letter code)",
        default=None,
    )
    country_ext: Optional[Element] = Field(
        description="Placeholder element for country extensions",
        default=None,
        alias="_country",
    )
    period: Optional[Period] = Field(
        description="Time period when address was/is in use",
        default=None,
    )
