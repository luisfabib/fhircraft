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
    Coding,
    ContactDetail,
    UsageContext,
    CodeableConcept,
    BackboneElement,
)
from .resource import Resource
from .domain_resource import DomainResource


class GraphDefinitionNode(BackboneElement):
    """
    Potential target for the link.
    """

    nodeId: Optional[fhir.id_] = Field(
        description="Internal ID - target for link references",
        default=None,
    )
    description: Optional[fhir.string] = Field(
        description="Why this node is specified",
        default=None,
    )
    type: Optional[fhir.code] = Field(
        description="Type of resource this link refers to",
        default=None,
    )
    profile: Optional[fhir.canonical] = Field(
        description="Profile for the target resource",
        default=None,
    )


class GraphDefinitionLinkCompartment(BackboneElement):
    """
    Compartment Consistency Rules.
    """

    use: Optional[fhir.code] = Field(
        description="where | requires",
        default=None,
    )
    rule: Optional[fhir.code] = Field(
        description="identical | matching | different | custom",
        default=None,
    )
    code: Optional[fhir.code] = Field(
        description="Patient | Encounter | RelatedPerson | Practitioner | Device | EpisodeOfCare",
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


class GraphDefinitionLink(BackboneElement):
    """
    Links this graph makes rules about.
    """

    description: Optional[fhir.string] = Field(
        description="Why this link is specified",
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
    sourceId: Optional[fhir.id_] = Field(
        description="Source Node for this link",
        default=None,
    )
    path: Optional[fhir.string] = Field(
        description="Path in the resource that contains the link",
        default=None,
    )
    sliceName: Optional[fhir.string] = Field(
        description="Which slice (if profiled)",
        default=None,
    )
    targetId: Optional[fhir.id_] = Field(
        description="Target Node for this link",
        default=None,
    )
    params: Optional[fhir.string] = Field(
        description="Criteria for reverse lookup",
        default=None,
    )
    compartment: Optional[ListType[GraphDefinitionLinkCompartment]] = Field(
        description="Compartment Consistency Rules",
        default=None,
    )


class GraphDefinition(DomainResource):
    """
    A formal computable definition of a graph of resources - that is, a coherent set of resources that form a graph by following references. The Graph Definition resource defines a set and makes rules about the set.
    """

    _abstract = False
    _type = "GraphDefinition"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/GraphDefinition"

    url: Optional[fhir.uri] = Field(
        description="canonical identifier for this graph definition, represented as a URI (globally unique)",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Additional identifier for the GraphDefinition (business identifier)",
        default=None,
    )
    version: Optional[fhir.string] = Field(
        description="Business version of the graph definition",
        default=None,
    )
    versionAlgorithmString: Optional[fhir.string] = Field(
        description="How to compare versions",
        default=None,
    )
    versionAlgorithmCoding: Optional[Coding] = Field(
        description="How to compare versions",
        default=None,
    )
    name: Optional[fhir.string] = Field(
        description="Name for this graph definition (computer friendly)",
        default=None,
    )
    title: Optional[fhir.string] = Field(
        description="Name for this graph definition (human friendly)",
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
        description="Name of the publisher/steward (organization or individual)",
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
    copyright: Optional[fhir.markdown] = Field(
        description="Use and/or publishing restrictions",
        default=None,
    )
    copyrightLabel: Optional[fhir.string] = Field(
        description="Copyright holder and year(s)",
        default=None,
    )
    start: Optional[fhir.id_] = Field(
        description="Starting Node",
        default=None,
    )
    node: Optional[ListType[GraphDefinitionNode]] = Field(
        description="Potential target for the link",
        default=None,
    )
    link: Optional[ListType[GraphDefinitionLink]] = Field(
        description="Links this graph makes rules about",
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
            field_types=[fhir.string, Coding],
            field_name_base="versionAlgorithm",
            required=False,
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
