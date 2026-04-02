from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from ..primitive import *

from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
)
from .resource import Resource
from .domain_resource import DomainResource

class AppointmentResponse(DomainResource):
    """
    A reply to an appointment request for a patient and/or practitioner(s), such as a confirmation or rejection.
    """

    _abstract = False
    _type = "AppointmentResponse"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/AppointmentResponse"

    identifier: Optional[ListType[Identifier]] = Field(
        description="External Ids for this item",
        default=None,
    )
    appointment: Optional[Reference] = Field(
        description="Appointment this response relates to",
        default=None,
    )
    proposedNewTime: Optional[Boolean] = Field(
        description="Indicator for a counter proposal",
        default=None,
    )
    start: Optional[Instant] = Field(
        description="Time from appointment, or requested new start time",
        default=None,
    )
    end: Optional[Instant] = Field(
        description="Time from appointment, or requested new end time",
        default=None,
    )
    participantType: Optional[ListType[CodeableConcept]] = Field(
        description="Role of participant in the appointment",
        default=None,
    )
    actor: Optional[Reference] = Field(
        description="Person(s), Location, HealthcareService, or Device",
        default=None,
    )
    participantStatus: Optional[Code] = Field(
        description="accepted | declined | tentative | needs-action | entered-in-error",
        default=None,
    )
    comment: Optional[Markdown] = Field(
        description="Additional comments",
        default=None,
    )
    recurring: Optional[Boolean] = Field(
        description="This response is for all occurrences in a recurring request",
        default=None,
    )
    occurrenceDate: Optional[Date] = Field(
        description="Original date within a recurring request",
        default=None,
    )
    recurrenceId: Optional[PositiveInt] = Field(
        description="The recurrence ID of the specific recurring request",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_apr_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="participantType.exists() or actor.exists()",
            human="Either the participantType or actor must be specified",
            key="apr-1",
            severity="error",
        )
