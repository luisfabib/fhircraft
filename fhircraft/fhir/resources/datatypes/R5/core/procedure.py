from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from ..primitive import *

from fhircraft.fhir.resources.datatypes.R5.complex import (
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
    Timing,
    BackboneElement,
    CodeableReference,
    Annotation,
)
from .resource import Resource
from .domain_resource import DomainResource

class ProcedurePerformer(BackboneElement):
    """
    Indicates who or what performed the procedure and how they were involved.
    """

    function: Optional[CodeableConcept] = Field(
        description="Type of performance",
        default=None,
    )
    actor: Optional[Reference] = Field(
        description="Who performed the procedure",
        default=None,
    )
    onBehalfOf: Optional[Reference] = Field(
        description="Organization the device or practitioner was acting for",
        default=None,
    )
    period: Optional[Period] = Field(
        description="When the performer performed the procedure",
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
    An action that is or was performed on or for a patient, practitioner, device, organization, or location. For example, this can be a physical intervention on a patient like an operation, or less invasive like long term services, counseling, or hypnotherapy.  This can be a quality or safety inspection for a location, organization, or device.  This can be an accreditation procedure on a practitioner for licensing.
    """

    _abstract = False
    _type = "Procedure"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Procedure"

    identifier: Optional[ListType[Identifier]] = Field(
        description="External Identifiers for this procedure",
        default=None,
    )
    instantiatesCanonical: Optional[ListType[Canonical]] = Field(
        description="Instantiates FHIR protocol or definition",
        default=None,
    )
    instantiatesUri: Optional[ListType[Uri]] = Field(
        description="Instantiates external protocol or definition",
        default=None,
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
    statusReason: Optional[CodeableConcept] = Field(
        description="Reason for current status",
        default=None,
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description="Classification of the procedure",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="Identification of the procedure",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="Individual or entity the procedure was performed on",
        default=None,
    )
    focus: Optional[Reference] = Field(
        description="Who is the target of the procedure when it is not the subject of record only",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="The Encounter during which this Procedure was created",
        default=None,
    )
    occurrenceDateTime: Optional[DateTime] = Field(
        description="When the procedure occurred or is occurring",
        default=None,
    )
    occurrencePeriod: Optional[Period] = Field(
        description="When the procedure occurred or is occurring",
        default=None,
    )
    occurrenceString: Optional[String] = Field(
        description="When the procedure occurred or is occurring",
        default=None,
    )
    occurrenceAge: Optional[Age] = Field(
        description="When the procedure occurred or is occurring",
        default=None,
    )
    occurrenceRange: Optional[Range] = Field(
        description="When the procedure occurred or is occurring",
        default=None,
    )
    occurrenceTiming: Optional[Timing] = Field(
        description="When the procedure occurred or is occurring",
        default=None,
    )
    recorded: Optional[DateTime] = Field(
        description="When the procedure was first captured in the subject\u0027s record",
        default=None,
    )
    recorder: Optional[Reference] = Field(
        description="Who recorded the procedure",
        default=None,
    )
    reportedBoolean: Optional[Boolean] = Field(
        description="Reported rather than primary record",
        default=None,
    )
    reportedReference: Optional[Reference] = Field(
        description="Reported rather than primary record",
        default=None,
    )
    performer: Optional[ListType[ProcedurePerformer]] = Field(
        description="Who performed the procedure and what they did",
        default=None,
    )
    location: Optional[Reference] = Field(
        description="Where the procedure happened",
        default=None,
    )
    reason: Optional[ListType[CodeableReference]] = Field(
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
    complication: Optional[ListType[CodeableReference]] = Field(
        description="Complication following the procedure",
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
    used: Optional[ListType[CodeableReference]] = Field(
        description="Items used during procedure",
        default=None,
    )
    supportingInfo: Optional[ListType[Reference]] = Field(
        description="Extra information relevant to the procedure",
        default=None,
    )

    @property
    def occurrence(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="occurrence",
        )

    @property
    def reported(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="reported",
        )

    @model_validator(mode="after")
    def occurrence_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[DateTime, Period, String, Age, Range, Timing],
            field_name_base="occurrence",
            required=False,
        )

    @model_validator(mode="after")
    def reported_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Boolean, Reference],
            field_name_base="reported",
            required=False,
        )

    @model_validator(mode="after")
    def FHIR_prc_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("performer",),
            expression="onBehalfOf.exists() and actor.resolve().exists() implies actor.resolve().where($this is Practitioner or $this is PractitionerRole).empty()",
            human="Procedure.performer.onBehalfOf can only be populated when performer.actor isn't Practitioner or PractitionerRole",
            key="prc-1",
            severity="error",
        )
