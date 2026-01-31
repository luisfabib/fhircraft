from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R5.complex import Element


class Availability(Element):
    """
    Availability data for an {item}
    """

    _type = "Availability"

    availableTime: Optional[List[Element]] = Field(
        description="Times the {item} is available",
        default=None,
    )
    notAvailableTime: Optional[List[Element]] = Field(
        description="Not available during this time due to provided reason",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_av_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("availableTime",),
            expression="allDay.exists().not() or (allDay implies availableStartTime.exists().not() and availableEndTime.exists().not())",
            human="Cannot include start/end times when selecting all day availability.",
            key="av-1",
            severity="error",
        )
