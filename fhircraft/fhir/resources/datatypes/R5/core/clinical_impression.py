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
    Period,
    BackboneElement,
    CodeableReference,
    Annotation,
)
from .resource import Resource
from .domain_resource import DomainResource

class ClinicalImpressionFinding(BackboneElement):
    """
    Specific findings or diagnoses that were considered likely or relevant to ongoing treatment.
    """

    item: Optional[CodeableReference] = Field(
        description="What was found",
        default=None,
    )
    basis: Optional[fhir.string] = Field(
        description="Which investigations support finding",
        default=None,
    )

class ClinicalImpression(DomainResource):
    """
    A record of a clinical assessment performed to determine what problem(s) may affect the patient and before planning the treatments or management strategies that are best to manage a patient's condition. Assessments are often 1:1 with a clinical consultation / encounter,  but this varies greatly depending on the clinical workflow. This resource is called "ClinicalImpression" rather than "ClinicalAssessment" to avoid confusion with the recording of assessment tools such as Apgar score.
    """

    _abstract = False
    _type = "ClinicalImpression"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/ClinicalImpression"

    identifier: Optional[ListType[Identifier]] = Field(
        description="Business identifier",
        default=None,
    )
    status: Optional[fhir.code] = Field(
        description="preparation | in-progress | not-done | on-hold | stopped | completed | entered-in-error | unknown",
        default=None,
    )
    statusReason: Optional[CodeableConcept] = Field(
        description="Reason for current status",
        default=None,
    )
    description: Optional[fhir.string] = Field(
        description="Why/how the assessment was performed",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="Patient or group assessed",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="The Encounter during which this ClinicalImpression was created",
        default=None,
    )
    effectiveDateTime: Optional[fhir.dateTime] = Field(
        description="time of assessment",
        default=None,
    )
    effectivePeriod: Optional[Period] = Field(
        description="time of assessment",
        default=None,
    )
    date: Optional[fhir.dateTime] = Field(
        description="When the assessment was documented",
        default=None,
    )
    performer: Optional[Reference] = Field(
        description="The clinician performing the assessment",
        default=None,
    )
    previous: Optional[Reference] = Field(
        description="Reference to last assessment",
        default=None,
    )
    problem: Optional[ListType[Reference]] = Field(
        description="Relevant impressions of patient state",
        default=None,
    )
    changePattern: Optional[CodeableConcept] = Field(
        description="Change in the status/pattern of a subject\u0027s condition since previously assessed, such as worsening, improving, or no change",
        default=None,
    )
    protocol: Optional[ListType[fhir.uri]] = Field(
        description="Clinical Protocol followed",
        default=None,
    )
    summary: Optional[fhir.string] = Field(
        description="Summary of the assessment",
        default=None,
    )
    finding: Optional[ListType[ClinicalImpressionFinding]] = Field(
        description="Possible or likely findings and diagnoses",
        default=None,
    )
    prognosisCodeableConcept: Optional[ListType[CodeableConcept]] = Field(
        description="Estimate of likely outcome",
        default=None,
    )
    prognosisReference: Optional[ListType[Reference]] = Field(
        description="RiskAssessment expressing likely outcome",
        default=None,
    )
    supportingInfo: Optional[ListType[Reference]] = Field(
        description="Information supporting the clinical impression",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Comments made about the ClinicalImpression",
        default=None,
    )

    @property
    def effective(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="effective",
        )

    @model_validator(mode="after")
    def effective_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.dateTime, Period],
            field_name_base="effective",
            required=False,
        )
