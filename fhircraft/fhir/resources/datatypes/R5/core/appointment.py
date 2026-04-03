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
    CodeableConcept,
    CodeableReference,
    Reference,
    VirtualServiceDetail,
    Period,
    Annotation,
    BackboneElement,
    Coding,
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
    period: Optional[Period] = Field(
        description="Participation period of the actor",
        default=None,
    )
    actor: Optional[Reference] = Field(
        description="The individual, device, location, or service participating in the appointment",
        default=None,
    )
    required: Optional[Boolean] = Field(
        description="The participant is required to attend (optional when false)",
        default=None,
    )
    status: Optional[Code] = Field(
        description="accepted | declined | tentative | needs-action",
        default=None,
    )

class AppointmentRecurrenceTemplateWeeklyTemplate(BackboneElement):
    """
    Information about weekly recurring appointments.
    """

    monday: Optional[Boolean] = Field(
        description="Recurs on Mondays",
        default=None,
    )
    tuesday: Optional[Boolean] = Field(
        description="Recurs on Tuesday",
        default=None,
    )
    wednesday: Optional[Boolean] = Field(
        description="Recurs on Wednesday",
        default=None,
    )
    thursday: Optional[Boolean] = Field(
        description="Recurs on Thursday",
        default=None,
    )
    friday: Optional[Boolean] = Field(
        description="Recurs on Friday",
        default=None,
    )
    saturday: Optional[Boolean] = Field(
        description="Recurs on Saturday",
        default=None,
    )
    sunday: Optional[Boolean] = Field(
        description="Recurs on Sunday",
        default=None,
    )
    weekInterval: Optional[PositiveInt] = Field(
        description="Recurs every nth week",
        default=None,
    )

class AppointmentRecurrenceTemplateMonthlyTemplate(BackboneElement):
    """
    Information about monthly recurring appointments.
    """

    dayOfMonth: Optional[PositiveInt] = Field(
        description="Recurs on a specific day of the month",
        default=None,
    )
    nthWeekOfMonth: Optional[Coding] = Field(
        description="Indicates which week of the month the appointment should occur",
        default=None,
    )
    dayOfWeek: Optional[Coding] = Field(
        description="Indicates which day of the week the appointment should occur",
        default=None,
    )
    monthInterval: Optional[PositiveInt] = Field(
        description="Recurs every nth month",
        default=None,
    )

class AppointmentRecurrenceTemplateYearlyTemplate(BackboneElement):
    """
    Information about yearly recurring appointments.
    """

    yearInterval: Optional[PositiveInt] = Field(
        description="Recurs every nth year",
        default=None,
    )

class AppointmentRecurrenceTemplate(BackboneElement):
    """
    The details of the recurrence pattern or template that is used to generate recurring appointments.
    """

    timezone: Optional[CodeableConcept] = Field(
        description="The timezone of the occurrences",
        default=None,
    )
    recurrenceType: Optional[CodeableConcept] = Field(
        description="The frequency of the recurrence",
        default=None,
    )
    lastOccurrenceDate: Optional[Date] = Field(
        description="The date when the recurrence should end",
        default=None,
    )
    occurrenceCount: Optional[PositiveInt] = Field(
        description="The number of planned occurrences",
        default=None,
    )
    occurrenceDate: Optional[ListType[Date]] = Field(
        description="Specific dates for a recurring set of appointments (no template)",
        default=None,
    )
    weeklyTemplate: Optional[AppointmentRecurrenceTemplateWeeklyTemplate] = Field(
        description="Information about weekly recurring appointments",
        default=None,
    )
    monthlyTemplate: Optional[AppointmentRecurrenceTemplateMonthlyTemplate] = Field(
        description="Information about monthly recurring appointments",
        default=None,
    )
    yearlyTemplate: Optional[AppointmentRecurrenceTemplateYearlyTemplate] = Field(
        description="Information about yearly recurring appointments",
        default=None,
    )
    excludingDate: Optional[ListType[Date]] = Field(
        description="Any dates that should be excluded from the series",
        default=None,
    )
    excludingRecurrenceId: Optional[ListType[PositiveInt]] = Field(
        description="Any recurrence IDs that should be excluded from the recurrence",
        default=None,
    )

class Appointment(DomainResource):
    """
    A booking of a healthcare event among patient(s), practitioner(s), related person(s) and/or device(s) for a specific date/time. This may result in one or more Encounter(s).
    """

    _abstract = False
    _type = "Appointment"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Appointment"

    identifier: Optional[ListType[Identifier]] = Field(
        description="External Ids for this item",
        default=None,
    )
    status: Optional[Code] = Field(
        description="proposed | pending | booked | arrived | fulfilled | cancelled | noshow | entered-in-error | checked-in | waitlist",
        default=None,
    )
    cancellationReason: Optional[CodeableConcept] = Field(
        description="The coded reason for the appointment being cancelled",
        default=None,
    )
    class_: Optional[ListType[CodeableConcept]] = Field(
        description="Classification when becoming an encounter",
        default=None,
        alias="class",
    )
    serviceCategory: Optional[ListType[CodeableConcept]] = Field(
        description="A broad categorization of the service that is to be performed during this appointment",
        default=None,
    )
    serviceType: Optional[ListType[CodeableReference]] = Field(
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
    reason: Optional[ListType[CodeableReference]] = Field(
        description="Reason this appointment is scheduled",
        default=None,
    )
    priority: Optional[CodeableConcept] = Field(
        description="Used to make informed decisions if needing to re-prioritize",
        default=None,
    )
    description: Optional[String] = Field(
        description="Shown on a subject line in a meeting request, or appointment list",
        default=None,
    )
    replaces: Optional[ListType[Reference]] = Field(
        description="Appointment replaced by this Appointment",
        default=None,
    )
    virtualService: Optional[ListType[VirtualServiceDetail]] = Field(
        description="Connection details of a virtual service (e.g. conference call)",
        default=None,
    )
    supportingInformation: Optional[ListType[Reference]] = Field(
        description="Additional information to support the appointment",
        default=None,
    )
    previousAppointment: Optional[Reference] = Field(
        description="The previous appointment in a series",
        default=None,
    )
    originatingAppointment: Optional[Reference] = Field(
        description="The originating appointment in a recurring set of appointments",
        default=None,
    )
    start: Optional[Instant] = Field(
        description="When appointment is to take place",
        default=None,
    )
    end: Optional[Instant] = Field(
        description="When appointment is to conclude",
        default=None,
    )
    minutesDuration: Optional[PositiveInt] = Field(
        description="Can be less than start/end (e.g. estimate)",
        default=None,
    )
    requestedPeriod: Optional[ListType[Period]] = Field(
        description="Potential date/time interval(s) requested to allocate the appointment within",
        default=None,
    )
    slot: Optional[ListType[Reference]] = Field(
        description="The slots that this appointment is filling",
        default=None,
    )
    account: Optional[ListType[Reference]] = Field(
        description="The set of accounts that may be used for billing for this Appointment",
        default=None,
    )
    created: Optional[DateTime] = Field(
        description="The date that this appointment was initially created",
        default=None,
    )
    cancellationDate: Optional[DateTime] = Field(
        description="When the appointment was cancelled",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Additional comments",
        default=None,
    )
    patientInstruction: Optional[ListType[CodeableReference]] = Field(
        description="Detailed information and instructions for the patient",
        default=None,
    )
    basedOn: Optional[ListType[Reference]] = Field(
        description="The request this appointment is allocated to assess",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="The patient or group associated with the appointment",
        default=None,
    )
    participant: Optional[ListType[AppointmentParticipant]] = Field(
        description="Participants involved in appointment",
        default=None,
    )
    recurrenceId: Optional[PositiveInt] = Field(
        description="The sequence number in the recurrence",
        default=None,
    )
    occurrenceChanged: Optional[Boolean] = Field(
        description="Indicates that this appointment varies from a recurrence pattern",
        default=None,
    )
    recurrenceTemplate: Optional[ListType[AppointmentRecurrenceTemplate]] = Field(
        description="Details of the recurrence pattern/template used to generate occurrences",
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
            expression="cancellationReason.exists() implies (status='noshow' or status='cancelled')",
            human="Cancellation reason is only used for appointments that have been cancelled, or noshow",
            key="app-4",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_app_5_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="start.exists() implies start <= end",
            human="The start must be less than or equal to the end",
            key="app-5",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_app_6_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="originatingAppointment.exists().not() or recurrenceTemplate.exists().not()",
            human="An appointment may have an originatingAppointment or recurrenceTemplate, but not both",
            key="app-6",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_app_7_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="cancellationDate.exists() implies (status='noshow' or status='cancelled')",
            human="Cancellation date is only used for appointments that have been cancelled, or noshow",
            key="app-7",
            severity="error",
        )
