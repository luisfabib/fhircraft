from typing import Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
import fhircraft.fhir.resources.datatypes.R5.primitive as fhir
from fhircraft.fhir.resources.datatypes.R5.complex import DataType, Element, Quantity

class SampledData(DataType):
    """
    A series of measurements taken by a device
    """

    _type = "SampledData"

    origin: Optional[Quantity] = Field(
        description="Zero value and units",
        default=None,
    )
    interval: Optional[fhir.decimal] = Field(
        description="Number of intervalUnits between samples",
        default=None,
    )
    intervalUnit: Optional[fhir.code] = Field(
        description="The measurement unit of the interval between samples",
        default=None,
    )
    factor: Optional[fhir.decimal] = Field(
        description="Multiply data by this before adding to origin",
        default=None,
    )
    lowerLimit: Optional[fhir.decimal] = Field(
        description="Lower limit of detection",
        default=None,
    )
    upperLimit: Optional[fhir.decimal] = Field(
        description="Upper limit of detection",
        default=None,
    )
    dimensions: Optional[fhir.positiveInt] = Field(
        description="Number of sample points at each time point",
        default=None,
    )
    codeMap: Optional[fhir.canonical] = Field(
        description="Defines the codes used in the data",
        default=None,
    )
    offsets: Optional[fhir.string] = Field(
        description="Offsets, typically in time, at which data values were taken",
        default=None,
    )
    data: Optional[fhir.string] = Field(
        description='decimal values with spaces, or "E" | "U" | "L", or another code',
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_sdd_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="interval.exists().not() xor offsets.exists().not()",
            human="A SampledData SAHLL have either an interval and offsets but not both",
            key="sdd-1",
            severity="error",
        )
