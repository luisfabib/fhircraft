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
)
from .resource import Resource
from .domain_resource import DomainResource

class DetectedIssueEvidence(BackboneElement):
    """
    Supporting evidence or manifestations that provide the basis for identifying the detected issue such as a GuidanceResponse or MeasureReport.
    """

    code: Optional[ListType[CodeableConcept]] = Field(
        description="Manifestation",
        default=None,
    )
    detail: Optional[ListType[Reference]] = Field(
        description="Supporting information",
        default=None,
    )

class DetectedIssueMitigation(BackboneElement):
    """
    Indicates an action that has been taken or is committed to reduce or eliminate the likelihood of the risk identified by the detected issue from manifesting.  Can also reflect an observation of known mitigating factors that may reduce/eliminate the need for any action.
    """

    action: Optional[CodeableConcept] = Field(
        description="What mitigation?",
        default=None,
    )
    date: Optional[DateTime] = Field(
        description="Date committed",
        default=None,
    )
    author: Optional[Reference] = Field(
        description="Who is committing?",
        default=None,
    )

class DetectedIssue(DomainResource):
    """
    Indicates an actual or potential clinical issue with or between one or more active or proposed clinical actions for a patient; e.g. Drug-drug interaction, Ineffective treatment frequency, Procedure-condition conflict, etc.
    """

    _abstract = False
    _type = "DetectedIssue"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/DetectedIssue"

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
        description="Unique id for the detected issue",
        default=None,
    )
    status: Optional[Code] = Field(
        description="registered | preliminary | final | amended +",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="Issue Category, e.g. drug-drug, duplicate therapy, etc.",
        default=None,
    )
    severity: Optional[Code] = Field(
        description="high | moderate | low",
        default=None,
    )
    patient: Optional[Reference] = Field(
        description="Associated patient",
        default=None,
    )
    identifiedDateTime: Optional[DateTime] = Field(
        description="When identified",
        default=None,
    )
    identifiedPeriod: Optional[Period] = Field(
        description="When identified",
        default=None,
    )
    author: Optional[Reference] = Field(
        description="The provider or device that identified the issue",
        default=None,
    )
    implicated: Optional[ListType[Reference]] = Field(
        description="Problem resource",
        default=None,
    )
    evidence: Optional[ListType[DetectedIssueEvidence]] = Field(
        description="Supporting evidence",
        default=None,
    )
    detail: Optional[String] = Field(
        description="Description and context",
        default=None,
    )
    reference: Optional[Uri] = Field(
        description="Authority for issue",
        default=None,
    )
    mitigation: Optional[ListType[DetectedIssueMitigation]] = Field(
        description="Step taken to address",
        default=None,
    )

    @property
    def identified(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="identified",
        )

    @model_validator(mode="after")
    def identified_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[DateTime, Period],
            field_name_base="identified",
            required=False,
        )
