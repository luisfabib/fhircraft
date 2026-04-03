from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators


from ..primitive import *
from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Reference,
    Period,
    CodeableConcept,
    BackboneElement,
    Quantity,
    Range,
    Duration,
)
from .resource import Resource
from .domain_resource import DomainResource

class MeasureReportGroupPopulation(BackboneElement):
    """
    The populations that make up the population group, one for each type of population appropriate for the measure.
    """

    linkId: Optional[String] = Field(
        description="Pointer to specific population from Measure",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="initial-population | numerator | numerator-exclusion | denominator | denominator-exclusion | denominator-exception | measure-population | measure-population-exclusion | measure-observation",
        default=None,
    )
    count: Optional[Integer] = Field(
        description="Size of the population",
        default=None,
    )
    subjectResults: Optional[Reference] = Field(
        description="For subject-list reports, the subject results in this population",
        default=None,
    )
    subjectReport: Optional[ListType[Reference]] = Field(
        description="For subject-list reports, a subject result in this population",
        default=None,
    )
    subjects: Optional[Reference] = Field(
        description="What individual(s) in the population",
        default=None,
    )

class MeasureReportGroupStratifierStratumComponent(BackboneElement):
    """
    A stratifier component value.
    """

    linkId: Optional[String] = Field(
        description="Pointer to specific stratifier component from Measure",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="What stratifier component of the group",
        default=None,
    )
    valueCodeableConcept: Optional[CodeableConcept] = Field(
        description="The stratum component value, e.g. male",
        default=None,
    )
    valueBoolean: Optional[Boolean] = Field(
        description="The stratum component value, e.g. male",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="The stratum component value, e.g. male",
        default=None,
    )
    valueRange: Optional[Range] = Field(
        description="The stratum component value, e.g. male",
        default=None,
    )
    valueReference: Optional[Reference] = Field(
        description="The stratum component value, e.g. male",
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
            field_types=[CodeableConcept, Boolean, Quantity, Range, Reference],
            field_name_base="value",
            required=True,
        )

class MeasureReportGroupStratifierStratumPopulation(BackboneElement):
    """
    The populations that make up the stratum, one for each type of population appropriate to the measure.
    """

    linkId: Optional[String] = Field(
        description="Pointer to specific population from Measure",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="initial-population | numerator | numerator-exclusion | denominator | denominator-exclusion | denominator-exception | measure-population | measure-population-exclusion | measure-observation",
        default=None,
    )
    count: Optional[Integer] = Field(
        description="Size of the population",
        default=None,
    )
    subjectResults: Optional[Reference] = Field(
        description="For subject-list reports, the subject results in this population",
        default=None,
    )
    subjectReport: Optional[ListType[Reference]] = Field(
        description="For subject-list reports, a subject result in this population",
        default=None,
    )
    subjects: Optional[Reference] = Field(
        description="What individual(s) in the population",
        default=None,
    )

class MeasureReportGroupStratifierStratum(BackboneElement):
    """
    This element contains the results for a single stratum within the stratifier. For example, when stratifying on administrative gender, there will be four strata, one for each possible gender value.
    """

    valueCodeableConcept: Optional[CodeableConcept] = Field(
        description="The stratum value, e.g. male",
        default=None,
    )
    valueBoolean: Optional[Boolean] = Field(
        description="The stratum value, e.g. male",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="The stratum value, e.g. male",
        default=None,
    )
    valueRange: Optional[Range] = Field(
        description="The stratum value, e.g. male",
        default=None,
    )
    valueReference: Optional[Reference] = Field(
        description="The stratum value, e.g. male",
        default=None,
    )
    component: Optional[ListType[MeasureReportGroupStratifierStratumComponent]] = Field(
        description="Stratifier component values",
        default=None,
    )
    population: Optional[ListType[MeasureReportGroupStratifierStratumPopulation]] = (
        Field(
            description="Population results in this stratum",
            default=None,
        )
    )
    measureScoreQuantity: Optional[Quantity] = Field(
        description="What score this stratum achieved",
        default=None,
    )
    measureScoreDateTime: Optional[DateTime] = Field(
        description="What score this stratum achieved",
        default=None,
    )
    measureScoreCodeableConcept: Optional[CodeableConcept] = Field(
        description="What score this stratum achieved",
        default=None,
    )
    measureScorePeriod: Optional[Period] = Field(
        description="What score this stratum achieved",
        default=None,
    )
    measureScoreRange: Optional[Range] = Field(
        description="What score this stratum achieved",
        default=None,
    )
    measureScoreDuration: Optional[Duration] = Field(
        description="What score this stratum achieved",
        default=None,
    )

    @property
    def value(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="value",
        )

    @property
    def measureScore(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="measureScore",
        )

    @model_validator(mode="after")
    def value_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[CodeableConcept, Boolean, Quantity, Range, Reference],
            field_name_base="value",
            required=False,
        )

    @model_validator(mode="after")
    def measureScore_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Quantity, DateTime, CodeableConcept, Period, Range, Duration],
            field_name_base="measureScore",
            required=False,
        )

class MeasureReportGroupStratifier(BackboneElement):
    """
    When a measure includes multiple stratifiers, there will be a stratifier group for each stratifier defined by the measure.
    """

    linkId: Optional[String] = Field(
        description="Pointer to specific stratifier from Measure",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="What stratifier of the group",
        default=None,
    )
    stratum: Optional[ListType[MeasureReportGroupStratifierStratum]] = Field(
        description="Stratum results, one for each unique value, or set of values, in the stratifier, or stratifier components",
        default=None,
    )

class MeasureReportGroup(BackboneElement):
    """
    The results of the calculation, one for each population group in the measure.
    """

    linkId: Optional[String] = Field(
        description="Pointer to specific group from Measure",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="Meaning of the group",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="What individual(s) the report is for",
        default=None,
    )
    population: Optional[ListType[MeasureReportGroupPopulation]] = Field(
        description="The populations in the group",
        default=None,
    )
    measureScoreQuantity: Optional[Quantity] = Field(
        description="What score this group achieved",
        default=None,
    )
    measureScoreDateTime: Optional[DateTime] = Field(
        description="What score this group achieved",
        default=None,
    )
    measureScoreCodeableConcept: Optional[CodeableConcept] = Field(
        description="What score this group achieved",
        default=None,
    )
    measureScorePeriod: Optional[Period] = Field(
        description="What score this group achieved",
        default=None,
    )
    measureScoreRange: Optional[Range] = Field(
        description="What score this group achieved",
        default=None,
    )
    measureScoreDuration: Optional[Duration] = Field(
        description="What score this group achieved",
        default=None,
    )
    stratifier: Optional[ListType[MeasureReportGroupStratifier]] = Field(
        description="Stratification results",
        default=None,
    )

    @property
    def measureScore(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="measureScore",
        )

    @model_validator(mode="after")
    def measureScore_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Quantity, DateTime, CodeableConcept, Period, Range, Duration],
            field_name_base="measureScore",
            required=False,
        )

class MeasureReport(DomainResource):
    """
    The MeasureReport resource contains the results of the calculation of a measure; and optionally a reference to the resources involved in that calculation.
    """

    _abstract = False
    _type = "MeasureReport"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/MeasureReport"

    identifier: Optional[ListType[Identifier]] = Field(
        description="Additional identifier for the MeasureReport",
        default=None,
    )
    status: Optional[Code] = Field(
        description="complete | pending | error",
        default=None,
    )
    type: Optional[Code] = Field(
        description="individual | subject-list | summary | data-exchange",
        default=None,
    )
    dataUpdateType: Optional[Code] = Field(
        description="incremental | snapshot",
        default=None,
    )
    measure: Optional[Canonical] = Field(
        description="What measure was calculated",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="What individual(s) the report is for",
        default=None,
    )
    date: Optional[DateTime] = Field(
        description="When the measure was calculated",
        default=None,
    )
    reporter: Optional[Reference] = Field(
        description="Who is reporting the data",
        default=None,
    )
    reportingVendor: Optional[Reference] = Field(
        description="What vendor prepared the data",
        default=None,
    )
    location: Optional[Reference] = Field(
        description="Where the reported data is from",
        default=None,
    )
    period: Optional[Period] = Field(
        description="What period the report covers",
        default=None,
    )
    inputParameters: Optional[Reference] = Field(
        description="What parameters were provided to the report",
        default=None,
    )
    scoring: Optional[CodeableConcept] = Field(
        description="What scoring method (e.g. proportion, ratio, continuous-variable)",
        default=None,
    )
    improvementNotation: Optional[CodeableConcept] = Field(
        description="increase | decrease",
        default=None,
    )
    group: Optional[ListType[MeasureReportGroup]] = Field(
        description="Measure results for each group",
        default=None,
    )
    supplementalData: Optional[ListType[Reference]] = Field(
        description="Additional information collected for the report",
        default=None,
    )
    evaluatedResource: Optional[ListType[Reference]] = Field(
        description="What data was used to calculate the measure score",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_mrp_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(type != 'data-exchange') or group.exists().not()",
            human="Measure Reports used for data collection SHALL NOT communicate group and score information",
            key="mrp-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_mrp_2_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="group.stratifier.stratum.all(value.exists() xor component.exists())",
            human="Stratifiers SHALL be either a single criteria or a set of criteria components",
            key="mrp-2",
            severity="error",
        )
