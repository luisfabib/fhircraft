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
    Reference,
    ContactDetail,
    UsageContext,
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

    description: Optional[fhir.markdown] = Field(
        description="A text description or summary of the variable",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Footnotes and/or explanatory notes",
        default=None,
    )
    variableRole: CodeableConcept = Field(
        description="population | subpopulation | exposure | referenceExposure | measuredVariable | confounder",
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

    description: Optional[fhir.markdown] = Field(
        description="Textual description of sample size for statistic",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Footnote or explanatory note about the sample size",
        default=None,
    )
    numberOfStudies: Optional[fhir.unsignedInt] = Field(
        description="Number of contributing studies",
        default=None,
    )
    numberOfParticipants: Optional[fhir.unsignedInt] = Field(
        description="Cumulative number of participants",
        default=None,
    )
    knownDataCount: Optional[fhir.unsignedInt] = Field(
        description="Number of participants with known results for measured variables",
        default=None,
    )


class EvidenceStatisticAttributeEstimate(BackboneElement):
    """
    A statistical attribute of the statistic such as a measure of heterogeneity.
    """

    description: Optional[fhir.markdown] = Field(
        description="Textual description of the attribute estimate",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Footnote or explanatory note about the estimate",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="The type of attribute estimate, e.g., confidence interval or p value",
        default=None,
    )
    quantity: Optional[Quantity] = Field(
        description="The singular quantity of the attribute estimate, for attribute estimates represented as single values; also used to report unit of measure",
        default=None,
    )
    level: Optional[fhir.decimal] = Field(
        description="Level of confidence interval, e.g., 0.95 for 95% confidence interval",
        default=None,
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

    variableDefinition: Reference = Field(
        description="Description of the variable",
    )
    handling: Optional[fhir.code] = Field(
        description="continuous | dichotomous | ordinal | polychotomous",
        default=None,
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

    description: Optional[fhir.markdown] = Field(
        description="Textual description of the attribute estimate",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Footnote or explanatory note about the estimate",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="The type of attribute estimate, e.g., confidence interval or p value",
        default=None,
    )
    quantity: Optional[Quantity] = Field(
        description="The singular quantity of the attribute estimate, for attribute estimates represented as single values; also used to report unit of measure",
        default=None,
    )
    level: Optional[fhir.decimal] = Field(
        description="Level of confidence interval, e.g., 0.95 for 95% confidence interval",
        default=None,
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

    code: CodeableConcept = Field(
        description="Model specification",
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

    description: Optional[fhir.markdown] = Field(
        description="Description of content",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Footnotes and/or explanatory notes",
        default=None,
    )
    statisticType: Optional[CodeableConcept] = Field(
        description="Type of statistic, e.g., relative risk",
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
    numberOfEvents: Optional[fhir.unsignedInt] = Field(
        description="The number of events associated with the statistic",
        default=None,
    )
    numberAffected: Optional[fhir.unsignedInt] = Field(
        description="The number of participants affected",
        default=None,
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

    description: Optional[fhir.markdown] = Field(
        description="Textual description of certainty",
        default=None,
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
    rater: Optional[fhir.string] = Field(
        description="Individual or group who did the rating",
        default=None,
    )
    subcomponent: Optional[ListType["EvidenceCertainty"]] = Field(
        description="A domain or subdomain of certainty",
        default=None,
    )


class Evidence(DomainResource):
    """
    The Evidence Resource provides a machine-interpretable expression of an evidence concept including the evidence variables (e.g., population, exposures/interventions, comparators, outcomes, measured variables, confounding variables), the statistics, and the certainty of this evidence.
    """

    _abstract = False
    _type = "Evidence"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Evidence"

    url: Optional[fhir.uri] = Field(
        description="canonical identifier for this evidence, represented as a globally unique URI",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Additional identifier for the summary",
        default=None,
    )
    version: Optional[fhir.string] = Field(
        description="Business version of this summary",
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
        description="Name for this summary (machine friendly)",
        default=None,
    )
    title: Optional[fhir.string] = Field(
        description="Name for this summary (human friendly)",
        default=None,
    )
    citeAsReference: Optional[Reference] = Field(
        description="Citation for this evidence",
        default=None,
    )
    citeAsMarkdown: Optional[fhir.markdown] = Field(
        description="Citation for this evidence",
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
    approvalDate: Optional[fhir.date_] = Field(
        description="When the summary was approved by publisher",
        default=None,
    )
    lastReviewDate: Optional[fhir.date_] = Field(
        description="When the summary was last reviewed by the publisher",
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
    useContext: Optional[ListType[UsageContext]] = Field(
        description="The context that the content is intended to support",
        default=None,
    )
    purpose: Optional[fhir.markdown] = Field(
        description="Why this Evidence is defined",
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
    relatedArtifact: Optional[ListType[RelatedArtifact]] = Field(
        description="Link or citation to artifact associated with the summary",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
        description="Description of the particular summary",
        default=None,
    )
    assertion: Optional[fhir.markdown] = Field(
        description="Declarative description of the Evidence",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Footnotes and/or explanatory notes",
        default=None,
    )
    variableDefinition: ListType[EvidenceVariableDefinition] = Field(
        description="Evidence variable such as population, exposure, or outcome",
        min_length=1,
    )
    synthesisType: Optional[CodeableConcept] = Field(
        description="The method to combine studies",
        default=None,
    )
    studyDesign: Optional[ListType[CodeableConcept]] = Field(
        description="The design of the study that produced this evidence",
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
    def versionAlgorithm(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="versionAlgorithm",
        )

    @property
    def citeAs(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="citeAs",
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
    def citeAs_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Reference, fhir.Markdown],
            field_name_base="citeAs",
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
