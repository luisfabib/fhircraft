from typing import Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
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
