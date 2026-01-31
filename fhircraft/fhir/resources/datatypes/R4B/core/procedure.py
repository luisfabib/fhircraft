import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    Canonical,
    DateTime,
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
    Age,
    Range,
    BackboneElement,
    Annotation,
)
from .resource import Resource
from .domain_resource import DomainResource


class ProcedurePerformer(BackboneElement):
    """
    Limited to "real" people rather than equipment.
    """

    function: Optional[CodeableConcept] = Field(
        description="Type of performance",
        default=None,
    )
    actor: Optional[Reference] = Field(
        description="The reference to the practitioner",
        default=None,
    )
    onBehalfOf: Optional[Reference] = Field(
        description="Organization the device or practitioner was acting for",
        default=None,
    )


class ProcedureFocalDevice(BackboneElement):
    """
    A device that is implanted, removed or otherwise manipulated (calibration, battery replacement, fitting a prosthesis, attaching a wound-vac, etc.) as a focal portion of the Procedure.
    """

    action: Optional[CodeableConcept] = Field(
        description="Kind of change to device",
        default=None,
    )
    manipulated: Optional[Reference] = Field(
        description="Device that was changed",
        default=None,
    )


class Procedure(DomainResource):
    """
    An action that is or was performed on or for a patient. This can be a physical intervention like an operation, or less invasive like long term services, counseling, or hypnotherapy.
    """

    _abstract = False
    _type = "Procedure"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Procedure"

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
        description="External Identifiers for this procedure",
        default=None,
    )
    instantiatesCanonical: Optional[ListType[Canonical]] = Field(
        description="Instantiates FHIR protocol or definition",
        default=None,
    )
    instantiatesCanonical_ext: Optional[Element] = Field(
        description="Placeholder element for instantiatesCanonical extensions",
        default=None,
        alias="_instantiatesCanonical",
    )
    instantiatesUri: Optional[ListType[Uri]] = Field(
        description="Instantiates external protocol or definition",
        default=None,
    )
    instantiatesUri_ext: Optional[Element] = Field(
        description="Placeholder element for instantiatesUri extensions",
        default=None,
        alias="_instantiatesUri",
    )
    basedOn: Optional[ListType[Reference]] = Field(
        description="A request for this procedure",
        default=None,
    )
    partOf: Optional[ListType[Reference]] = Field(
        description="Part of referenced event",
        default=None,
    )
    status: Optional[Code] = Field(
        description="preparation | in-progress | not-done | on-hold | stopped | completed | entered-in-error | unknown",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    statusReason: Optional[CodeableConcept] = Field(
        description="Reason for current status",
        default=None,
    )
    category: Optional[CodeableConcept] = Field(
        description="Classification of the procedure",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="Identification of the procedure",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="Who the procedure was performed on",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="Encounter created as part of",
        default=None,
    )
    performedDateTime: Optional[DateTime] = Field(
        description="When the procedure was performed",
        default=None,
    )
    performedDateTime_ext: Optional[Element] = Field(
        description="Placeholder element for performedDateTime extensions",
        default=None,
        alias="_performedDateTime",
    )
    performedPeriod: Optional[Period] = Field(
        description="When the procedure was performed",
        default=None,
    )
    performedString: Optional[String] = Field(
        description="When the procedure was performed",
        default=None,
    )
    performedString_ext: Optional[Element] = Field(
        description="Placeholder element for performedString extensions",
        default=None,
        alias="_performedString",
    )
    performedAge: Optional[Age] = Field(
        description="When the procedure was performed",
        default=None,
    )
    performedRange: Optional[Range] = Field(
        description="When the procedure was performed",
        default=None,
    )
    recorder: Optional[Reference] = Field(
        description="Who recorded the procedure",
        default=None,
    )
    asserter: Optional[Reference] = Field(
        description="Person who asserts this procedure",
        default=None,
    )
    performer: Optional[ListType[ProcedurePerformer]] = Field(
        description="The people who performed the procedure",
        default=None,
    )
    location: Optional[Reference] = Field(
        description="Where the procedure happened",
        default=None,
    )
    reasonCode: Optional[ListType[CodeableConcept]] = Field(
        description="Coded reason procedure performed",
        default=None,
    )
    reasonReference: Optional[ListType[Reference]] = Field(
        description="The justification that the procedure was performed",
        default=None,
    )
    bodySite: Optional[ListType[CodeableConcept]] = Field(
        description="Target body sites",
        default=None,
    )
    outcome: Optional[CodeableConcept] = Field(
        description="The result of procedure",
        default=None,
    )
    report: Optional[ListType[Reference]] = Field(
        description="Any report resulting from the procedure",
        default=None,
    )
    complication: Optional[ListType[CodeableConcept]] = Field(
        description="Complication following the procedure",
        default=None,
    )
    complicationDetail: Optional[ListType[Reference]] = Field(
        description="A condition that is a result of the procedure",
        default=None,
    )
    followUp: Optional[ListType[CodeableConcept]] = Field(
        description="Instructions for follow up",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Additional information about the procedure",
        default=None,
    )
    focalDevice: Optional[ListType[ProcedureFocalDevice]] = Field(
        description="Manipulated, implanted, or removed device",
        default=None,
    )
    usedReference: Optional[ListType[Reference]] = Field(
        description="Items used during procedure",
        default=None,
    )
    usedCode: Optional[ListType[CodeableConcept]] = Field(
        description="Coded items used during the procedure",
        default=None,
    )

    @property
    def performed(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="performed",
        )

    @model_validator(mode="after")
    def performed_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[DateTime, Period, String, Age, Range],
            field_name_base="performed",
            required=False,
        )
