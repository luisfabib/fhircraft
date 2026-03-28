import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator

NoneType = type(None)

from typing import Optional, List as ListType

from fhircraft.fhir.resources.datatypes.primitives import String, Uri, Code, Instant

from fhircraft.fhir.resources.datatypes.R4.complex import (
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

    contained: Optional[ListType[Resource]] = Field(
        description="Contained, inline Resources",
        default=None,
    )
    extension: Optional[ListType[Extension]] = Field(
        description="Additional content defined by implementations",
        default=None,
    )
    modifierExtension: Optional[ListType[Extension]] = Field(
        description="Extensions that cannot be ignored",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="External Ids for this item",
        default=None,
    )
    appointment: Optional[Reference] = Field(
        description="Appointment this response relates to",
        default=None,
    )
    start: Optional[Instant] = Field(
        description="Time from appointment, or requested new start time",
        default=None,
    )
    start_ext: Optional[Element] = Field(
        description="Placeholder element for start extensions",
        default=None,
        alias="_start",
    )
    end: Optional[Instant] = Field(
        description="Time from appointment, or requested new end time",
        default=None,
    )
    end_ext: Optional[Element] = Field(
        description="Placeholder element for end extensions",
        default=None,
        alias="_end",
    )
    participantType: Optional[ListType[CodeableConcept]] = Field(
        description="Role of participant in the appointment",
        default=None,
    )
    actor: Optional[Reference] = Field(
        description="Person, Location, HealthcareService, or Device",
        default=None,
    )
    participantStatus: Optional[Code] = Field(
        description="accepted | declined | tentative | needs-action",
        default=None,
    )
    participantStatus_ext: Optional[Element] = Field(
        description="Placeholder element for participantStatus extensions",
        default=None,
        alias="_participantStatus",
    )
    comment: Optional[String] = Field(
        description="Additional comments",
        default=None,
    )
    comment_ext: Optional[Element] = Field(
        description="Placeholder element for comment extensions",
        default=None,
        alias="_comment",
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
