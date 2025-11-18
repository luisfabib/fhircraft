from typing import Optional

from pydantic import Field, field_validator, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R4B.complex import Element, Quantity


class SampledData(Element):
    """
    A series of measurements taken by a device
    """

    origin: Optional[Quantity] = Field(
        description="Zero value and units",
        default=None,
    )
    period: Optional[Decimal] = Field(
        description="Number of milliseconds between samples",
        default=None,
    )
    period_ext: Optional[Element] = Field(
        description="Placeholder element for period extensions",
        default=None,
        alias="_period",
    )
    factor: Optional[Decimal] = Field(
        description="Multiply data by this before adding to origin",
        default=None,
    )
    factor_ext: Optional[Element] = Field(
        description="Placeholder element for factor extensions",
        default=None,
        alias="_factor",
    )
    lowerLimit: Optional[Decimal] = Field(
        description="Lower limit of detection",
        default=None,
    )
    lowerLimit_ext: Optional[Element] = Field(
        description="Placeholder element for lowerLimit extensions",
        default=None,
        alias="_lowerLimit",
    )
    upperLimit: Optional[Decimal] = Field(
        description="Upper limit of detection",
        default=None,
    )
    upperLimit_ext: Optional[Element] = Field(
        description="Placeholder element for upperLimit extensions",
        default=None,
        alias="_upperLimit",
    )
    dimensions: Optional[PositiveInt] = Field(
        description="Number of sample points at each time point",
        default=None,
    )
    dimensions_ext: Optional[Element] = Field(
        description="Placeholder element for dimensions extensions",
        default=None,
        alias="_dimensions",
    )
    data: Optional[String] = Field(
        description='Decimal values with spaces, or "E" | "U" | "L"',
        default=None,
    )
    data_ext: Optional[Element] = Field(
        description="Placeholder element for data extensions",
        default=None,
        alias="_data",
    )

    @field_validator(
        *(
            "data",
            "dimensions",
            "upperLimit",
            "lowerLimit",
            "factor",
            "period",
            "origin",
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
