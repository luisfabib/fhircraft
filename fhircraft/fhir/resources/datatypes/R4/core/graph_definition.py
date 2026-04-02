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
    ContactDetail,
    UsageContext,
    CodeableConcept,
    BackboneElement,
)
from .resource import Resource
from .domain_resource import DomainResource


class GraphDefinitionLinkTargetCompartment(BackboneElement):
    """
    Compartment Consistency Rules.
    """

    use: Optional[Code] = Field(
        description="condition | requirement",
        default=None,
    )
    code: Optional[Code] = Field(
        description="Patient | Encounter | RelatedPerson | Practitioner | Device",
        default=None,
    )
    rule: Optional[Code] = Field(
        description="identical | matching | different | custom",
        default=None,
    )
    expression: Optional[String] = Field(
        description="Custom rule, as a FHIRPath expression",
        default=None,
    )
    description: Optional[String] = Field(
        description="Documentation for FHIRPath expression",
        default=None,
    )


class GraphDefinitionLinkTarget(BackboneElement):
    """
    Potential target for the link.
    """

    type: Optional[Code] = Field(
        description="Type of resource this link refers to",
        default=None,
    )
    params: Optional[String] = Field(
        description="Criteria for reverse lookup",
        default=None,
    )
    profile: Optional[Canonical] = Field(
        description="Profile for the target resource",
        default=None,
    )
    compartment: Optional[ListType[GraphDefinitionLinkTargetCompartment]] = Field(
        description="Compartment Consistency Rules",
        default=None,
    )
    link: Optional[ListType["GraphDefinitionLink"]] = Field(
        description="Additional links from target resource",
        default=None,
    )


class GraphDefinitionLink(BackboneElement):
    """
    Links this graph makes rules about.
    """

    path: Optional[String] = Field(
        description="Path in the resource that contains the link",
        default=None,
    )
    sliceName: Optional[String] = Field(
        description="Which slice (if profiled)",
        default=None,
    )
    min: Optional[Integer] = Field(
        description="Minimum occurrences for this link",
        default=None,
    )
    max: Optional[String] = Field(
        description="Maximum occurrences for this link",
        default=None,
    )
    description: Optional[String] = Field(
        description="Why this link is specified",
        default=None,
    )
    target: Optional[ListType[GraphDefinitionLinkTarget]] = Field(
        description="Potential target for the link",
        default=None,
    )


class GraphDefinition(DomainResource):
    """
    A formal computable definition of a graph of resources - that is, a coherent set of resources that form a graph by following references. The Graph Definition resource defines a set and makes rules about the set.
    """

    _abstract = False
    _type = "GraphDefinition"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/GraphDefinition"

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
        description="Canonical identifier for this graph definition, represented as a URI (globally unique)",
        default=None,
    )
    version: Optional[String] = Field(
        description="Business version of the graph definition",
        default=None,
    )
    name: Optional[String] = Field(
        description="Name for this graph definition (computer friendly)",
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
        description="Natural language description of the graph definition",
        default=None,
    )
    useContext: Optional[ListType[UsageContext]] = Field(
        description="The context that the content is intended to support",
        default=None,
    )
    jurisdiction: Optional[ListType[CodeableConcept]] = Field(
        description="Intended jurisdiction for graph definition (if applicable)",
        default=None,
    )
    purpose: Optional[Markdown] = Field(
        description="Why this graph definition is defined",
        default=None,
    )
    start: Optional[Code] = Field(
        description="Type of resource at which the graph starts",
        default=None,
    )
    profile: Optional[Canonical] = Field(
        description="Profile on base resource",
        default=None,
    )
    link: Optional[ListType[GraphDefinitionLink]] = Field(
        description="Links this graph makes rules about",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_gdf_0_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.matches('[A-Z]([A-Za-z0-9_]){0,254}')",
            human="Name should be usable as an identifier for the module by machine processing applications such as code generation",
            key="gdf-0",
            severity="warning",
        )
