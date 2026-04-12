from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
import fhircraft.fhir.resources.datatypes.R5.primitive as fhir
from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    BackboneElement,
    Period,
)

class AvailabilityAvailableTime(BackboneElement):
    """
    Times the {item} is available
    """

    daysOfWeek: Optional[List[fhir.code]] = Field(
        description="Days of the week when the {item} is available",
        default=None,
    )
    allDay: Optional[fhir.boolean] = Field(
        description="Is this always available? e.g. 24 hour service",
        default=None,
    )
    availableStartTime: Optional[fhir.time_] = Field(
        description="Opening time of day (ignored if allDay = true)",
        default=None,
    )
    availableEndTime: Optional[fhir.time_] = Field(
        description="Closing time of day (ignored if allDay = true)",
        default=None,
    )

class AvailabilityNotAvailableTime(BackboneElement):
    """
    Not available during this time due to provided reason
    """

    description: fhir.string = Field(
        description="Reason presented to the user explaining why time not available",
    )
    during: Optional[Period] = Field(
        description="Service not available from this date",
        default=None,
    )

class Availability(Element):
    """
    Availability data for an {item}
    """

    _type = "Availability"

    availableTime: Optional[List[AvailabilityAvailableTime]] = Field(
        description="Times the {item} is available",
        default=None,
    )
    notAvailableTime: Optional[List[AvailabilityNotAvailableTime]] = Field(
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
