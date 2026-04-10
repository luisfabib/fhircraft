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
    CodeableConcept,
    Reference,
    ContactDetail,
    UsageContext,
    Period,
    RelatedArtifact,
    BackboneElement,
    Expression,
)
from .resource import Resource
from .domain_resource import DomainResource


class MeasureGroupPopulation(BackboneElement):
    """
    A population criteria for the measure.
    """

    code: Optional[CodeableConcept] = Field(
        description="initial-population | numerator | numerator-exclusion | denominator | denominator-exclusion | denominator-exception | measure-population | measure-population-exclusion | measure-observation",
        default=None,
    )
    description: Optional[fhir.string] = Field(
        description="The human readable description of this population criteria",
        default=None,
    )
    criteria: Optional[Expression] = Field(
        description="The criteria that defines this population",
        default=None,
    )


class MeasureGroupStratifierComponent(BackboneElement):
    """
    A component of the stratifier criteria for the measure report, specified as either the name of a valid CQL expression defined within a referenced library or a valid FHIR Resource Path.
    """

    code: Optional[CodeableConcept] = Field(
        description="Meaning of the stratifier component",
        default=None,
    )
    description: Optional[fhir.string] = Field(
        description="The human readable description of this stratifier component",
        default=None,
    )
    criteria: Optional[Expression] = Field(
        description="Component of how the measure should be stratified",
        default=None,
    )


class MeasureGroupStratifier(BackboneElement):
    """
    The stratifier criteria for the measure report, specified as either the name of a valid CQL expression defined within a referenced library or a valid FHIR Resource Path.
    """

    code: Optional[CodeableConcept] = Field(
        description="Meaning of the stratifier",
        default=None,
    )
    description: Optional[fhir.string] = Field(
        description="The human readable description of this stratifier",
        default=None,
    )
    criteria: Optional[Expression] = Field(
        description="How the measure should be stratified",
        default=None,
    )
    component: Optional[ListType[MeasureGroupStratifierComponent]] = Field(
        description="Stratifier criteria component for the measure",
        default=None,
    )


class MeasureGroup(BackboneElement):
    """
    A group of population criteria for the measure.
    """

    code: Optional[CodeableConcept] = Field(
        description="Meaning of the group",
        default=None,
    )
    description: Optional[fhir.string] = Field(
        description="Summary description",
        default=None,
    )
    population: Optional[ListType[MeasureGroupPopulation]] = Field(
        description="Population criteria",
        default=None,
    )
    stratifier: Optional[ListType[MeasureGroupStratifier]] = Field(
        description="Stratifier criteria for the measure",
        default=None,
    )


class MeasureSupplementalData(BackboneElement):
    """
    The supplemental data criteria for the measure report, specified as either the name of a valid CQL expression within a referenced library, or a valid FHIR Resource Path.
    """

    code: Optional[CodeableConcept] = Field(
        description="Meaning of the supplemental data",
        default=None,
    )
    usage: Optional[ListType[CodeableConcept]] = Field(
        description="supplemental-data | risk-adjustment-factor",
        default=None,
    )
    description: Optional[fhir.string] = Field(
        description="The human readable description of this supplemental data",
        default=None,
    )
    criteria: Optional[Expression] = Field(
        description="Expression describing additional data to be reported",
        default=None,
    )


class Measure(DomainResource):
    """
    The Measure resource provides the definition of a quality measure.
    """

    _abstract = False
    _type = "Measure"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Measure"

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
        description="canonical identifier for this measure, represented as a URI (globally unique)",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Additional identifier for the measure",
        default=None,
    )
    version: Optional[fhir.string] = Field(
        description="Business version of the measure",
        default=None,
    )
    name: Optional[fhir.string] = Field(
        description="Name for this measure (computer friendly)",
        default=None,
    )
    title: Optional[fhir.string] = Field(
        description="Name for this measure (human friendly)",
        default=None,
    )
    subtitle: Optional[fhir.string] = Field(
        description="Subordinate title of the measure",
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
    subjectCodeableConcept: Optional[CodeableConcept] = Field(
        description="E.g. Patient, Practitioner, RelatedPerson, Organization, Location, Device",
        default=None,
    )
    subjectReference: Optional[Reference] = Field(
        description="E.g. Patient, Practitioner, RelatedPerson, Organization, Location, Device",
        default=None,
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
        description="Natural language description of the measure",
        default=None,
    )
    useContext: Optional[ListType[UsageContext]] = Field(
        description="The context that the content is intended to support",
        default=None,
    )
    jurisdiction: Optional[ListType[CodeableConcept]] = Field(
        description="Intended jurisdiction for measure (if applicable)",
        default=None,
    )
    purpose: Optional[fhir.markdown] = Field(
        description="Why this measure is defined",
        default=None,
    )
    usage: Optional[fhir.string] = Field(
        description="Describes the clinical usage of the measure",
        default=None,
    )
    copyright: Optional[fhir.markdown] = Field(
        description="Use and/or publishing restrictions",
        default=None,
    )
    approvalDate: Optional[fhir.date_] = Field(
        description="When the measure was approved by publisher",
        default=None,
    )
    lastReviewDate: Optional[fhir.date_] = Field(
        description="When the measure was last reviewed",
        default=None,
    )
    effectivePeriod: Optional[Period] = Field(
        description="When the measure is expected to be used",
        default=None,
    )
    topic: Optional[ListType[CodeableConcept]] = Field(
        description="The category of the measure, such as Education, Treatment, Assessment, etc.",
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
    library: Optional[ListType[fhir.canonical]] = Field(
        description="Logic used by the measure",
        default=None,
    )
    disclaimer: Optional[fhir.markdown] = Field(
        description="Disclaimer for use of the measure or its referenced content",
        default=None,
    )
    scoring: Optional[CodeableConcept] = Field(
        description="proportion | ratio | continuous-variable | cohort",
        default=None,
    )
    compositeScoring: Optional[CodeableConcept] = Field(
        description="opportunity | all-or-nothing | linear | weighted",
        default=None,
    )
    type: Optional[ListType[CodeableConcept]] = Field(
        description="process | outcome | structure | patient-reported-outcome | composite",
        default=None,
    )
    riskAdjustment: Optional[fhir.string] = Field(
        description="How risk adjustment is applied for this measure",
        default=None,
    )
    rateAggregation: Optional[fhir.string] = Field(
        description="How is rate aggregation performed for this measure",
        default=None,
    )
    rationale: Optional[fhir.markdown] = Field(
        description="Detailed description of why the measure exists",
        default=None,
    )
    clinicalRecommendationStatement: Optional[fhir.markdown] = Field(
        description="Summary of clinical guidelines",
        default=None,
    )
    improvementNotation: Optional[CodeableConcept] = Field(
        description="increase | decrease",
        default=None,
    )
    definition: Optional[ListType[fhir.markdown]] = Field(
        description="Defined terms used in the measure documentation",
        default=None,
    )
    guidance: Optional[fhir.markdown] = Field(
        description="Additional guidance for implementers",
        default=None,
    )
    group: Optional[ListType[MeasureGroup]] = Field(
        description="Population criteria group",
        default=None,
    )
    supplementalData: Optional[ListType[MeasureSupplementalData]] = Field(
        description="What other data should be reported with the measure",
        default=None,
    )

    @property
    def subject(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="subject",
        )

    @model_validator(mode="after")
    def subject_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[CodeableConcept, Reference],
            field_name_base="subject",
            required=False,
        )

    @model_validator(mode="after")
    def FHIR_mea_0_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.matches('[A-Z]([A-Za-z0-9_]){0,254}')",
            human="Name should be usable as an identifier for the module by machine processing applications such as code generation",
            key="mea-0",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_mea_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="group.stratifier.all((code | description | criteria).exists() xor component.exists())",
            human="Stratifier SHALL be either a single criteria or a set of criteria components",
            key="mea-1",
            severity="error",
        )
