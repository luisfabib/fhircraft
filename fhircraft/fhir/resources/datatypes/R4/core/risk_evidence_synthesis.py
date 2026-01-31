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
    Integer,
    Decimal,
)

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

    description: Optional[String] = Field(
        description="Description of sample size",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    numberOfStudies: Optional[Integer] = Field(
        description="How many studies?",
        default=None,
    )
    numberOfStudies_ext: Optional[Element] = Field(
        description="Placeholder element for numberOfStudies extensions",
        default=None,
        alias="_numberOfStudies",
    )
    numberOfParticipants: Optional[Integer] = Field(
        description="How many participants?",
        default=None,
    )
    numberOfParticipants_ext: Optional[Element] = Field(
        description="Placeholder element for numberOfParticipants extensions",
        default=None,
        alias="_numberOfParticipants",
    )


class RiskEvidenceSynthesisRiskEstimatePrecisionEstimate(BackboneElement):
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
    level_ext: Optional[Element] = Field(
        description="Placeholder element for level extensions",
        default=None,
        alias="_level",
    )
    from_: Optional[Decimal] = Field(
        description="Lower bound",
        default=None,
        alias="from",
    )
    from_ext: Optional[Element] = Field(
        description="Placeholder element for from extensions",
        default=None,
        alias="_from",
    )
    to: Optional[Decimal] = Field(
        description="Upper bound",
        default=None,
    )
    to_ext: Optional[Element] = Field(
        description="Placeholder element for to extensions",
        default=None,
        alias="_to",
    )


class RiskEvidenceSynthesisRiskEstimate(BackboneElement):
    """
    The estimated risk of the outcome.
    """

    description: Optional[String] = Field(
        description="Description of risk estimate",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    type: Optional[CodeableConcept] = Field(
        description="Type of risk estimate",
        default=None,
    )
    value: Optional[Decimal] = Field(
        description="Point estimate",
        default=None,
    )
    value_ext: Optional[Element] = Field(
        description="Placeholder element for value extensions",
        default=None,
        alias="_value",
    )
    unitOfMeasure: Optional[CodeableConcept] = Field(
        description="What unit is the outcome described in?",
        default=None,
    )
    denominatorCount: Optional[Integer] = Field(
        description="Sample size for group measured",
        default=None,
    )
    denominatorCount_ext: Optional[Element] = Field(
        description="Placeholder element for denominatorCount extensions",
        default=None,
        alias="_denominatorCount",
    )
    numeratorCount: Optional[Integer] = Field(
        description="Number with the outcome",
        default=None,
    )
    numeratorCount_ext: Optional[Element] = Field(
        description="Placeholder element for numeratorCount extensions",
        default=None,
        alias="_numeratorCount",
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
    url: Optional[Uri] = Field(
        description="Canonical identifier for this risk evidence synthesis, represented as a URI (globally unique)",
        default=None,
    )
    url_ext: Optional[Element] = Field(
        description="Placeholder element for url extensions",
        default=None,
        alias="_url",
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Additional identifier for the risk evidence synthesis",
        default=None,
    )
    version: Optional[String] = Field(
        description="Business version of the risk evidence synthesis",
        default=None,
    )
    version_ext: Optional[Element] = Field(
        description="Placeholder element for version extensions",
        default=None,
        alias="_version",
    )
    name: Optional[String] = Field(
        description="Name for this risk evidence synthesis (computer friendly)",
        default=None,
    )
    name_ext: Optional[Element] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    title: Optional[String] = Field(
        description="Name for this risk evidence synthesis (human friendly)",
        default=None,
    )
    title_ext: Optional[Element] = Field(
        description="Placeholder element for title extensions",
        default=None,
        alias="_title",
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
        description="Natural language description of the risk evidence synthesis",
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
        description="Intended jurisdiction for risk evidence synthesis (if applicable)",
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
        description="When the risk evidence synthesis was approved by publisher",
        default=None,
    )
    approvalDate_ext: Optional[Element] = Field(
        description="Placeholder element for approvalDate extensions",
        default=None,
        alias="_approvalDate",
    )
    lastReviewDate: Optional[Date] = Field(
        description="When the risk evidence synthesis was last reviewed",
        default=None,
    )
    lastReviewDate_ext: Optional[Element] = Field(
        description="Placeholder element for lastReviewDate extensions",
        default=None,
        alias="_lastReviewDate",
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
    population: Optional[Reference] = Field(
        description="What population?",
        default=None,
    )
    exposure: Optional[Reference] = Field(
        description="What exposure?",
        default=None,
    )
    outcome: Optional[Reference] = Field(
        description="What outcome?",
        default=None,
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
    def FHIR_rvs_0_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.matches('[A-Z]([A-Za-z0-9_]){0,254}')",
            human="Name should be usable as an identifier for the module by machine processing applications such as code generation",
            key="rvs-0",
            severity="warning",
        )
