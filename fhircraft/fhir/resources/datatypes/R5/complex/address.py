from typing import List, Optional

from pydantic import Field, field_validator, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R5.complex import Element, Period


class Address(Element):
    """
    An address expressed using postal conventions (as opposed to GPS or other location definition formats)
    """

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
    line_ext: Optional[Element] = Field(
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

    @field_validator(
        *(
            "period",
            "country",
            "postalCode",
            "state",
            "district",
            "city",
            "line",
            "text",
            "type",
            "use",
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
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )
