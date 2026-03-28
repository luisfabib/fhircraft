from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R5.complex import DataType, Element


class Period(DataType):
    """
    Time range defined by start and end date/time
    """

    _type = "Period"

    start: Optional[DateTime] = Field(
        description="Starting time with inclusive boundary",
        default=None,
    )
    start_ext: Optional[Element] = Field(
        description="Placeholder element for start extensions",
        default=None,
        alias="_start",
    )
    end: Optional[DateTime] = Field(
        description="End time with inclusive boundary, if not ongoing",
        default=None,
    )
    end_ext: Optional[Element] = Field(
        description="Placeholder element for end extensions",
        default=None,
        alias="_end",
    )

    @model_validator(mode="after")
    def FHIR_per_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="start.hasValue().not() or end.hasValue().not() or (start.lowBoundary() <= end.highBoundary())",
            human="If present, start SHALL have a lower or equal value than end",
            key="per-1",
            severity="error",
        )
