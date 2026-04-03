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
    Coding,
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
    startParam: Optional[Uri] = Field(
        description="Search Param for interpreting $everything.start",
        default=None,
    )
    endParam: Optional[Uri] = Field(
        description="Search Param for interpreting $everything.end",
        default=None,
    )

class CompartmentDefinition(DomainResource):
    """
    A compartment definition that defines how resources are accessed on a server.
    """

    _abstract = False
    _type = "CompartmentDefinition"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/CompartmentDefinition"

    url: Optional[Uri] = Field(
        description="Canonical identifier for this compartment definition, represented as a URI (globally unique)",
        default=None,
    )
    version: Optional[String] = Field(
        description="Business version of the compartment definition",
        default=None,
    )
    versionAlgorithmString: Optional[String] = Field(
        description="How to compare versions",
        default=None,
    )
    versionAlgorithmCoding: Optional[Coding] = Field(
        description="How to compare versions",
        default=None,
    )
    name: Optional[String] = Field(
        description="Name for this compartment definition (computer friendly)",
        default=None,
    )
    title: Optional[String] = Field(
        description="Name for this compartment definition (human friendly)",
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
        description="Name of the publisher/steward (organization or individual)",
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
        description="Patient | Encounter | RelatedPerson | Practitioner | Device | EpisodeOfCare",
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

    @property
    def versionAlgorithm(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="versionAlgorithm",
        )

    @model_validator(mode="after")
    def versionAlgorithm_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[String, Coding],
            field_name_base="versionAlgorithm",
            required=False,
        )

    @model_validator(mode="after")
    def FHIR_cnl_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("url",),
            expression="exists() implies matches('^[^|# ]+$')",
            human="URL should not contain | or # - these characters make processing canonical references problematic",
            key="cnl-1",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_cnl_0_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.exists() implies name.matches('^[A-Z]([A-Za-z0-9_]){1,254}$')",
            human="Name should be usable as an identifier for the module by machine processing applications such as code generation",
            key="cnl-0",
            severity="warning",
        )
