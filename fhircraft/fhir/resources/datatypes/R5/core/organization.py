from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators


import fhircraft.fhir.resources.datatypes.R5.primitive as fhir
from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    CodeableConcept,
    ExtendedContactDetail,
    Reference,
    BackboneElement,
    Period,
)
from .resource import Resource
from .domain_resource import DomainResource


class OrganizationQualification(BackboneElement):
    """
        The official certifications, accreditations, training, designations and licenses that authorize and/or otherwise endorse the provision of care by the organization.

    For example, an approval to provide a type of services issued by a certifying body (such as the US Joint Commission) to an organization.
    """

    identifier: Optional[ListType[Identifier]] = Field(
        description="An identifier for this qualification for the organization",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="Coded representation of the qualification",
        default=None,
    )
    period: Optional[Period] = Field(
        description="Period during which the qualification is valid",
        default=None,
    )
    issuer: Optional[Reference] = Field(
        description="Organization that regulates and issues the qualification",
        default=None,
    )


class Organization(DomainResource):
    """
    A formally or informally recognized grouping of people or organizations formed for the purpose of achieving some form of collective action.  Includes companies, institutions, corporations, departments, community groups, healthcare practice groups, payer/insurer, etc.
    """

    _abstract = False
    _type = "Organization"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Organization"

    identifier: Optional[ListType[Identifier]] = Field(
        description="Identifies this organization  across multiple systems",
        default=None,
    )
    active: Optional[fhir.boolean] = Field(
        description="Whether the organization\u0027s record is still in active use",
        default=None,
    )
    type: Optional[ListType[CodeableConcept]] = Field(
        description="Kind of organization",
        default=None,
    )
    name: Optional[fhir.string] = Field(
        description="Name used for the organization",
        default=None,
    )
    alias: Optional[ListType[fhir.string]] = Field(
        description="A list of alternate names that the organization is known as, or was known as in the past",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
        description="Additional details about the Organization that could be displayed as further information to identify the Organization beyond its name",
        default=None,
    )
    contact: Optional[ListType[ExtendedContactDetail]] = Field(
        description="Official contact details for the Organization",
        default=None,
    )
    partOf: Optional[Reference] = Field(
        description="The organization of which this organization forms a part",
        default=None,
    )
    endpoint: Optional[ListType[Reference]] = Field(
        description="Technical endpoints providing access to services operated for the organization",
        default=None,
    )
    qualification: Optional[ListType[OrganizationQualification]] = Field(
        description="Qualifications, certifications, accreditations, licenses, training, etc. pertaining to the provision of care",
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
