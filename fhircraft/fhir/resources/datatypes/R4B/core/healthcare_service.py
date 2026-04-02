import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from ..primitive import *

from fhircraft.fhir.resources.datatypes.R4B.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    Attachment,
    ContactPoint,
    BackboneElement,
    Period,
)
from .resource import Resource
from .domain_resource import DomainResource

class HealthcareServiceEligibility(BackboneElement):
    """
    Does this service have specific eligibility requirements that need to be met in order to use the service?
    """

    code: Optional[CodeableConcept] = Field(
        description="Coded value for the eligibility",
        default=None,
    )
    comment: Optional[Markdown] = Field(
        description="Describes the eligibility conditions for the service",
        default=None,
    )

class HealthcareServiceAvailableTime(BackboneElement):
    """
    A collection of times that the Service Site is available.
    """

    daysOfWeek: Optional[ListType[Code]] = Field(
        description="mon | tue | wed | thu | fri | sat | sun",
        default=None,
    )
    allDay: Optional[Boolean] = Field(
        description="Always available? e.g. 24 hour service",
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

class HealthcareServiceNotAvailable(BackboneElement):
    """
    The HealthcareService is not available during this period of time due to the provided reason.
    """

    description: Optional[String] = Field(
        description="Reason presented to the user explaining why time not available",
        default=None,
    )
    during: Optional[Period] = Field(
        description="Service not available from this date",
        default=None,
    )

class HealthcareService(DomainResource):
    """
    The details of a healthcare service available at a location.
    """

    _abstract = False
    _type = "HealthcareService"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/HealthcareService"

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
        description="External identifiers for this item",
        default=None,
    )
    active: Optional[Boolean] = Field(
        description="Whether this HealthcareService record is in active use",
        default=None,
    )
    providedBy: Optional[Reference] = Field(
        description="Organization that provides this service",
        default=None,
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description="Broad category of service being performed or delivered",
        default=None,
    )
    type: Optional[ListType[CodeableConcept]] = Field(
        description="Type of service that may be delivered or performed",
        default=None,
    )
    specialty: Optional[ListType[CodeableConcept]] = Field(
        description="Specialties handled by the HealthcareService",
        default=None,
    )
    location: Optional[ListType[Reference]] = Field(
        description="Location(s) where service may be provided",
        default=None,
    )
    name: Optional[String] = Field(
        description="Description of service as presented to a consumer while searching",
        default=None,
    )
    comment: Optional[String] = Field(
        description="Additional description and/or any specific issues not covered elsewhere",
        default=None,
    )
    extraDetails: Optional[Markdown] = Field(
        description="Extra details about the service that can\u0027t be placed in the other fields",
        default=None,
    )
    photo: Optional[Attachment] = Field(
        description="Facilitates quick identification of the service",
        default=None,
    )
    telecom: Optional[ListType[ContactPoint]] = Field(
        description="Contacts related to the healthcare service",
        default=None,
    )
    coverageArea: Optional[ListType[Reference]] = Field(
        description="Location(s) service is intended for/available to",
        default=None,
    )
    serviceProvisionCode: Optional[ListType[CodeableConcept]] = Field(
        description="Conditions under which service is available/offered",
        default=None,
    )
    eligibility: Optional[ListType[HealthcareServiceEligibility]] = Field(
        description="Specific eligibility requirements required to use the service",
        default=None,
    )
    program: Optional[ListType[CodeableConcept]] = Field(
        description="Programs that this service is applicable to",
        default=None,
    )
    characteristic: Optional[ListType[CodeableConcept]] = Field(
        description="Collection of characteristics (attributes)",
        default=None,
    )
    communication: Optional[ListType[CodeableConcept]] = Field(
        description="The language that this service is offered in",
        default=None,
    )
    referralMethod: Optional[ListType[CodeableConcept]] = Field(
        description="Ways that the service accepts referrals",
        default=None,
    )
    appointmentRequired: Optional[Boolean] = Field(
        description="If an appointment is required for access to this service",
        default=None,
    )
    availableTime: Optional[ListType[HealthcareServiceAvailableTime]] = Field(
        description="Times the Service Site is available",
        default=None,
    )
    notAvailable: Optional[ListType[HealthcareServiceNotAvailable]] = Field(
        description="Not available during this time due to provided reason",
        default=None,
    )
    availabilityExceptions: Optional[String] = Field(
        description="Description of availability exceptions",
        default=None,
    )
    endpoint: Optional[ListType[Reference]] = Field(
        description="Technical endpoints providing access to electronic services operated for the healthcare service",
        default=None,
    )
