import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from ..primitive import *

from .resource import Resource
from .domain_resource import DomainResource

from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    Period,
    BackboneElement,
    Range,
    Annotation,
)
from .resource import Resource
from .domain_resource import DomainResource

class RiskAssessmentPrediction(BackboneElement):
    """
    Describes the expected outcome for the subject.
    """

    outcome: Optional[CodeableConcept] = Field(
        description="Possible outcome for the subject",
        default=None,
    )
    probabilityDecimal: Optional[Decimal] = Field(
        description="Likelihood of specified outcome",
        default=None,
    )
    probabilityRange: Optional[Range] = Field(
        description="Likelihood of specified outcome",
        default=None,
    )
    qualitativeRisk: Optional[CodeableConcept] = Field(
        description="Likelihood of specified outcome as a qualitative value",
        default=None,
    )
    relativeRisk: Optional[Decimal] = Field(
        description="Relative likelihood",
        default=None,
    )
    whenPeriod: Optional[Period] = Field(
        description="Timeframe or age range",
        default=None,
    )
    whenRange: Optional[Range] = Field(
        description="Timeframe or age range",
        default=None,
    )
    rationale: Optional[String] = Field(
        description="Explanation of prediction",
        default=None,
    )

    @property
    def probability(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="probability",
        )

    @property
    def when(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="when",
        )

    @model_validator(mode="after")
    def probability_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Decimal, Range],
            field_name_base="probability",
            required=False,
        )

    @model_validator(mode="after")
    def when_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Period, Range],
            field_name_base="when",
            required=False,
        )

class RiskAssessment(DomainResource):
    """
    An assessment of the likely outcome(s) for a patient or other subject as well as the likelihood of each outcome.
    """

    _abstract = False
    _type = "RiskAssessment"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/RiskAssessment"

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
        description="Unique identifier for the assessment",
        default=None,
    )
    basedOn: Optional[Reference] = Field(
        description="Request fulfilled by this assessment",
        default=None,
    )
    parent: Optional[Reference] = Field(
        description="Part of this occurrence",
        default=None,
    )
    status: Optional[Code] = Field(
        description="registered | preliminary | final | amended +",
        default=None,
    )
    method: Optional[CodeableConcept] = Field(
        description="Evaluation mechanism",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="Type of assessment",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="Who/what does assessment apply to?",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="Where was assessment performed?",
        default=None,
    )
    occurrenceDateTime: Optional[DateTime] = Field(
        description="When was assessment made?",
        default=None,
    )
    occurrencePeriod: Optional[Period] = Field(
        description="When was assessment made?",
        default=None,
    )
    condition: Optional[Reference] = Field(
        description="Condition assessed",
        default=None,
    )
    performer: Optional[Reference] = Field(
        description="Who did assessment?",
        default=None,
    )
    reasonCode: Optional[ListType[CodeableConcept]] = Field(
        description="Why the assessment was necessary?",
        default=None,
    )
    reasonReference: Optional[ListType[Reference]] = Field(
        description="Why the assessment was necessary?",
        default=None,
    )
    basis: Optional[ListType[Reference]] = Field(
        description="Information used in assessment",
        default=None,
    )
    prediction: Optional[ListType[RiskAssessmentPrediction]] = Field(
        description="Outcome predicted",
        default=None,
    )
    mitigation: Optional[String] = Field(
        description="How to reduce risk",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Comments on the risk assessment",
        default=None,
    )

    @property
    def occurrence(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="occurrence",
        )

    @model_validator(mode="after")
    def FHIR_ras_2_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("prediction",),
            expression="probability is decimal implies (probability as decimal) <= 100",
            human="Must be <= 100",
            key="ras-2",
            severity="error",
        )

    @model_validator(mode="after")
    def occurrence_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[DateTime, Period],
            field_name_base="occurrence",
            required=False,
        )
