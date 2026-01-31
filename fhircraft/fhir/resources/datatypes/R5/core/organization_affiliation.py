from pydantic import Field, model_validator
from typing import Optional, List

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
)
from .resource import Resource
from .domain_resource import DomainResource


class OrganizationAffiliation(DomainResource):
    """
    Defines an affiliation/assotiation/relationship between 2 distinct organizations, that is not a part-of relationship/sub-division relationship.
    """

    _abstract = False
    _type = "OrganizationAffiliation"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/OrganizationAffiliation"

    identifier: Optional[List[Identifier]] = Field(
        description="Business identifiers that are specific to this role",
        default=None,
    )
    active: Optional[Boolean] = Field(
        description="Whether this organization affiliation record is in active use",
        default=None,
    )
    active_ext: Optional[Element] = Field(
        description="Placeholder element for active extensions",
        default=None,
        alias="_active",
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
    network: Optional[List[Reference]] = Field(
        description="The network in which the participatingOrganization provides the role\u0027s services (if defined) at the indicated locations (if defined)",
        default=None,
    )
    code: Optional[List[CodeableConcept]] = Field(
        description="Definition of the role the participatingOrganization plays",
        default=None,
    )
    specialty: Optional[List[CodeableConcept]] = Field(
        description="Specific specialty of the participatingOrganization in the context of the role",
        default=None,
    )
    location: Optional[List[Reference]] = Field(
        description="The location(s) at which the role occurs",
        default=None,
    )
    healthcareService: Optional[List[Reference]] = Field(
        description="Healthcare services provided through the role",
        default=None,
    )
    contact: Optional[List[ExtendedContactDetail]] = Field(
        description="Official contact details at the participatingOrganization relevant to this Affiliation",
        default=None,
    )
    endpoint: Optional[List[Reference]] = Field(
        description="Technical endpoints providing access to services operated for this role",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_org_3_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("contact",),
            expression="telecom.where(use = 'home').empty()",
            human="The telecom of an organization can never be of use 'home'",
            key="org-3",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_org_4_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("contact",),
            expression="address.where(use = 'home').empty()",
            human="The address of an organization can never be of use 'home'",
            key="org-4",
            severity="error",
        )
