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
    Reference,
    CodeableConcept,
    Period,
    Annotation,
    BackboneElement,
    Attachment,
)
from .resource import Resource
from .domain_resource import DomainResource


class DiagnosticReportSupportingInfo(BackboneElement):
    """
    This backbone element contains supporting information that was used in the creation of the report not included in the results already included in the report.
    """

    type: Optional[CodeableConcept] = Field(
        description="Supporting information role code",
        default=None,
    )
    reference: Optional[Reference] = Field(
        description="Supporting information reference",
        default=None,
    )


class DiagnosticReportMedia(BackboneElement):
    """
    A list of key images or data associated with this report. The images or data are generally created during the diagnostic process, and may be directly of the patient, or of treated specimens (i.e. slides of interest).
    """

    comment: Optional[fhir.string] = Field(
        description="Comment about the image or data (e.g. explanation)",
        default=None,
    )
    link: Optional[Reference] = Field(
        description="Reference to the image or data source",
        default=None,
    )


class DiagnosticReport(DomainResource):
    """
    The findings and interpretation of diagnostic tests performed on patients, groups of patients, products, substances, devices, and locations, and/or specimens derived from these. The report includes clinical context such as requesting provider information, and some mix of atomic results, images, textual and coded interpretations, and formatted representation of diagnostic reports. The report also includes non-clinical context such as batch analysis and stability reporting of products and substances.
    """

    _abstract = False
    _type = "DiagnosticReport"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/DiagnosticReport"

    identifier: Optional[ListType[Identifier]] = Field(
        description="Business identifier for report",
        default=None,
    )
    basedOn: Optional[ListType[Reference]] = Field(
        description="What was requested",
        default=None,
    )
    status: Optional[fhir.code] = Field(
        description="registered | partial | preliminary | modified | final | amended | corrected | appended | cancelled | entered-in-error | unknown",
        default=None,
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description="Service category",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="Name/code for this diagnostic report",
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
    effectiveDateTime: Optional[fhir.dateTime] = Field(
        description="Clinically relevant time/time-period for report",
        default=None,
    )
    effectivePeriod: Optional[Period] = Field(
        description="Clinically relevant time/time-period for report",
        default=None,
    )
    issued: Optional[fhir.instant] = Field(
        description="DateTime this version was made",
        default=None,
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
    note: Optional[ListType[Annotation]] = Field(
        description="Comments about the diagnostic report",
        default=None,
    )
    study: Optional[ListType[Reference]] = Field(
        description="Reference to full details of an analysis associated with the diagnostic report",
        default=None,
    )
    supportingInfo: Optional[ListType[DiagnosticReportSupportingInfo]] = Field(
        description="Additional information supporting the diagnostic report",
        default=None,
    )
    media: Optional[ListType[DiagnosticReportMedia]] = Field(
        description="Key images or data associated with this report",
        default=None,
    )
    composition: Optional[Reference] = Field(
        description="Reference to a Composition resource for the DiagnosticReport structure",
        default=None,
    )
    conclusion: Optional[fhir.markdown] = Field(
        description="Clinical conclusion (interpretation) of test results",
        default=None,
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
            field_types=[fhir.dateTime, Period],
            field_name_base="effective",
            required=False,
        )

    @model_validator(mode="after")
    def FHIR_dgr_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="composition.exists() implies (composition.resolve().section.entry.reference.where(resolve() is Observation) in (result.reference|result.reference.resolve().hasMember.reference))",
            human="When a Composition is referenced in `Diagnostic.composition`, all Observation resources referenced in `Composition.entry` must also be referenced in `Diagnostic.entry` or in the references Observations in `Observation.hasMember`",
            key="dgr-1",
            severity="error",
        )
