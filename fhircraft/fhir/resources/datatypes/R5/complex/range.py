from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from ..primitive import *
from fhircraft.fhir.resources.datatypes.R5.complex import DataType, Quantity

class Range(DataType):
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
            expression="low.value.empty() or high.value.empty() or low.lowBoundary().comparable(high.highBoundary()).not() or (low.lowBoundary() <= high.highBoundary())",
            human="If present, low SHALL have a lower value than high",
            key="rng-2",
            severity="error",
        )
