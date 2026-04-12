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


class MeasureTerm(BackboneElement):
    """
    Provides a description of an individual term used within the measure.
    """

    code: Optional[CodeableConcept] = Field(
        description="What term?",
        default=None,
    )
    definition: Optional[fhir.markdown] = Field(
        description="Meaning of the term",
        default=None,
    )


class MeasureGroupPopulation(BackboneElement):
    """
    A population criteria for the measure.
    """

    linkId: Optional[fhir.string] = Field(
        description="Unique id for population in measure",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="initial-population | numerator | numerator-exclusion | denominator | denominator-exclusion | denominator-exception | measure-population | measure-population-exclusion | measure-observation",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
        description="The human readable description of this population criteria",
        default=None,
    )
    criteria: Optional[Expression] = Field(
        description="The criteria that defines this population",
        default=None,
    )
    groupDefinition: Optional[Reference] = Field(
        description="A group resource that defines this population",
        default=None,
    )
    inputPopulationId: Optional[fhir.string] = Field(
        description="Which population",
        default=None,
    )
    aggregateMethod: Optional[CodeableConcept] = Field(
        description="Aggregation method for a measure score (e.g. sum, average, median, minimum, maximum, count)",
        default=None,
    )


class MeasureGroupStratifierComponent(BackboneElement):
    """
    A component of the stratifier criteria for the measure report, specified as either the name of a valid CQL expression defined within a referenced library or a valid FHIR Resource Path.
    """

    linkId: Optional[fhir.string] = Field(
        description="Unique id for stratifier component in measure",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="Meaning of the stratifier component",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
        description="The human readable description of this stratifier component",
        default=None,
    )
    criteria: Optional[Expression] = Field(
        description="Component of how the measure should be stratified",
        default=None,
    )
    groupDefinition: Optional[Reference] = Field(
        description="A group resource that defines this population",
        default=None,
    )


class MeasureGroupStratifier(BackboneElement):
    """
    The stratifier criteria for the measure report, specified as either the name of a valid CQL expression defined within a referenced library or a valid FHIR Resource Path.
    """

    linkId: Optional[fhir.string] = Field(
        description="Unique id for stratifier in measure",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="Meaning of the stratifier",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
        description="The human readable description of this stratifier",
        default=None,
    )
    criteria: Optional[Expression] = Field(
        description="How the measure should be stratified",
        default=None,
    )
    groupDefinition: Optional[Reference] = Field(
        description="A group resource that defines this population",
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

    linkId: Optional[fhir.string] = Field(
        description="Unique id for group in measure",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="Meaning of the group",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
        description="Summary description",
        default=None,
    )
    type: Optional[ListType[CodeableConcept]] = Field(
        description="process | outcome | structure | patient-reported-outcome | composite",
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
    basis: Optional[fhir.code] = Field(
        description="Population basis",
        default=None,
    )
    scoring: Optional[CodeableConcept] = Field(
        description="proportion | ratio | continuous-variable | cohort",
        default=None,
    )
    scoringUnit: Optional[CodeableConcept] = Field(
        description="What units?",
        default=None,
    )
    rateAggregation: Optional[fhir.markdown] = Field(
        description="How is rate aggregation performed for this measure",
        default=None,
    )
    improvementNotation: Optional[CodeableConcept] = Field(
        description="increase | decrease",
        default=None,
    )
    library: Optional[ListType[fhir.canonical]] = Field(
        description="Logic used by the measure group",
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


class MeasureSupplementalData(BackboneElement):
    """
    The supplemental data criteria for the measure report, specified as either the name of a valid CQL expression within a referenced library, or a valid FHIR Resource Path.
    """

    linkId: Optional[fhir.string] = Field(
        description="Unique id for supplementalData in measure",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="Meaning of the supplemental data",
        default=None,
    )
    usage: Optional[ListType[CodeableConcept]] = Field(
        description="supplemental-data | risk-adjustment-factor",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
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
    versionAlgorithmString: Optional[fhir.string] = Field(
        description="How to compare versions",
        default=None,
    )
    versionAlgorithmCoding: Optional[Coding] = Field(
        description="How to compare versions",
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
    basis: Optional[fhir.code] = Field(
        description="Population basis",
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
    usage: Optional[fhir.markdown] = Field(
        description="Describes the clinical usage of the measure",
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
    approvalDate: Optional[fhir.date_] = Field(
        description="When the measure was approved by publisher",
        default=None,
    )
    lastReviewDate: Optional[fhir.date_] = Field(
        description="When the measure was last reviewed by the publisher",
        default=None,
    )
    effectivePeriod: Optional[Period] = Field(
        description="When the measure is expected to be used",
        default=None,
    )
    topic: Optional[ListType[CodeableConcept]] = Field(
        description="The category of the measure, such as Education, Treatment, Assessment, etc",
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
        description="Additional documentation, citations, etc",
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
    scoringUnit: Optional[CodeableConcept] = Field(
        description="What units?",
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
    riskAdjustment: Optional[fhir.markdown] = Field(
        description="How risk adjustment is applied for this measure",
        default=None,
    )
    rateAggregation: Optional[fhir.markdown] = Field(
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
    term: Optional[ListType[MeasureTerm]] = Field(
        description="Defined terms used in the measure documentation",
        default=None,
    )
    guidance: Optional[fhir.markdown] = Field(
        description="Additional guidance for implementers (deprecated)",
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
    def versionAlgorithm(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="versionAlgorithm",
        )

    @property
    def subject(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="subject",
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
    def subject_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[CodeableConcept, Reference],
            field_name_base="subject",
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

    @model_validator(mode="after")
    def FHIR_mea_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="group.stratifier.all((code | description | criteria).exists() xor component.exists())",
            human="Stratifier SHALL be either a single criteria or a set of criteria components",
            key="mea-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_mea_2_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("group.linkId",),
            expression="$this.length() <= 255",
            human="Link ids should be 255 characters or less",
            key="mea-2",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_mea_3_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("group.population.linkId",),
            expression="$this.length() <= 255",
            human="Link ids should be 255 characters or less",
            key="mea-3",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_mea_4_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("group.stratifier.linkId",),
            expression="$this.length() <= 255",
            human="Link ids should be 255 characters or less",
            key="mea-4",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_mea_5_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("group.stratifier.component.linkId",),
            expression="$this.length() <= 255",
            human="Link ids should be 255 characters or less",
            key="mea-5",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_mea_6_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("supplementalData.linkId",),
            expression="$this.length() <= 255",
            human="Link ids should be 255 characters or less",
            key="mea-6",
            severity="warning",
        )
