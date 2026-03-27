from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R5.complex import DataType, Quantity


class Ratio(DataType):
    """
    A ratio of two Quantity values - a numerator and a denominator
    """

    _type = "Ratio"

    numerator: Optional[Quantity] = Field(
        description="Numerator value",
        default=None,
    )
    denominator: Optional[Quantity] = Field(
        description="Denominator value",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_rat_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(numerator.exists() and denominator.exists()) or (numerator.empty() and denominator.empty() and extension.exists())",
            human="Numerator and denominator SHALL both be present, or both are absent. If both are absent, there SHALL be some extension present",
            key="rat-1",
            severity="error",
        )
