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
    Attachment,
    ExtendedContactDetail,
    BackboneElement,
    Availability,
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

class HealthcareService(DomainResource):
    """
    The details of a healthcare service available at a location or in a catalog.  In the case where there is a hierarchy of services (for example, Lab -> Pathology -> Wound Cultures), this can be represented using a set of linked HealthcareServices.
    """

    _abstract = False
    _type = "HealthcareService"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/HealthcareService"

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
    offeredIn: Optional[ListType[Reference]] = Field(
        description="The service within which this service is offered",
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
    comment: Optional[Markdown] = Field(
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
    contact: Optional[ListType[ExtendedContactDetail]] = Field(
        description="Official contact details for the HealthcareService",
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
    availability: Optional[ListType[Availability]] = Field(
        description="Times the healthcare service is available (including exceptions)",
        default=None,
    )
    endpoint: Optional[ListType[Reference]] = Field(
        description="Technical endpoints providing access to electronic services operated for the healthcare service",
        default=None,
    )
