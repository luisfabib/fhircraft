from typing import Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators

from ..primitive import *
from .element import Element
from .quantity import Quantity

class Range(Element):
    """
    Set of values bounded by low and high
    """

    _type = "Range"

    low: Optional[Quantity] = Field(
        description="Low limit",
        default=None,
    )
    high: Optional[Quantity] = Field(
        description="High limit",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_rng_2_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="low.empty() or high.empty() or (low <= high)",
            human="If present, low SHALL have a lower value than high",
            key="rng-2",
            severity="error",
        )
