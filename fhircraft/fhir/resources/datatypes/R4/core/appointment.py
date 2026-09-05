import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)


import fhircraft.fhir.resources.datatypes.R4.primitive as fhir
from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    BackboneElement,
    Period,
)
from .resource import Resource
from .domain_resource import DomainResource


class AppointmentParticipant(BackboneElement):
    """
    List of participants involved in the appointment.
    """

    type: Optional[ListType[CodeableConcept]] = Field(
        description="Role of participant in the appointment",
        default=None,
    )
    actor: Optional[Reference] = Field(
        description="Person, Location/HealthcareService or Device",
        default=None,
    )
    required: Optional[fhir.code] = Field(
        description="required | optional | information-only",
        default=None,
    )
    status: fhir.code = Field(
        description="accepted | declined | tentative | needs-action",
    )
    period: Optional[Period] = Field(
        description="Participation period of the actor",
        default=None,
    )


class Appointment(DomainResource):
    """
    A booking of a healthcare event among patient(s), practitioner(s), related person(s) and/or device(s) for a specific date/time. This may result in one or more Encounter(s).
    """

    _abstract = False
    _type = "Appointment"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Appointment"

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
    status: fhir.code = Field(
        description="proposed | pending | booked | arrived | fulfilled | cancelled | noshow | entered-in-error | checked-in | waitlist",
    )
    cancelationReason: Optional[CodeableConcept] = Field(
        description="The coded reason for the appointment being cancelled",
        default=None,
    )
    serviceCategory: Optional[ListType[CodeableConcept]] = Field(
        description="A broad categorization of the service that is to be performed during this appointment",
        default=None,
    )
    serviceType: Optional[ListType[CodeableConcept]] = Field(
        description="The specific service that is to be performed during this appointment",
        default=None,
    )
    specialty: Optional[ListType[CodeableConcept]] = Field(
        description="The specialty of a practitioner that would be required to perform the service requested in this appointment",
        default=None,
    )
    appointmentType: Optional[CodeableConcept] = Field(
        description="The style of appointment or patient that has been booked in the slot (not service type)",
        default=None,
    )
    reasonCode: Optional[ListType[CodeableConcept]] = Field(
        description="Coded reason this appointment is scheduled",
        default=None,
    )
    reasonReference: Optional[ListType[Reference]] = Field(
        description="Reason the appointment is to take place (resource)",
        default=None,
    )
    priority: Optional[fhir.unsignedInt] = Field(
        description="Used to make informed decisions if needing to re-prioritize",
        default=None,
    )
    description: Optional[fhir.string] = Field(
        description="Shown on a subject line in a meeting request, or appointment list",
        default=None,
    )
    supportingInformation: Optional[ListType[Reference]] = Field(
        description="Additional information to support the appointment",
        default=None,
    )
    start: Optional[fhir.instant] = Field(
        description="When appointment is to take place",
        default=None,
    )
    end: Optional[fhir.instant] = Field(
        description="When appointment is to conclude",
        default=None,
    )
    minutesDuration: Optional[fhir.positiveInt] = Field(
        description="Can be less than start/end (e.g. estimate)",
        default=None,
    )
    slot: Optional[ListType[Reference]] = Field(
        description="The slots that this appointment is filling",
        default=None,
    )
    created: Optional[fhir.dateTime] = Field(
        description="The date that this appointment was initially created",
        default=None,
    )
    comment: Optional[fhir.string] = Field(
        description="Additional comments",
        default=None,
    )
    patientInstruction: Optional[fhir.string] = Field(
        description="Detailed information and instructions for the patient",
        default=None,
    )
    basedOn: Optional[ListType[Reference]] = Field(
        description="The service request this appointment is allocated to assess",
        default=None,
    )
    participant: ListType[AppointmentParticipant] = Field(
        description="Participants involved in appointment",
        min_length=1,
    )
    requestedPeriod: Optional[ListType[Period]] = Field(
        description="Potential date/time interval(s) requested to allocate the appointment within",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_app_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("participant",),
            expression="type.exists() or actor.exists()",
            human="Either the type or actor on the participant SHALL be specified",
            key="app-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_app_2_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="start.exists() = end.exists()",
            human="Either start and end are specified, or neither",
            key="app-2",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_app_3_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(start.exists() and end.exists()) or (status in ('proposed' | 'cancelled' | 'waitlist'))",
            human="Only proposed or cancelled appointments can be missing start/end dates",
            key="app-3",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_app_4_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="Appointment.cancelationReason.exists() implies (Appointment.status='no-show' or Appointment.status='cancelled')",
            human="Cancelation reason is only used for appointments that have been cancelled, or no-show",
            key="app-4",
            severity="error",
        )
