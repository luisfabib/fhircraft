import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)


from ..primitive import *
from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    ContactDetail,
    Annotation,
    UsageContext,
    CodeableConcept,
    BackboneElement,
    Period,
    RelatedArtifact,
    Reference,
)
from .resource import Resource
from .domain_resource import DomainResource

class EffectEvidenceSynthesisSampleSize(BackboneElement):
    """
    A description of the size of the sample involved in the synthesis.
    """

    description: Optional[String] = Field(
        description="Description of sample size",
        default=None,
    )
    numberOfStudies: Optional[Integer] = Field(
        description="How many studies?",
        default=None,
    )
    numberOfParticipants: Optional[Integer] = Field(
        description="How many participants?",
        default=None,
    )

class EffectEvidenceSynthesisResultsByExposure(BackboneElement):
    """
    A description of the results for each exposure considered in the effect estimate.
    """

    description: Optional[String] = Field(
        description="Description of results by exposure",
        default=None,
    )
    exposureState: Optional[Code] = Field(
        description="exposure | exposure-alternative",
        default=None,
    )
    variantState: Optional[CodeableConcept] = Field(
        description="Variant exposure states",
        default=None,
    )
    riskEvidenceSynthesis: Optional[Reference] = Field(
        description="Risk evidence synthesis",
        default=None,
    )

class EffectEvidenceSynthesisEffectEstimatePrecisionEstimate(BackboneElement):
    """
    A description of the precision of the estimate for the effect.
    """

    type: Optional[CodeableConcept] = Field(
        description="Type of precision estimate",
        default=None,
    )
    level: Optional[Decimal] = Field(
        description="Level of confidence interval",
        default=None,
    )
    from_: Optional[Decimal] = Field(
        description="Lower bound",
        default=None,
        alias="from",
    )
    to: Optional[Decimal] = Field(
        description="Upper bound",
        default=None,
    )

class EffectEvidenceSynthesisEffectEstimate(BackboneElement):
    """
    The estimated effect of the exposure variant.
    """

    description: Optional[String] = Field(
        description="Description of effect estimate",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Type of efffect estimate",
        default=None,
    )
    variantState: Optional[CodeableConcept] = Field(
        description="Variant exposure states",
        default=None,
    )
    value: Optional[Decimal] = Field(
        description="Point estimate",
        default=None,
    )
    unitOfMeasure: Optional[CodeableConcept] = Field(
        description="What unit is the outcome described in?",
        default=None,
    )
    precisionEstimate: Optional[
        ListType[EffectEvidenceSynthesisEffectEstimatePrecisionEstimate]
    ] = Field(
        description="How precise the estimate is",
        default=None,
    )

class EffectEvidenceSynthesisCertaintyCertaintySubcomponent(BackboneElement):
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

class EffectEvidenceSynthesisCertainty(BackboneElement):
    """
    A description of the certainty of the effect estimate.
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
        ListType[EffectEvidenceSynthesisCertaintyCertaintySubcomponent]
    ] = Field(
        description="A component that contributes to the overall certainty",
        default=None,
    )

class EffectEvidenceSynthesis(DomainResource):
    """
    The EffectEvidenceSynthesis resource describes the difference in an outcome between exposures states in a population where the effect estimate is derived from a combination of research studies.
    """

    _abstract = False
    _type = "EffectEvidenceSynthesis"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/EffectEvidenceSynthesis"

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
        description="Canonical identifier for this effect evidence synthesis, represented as a URI (globally unique)",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Additional identifier for the effect evidence synthesis",
        default=None,
    )
    version: Optional[String] = Field(
        description="Business version of the effect evidence synthesis",
        default=None,
    )
    name: Optional[String] = Field(
        description="Name for this effect evidence synthesis (computer friendly)",
        default=None,
    )
    title: Optional[String] = Field(
        description="Name for this effect evidence synthesis (human friendly)",
        default=None,
    )
    status: Optional[Code] = Field(
        description="draft | active | retired | unknown",
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
        description="Natural language description of the effect evidence synthesis",
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
        description="Intended jurisdiction for effect evidence synthesis (if applicable)",
        default=None,
    )
    copyright: Optional[Markdown] = Field(
        description="Use and/or publishing restrictions",
        default=None,
    )
    approvalDate: Optional[Date] = Field(
        description="When the effect evidence synthesis was approved by publisher",
        default=None,
    )
    lastReviewDate: Optional[Date] = Field(
        description="When the effect evidence synthesis was last reviewed",
        default=None,
    )
    effectivePeriod: Optional[Period] = Field(
        description="When the effect evidence synthesis is expected to be used",
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
    population: Optional[Reference] = Field(
        description="What population?",
        default=None,
    )
    exposure: Optional[Reference] = Field(
        description="What exposure?",
        default=None,
    )
    exposureAlternative: Optional[Reference] = Field(
        description="What comparison exposure?",
        default=None,
    )
    outcome: Optional[Reference] = Field(
        description="What outcome?",
        default=None,
    )
    sampleSize: Optional[EffectEvidenceSynthesisSampleSize] = Field(
        description="What sample size was involved?",
        default=None,
    )
    resultsByExposure: Optional[ListType[EffectEvidenceSynthesisResultsByExposure]] = (
        Field(
            description="What was the result per exposure?",
            default=None,
        )
    )
    effectEstimate: Optional[ListType[EffectEvidenceSynthesisEffectEstimate]] = Field(
        description="What was the estimated effect",
        default=None,
    )
    certainty: Optional[ListType[EffectEvidenceSynthesisCertainty]] = Field(
        description="How certain is the effect",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ees_0_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.matches('[A-Z]([A-Za-z0-9_]){0,254}')",
            human="Name should be usable as an identifier for the module by machine processing applications such as code generation",
            key="ees-0",
            severity="warning",
        )
