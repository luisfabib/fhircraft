from pydantic import Field, model_validator
from typing import Optional, List

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    Boolean,
    Markdown,
)

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
    comment_ext: Optional[Element] = Field(
        description="Placeholder element for comment extensions",
        default=None,
        alias="_comment",
    )


class HealthcareService(DomainResource):
    """
    The details of a healthcare service available at a location or in a catalog.  In the case where there is a hierarchy of services (for example, Lab -> Pathology -> Wound Cultures), this can be represented using a set of linked HealthcareServices.
    """

    _abstract = False
    _type = "HealthcareService"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/HealthcareService"

    identifier: Optional[List[Identifier]] = Field(
        description="External identifiers for this item",
        default=None,
    )
    active: Optional[Boolean] = Field(
        description="Whether this HealthcareService record is in active use",
        default=None,
    )
    active_ext: Optional[Element] = Field(
        description="Placeholder element for active extensions",
        default=None,
        alias="_active",
    )
    providedBy: Optional[Reference] = Field(
        description="Organization that provides this service",
        default=None,
    )
    offeredIn: Optional[List[Reference]] = Field(
        description="The service within which this service is offered",
        default=None,
    )
    category: Optional[List[CodeableConcept]] = Field(
        description="Broad category of service being performed or delivered",
        default=None,
    )
    type: Optional[List[CodeableConcept]] = Field(
        description="Type of service that may be delivered or performed",
        default=None,
    )
    specialty: Optional[List[CodeableConcept]] = Field(
        description="Specialties handled by the HealthcareService",
        default=None,
    )
    location: Optional[List[Reference]] = Field(
        description="Location(s) where service may be provided",
        default=None,
    )
    name: Optional[String] = Field(
        description="Description of service as presented to a consumer while searching",
        default=None,
    )
    name_ext: Optional[Element] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    comment: Optional[Markdown] = Field(
        description="Additional description and/or any specific issues not covered elsewhere",
        default=None,
    )
    comment_ext: Optional[Element] = Field(
        description="Placeholder element for comment extensions",
        default=None,
        alias="_comment",
    )
    extraDetails: Optional[Markdown] = Field(
        description="Extra details about the service that can\u0027t be placed in the other fields",
        default=None,
    )
    extraDetails_ext: Optional[Element] = Field(
        description="Placeholder element for extraDetails extensions",
        default=None,
        alias="_extraDetails",
    )
    photo: Optional[Attachment] = Field(
        description="Facilitates quick identification of the service",
        default=None,
    )
    contact: Optional[List[ExtendedContactDetail]] = Field(
        description="Official contact details for the HealthcareService",
        default=None,
    )
    coverageArea: Optional[List[Reference]] = Field(
        description="Location(s) service is intended for/available to",
        default=None,
    )
    serviceProvisionCode: Optional[List[CodeableConcept]] = Field(
        description="Conditions under which service is available/offered",
        default=None,
    )
    eligibility: Optional[List[HealthcareServiceEligibility]] = Field(
        description="Specific eligibility requirements required to use the service",
        default=None,
    )
    program: Optional[List[CodeableConcept]] = Field(
        description="Programs that this service is applicable to",
        default=None,
    )
    characteristic: Optional[List[CodeableConcept]] = Field(
        description="Collection of characteristics (attributes)",
        default=None,
    )
    communication: Optional[List[CodeableConcept]] = Field(
        description="The language that this service is offered in",
        default=None,
    )
    referralMethod: Optional[List[CodeableConcept]] = Field(
        description="Ways that the service accepts referrals",
        default=None,
    )
    appointmentRequired: Optional[Boolean] = Field(
        description="If an appointment is required for access to this service",
        default=None,
    )
    appointmentRequired_ext: Optional[Element] = Field(
        description="Placeholder element for appointmentRequired extensions",
        default=None,
        alias="_appointmentRequired",
    )
    availability: Optional[List[Availability]] = Field(
        description="Times the healthcare service is available (including exceptions)",
        default=None,
    )
    endpoint: Optional[List[Reference]] = Field(
        description="Technical endpoints providing access to electronic services operated for the healthcare service",
        default=None,
    )
