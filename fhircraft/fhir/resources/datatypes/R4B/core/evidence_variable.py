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
    Identifier,
    Annotation,
    UsageContext,
    ContactDetail,
    RelatedArtifact,
    BackboneElement,
    Reference,
    CodeableConcept,
    Expression,
    Quantity,
    Range,
)
from .resource import Resource
from .domain_resource import DomainResource


class EvidenceVariableCharacteristicTimeFromStart(BackboneElement):
    """
    Indicates duration, period, or point of observation from the participant's study entry.
    """

    description: Optional[fhir.string] = Field(
        description="Human readable description",
        default=None,
    )
    quantity: Optional[Quantity] = Field(
        description="Used to express the observation at a defined amount of time after the study start",
        default=None,
    )
    range: Optional[Range] = Field(
        description="Used to express the observation within a period after the study start",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Used for footnotes or explanatory notes",
        default=None,
    )


class EvidenceVariableCharacteristic(BackboneElement):
    """
    A characteristic that defines the members of the evidence element. Multiple characteristics are applied with "and" semantics.
    """

    description: Optional[fhir.string] = Field(
        description="Natural language description of the characteristic",
        default=None,
    )
    definitionReference: Optional[Reference] = Field(
        description="What code or expression defines members?",
        default=None,
    )
    definitionCanonical: Optional[fhir.canonical] = Field(
        description="What code or expression defines members?",
        default=None,
    )
    definitionCodeableConcept: Optional[CodeableConcept] = Field(
        description="What code or expression defines members?",
        default=None,
    )
    definitionExpression: Optional[Expression] = Field(
        description="What code or expression defines members?",
        default=None,
    )
    method: Optional[CodeableConcept] = Field(
        description="Method used for describing characteristic",
        default=None,
    )
    device: Optional[Reference] = Field(
        description="Device used for determining characteristic",
        default=None,
    )
    exclude: Optional[fhir.boolean] = Field(
        description="Whether the characteristic includes or excludes members",
        default=None,
    )
    timeFromStart: Optional[EvidenceVariableCharacteristicTimeFromStart] = Field(
        description="Observation time from study start",
        default=None,
    )
    groupMeasure: Optional[fhir.code] = Field(
        description="mean | median | mean-of-mean | mean-of-median | median-of-mean | median-of-median",
        default=None,
    )

    @property
    def definition(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="definition",
        )

    @model_validator(mode="after")
    def definition_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Reference, fhir.Canonical, CodeableConcept, Expression],
            field_name_base="definition",
            required=True,
        )


class EvidenceVariableCategory(BackboneElement):
    """
    A grouping (or set of values) described along with other groupings to specify the set of groupings allowed for the variable.
    """

    name: Optional[fhir.string] = Field(
        description="Description of the grouping",
        default=None,
    )
    valueCodeableConcept: Optional[CodeableConcept] = Field(
        description="Definition of the grouping",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="Definition of the grouping",
        default=None,
    )
    valueRange: Optional[Range] = Field(
        description="Definition of the grouping",
        default=None,
    )

    @property
    def value(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="value",
        )

    @model_validator(mode="after")
    def value_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[CodeableConcept, Quantity, Range],
            field_name_base="value",
            required=False,
        )


class EvidenceVariable(DomainResource):
    """
    The EvidenceVariable resource describes an element that knowledge (Evidence) is about.
    """

    _abstract = False
    _type = "EvidenceVariable"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/EvidenceVariable"

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
        description="canonical identifier for this evidence variable, represented as a URI (globally unique)",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Additional identifier for the evidence variable",
        default=None,
    )
    version: Optional[fhir.string] = Field(
        description="Business version of the evidence variable",
        default=None,
    )
    name: Optional[fhir.string] = Field(
        description="Name for this evidence variable (computer friendly)",
        default=None,
    )
    title: Optional[fhir.string] = Field(
        description="Name for this evidence variable (human friendly)",
        default=None,
    )
    shortTitle: Optional[fhir.string] = Field(
        description="Title for use in informal contexts",
        default=None,
    )
    subtitle: Optional[fhir.string] = Field(
        description="Subordinate title of the EvidenceVariable",
        default=None,
    )
    status: fhir.code = Field(
        description="draft | active | retired | unknown",
    )
    date: Optional[fhir.dateTime] = Field(
        description="Date last changed",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
        description="Natural language description of the evidence variable",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Used for footnotes or explanatory notes",
        default=None,
    )
    useContext: Optional[ListType[UsageContext]] = Field(
        description="The context that the content is intended to support",
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
    author: Optional[ListType[ContactDetail]] = Field(
        description="Who authored the content",
        default=None,
    )
    editor: Optional[ListType[ContactDetail]] = Field(
        description="Who edited the content",
        default=None,
    )
    reviewer: Optional[ListType[ContactDetail]] = Field(
        description="Who reviewed the content",
        default=None,
    )
    endorser: Optional[ListType[ContactDetail]] = Field(
        description="Who endorsed the content",
        default=None,
    )
    relatedArtifact: Optional[ListType[RelatedArtifact]] = Field(
        description="Additional documentation, citations, etc.",
        default=None,
    )
    actual: Optional[fhir.boolean] = Field(
        description="Actual or conceptual",
        default=None,
    )
    characteristicCombination: Optional[fhir.code] = Field(
        description="intersection | union",
        default=None,
    )
    characteristic: Optional[ListType[EvidenceVariableCharacteristic]] = Field(
        description="What defines the members of the evidence element",
        default=None,
    )
    handling: Optional[fhir.code] = Field(
        description="continuous | dichotomous | ordinal | polychotomous",
        default=None,
    )
    category: Optional[ListType[EvidenceVariableCategory]] = Field(
        description="A grouping for ordinal or polychotomous variables",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_cnl_0_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.exists() implies name.matches('[A-Z]([A-Za-z0-9_]){0,254}')",
            human="Name should be usable as an identifier for the module by machine processing applications such as code generation",
            key="cnl-0",
            severity="warning",
        )
