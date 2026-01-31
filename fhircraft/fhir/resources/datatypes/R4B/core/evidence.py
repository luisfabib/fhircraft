import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    Markdown,
    DateTime,
    Date,
    UnsignedInt,
    Decimal,
)

from fhircraft.fhir.resources.datatypes.R4B.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Reference,
    UsageContext,
    ContactDetail,
    RelatedArtifact,
    Annotation,
    BackboneElement,
    CodeableConcept,
    Quantity,
    Range,
)
from .resource import Resource
from .domain_resource import DomainResource


class EvidenceVariableDefinition(BackboneElement):
    """
    Evidence variable such as population, exposure, or outcome.
    """

    description: Optional[Markdown] = Field(
        description="A text description or summary of the variable",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Footnotes and/or explanatory notes",
        default=None,
    )
    variableRole: Optional[CodeableConcept] = Field(
        description="population | subpopulation | exposure | referenceExposure | measuredVariable | confounder",
        default=None,
    )
    observed: Optional[Reference] = Field(
        description="Definition of the actual variable related to the statistic(s)",
        default=None,
    )
    intended: Optional[Reference] = Field(
        description="Definition of the intended variable related to the Evidence",
        default=None,
    )
    directnessMatch: Optional[CodeableConcept] = Field(
        description="low | moderate | high | exact",
        default=None,
    )


class EvidenceStatisticSampleSize(BackboneElement):
    """
    Number of samples in the statistic.
    """

    description: Optional[String] = Field(
        description="Textual description of sample size for statistic",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Footnote or explanatory note about the sample size",
        default=None,
    )
    numberOfStudies: Optional[UnsignedInt] = Field(
        description="Number of contributing studies",
        default=None,
    )
    numberOfStudies_ext: Optional[Element] = Field(
        description="Placeholder element for numberOfStudies extensions",
        default=None,
        alias="_numberOfStudies",
    )
    numberOfParticipants: Optional[UnsignedInt] = Field(
        description="Cumulative number of participants",
        default=None,
    )
    numberOfParticipants_ext: Optional[Element] = Field(
        description="Placeholder element for numberOfParticipants extensions",
        default=None,
        alias="_numberOfParticipants",
    )
    knownDataCount: Optional[UnsignedInt] = Field(
        description="Number of participants with known results for measured variables",
        default=None,
    )
    knownDataCount_ext: Optional[Element] = Field(
        description="Placeholder element for knownDataCount extensions",
        default=None,
        alias="_knownDataCount",
    )


class EvidenceStatisticAttributeEstimate(BackboneElement):
    """
    A statistical attribute of the statistic such as a measure of heterogeneity.
    """

    description: Optional[String] = Field(
        description="Textual description of the attribute estimate",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Footnote or explanatory note about the estimate",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="The type of attribute estimate, eg confidence interval or p value",
        default=None,
    )
    quantity: Optional[Quantity] = Field(
        description="The singular quantity of the attribute estimate, for attribute estimates represented as single values; also used to report unit of measure",
        default=None,
    )
    level: Optional[Decimal] = Field(
        description="Level of confidence interval, eg 0.95 for 95% confidence interval",
        default=None,
    )
    level_ext: Optional[Element] = Field(
        description="Placeholder element for level extensions",
        default=None,
        alias="_level",
    )
    range: Optional[Range] = Field(
        description="Lower and upper bound values of the attribute estimate",
        default=None,
    )
    attributeEstimate: Optional[ListType["EvidenceStatisticAttributeEstimate"]] = Field(
        description="A nested attribute estimate; which is the attribute estimate of an attribute estimate",
        default=None,
    )


class EvidenceStatisticModelCharacteristicVariable(BackboneElement):
    """
    A variable adjusted for in the adjusted analysis.
    """

    variableDefinition: Optional[Reference] = Field(
        description="Description of the variable",
        default=None,
    )
    handling: Optional[Code] = Field(
        description="continuous | dichotomous | ordinal | polychotomous",
        default=None,
    )
    handling_ext: Optional[Element] = Field(
        description="Placeholder element for handling extensions",
        default=None,
        alias="_handling",
    )
    valueCategory: Optional[ListType[CodeableConcept]] = Field(
        description="Description for grouping of ordinal or polychotomous variables",
        default=None,
    )
    valueQuantity: Optional[ListType[Quantity]] = Field(
        description="Discrete value for grouping of ordinal or polychotomous variables",
        default=None,
    )
    valueRange: Optional[ListType[Range]] = Field(
        description="Range of values for grouping of ordinal or polychotomous variables",
        default=None,
    )


class EvidenceStatisticModelCharacteristicAttributeEstimate(BackboneElement):
    """
    An attribute of the statistic used as a model characteristic.
    """

    description: Optional[String] = Field(
        description="Textual description of the attribute estimate",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Footnote or explanatory note about the estimate",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="The type of attribute estimate, eg confidence interval or p value",
        default=None,
    )
    quantity: Optional[Quantity] = Field(
        description="The singular quantity of the attribute estimate, for attribute estimates represented as single values; also used to report unit of measure",
        default=None,
    )
    level: Optional[Decimal] = Field(
        description="Level of confidence interval, eg 0.95 for 95% confidence interval",
        default=None,
    )
    level_ext: Optional[Element] = Field(
        description="Placeholder element for level extensions",
        default=None,
        alias="_level",
    )
    range: Optional[Range] = Field(
        description="Lower and upper bound values of the attribute estimate",
        default=None,
    )
    attributeEstimate: Optional[ListType[EvidenceStatisticAttributeEstimate]] = Field(
        description="A nested attribute estimate; which is the attribute estimate of an attribute estimate",
        default=None,
    )


class EvidenceStatisticModelCharacteristic(BackboneElement):
    """
    A component of the method to generate the statistic.
    """

    code: Optional[CodeableConcept] = Field(
        description="Model specification",
        default=None,
    )
    value: Optional[Quantity] = Field(
        description="Numerical value to complete model specification",
        default=None,
    )
    variable: Optional[ListType[EvidenceStatisticModelCharacteristicVariable]] = Field(
        description="A variable adjusted for in the adjusted analysis",
        default=None,
    )
    attributeEstimate: Optional[
        ListType[EvidenceStatisticModelCharacteristicAttributeEstimate]
    ] = Field(
        description="An attribute of the statistic used as a model characteristic",
        default=None,
    )


class EvidenceStatistic(BackboneElement):
    """
    Values and parameters for a single statistic.
    """

    description: Optional[String] = Field(
        description="Description of content",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Footnotes and/or explanatory notes",
        default=None,
    )
    statisticType: Optional[CodeableConcept] = Field(
        description="Type of statistic, eg relative risk",
        default=None,
    )
    category: Optional[CodeableConcept] = Field(
        description="Associated category for categorical variable",
        default=None,
    )
    quantity: Optional[Quantity] = Field(
        description="Statistic value",
        default=None,
    )
    numberOfEvents: Optional[UnsignedInt] = Field(
        description="The number of events associated with the statistic",
        default=None,
    )
    numberOfEvents_ext: Optional[Element] = Field(
        description="Placeholder element for numberOfEvents extensions",
        default=None,
        alias="_numberOfEvents",
    )
    numberAffected: Optional[UnsignedInt] = Field(
        description="The number of participants affected",
        default=None,
    )
    numberAffected_ext: Optional[Element] = Field(
        description="Placeholder element for numberAffected extensions",
        default=None,
        alias="_numberAffected",
    )
    sampleSize: Optional[EvidenceStatisticSampleSize] = Field(
        description="Number of samples in the statistic",
        default=None,
    )
    attributeEstimate: Optional[ListType[EvidenceStatisticAttributeEstimate]] = Field(
        description="An attribute of the Statistic",
        default=None,
    )
    modelCharacteristic: Optional[ListType[EvidenceStatisticModelCharacteristic]] = (
        Field(
            description="An aspect of the statistical model",
            default=None,
        )
    )


class EvidenceCertainty(BackboneElement):
    """
    Assessment of certainty, confidence in the estimates, or quality of the evidence.
    """

    description: Optional[String] = Field(
        description="Textual description of certainty",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Footnotes and/or explanatory notes",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Aspect of certainty being rated",
        default=None,
    )
    rating: Optional[CodeableConcept] = Field(
        description="Assessment or judgement of the aspect",
        default=None,
    )
    rater: Optional[String] = Field(
        description="Individual or group who did the rating",
        default=None,
    )
    rater_ext: Optional[Element] = Field(
        description="Placeholder element for rater extensions",
        default=None,
        alias="_rater",
    )
    subcomponent: Optional[ListType["EvidenceCertainty"]] = Field(
        description="A domain or subdomain of certainty",
        default=None,
    )


class Evidence(DomainResource):
    """
    The Evidence Resource provides a machine-interpretable expression of an evidence concept including the evidence variables (eg population, exposures/interventions, comparators, outcomes, measured variables, confounding variables), the statistics, and the certainty of this evidence.
    """

    _abstract = False
    _type = "Evidence"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Evidence"

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
        description="Canonical identifier for this evidence, represented as a globally unique URI",
        default=None,
    )
    url_ext: Optional[Element] = Field(
        description="Placeholder element for url extensions",
        default=None,
        alias="_url",
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Additional identifier for the summary",
        default=None,
    )
    version: Optional[String] = Field(
        description="Business version of this summary",
        default=None,
    )
    version_ext: Optional[Element] = Field(
        description="Placeholder element for version extensions",
        default=None,
        alias="_version",
    )
    title: Optional[String] = Field(
        description="Name for this summary (human friendly)",
        default=None,
    )
    title_ext: Optional[Element] = Field(
        description="Placeholder element for title extensions",
        default=None,
        alias="_title",
    )
    citeAsReference: Optional[Reference] = Field(
        description="Citation for this evidence",
        default=None,
    )
    citeAsMarkdown: Optional[Markdown] = Field(
        description="Citation for this evidence",
        default=None,
    )
    citeAsMarkdown_ext: Optional[Element] = Field(
        description="Placeholder element for citeAsMarkdown extensions",
        default=None,
        alias="_citeAsMarkdown",
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
    useContext: Optional[ListType[UsageContext]] = Field(
        description="The context that the content is intended to support",
        default=None,
    )
    approvalDate: Optional[Date] = Field(
        description="When the summary was approved by publisher",
        default=None,
    )
    approvalDate_ext: Optional[Element] = Field(
        description="Placeholder element for approvalDate extensions",
        default=None,
        alias="_approvalDate",
    )
    lastReviewDate: Optional[Date] = Field(
        description="When the summary was last reviewed",
        default=None,
    )
    lastReviewDate_ext: Optional[Element] = Field(
        description="Placeholder element for lastReviewDate extensions",
        default=None,
        alias="_lastReviewDate",
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
        description="Link or citation to artifact associated with the summary",
        default=None,
    )
    description: Optional[Markdown] = Field(
        description="Description of the particular summary",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    assertion: Optional[Markdown] = Field(
        description="Declarative description of the Evidence",
        default=None,
    )
    assertion_ext: Optional[Element] = Field(
        description="Placeholder element for assertion extensions",
        default=None,
        alias="_assertion",
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Footnotes and/or explanatory notes",
        default=None,
    )
    variableDefinition: Optional[ListType[EvidenceVariableDefinition]] = Field(
        description="Evidence variable such as population, exposure, or outcome",
        default=None,
    )
    synthesisType: Optional[CodeableConcept] = Field(
        description="The method to combine studies",
        default=None,
    )
    studyType: Optional[CodeableConcept] = Field(
        description="The type of study that produced this evidence",
        default=None,
    )
    statistic: Optional[ListType[EvidenceStatistic]] = Field(
        description="Values and parameters for a single statistic",
        default=None,
    )
    certainty: Optional[ListType[EvidenceCertainty]] = Field(
        description="Certainty or quality of the evidence",
        default=None,
    )

    @property
    def citeAs(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="citeAs",
        )

    @model_validator(mode="after")
    def citeAs_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Reference, Markdown],
            field_name_base="citeAs",
            required=False,
        )

    @model_validator(mode="after")
    def FHIR_cnl_0_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.exists() implies name.matches('[A-Z]([A-Za-z0-9_]){0,254}')",
            human="Name should be usable as an identifier for the module by machine processing applications such as code generation",
            key="cnl-0",
            severity="warning",
        )
