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
    CodeableConcept,
    Reference,
    Age,
    Period,
    Range,
    BackboneElement,
    CodeableReference,
    Annotation,
)
from .resource import Resource
from .domain_resource import DomainResource


class ConditionParticipant(BackboneElement):
    """
    Indicates who or what participated in the activities related to the condition and how they were involved.
    """

    function: Optional[CodeableConcept] = Field(
        description="Type of involvement",
        default=None,
    )
    actor: Optional[Reference] = Field(
        description="Who or what participated in the activities related to the condition",
        default=None,
    )


class ConditionStage(BackboneElement):
    """
    A simple summary of the stage such as "Stage 3" or "Early Onset". The determination of the stage is disease-specific, such as cancer, retinopathy of prematurity, kidney diseases, Alzheimer's, or Parkinson disease.
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


class Condition(DomainResource):
    """
    A clinical condition, problem, diagnosis, or other event, situation, issue, or clinical concept that has risen to a level of concern.
    """

    _abstract = False
    _type = "Condition"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Condition"

    identifier: Optional[ListType[Identifier]] = Field(
        description="External Ids for this condition",
        default=None,
    )
    clinicalStatus: Optional[CodeableConcept] = Field(
        description="active | recurrence | relapse | inactive | remission | resolved | unknown",
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
        description="The Encounter during which this Condition was created",
        default=None,
    )
    onsetDateTime: Optional[fhir.dateTime] = Field(
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
    onsetString: Optional[fhir.string] = Field(
        description="Estimated or actual date,  date-time, or age",
        default=None,
    )
    abatementDateTime: Optional[fhir.dateTime] = Field(
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
    abatementString: Optional[fhir.string] = Field(
        description="When in resolution/remission",
        default=None,
    )
    recordedDate: Optional[fhir.dateTime] = Field(
        description="Date condition was first recorded",
        default=None,
    )
    participant: Optional[ListType[ConditionParticipant]] = Field(
        description="Who or what participated in the activities related to the condition and how they were involved",
        default=None,
    )
    stage: Optional[ListType[ConditionStage]] = Field(
        description="Stage/grade, usually assessed formally",
        default=None,
    )
    evidence: Optional[ListType[CodeableReference]] = Field(
        description="Supporting evidence for the verification status",
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
            field_types=[fhir.DateTime, Age, Period, Range, fhir.String],
            field_name_base="onset",
            required=False,
        )

    @model_validator(mode="after")
    def abatement_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.DateTime, Age, Period, Range, fhir.String],
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
        return fhir_validators.validate_model_constraint(
            self,
            expression="category.coding.where(system='http://terminology.hl7.org/CodeSystem/condition-category' and code='problem-list-item').exists() implies clinicalStatus.coding.where(system='http://terminology.hl7.org/CodeSystem/condition-clinical' and code='unknown').exists().not()",
            human="If category is problems list item, the clinicalStatus should not be unknown",
            key="con-2",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_con_3_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="abatement.exists() implies (clinicalStatus.coding.where(system='http://terminology.hl7.org/CodeSystem/condition-clinical' and (code='inactive' or code='resolved' or code='remission')).exists())",
            human="If condition is abated, then clinicalStatus must be either inactive, resolved, or remission.",
            key="con-3",
            severity="error",
        )
