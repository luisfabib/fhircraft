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
    Timing,
    Period,
    BackboneElement,
    CodeableReference,
    Annotation,
)
from .resource import Resource
from .domain_resource import DomainResource


class DeviceUsageAdherence(BackboneElement):
    """
    This indicates how or if the device is being used.
    """

    code: Optional[CodeableConcept] = Field(
        description="always | never | sometimes",
        default=None,
    )
    reason: Optional[ListType[CodeableConcept]] = Field(
        description="lost | stolen | prescribed | broken | burned | forgot",
        default=None,
    )


class DeviceUsage(DomainResource):
    """
    A record of a device being used by a patient where the record is the result of a report from the patient or a clinician.
    """

    _abstract = False
    _type = "DeviceUsage"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/DeviceUsage"

    identifier: Optional[ListType[Identifier]] = Field(
        description="External identifier for this record",
        default=None,
    )
    basedOn: Optional[ListType[Reference]] = Field(
        description="Fulfills plan, proposal or order",
        default=None,
    )
    status: Optional[fhir.code] = Field(
        description="active | completed | not-done | entered-in-error +",
        default=None,
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description="The category of the statement - classifying how the statement is made",
        default=None,
    )
    patient: Optional[Reference] = Field(
        description="Patient using device",
        default=None,
    )
    derivedFrom: Optional[ListType[Reference]] = Field(
        description="Supporting information",
        default=None,
    )
    context: Optional[Reference] = Field(
        description="The encounter or episode of care that establishes the context for this device use statement",
        default=None,
    )
    timingTiming: Optional[Timing] = Field(
        description="How often  the device was used",
        default=None,
    )
    timingPeriod: Optional[Period] = Field(
        description="How often  the device was used",
        default=None,
    )
    timingDateTime: Optional[fhir.dateTime] = Field(
        description="How often  the device was used",
        default=None,
    )
    dateAsserted: Optional[fhir.dateTime] = Field(
        description="When the statement was made (and recorded)",
        default=None,
    )
    usageStatus: Optional[CodeableConcept] = Field(
        description="The status of the device usage, for example always, sometimes, never. This is not the same as the status of the statement",
        default=None,
    )
    usageReason: Optional[ListType[CodeableConcept]] = Field(
        description="The reason for asserting the usage status - for example forgot, lost, stolen, broken",
        default=None,
    )
    adherence: Optional[DeviceUsageAdherence] = Field(
        description="How device is being used",
        default=None,
    )
    informationSource: Optional[Reference] = Field(
        description="Who made the statement",
        default=None,
    )
    device: Optional[CodeableReference] = Field(
        description="code or Reference to device used",
        default=None,
    )
    reason: Optional[ListType[CodeableReference]] = Field(
        description="Why device was used",
        default=None,
    )
    bodySite: Optional[CodeableReference] = Field(
        description="Target body site",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Addition details (comments, instructions)",
        default=None,
    )

    @property
    def timing(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="timing",
        )

    @model_validator(mode="after")
    def timing_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Timing, Period, fhir.DateTime],
            field_name_base="timing",
            required=False,
        )
