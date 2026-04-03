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
    Period,
    Reference,
    CodeableConcept,
    ContactPoint,
    BackboneElement,
)
from .resource import Resource
from .domain_resource import DomainResource

class PractitionerRoleAvailableTime(BackboneElement):
    """
    A collection of times the practitioner is available or performing this role at the location and/or healthcareservice.
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

class PractitionerRoleNotAvailable(BackboneElement):
    """
    The practitioner is not available or performing this role during this period of time due to the provided reason.
    """

    description: Optional[String] = Field(
        description="Reason presented to the user explaining why time not available",
        default=None,
    )
    during: Optional[Period] = Field(
        description="Service not available from this date",
        default=None,
    )

class PractitionerRole(DomainResource):
    """
    A specific set of Roles/Locations/specialties/services that a practitioner may perform at an organization for a period of time.
    """

    _abstract = False
    _type = "PractitionerRole"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/PractitionerRole"

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
        description="Business Identifiers that are specific to a role/location",
        default=None,
    )
    active: Optional[Boolean] = Field(
        description="Whether this practitioner role record is in active use",
        default=None,
    )
    period: Optional[Period] = Field(
        description="The period during which the practitioner is authorized to perform in these role(s)",
        default=None,
    )
    practitioner: Optional[Reference] = Field(
        description="Practitioner that is able to provide the defined services for the organization",
        default=None,
    )
    organization: Optional[Reference] = Field(
        description="Organization where the roles are available",
        default=None,
    )
    code: Optional[ListType[CodeableConcept]] = Field(
        description="Roles which this practitioner may perform",
        default=None,
    )
    specialty: Optional[ListType[CodeableConcept]] = Field(
        description="Specific specialty of the practitioner",
        default=None,
    )
    location: Optional[ListType[Reference]] = Field(
        description="The location(s) at which this practitioner provides care",
        default=None,
    )
    healthcareService: Optional[ListType[Reference]] = Field(
        description="The list of healthcare services that this worker provides for this role\u0027s Organization/Location(s)",
        default=None,
    )
    telecom: Optional[ListType[ContactPoint]] = Field(
        description="Contact details that are specific to the role/location/service",
        default=None,
    )
    availableTime: Optional[ListType[PractitionerRoleAvailableTime]] = Field(
        description="Times the Service Site is available",
        default=None,
    )
    notAvailable: Optional[ListType[PractitionerRoleNotAvailable]] = Field(
        description="Not available during this time due to provided reason",
        default=None,
    )
    availabilityExceptions: Optional[String] = Field(
        description="Description of availability exceptions",
        default=None,
    )
    endpoint: Optional[ListType[Reference]] = Field(
        description="Technical endpoints providing access to services operated for the practitioner with this role",
        default=None,
    )
