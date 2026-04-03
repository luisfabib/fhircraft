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
    Period,
    BackboneElement,
    Annotation,
)
from .resource import Resource
from .domain_resource import DomainResource

class ClinicalImpressionInvestigation(BackboneElement):
    """
    One or more sets of investigations (signs, symptoms, etc.). The actual grouping of investigations varies greatly depending on the type and context of the assessment. These investigations may include data generated during the assessment process, or data previously generated and recorded that is pertinent to the outcomes.
    """

    code: Optional[CodeableConcept] = Field(
        description="A name/code for the set",
        default=None,
    )
    item: Optional[ListType[Reference]] = Field(
        description="Record of a specific investigation",
        default=None,
    )

class ClinicalImpressionFinding(BackboneElement):
    """
    Specific findings or diagnoses that were considered likely or relevant to ongoing treatment.
    """

    itemCodeableConcept: Optional[CodeableConcept] = Field(
        description="What was found",
        default=None,
    )
    itemReference: Optional[Reference] = Field(
        description="What was found",
        default=None,
    )
    basis: Optional[String] = Field(
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
        description="Business identifier",
        default=None,
    )
    status: Optional[Code] = Field(
        description="in-progress | completed | entered-in-error",
        default=None,
    )
    statusReason: Optional[CodeableConcept] = Field(
        description="Reason for current status",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="Kind of assessment performed",
        default=None,
    )
    description: Optional[String] = Field(
        description="Why/how the assessment was performed",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="Patient or group assessed",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="Encounter created as part of",
        default=None,
    )
    effectiveDateTime: Optional[DateTime] = Field(
        description="Time of assessment",
        default=None,
    )
    effectivePeriod: Optional[Period] = Field(
        description="Time of assessment",
        default=None,
    )
    date: Optional[DateTime] = Field(
        description="When the assessment was documented",
        default=None,
    )
    assessor: Optional[Reference] = Field(
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
    investigation: Optional[ListType[ClinicalImpressionInvestigation]] = Field(
        description="One or more sets of investigations (signs, symptoms, etc.)",
        default=None,
    )
    protocol: Optional[ListType[Uri]] = Field(
        description="Clinical Protocol followed",
        default=None,
    )
    summary: Optional[String] = Field(
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
            field_types=[DateTime, Period],
            field_name_base="effective",
            required=False,
        )
