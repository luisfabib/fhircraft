import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)


import fhircraft.fhir.resources.datatypes.R4.primitive as fhir
from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Timing,
    Extension,
    Identifier,
    ContactDetail,
    Annotation,
    UsageContext,
    CodeableConcept,
    Period,
    RelatedArtifact,
    BackboneElement,
    Reference,
    Expression,
    DataRequirement,
    TriggerDefinition,
    Duration,
)
from .resource import Resource
from .domain_resource import DomainResource


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
    definitionDataRequirement: Optional[DataRequirement] = Field(
        description="What code or expression defines members?",
        default=None,
    )
    definitionTriggerDefinition: Optional[TriggerDefinition] = Field(
        description="What code or expression defines members?",
        default=None,
    )
    usageContext: Optional[ListType[UsageContext]] = Field(
        description="What code/value pairs define members?",
        default=None,
    )
    exclude: Optional[fhir.boolean] = Field(
        description="Whether the characteristic includes or excludes members",
        default=None,
    )
    participantEffectiveDateTime: Optional[fhir.dateTime] = Field(
        description="What time period do participants cover",
        default=None,
    )
    participantEffectivePeriod: Optional[Period] = Field(
        description="What time period do participants cover",
        default=None,
    )
    participantEffectiveDuration: Optional[Duration] = Field(
        description="What time period do participants cover",
        default=None,
    )
    participantEffectiveTiming: Optional[Timing] = Field(
        description="What time period do participants cover",
        default=None,
    )
    timeFromStart: Optional[Duration] = Field(
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

    @property
    def participantEffective(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="participantEffective",
        )

    @model_validator(mode="after")
    def definition_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[
                Reference,
                fhir.Canonical,
                CodeableConcept,
                Expression,
                DataRequirement,
                TriggerDefinition,
            ],
            field_name_base="definition",
            required=True,
        )

    @model_validator(mode="after")
    def participantEffective_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.DateTime, Period, Duration, Timing],
            field_name_base="participantEffective",
            required=False,
        )


class EvidenceVariable(DomainResource):
    """
    The EvidenceVariable resource describes a "PICO" element that knowledge (evidence, assertion, recommendation) is about.
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
    publisher: Optional[fhir.string] = Field(
        description="Name of the publisher (organization or individual)",
        default=None,
    )
    contact: Optional[ListType[ContactDetail]] = Field(
        description="Contact details for the publisher",
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
    jurisdiction: Optional[ListType[CodeableConcept]] = Field(
        description="Intended jurisdiction for evidence variable (if applicable)",
        default=None,
    )
    copyright: Optional[fhir.markdown] = Field(
        description="Use and/or publishing restrictions",
        default=None,
    )
    approvalDate: Optional[fhir.date_] = Field(
        description="When the evidence variable was approved by publisher",
        default=None,
    )
    lastReviewDate: Optional[fhir.date_] = Field(
        description="When the evidence variable was last reviewed",
        default=None,
    )
    effectivePeriod: Optional[Period] = Field(
        description="When the evidence variable is expected to be used",
        default=None,
    )
    topic: Optional[ListType[CodeableConcept]] = Field(
        description="The category of the EvidenceVariable, such as Education, Treatment, Assessment, etc.",
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
    type: Optional[fhir.code] = Field(
        description="dichotomous | continuous | descriptive",
        default=None,
    )
    characteristic: ListType[EvidenceVariableCharacteristic] = Field(
        description="What defines the members of the evidence element",
     	min_length=1,
	)

    @model_validator(mode="after")
    def FHIR_evv_0_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.matches('[A-Z]([A-Za-z0-9_]){0,254}')",
            human="Name should be usable as an identifier for the module by machine processing applications such as code generation",
            key="evv-0",
            severity="warning",
        )
