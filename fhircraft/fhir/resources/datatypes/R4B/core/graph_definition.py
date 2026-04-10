import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)


import fhircraft.fhir.resources.datatypes.R4B.primitive as fhir
from fhircraft.fhir.resources.datatypes.R4B.complex import (
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

    use: Optional[fhir.code] = Field(
        description="condition | requirement",
        default=None,
    )
    code: Optional[fhir.code] = Field(
        description="Patient | Encounter | RelatedPerson | Practitioner | Device",
        default=None,
    )
    rule: Optional[fhir.code] = Field(
        description="identical | matching | different | custom",
        default=None,
    )
    expression: Optional[fhir.string] = Field(
        description="Custom rule, as a FHIRPath expression",
        default=None,
    )
    description: Optional[fhir.string] = Field(
        description="Documentation for FHIRPath expression",
        default=None,
    )


class GraphDefinitionLinkTarget(BackboneElement):
    """
    Potential target for the link.
    """

    type: Optional[fhir.code] = Field(
        description="Type of resource this link refers to",
        default=None,
    )
    params: Optional[fhir.string] = Field(
        description="Criteria for reverse lookup",
        default=None,
    )
    profile: Optional[fhir.canonical] = Field(
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

    path: Optional[fhir.string] = Field(
        description="Path in the resource that contains the link",
        default=None,
    )
    sliceName: Optional[fhir.string] = Field(
        description="Which slice (if profiled)",
        default=None,
    )
    min: Optional[fhir.integer] = Field(
        description="Minimum occurrences for this link",
        default=None,
    )
    max: Optional[fhir.string] = Field(
        description="Maximum occurrences for this link",
        default=None,
    )
    description: Optional[fhir.string] = Field(
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
    url: Optional[fhir.uri] = Field(
        description="canonical identifier for this graph definition, represented as a URI (globally unique)",
        default=None,
    )
    version: Optional[fhir.string] = Field(
        description="Business version of the graph definition",
        default=None,
    )
    name: Optional[fhir.string] = Field(
        description="Name for this graph definition (computer friendly)",
        default=None,
    )
    status: Optional[fhir.code] = Field(
        description="draft | active | retired | unknown",
        default=None,
    )
    experimental: Optional[fhir.boolean] = Field(
        description="For testing purposes, not real usage",
        default=None,
    )
    date: Optional[fhir.dateTime] = Field(
        description="Date last changed",
        default=None,
    )
    publisher: Optional[fhir.string] = Field(
        description="Name of the publisher (organization or individual)",
        default=None,
    )
    contact: Optional[ListType[ContactDetail]] = Field(
        description="Contact details for the publisher",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
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
    purpose: Optional[fhir.markdown] = Field(
        description="Why this graph definition is defined",
        default=None,
    )
    start: Optional[fhir.code] = Field(
        description="Type of resource at which the graph starts",
        default=None,
    )
    profile: Optional[fhir.canonical] = Field(
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
            expression="name.exists() implies name.matches('[A-Z]([A-Za-z0-9_]){0,254}')",
            human="Name should be usable as an identifier for the module by machine processing applications such as code generation",
            key="gdf-0",
            severity="warning",
        )
