from typing import Optional

from pydantic import Field, field_validator, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R5.complex import DataType, Element, Quantity


class SampledData(DataType):
    """
    A series of measurements taken by a device
    """

    origin: Optional[Quantity] = Field(
        description="Zero value and units",
        default=None,
    )
    interval: Optional[Decimal] = Field(
        description="Number of intervalUnits between samples",
        default=None,
    )
    interval_ext: Optional[Element] = Field(
        description="Placeholder element for interval extensions",
        default=None,
        alias="_interval",
    )
    intervalUnit: Optional[Code] = Field(
        description="The measurement unit of the interval between samples",
        default=None,
    )
    intervalUnit_ext: Optional[Element] = Field(
        description="Placeholder element for intervalUnit extensions",
        default=None,
        alias="_intervalUnit",
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
    codeMap: Optional[Canonical] = Field(
        description="Defines the codes used in the data",
        default=None,
    )
    codeMap_ext: Optional[Element] = Field(
        description="Placeholder element for codeMap extensions",
        default=None,
        alias="_codeMap",
    )
    offsets: Optional[String] = Field(
        description="Offsets, typically in time, at which data values were taken",
        default=None,
    )
    offsets_ext: Optional[Element] = Field(
        description="Placeholder element for offsets extensions",
        default=None,
        alias="_offsets",
    )
    data: Optional[String] = Field(
        description='Decimal values with spaces, or "E" | "U" | "L", or another code',
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
            "offsets",
            "codeMap",
            "dimensions",
            "upperLimit",
            "lowerLimit",
            "factor",
            "intervalUnit",
            "interval",
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
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_sdd_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="interval.exists().not() xor offsets.exists().not()",
            human="A SampledData SAHLL have either an interval and offsets but not both",
            key="sdd-1",
            severity="error",
        )
