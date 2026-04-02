from typing import Optional, TYPE_CHECKING

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from ..primitive import *

from .element import Element
from .quantity import Quantity

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
    factor: Optional[Decimal] = Field(
        description="Multiply data by this before adding to origin",
        default=None,
    )
    lowerLimit: Optional[Decimal] = Field(
        description="Lower limit of detection",
        default=None,
    )
    upperLimit: Optional[Decimal] = Field(
        description="Upper limit of detection",
        default=None,
    )
    dimensions: Optional[PositiveInt] = Field(
        description="Number of sample points at each time point",
        default=None,
    )
    data: Optional[String] = Field(
        description='Decimal values with spaces, or "E" | "U" | "L"',
        default=None,
    )
