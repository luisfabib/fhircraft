from typing import Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
import fhircraft.fhir.resources.datatypes.R4B.primitive as fhir
from fhircraft.fhir.resources.datatypes.R4B.complex import Element, Quantity

class SampledData(Element):
    """
    A series of measurements taken by a device
    """

    _type = "SampledData"

    origin: Optional[Quantity] = Field(
        description="Zero value and units",
        default=None,
    )
    period: Optional[fhir.decimal] = Field(
        description="Number of milliseconds between samples",
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
    data: Optional[fhir.string] = Field(
        description='decimal values with spaces, or "E" | "U" | "L"',
        default=None,
    )
