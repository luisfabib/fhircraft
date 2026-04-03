import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)


from ..primitive import *
from fhircraft.fhir.resources.datatypes.R4B.complex import (
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
)
from .resource import Resource
from .domain_resource import DomainResource

class MeasureReportGroupPopulation(BackboneElement):
    """
    The populations that make up the population group, one for each type of population appropriate for the measure.
    """

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

class MeasureReportGroupStratifierStratumComponent(BackboneElement):
    """
    A stratifier component value.
    """

    code: Optional[CodeableConcept] = Field(
        description="What stratifier component of the group",
        default=None,
    )
    value: Optional[CodeableConcept] = Field(
        description="The stratum component value, e.g. male",
        default=None,
    )

class MeasureReportGroupStratifierStratumPopulation(BackboneElement):
    """
    The populations that make up the stratum, one for each type of population appropriate to the measure.
    """

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

class MeasureReportGroupStratifierStratum(BackboneElement):
    """
    This element contains the results for a single stratum within the stratifier. For example, when stratifying on administrative gender, there will be four strata, one for each possible gender value.
    """

    value: Optional[CodeableConcept] = Field(
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
    measureScore: Optional[Quantity] = Field(
        description="What score this stratum achieved",
        default=None,
    )

class MeasureReportGroupStratifier(BackboneElement):
    """
    When a measure includes multiple stratifiers, there will be a stratifier group for each stratifier defined by the measure.
    """

    code: Optional[ListType[CodeableConcept]] = Field(
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

    code: Optional[CodeableConcept] = Field(
        description="Meaning of the group",
        default=None,
    )
    population: Optional[ListType[MeasureReportGroupPopulation]] = Field(
        description="The populations in the group",
        default=None,
    )
    measureScore: Optional[Quantity] = Field(
        description="What score this group achieved",
        default=None,
    )
    stratifier: Optional[ListType[MeasureReportGroupStratifier]] = Field(
        description="Stratification results",
        default=None,
    )

class MeasureReport(DomainResource):
    """
    The MeasureReport resource contains the results of the calculation of a measure; and optionally a reference to the resources involved in that calculation.
    """

    _abstract = False
    _type = "MeasureReport"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/MeasureReport"

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
    identifier: Optional[ListType[Identifier]] = Field(
        description="Additional identifier for the MeasureReport",
        default=None,
    )
    status: Optional[Code] = Field(
        description="complete | pending | error",
        default=None,
    )
    type: Optional[Code] = Field(
        description="individual | subject-list | summary | data-collection",
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
        description="When the report was generated",
        default=None,
    )
    reporter: Optional[Reference] = Field(
        description="Who is reporting the data",
        default=None,
    )
    period: Optional[Period] = Field(
        description="What period the report covers",
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
    evaluatedResource: Optional[ListType[Reference]] = Field(
        description="What data was used to calculate the measure score",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_mrp_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(type != 'data-collection') or group.exists().not()",
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
