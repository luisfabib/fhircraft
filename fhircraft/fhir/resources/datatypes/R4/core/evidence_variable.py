import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    DateTime,
    Markdown,
    Date,
    Canonical,
    Boolean,
)

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

    description: Optional[String] = Field(
        description="Natural language description of the characteristic",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    definitionReference: Optional[Reference] = Field(
        description="What code or expression defines members?",
        default=None,
    )
    definitionCanonical: Optional[Canonical] = Field(
        description="What code or expression defines members?",
        default=None,
    )
    definitionCanonical_ext: Optional[Element] = Field(
        description="Placeholder element for definitionCanonical extensions",
        default=None,
        alias="_definitionCanonical",
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
    exclude: Optional[Boolean] = Field(
        description="Whether the characteristic includes or excludes members",
        default=None,
    )
    exclude_ext: Optional[Element] = Field(
        description="Placeholder element for exclude extensions",
        default=None,
        alias="_exclude",
    )
    participantEffectiveDateTime: Optional[DateTime] = Field(
        description="What time period do participants cover",
        default=None,
    )
    participantEffectiveDateTime_ext: Optional[Element] = Field(
        description="Placeholder element for participantEffectiveDateTime extensions",
        default=None,
        alias="_participantEffectiveDateTime",
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
    groupMeasure: Optional[Code] = Field(
        description="mean | median | mean-of-mean | mean-of-median | median-of-mean | median-of-median",
        default=None,
    )
    groupMeasure_ext: Optional[Element] = Field(
        description="Placeholder element for groupMeasure extensions",
        default=None,
        alias="_groupMeasure",
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
                Canonical,
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
            field_types=[DateTime, Period, Duration, Timing],
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
    url: Optional[Uri] = Field(
        description="Canonical identifier for this evidence variable, represented as a URI (globally unique)",
        default=None,
    )
    url_ext: Optional[Element] = Field(
        description="Placeholder element for url extensions",
        default=None,
        alias="_url",
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Additional identifier for the evidence variable",
        default=None,
    )
    version: Optional[String] = Field(
        description="Business version of the evidence variable",
        default=None,
    )
    version_ext: Optional[Element] = Field(
        description="Placeholder element for version extensions",
        default=None,
        alias="_version",
    )
    name: Optional[String] = Field(
        description="Name for this evidence variable (computer friendly)",
        default=None,
    )
    name_ext: Optional[Element] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    title: Optional[String] = Field(
        description="Name for this evidence variable (human friendly)",
        default=None,
    )
    title_ext: Optional[Element] = Field(
        description="Placeholder element for title extensions",
        default=None,
        alias="_title",
    )
    shortTitle: Optional[String] = Field(
        description="Title for use in informal contexts",
        default=None,
    )
    shortTitle_ext: Optional[Element] = Field(
        description="Placeholder element for shortTitle extensions",
        default=None,
        alias="_shortTitle",
    )
    subtitle: Optional[String] = Field(
        description="Subordinate title of the EvidenceVariable",
        default=None,
    )
    subtitle_ext: Optional[Element] = Field(
        description="Placeholder element for subtitle extensions",
        default=None,
        alias="_subtitle",
    )
    status: Optional[Code] = Field(
        description="draft | active | retired | unknown",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    date: Optional[DateTime] = Field(
        description="Date last changed",
        default=None,
    )
    date_ext: Optional[Element] = Field(
        description="Placeholder element for date extensions",
        default=None,
        alias="_date",
    )
    publisher: Optional[String] = Field(
        description="Name of the publisher (organization or individual)",
        default=None,
    )
    publisher_ext: Optional[Element] = Field(
        description="Placeholder element for publisher extensions",
        default=None,
        alias="_publisher",
    )
    contact: Optional[ListType[ContactDetail]] = Field(
        description="Contact details for the publisher",
        default=None,
    )
    description: Optional[Markdown] = Field(
        description="Natural language description of the evidence variable",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
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
    copyright: Optional[Markdown] = Field(
        description="Use and/or publishing restrictions",
        default=None,
    )
    copyright_ext: Optional[Element] = Field(
        description="Placeholder element for copyright extensions",
        default=None,
        alias="_copyright",
    )
    approvalDate: Optional[Date] = Field(
        description="When the evidence variable was approved by publisher",
        default=None,
    )
    approvalDate_ext: Optional[Element] = Field(
        description="Placeholder element for approvalDate extensions",
        default=None,
        alias="_approvalDate",
    )
    lastReviewDate: Optional[Date] = Field(
        description="When the evidence variable was last reviewed",
        default=None,
    )
    lastReviewDate_ext: Optional[Element] = Field(
        description="Placeholder element for lastReviewDate extensions",
        default=None,
        alias="_lastReviewDate",
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
    type: Optional[Code] = Field(
        description="dichotomous | continuous | descriptive",
        default=None,
    )
    type_ext: Optional[Element] = Field(
        description="Placeholder element for type extensions",
        default=None,
        alias="_type",
    )
    characteristic: Optional[ListType[EvidenceVariableCharacteristic]] = Field(
        description="What defines the members of the evidence element",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_evv_0_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.matches('[A-Z]([A-Za-z0-9_]){0,254}')",
            human="Name should be usable as an identifier for the module by machine processing applications such as code generation",
            key="evv-0",
            severity="warning",
        )
