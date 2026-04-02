import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from ..primitive import *

from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    CodeableConcept,
    ContactPoint,
    Address,
    Reference,
    BackboneElement,
    HumanName,
)
from .resource import Resource
from .domain_resource import DomainResource

class OrganizationContact(BackboneElement):
    """
    Contact for the organization for a certain purpose.
    """

    purpose: Optional[CodeableConcept] = Field(
        description="The type of contact",
        default=None,
    )
    name: Optional[HumanName] = Field(
        description="A name associated with the contact",
        default=None,
    )
    telecom: Optional[ListType[ContactPoint]] = Field(
        description="Contact details (telephone, email, etc.)  for a contact",
        default=None,
    )
    address: Optional[Address] = Field(
        description="Visiting or postal addresses for the contact",
        default=None,
    )

class Organization(DomainResource):
    """
    A formally or informally recognized grouping of people or organizations formed for the purpose of achieving some form of collective action.  Includes companies, institutions, corporations, departments, community groups, healthcare practice groups, payer/insurer, etc.
    """

    _abstract = False
    _type = "Organization"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Organization"

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
        description="Identifies this organization  across multiple systems",
        default=None,
    )
    active: Optional[Boolean] = Field(
        description="Whether the organization\u0027s record is still in active use",
        default=None,
    )
    type: Optional[ListType[CodeableConcept]] = Field(
        description="Kind of organization",
        default=None,
    )
    name: Optional[String] = Field(
        description="Name used for the organization",
        default=None,
    )
    alias: Optional[ListType[String]] = Field(
        description="A list of alternate names that the organization is known as, or was known as in the past",
        default=None,
    )
    telecom: Optional[ListType[ContactPoint]] = Field(
        description="A contact detail for the organization",
        default=None,
    )
    address: Optional[ListType[Address]] = Field(
        description="An address for the organization",
        default=None,
    )
    partOf: Optional[Reference] = Field(
        description="The organization of which this organization forms a part",
        default=None,
    )
    contact: Optional[ListType[OrganizationContact]] = Field(
        description="Contact for the organization for a certain purpose",
        default=None,
    )
    endpoint: Optional[ListType[Reference]] = Field(
        description="Technical endpoints providing access to services operated for the organization",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_org_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(identifier.count() + name.count()) > 0",
            human="The organization SHALL at least have a name or an identifier, and possibly more than one",
            key="org-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_org_2_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("address",),
            expression="where(use = 'home').empty()",
            human="An address of an organization can never be of use 'home'",
            key="org-2",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_org_3_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("telecom",),
            expression="where(use = 'home').empty()",
            human="The telecom of an organization can never be of use 'home'",
            key="org-3",
            severity="error",
        )
