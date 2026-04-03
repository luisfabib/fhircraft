from typing import Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators

from ..primitive import *
from fhircraft.fhir.resources.datatypes.R4.complex import Element

class Period(Element):
    """
    Time range defined by start and end date/time
    """

    _type = "Period"

    start: Optional[DateTime] = Field(
        description="Starting time with inclusive boundary",
        default=None,
    )
    end: Optional[DateTime] = Field(
        description="End time with inclusive boundary, if not ongoing",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_per_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="start.hasValue().not() or end.hasValue().not() or (start <= end)",
            human="If present, start SHALL have a lower value than end",
            key="per-1",
            severity="error",
        )
