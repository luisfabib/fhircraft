from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from fhircraft.fhir.resources.datatypes.primitives import String, Uri, Code, Boolean

from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Period,
    Reference,
    CodeableConcept,
    ExtendedContactDetail,
    Availability,
)
from .resource import Resource
from .domain_resource import DomainResource


class PractitionerRole(DomainResource):
    """
    A specific set of Roles/Locations/specialties/services that a practitioner may perform, or has performed at an organization during a period of time.
    """

    _abstract = False
    _type = "PractitionerRole"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/PractitionerRole"

    identifier: Optional[ListType[Identifier]] = Field(
        description="Identifiers for a role/location",
        default=None,
    )
    active: Optional[Boolean] = Field(
        description="Whether this practitioner role record is in active use",
        default=None,
    )
    active_ext: Optional[Element] = Field(
        description="Placeholder element for active extensions",
        default=None,
        alias="_active",
    )
    period: Optional[Period] = Field(
        description="The period during which the practitioner is authorized to perform in these role(s)",
        default=None,
    )
    practitioner: Optional[Reference] = Field(
        description="Practitioner that provides services for the organization",
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
        description="Location(s) where the practitioner provides care",
        default=None,
    )
    healthcareService: Optional[ListType[Reference]] = Field(
        description="Healthcare services provided for this role\u0027s Organization/Location(s)",
        default=None,
    )
    contact: Optional[ListType[ExtendedContactDetail]] = Field(
        description="Official contact details relating to this PractitionerRole",
        default=None,
    )
    characteristic: Optional[ListType[CodeableConcept]] = Field(
        description="Collection of characteristics (attributes)",
        default=None,
    )
    communication: Optional[ListType[CodeableConcept]] = Field(
        description="A language the practitioner (in this role) can use in patient communication",
        default=None,
    )
    availability: Optional[ListType[Availability]] = Field(
        description="Times the Practitioner is available at this location and/or healthcare service (including exceptions)",
        default=None,
    )
    endpoint: Optional[ListType[Reference]] = Field(
        description="Endpoints for interacting with the practitioner in this role",
        default=None,
    )
