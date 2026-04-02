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
)
from .resource import Resource
from .domain_resource import DomainResource

class OrganizationAffiliation(DomainResource):
    """
    Defines an affiliation/assotiation/relationship between 2 distinct oganizations, that is not a part-of relationship/sub-division relationship.
    """

    _abstract = False
    _type = "OrganizationAffiliation"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/OrganizationAffiliation"

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
        description="Business identifiers that are specific to this role",
        default=None,
    )
    active: Optional[Boolean] = Field(
        description="Whether this organization affiliation record is in active use",
        default=None,
    )
    period: Optional[Period] = Field(
        description="The period during which the participatingOrganization is affiliated with the primary organization",
        default=None,
    )
    organization: Optional[Reference] = Field(
        description="Organization where the role is available",
        default=None,
    )
    participatingOrganization: Optional[Reference] = Field(
        description="Organization that provides/performs the role (e.g. providing services or is a member of)",
        default=None,
    )
    network: Optional[ListType[Reference]] = Field(
        description="Health insurance provider network in which the participatingOrganization provides the role\u0027s services (if defined) at the indicated locations (if defined)",
        default=None,
    )
    code: Optional[ListType[CodeableConcept]] = Field(
        description="Definition of the role the participatingOrganization plays",
        default=None,
    )
    specialty: Optional[ListType[CodeableConcept]] = Field(
        description="Specific specialty of the participatingOrganization in the context of the role",
        default=None,
    )
    location: Optional[ListType[Reference]] = Field(
        description="The location(s) at which the role occurs",
        default=None,
    )
    healthcareService: Optional[ListType[Reference]] = Field(
        description="Healthcare services provided through the role",
        default=None,
    )
    telecom: Optional[ListType[ContactPoint]] = Field(
        description="Contact details at the participatingOrganization relevant to this Affiliation",
        default=None,
    )
    endpoint: Optional[ListType[Reference]] = Field(
        description="Technical endpoints providing access to services operated for this role",
        default=None,
    )
