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
    Reference,
)
from .resource import Resource
from .domain_resource import DomainResource


class RequirementsStatement(BackboneElement):
    """
    The actual statement of requirement, in markdown format.
    """

    key: fhir.id_ = Field(
        description="Key that identifies this statement",
    )
    label: Optional[fhir.string] = Field(
        description="Short Human label for this statement",
        default=None,
    )
    conformance: Optional[ListType[fhir.code]] = Field(
        description="SHALL | SHOULD | MAY | SHOULD-NOT",
        default=None,
    )
    conditionality: Optional[fhir.boolean] = Field(
        description="Set to true if requirements statement is conditional",
        default=None,
    )
    requirement: fhir.markdown = Field(
        description="The actual requirement",
    )
    derivedFrom: Optional[fhir.string] = Field(
        description="Another statement this clarifies/restricts ([url#]key)",
        default=None,
    )
    parent: Optional[fhir.string] = Field(
        description="A larger requirement that this requirement helps to refine and enable",
        default=None,
    )
    satisfiedBy: Optional[ListType[fhir.url]] = Field(
        description="Design artifact that satisfies this requirement",
        default=None,
    )
    reference: Optional[ListType[fhir.url]] = Field(
        description="External artifact (rule/document etc. that) created this requirement",
        default=None,
    )
    source: Optional[ListType[Reference]] = Field(
        description="Who asked for this statement",
        default=None,
    )


class Requirements(DomainResource):
    """
    The Requirements resource is used to describe an actor - a human or an application that plays a role in data exchange, and that may have obligations associated with the role the actor plays.
    """

    _abstract = False
    _type = "Requirements"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Requirements"

    url: Optional[fhir.uri] = Field(
        description="canonical identifier for this Requirements, represented as a URI (globally unique)",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Additional identifier for the Requirements (business identifier)",
        default=None,
    )
    version: Optional[fhir.string] = Field(
        description="Business version of the Requirements",
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
        description="Name for this Requirements (computer friendly)",
        default=None,
    )
    title: Optional[fhir.string] = Field(
        description="Name for this Requirements (human friendly)",
        default=None,
    )
    status: fhir.code = Field(
        description="draft | active | retired | unknown",
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
        description="Natural language description of the requirements",
        default=None,
    )
    useContext: Optional[ListType[UsageContext]] = Field(
        description="The context that the content is intended to support",
        default=None,
    )
    jurisdiction: Optional[ListType[CodeableConcept]] = Field(
        description="Intended jurisdiction for Requirements (if applicable)",
        default=None,
    )
    purpose: Optional[fhir.markdown] = Field(
        description="Why this Requirements is defined",
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
    derivedFrom: Optional[ListType[fhir.canonical]] = Field(
        description="Other set of Requirements this builds on",
        default=None,
    )
    reference: Optional[ListType[fhir.url]] = Field(
        description="External artifact (rule/document etc. that) created this set of requirements",
        default=None,
    )
    actor: Optional[ListType[fhir.canonical]] = Field(
        description="Actor for these requirements",
        default=None,
    )
    statement: Optional[ListType[RequirementsStatement]] = Field(
        description="Actual statement as markdown",
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
            field_types=[fhir.String, Coding],
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
