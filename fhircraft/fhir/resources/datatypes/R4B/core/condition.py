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
    CodeableConcept,
    Reference,
    Age,
    Period,
    Range,
    BackboneElement,
    Annotation,
)
from .resource import Resource
from .domain_resource import DomainResource

class ConditionStage(BackboneElement):
    """
    Clinical stage or grade of a condition. May include formal severity assessments.
    """

    summary: Optional[CodeableConcept] = Field(
        description="Simple summary (disease specific)",
        default=None,
    )
    assessment: Optional[ListType[Reference]] = Field(
        description="Formal record of assessment",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Kind of staging",
        default=None,
    )

class ConditionEvidence(BackboneElement):
    """
    Supporting evidence / manifestations that are the basis of the Condition's verification status, such as evidence that confirmed or refuted the condition.
    """

    code: Optional[ListType[CodeableConcept]] = Field(
        description="Manifestation/symptom",
        default=None,
    )
    detail: Optional[ListType[Reference]] = Field(
        description="Supporting information found elsewhere",
        default=None,
    )

class Condition(DomainResource):
    """
    A clinical condition, problem, diagnosis, or other event, situation, issue, or clinical concept that has risen to a level of concern.
    """

    _abstract = False
    _type = "Condition"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Condition"

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
        description="External Ids for this condition",
        default=None,
    )
    clinicalStatus: Optional[CodeableConcept] = Field(
        description="active | recurrence | relapse | inactive | remission | resolved",
        default=None,
    )
    verificationStatus: Optional[CodeableConcept] = Field(
        description="unconfirmed | provisional | differential | confirmed | refuted | entered-in-error",
        default=None,
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description="problem-list-item | encounter-diagnosis",
        default=None,
    )
    severity: Optional[CodeableConcept] = Field(
        description="Subjective severity of condition",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="Identification of the condition, problem or diagnosis",
        default=None,
    )
    bodySite: Optional[ListType[CodeableConcept]] = Field(
        description="Anatomical location, if relevant",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="Who has the condition?",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="Encounter created as part of",
        default=None,
    )
    onsetDateTime: Optional[DateTime] = Field(
        description="Estimated or actual date,  date-time, or age",
        default=None,
    )
    onsetAge: Optional[Age] = Field(
        description="Estimated or actual date,  date-time, or age",
        default=None,
    )
    onsetPeriod: Optional[Period] = Field(
        description="Estimated or actual date,  date-time, or age",
        default=None,
    )
    onsetRange: Optional[Range] = Field(
        description="Estimated or actual date,  date-time, or age",
        default=None,
    )
    onsetString: Optional[String] = Field(
        description="Estimated or actual date,  date-time, or age",
        default=None,
    )
    abatementDateTime: Optional[DateTime] = Field(
        description="When in resolution/remission",
        default=None,
    )
    abatementAge: Optional[Age] = Field(
        description="When in resolution/remission",
        default=None,
    )
    abatementPeriod: Optional[Period] = Field(
        description="When in resolution/remission",
        default=None,
    )
    abatementRange: Optional[Range] = Field(
        description="When in resolution/remission",
        default=None,
    )
    abatementString: Optional[String] = Field(
        description="When in resolution/remission",
        default=None,
    )
    recordedDate: Optional[DateTime] = Field(
        description="Date record was first recorded",
        default=None,
    )
    recorder: Optional[Reference] = Field(
        description="Who recorded the condition",
        default=None,
    )
    asserter: Optional[Reference] = Field(
        description="Person who asserts this condition",
        default=None,
    )
    stage: Optional[ListType[ConditionStage]] = Field(
        description="Stage/grade, usually assessed formally",
        default=None,
    )
    evidence: Optional[ListType[ConditionEvidence]] = Field(
        description="Supporting evidence",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Additional information about the Condition",
        default=None,
    )

    @property
    def onset(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="onset",
        )

    @property
    def abatement(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="abatement",
        )

    @model_validator(mode="after")
    def onset_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[DateTime, Age, Period, Range, String],
            field_name_base="onset",
            required=False,
        )

    @model_validator(mode="after")
    def abatement_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[DateTime, Age, Period, Range, String],
            field_name_base="abatement",
            required=False,
        )

    @model_validator(mode="after")
    def FHIR_con_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("stage",),
            expression="summary.exists() or assessment.exists()",
            human="Stage SHALL have summary or assessment",
            key="con-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_con_2_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("evidence",),
            expression="code.exists() or detail.exists()",
            human="evidence SHALL have code or details",
            key="con-2",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_con_3_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="verificationStatus.empty().not() and verificationStatus.coding.where(system='http://terminology.hl7.org/CodeSystem/condition-ver-status' and code='entered-in-error').exists().not() and category.coding.where(system='http://terminology.hl7.org/CodeSystem/condition-category' and code='problem-list-item').exists() implies clinicalStatus.empty().not()",
            human="Condition.clinicalStatus SHOULD be present if verificationStatus is not entered-in-error and category is problem-list-item",
            key="con-3",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_con_4_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="abatement.empty() or clinicalStatus.coding.where(system='http://terminology.hl7.org/CodeSystem/condition-clinical' and (code='resolved' or code='remission' or code='inactive')).exists()",
            human="If condition is abated, then clinicalStatus must be either inactive, resolved, or remission",
            key="con-4",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_con_5_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="verificationStatus.coding.where(system='http://terminology.hl7.org/CodeSystem/condition-ver-status' and code='entered-in-error').empty() or clinicalStatus.empty()",
            human="Condition.clinicalStatus SHALL NOT be present if verification Status is entered-in-error",
            key="con-5",
            severity="error",
        )
