import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)


import fhircraft.fhir.resources.datatypes.R4.primitive as fhir
from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    ContactDetail,
    BackboneElement,
    Annotation,
    UsageContext,
    CodeableConcept,
    Period,
    RelatedArtifact,
    Reference,
)
from .resource import Resource
from .domain_resource import DomainResource


class RiskEvidenceSynthesisSampleSize(BackboneElement):
    """
    A description of the size of the sample involved in the synthesis.
    """

    description: Optional[fhir.string] = Field(
        description="Description of sample size",
        default=None,
    )
    numberOfStudies: Optional[fhir.integer] = Field(
        description="How many studies?",
        default=None,
    )
    numberOfParticipants: Optional[fhir.integer] = Field(
        description="How many participants?",
        default=None,
    )


class RiskEvidenceSynthesisRiskEstimatePrecisionEstimate(BackboneElement):
    """
    A description of the precision of the estimate for the effect.
    """

    type: Optional[CodeableConcept] = Field(
        description="Type of precision estimate",
        default=None,
    )
    level: Optional[fhir.decimal] = Field(
        description="Level of confidence interval",
        default=None,
    )
    from_: Optional[fhir.decimal] = Field(
        description="Lower bound",
        default=None,
        alias="from",
    )
    to: Optional[fhir.decimal] = Field(
        description="Upper bound",
        default=None,
    )


class RiskEvidenceSynthesisRiskEstimate(BackboneElement):
    """
    The estimated risk of the outcome.
    """

    description: Optional[fhir.string] = Field(
        description="Description of risk estimate",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Type of risk estimate",
        default=None,
    )
    value: Optional[fhir.decimal] = Field(
        description="Point estimate",
        default=None,
    )
    unitOfMeasure: Optional[CodeableConcept] = Field(
        description="What unit is the outcome described in?",
        default=None,
    )
    denominatorCount: Optional[fhir.integer] = Field(
        description="Sample size for group measured",
        default=None,
    )
    numeratorCount: Optional[fhir.integer] = Field(
        description="Number with the outcome",
        default=None,
    )
    precisionEstimate: Optional[
        ListType[RiskEvidenceSynthesisRiskEstimatePrecisionEstimate]
    ] = Field(
        description="How precise the estimate is",
        default=None,
    )


class RiskEvidenceSynthesisCertaintyCertaintySubcomponent(BackboneElement):
    """
    A description of a component of the overall certainty.
    """

    type: Optional[CodeableConcept] = Field(
        description="Type of subcomponent of certainty rating",
        default=None,
    )
    rating: Optional[ListType[CodeableConcept]] = Field(
        description="Subcomponent certainty rating",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Used for footnotes or explanatory notes",
        default=None,
    )


class RiskEvidenceSynthesisCertainty(BackboneElement):
    """
    A description of the certainty of the risk estimate.
    """

    rating: Optional[ListType[CodeableConcept]] = Field(
        description="Certainty rating",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Used for footnotes or explanatory notes",
        default=None,
    )
    certaintySubcomponent: Optional[
        ListType[RiskEvidenceSynthesisCertaintyCertaintySubcomponent]
    ] = Field(
        description="A component that contributes to the overall certainty",
        default=None,
    )


class RiskEvidenceSynthesis(DomainResource):
    """
    The RiskEvidenceSynthesis resource describes the likelihood of an outcome in a population plus exposure state where the risk estimate is derived from a combination of research studies.
    """

    _abstract = False
    _type = "RiskEvidenceSynthesis"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/RiskEvidenceSynthesis"

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
        description="canonical identifier for this risk evidence synthesis, represented as a URI (globally unique)",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Additional identifier for the risk evidence synthesis",
        default=None,
    )
    version: Optional[fhir.string] = Field(
        description="Business version of the risk evidence synthesis",
        default=None,
    )
    name: Optional[fhir.string] = Field(
        description="Name for this risk evidence synthesis (computer friendly)",
        default=None,
    )
    title: Optional[fhir.string] = Field(
        description="Name for this risk evidence synthesis (human friendly)",
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
        description="Natural language description of the risk evidence synthesis",
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
        description="Intended jurisdiction for risk evidence synthesis (if applicable)",
        default=None,
    )
    copyright: Optional[fhir.markdown] = Field(
        description="Use and/or publishing restrictions",
        default=None,
    )
    approvalDate: Optional[fhir.date_] = Field(
        description="When the risk evidence synthesis was approved by publisher",
        default=None,
    )
    lastReviewDate: Optional[fhir.date_] = Field(
        description="When the risk evidence synthesis was last reviewed",
        default=None,
    )
    effectivePeriod: Optional[Period] = Field(
        description="When the risk evidence synthesis is expected to be used",
        default=None,
    )
    topic: Optional[ListType[CodeableConcept]] = Field(
        description="The category of the EffectEvidenceSynthesis, such as Education, Treatment, Assessment, etc.",
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
    synthesisType: Optional[CodeableConcept] = Field(
        description="Type of synthesis",
        default=None,
    )
    studyType: Optional[CodeableConcept] = Field(
        description="Type of study",
        default=None,
    )
    population: Reference = Field(
        description="What population?",
    )
    exposure: Optional[Reference] = Field(
        description="What exposure?",
        default=None,
    )
    outcome: Reference = Field(
        description="What outcome?",
    )
    sampleSize: Optional[RiskEvidenceSynthesisSampleSize] = Field(
        description="What sample size was involved?",
        default=None,
    )
    riskEstimate: Optional[RiskEvidenceSynthesisRiskEstimate] = Field(
        description="What was the estimated risk",
        default=None,
    )
    certainty: Optional[ListType[RiskEvidenceSynthesisCertainty]] = Field(
        description="How certain is the risk",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_rvs_0_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.matches('[A-Z]([A-Za-z0-9_]){0,254}')",
            human="Name should be usable as an identifier for the module by machine processing applications such as code generation",
            key="rvs-0",
            severity="warning",
        )
