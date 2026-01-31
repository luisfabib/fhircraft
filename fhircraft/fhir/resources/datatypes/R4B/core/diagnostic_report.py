import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    DateTime,
    Instant,
)

from fhircraft.fhir.resources.datatypes.R4B.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    Period,
    BackboneElement,
    Attachment,
)
from .resource import Resource
from .domain_resource import DomainResource


class DiagnosticReportMedia(BackboneElement):
    """
    A list of key images associated with this report. The images are generally created during the diagnostic process, and may be directly of the patient, or of treated specimens (i.e. slides of interest).
    """

    comment: Optional[String] = Field(
        description="Comment about the image (e.g. explanation)",
        default=None,
    )
    comment_ext: Optional[Element] = Field(
        description="Placeholder element for comment extensions",
        default=None,
        alias="_comment",
    )
    link: Optional[Reference] = Field(
        description="Reference to the image source",
        default=None,
    )


class DiagnosticReport(DomainResource):
    """
    The findings and interpretation of diagnostic  tests performed on patients, groups of patients, devices, and locations, and/or specimens derived from these. The report includes clinical context such as requesting and provider information, and some mix of atomic results, images, textual and coded interpretations, and formatted representation of diagnostic reports.
    """

    _abstract = False
    _type = "DiagnosticReport"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/DiagnosticReport"

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
        description="Business identifier for report",
        default=None,
    )
    basedOn: Optional[ListType[Reference]] = Field(
        description="What was requested",
        default=None,
    )
    status: Optional[Code] = Field(
        description="registered | partial | preliminary | final +",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description="Service category",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="Name/Code for this diagnostic report",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="The subject of the report - usually, but not always, the patient",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="Health care event when test ordered",
        default=None,
    )
    effectiveDateTime: Optional[DateTime] = Field(
        description="Clinically relevant time/time-period for report",
        default=None,
    )
    effectiveDateTime_ext: Optional[Element] = Field(
        description="Placeholder element for effectiveDateTime extensions",
        default=None,
        alias="_effectiveDateTime",
    )
    effectivePeriod: Optional[Period] = Field(
        description="Clinically relevant time/time-period for report",
        default=None,
    )
    issued: Optional[Instant] = Field(
        description="DateTime this version was made",
        default=None,
    )
    issued_ext: Optional[Element] = Field(
        description="Placeholder element for issued extensions",
        default=None,
        alias="_issued",
    )
    performer: Optional[ListType[Reference]] = Field(
        description="Responsible Diagnostic Service",
        default=None,
    )
    resultsInterpreter: Optional[ListType[Reference]] = Field(
        description="Primary result interpreter",
        default=None,
    )
    specimen: Optional[ListType[Reference]] = Field(
        description="Specimens this report is based on",
        default=None,
    )
    result: Optional[ListType[Reference]] = Field(
        description="Observations",
        default=None,
    )
    imagingStudy: Optional[ListType[Reference]] = Field(
        description="Reference to full details of imaging associated with the diagnostic report",
        default=None,
    )
    media: Optional[ListType[DiagnosticReportMedia]] = Field(
        description="Key images associated with this report",
        default=None,
    )
    conclusion: Optional[String] = Field(
        description="Clinical conclusion (interpretation) of test results",
        default=None,
    )
    conclusion_ext: Optional[Element] = Field(
        description="Placeholder element for conclusion extensions",
        default=None,
        alias="_conclusion",
    )
    conclusionCode: Optional[ListType[CodeableConcept]] = Field(
        description="Codes for the clinical conclusion of test results",
        default=None,
    )
    presentedForm: Optional[ListType[Attachment]] = Field(
        description="Entire report as issued",
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
