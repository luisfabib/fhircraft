from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
import fhircraft.fhir.resources.datatypes.R5.primitive as fhir
from fhircraft.fhir.resources.datatypes.R5.complex import DataType, Quantity

class RatioRange(DataType):
    """
    Range of ratio values
    """

    _type = "RatioRange"

    lowNumerator: Optional[Quantity] = Field(
        description="Low Numerator limit",
        default=None,
    )
    highNumerator: Optional[Quantity] = Field(
        description="High Numerator limit",
        default=None,
    )
    denominator: Optional[Quantity] = Field(
        description="Denominator value",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ratrng_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="((lowNumerator.exists() or highNumerator.exists()) and denominator.exists()) or (lowNumerator.empty() and highNumerator.empty() and denominator.empty() and extension.exists())",
            human="One of lowNumerator or highNumerator and denominator SHALL be present, or all are absent. If all are absent, there SHALL be some extension present",
            key="ratrng-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ratrng_2_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="lowNumerator.hasValue().not() or highNumerator.hasValue().not()  or (lowNumerator.lowBoundary() <= highNumerator.highBoundary())",
            human="If present, lowNumerator SHALL have a lower value than highNumerator",
            key="ratrng-2",
            severity="error",
        )
