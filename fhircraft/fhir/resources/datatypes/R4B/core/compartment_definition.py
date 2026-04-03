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
    ContactDetail,
    UsageContext,
    BackboneElement,
)
from .resource import Resource
from .domain_resource import DomainResource

class CompartmentDefinitionResource(BackboneElement):
    """
    Information about how a resource is related to the compartment.
    """

    code: Optional[Code] = Field(
        description="Name of resource type",
        default=None,
    )
    param: Optional[ListType[String]] = Field(
        description="Search Parameter Name, or chained parameters",
        default=None,
    )
    documentation: Optional[String] = Field(
        description="Additional documentation about the resource and compartment",
        default=None,
    )

class CompartmentDefinition(DomainResource):
    """
    A compartment definition that defines how resources are accessed on a server.
    """

    _abstract = False
    _type = "CompartmentDefinition"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/CompartmentDefinition"

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
    url: Optional[Uri] = Field(
        description="Canonical identifier for this compartment definition, represented as a URI (globally unique)",
        default=None,
    )
    version: Optional[String] = Field(
        description="Business version of the compartment definition",
        default=None,
    )
    name: Optional[String] = Field(
        description="Name for this compartment definition (computer friendly)",
        default=None,
    )
    status: Optional[Code] = Field(
        description="draft | active | retired | unknown",
        default=None,
    )
    experimental: Optional[Boolean] = Field(
        description="For testing purposes, not real usage",
        default=None,
    )
    date: Optional[DateTime] = Field(
        description="Date last changed",
        default=None,
    )
    publisher: Optional[String] = Field(
        description="Name of the publisher (organization or individual)",
        default=None,
    )
    contact: Optional[ListType[ContactDetail]] = Field(
        description="Contact details for the publisher",
        default=None,
    )
    description: Optional[Markdown] = Field(
        description="Natural language description of the compartment definition",
        default=None,
    )
    useContext: Optional[ListType[UsageContext]] = Field(
        description="The context that the content is intended to support",
        default=None,
    )
    purpose: Optional[Markdown] = Field(
        description="Why this compartment definition is defined",
        default=None,
    )
    code: Optional[Code] = Field(
        description="Patient | Encounter | RelatedPerson | Practitioner | Device",
        default=None,
    )
    search: Optional[Boolean] = Field(
        description="Whether the search syntax is supported",
        default=None,
    )
    resource: Optional[ListType[CompartmentDefinitionResource]] = Field(
        description="How a resource is related to the compartment",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_cpd_0_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.exists() implies name.matches('[A-Z]([A-Za-z0-9_]){0,254}')",
            human="Name should be usable as an identifier for the module by machine processing applications such as code generation",
            key="cpd-0",
            severity="warning",
        )
