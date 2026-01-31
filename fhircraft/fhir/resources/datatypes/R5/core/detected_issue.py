from pydantic import Field, model_validator
from typing import Optional, List

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    DateTime,
    Markdown,
)

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
    Annotation,
)
from .resource import Resource
from .domain_resource import DomainResource


class DetectedIssueEvidence(BackboneElement):
    """
    Supporting evidence or manifestations that provide the basis for identifying the detected issue such as a GuidanceResponse or MeasureReport.
    """

    code: Optional[List[CodeableConcept]] = Field(
        description="Manifestation",
        default=None,
    )
    detail: Optional[List[Reference]] = Field(
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
    date_ext: Optional[Element] = Field(
        description="Placeholder element for date extensions",
        default=None,
        alias="_date",
    )
    author: Optional[Reference] = Field(
        description="Who is committing?",
        default=None,
    )
    note: Optional[List[Annotation]] = Field(
        description="Additional notes about the mitigation",
        default=None,
    )


class DetectedIssue(DomainResource):
    """
    Indicates an actual or potential clinical issue with or between one or more active or proposed clinical actions for a patient; e.g. Drug-drug interaction, Ineffective treatment frequency, Procedure-condition conflict, gaps in care, etc.
    """

    _abstract = False
    _type = "DetectedIssue"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/DetectedIssue"

    identifier: Optional[List[Identifier]] = Field(
        description="Unique id for the detected issue",
        default=None,
    )
    status: Optional[Code] = Field(
        description="preliminary | final | entered-in-error | mitigated",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    category: Optional[List[CodeableConcept]] = Field(
        description="Type of detected issue, e.g. drug-drug, duplicate therapy, etc",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="Specific type of detected issue, e.g. drug-drug, duplicate therapy, etc",
        default=None,
    )
    severity: Optional[Code] = Field(
        description="high | moderate | low",
        default=None,
    )
    severity_ext: Optional[Element] = Field(
        description="Placeholder element for severity extensions",
        default=None,
        alias="_severity",
    )
    subject: Optional[Reference] = Field(
        description="Associated subject",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="Encounter detected issue is part of",
        default=None,
    )
    identifiedDateTime: Optional[DateTime] = Field(
        description="When identified",
        default=None,
    )
    identifiedDateTime_ext: Optional[Element] = Field(
        description="Placeholder element for identifiedDateTime extensions",
        default=None,
        alias="_identifiedDateTime",
    )
    identifiedPeriod: Optional[Period] = Field(
        description="When identified",
        default=None,
    )
    author: Optional[Reference] = Field(
        description="The provider or device that identified the issue",
        default=None,
    )
    implicated: Optional[List[Reference]] = Field(
        description="Problem resource",
        default=None,
    )
    evidence: Optional[List[DetectedIssueEvidence]] = Field(
        description="Supporting evidence",
        default=None,
    )
    detail: Optional[Markdown] = Field(
        description="Description and context",
        default=None,
    )
    detail_ext: Optional[List[Optional[Element]]] = Field(
        description="Placeholder element for detail extensions",
        default=None,
        alias="_detail",
    )
    reference: Optional[Uri] = Field(
        description="Authority for issue",
        default=None,
    )
    reference_ext: Optional[Element] = Field(
        description="Placeholder element for reference extensions",
        default=None,
        alias="_reference",
    )
    mitigation: Optional[List[DetectedIssueMitigation]] = Field(
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
