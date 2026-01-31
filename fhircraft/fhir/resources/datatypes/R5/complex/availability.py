from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    BackboneElement,
    Period,
)


class AvailabilityAvailableTime(BackboneElement):
    """
    Times the {item} is available
    """

    daysOfWeek: Optional[List[Code]] = Field(
        description="Days of the week when the {item} is available",
        default=None,
    )
    allDay: Optional[Boolean] = Field(
        description="Is this always available? e.g. 24 hour service",
        default=None,
    )
    availableStartTime: Optional[Time] = Field(
        description="Opening time of day (ignored if allDay = true)",
        default=None,
    )
    availableEndTime: Optional[Time] = Field(
        description="Closing time of day (ignored if allDay = true)",
        default=None,
    )


class AvailabilityNotAvailableTime(BackboneElement):
    """
    Not available during this time due to provided reason
    """

    description: String = Field(
        description="Reason presented to the user explaining why time not available",
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
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
