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
    CodeableReference,
    CodeableConcept,
    BackboneElement,
    Quantity,
    Annotation,
)
from .resource import Resource
from .domain_resource import DomainResource

class DeviceDispensePerformer(BackboneElement):
    """
    Indicates who or what performed the event.
    """

    function: Optional[CodeableConcept] = Field(
        description="Who performed the dispense and what they did",
        default=None,
    )
    actor: Optional[Reference] = Field(
        description="Individual who was performing",
        default=None,
    )

class DeviceDispense(DomainResource):
    """
    Indicates that a device is to be or has been dispensed for a named person/patient.  This includes a description of the product (supply) provided and the instructions for using the device.
    """

    _abstract = False
    _type = "DeviceDispense"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/DeviceDispense"

    identifier: Optional[ListType[Identifier]] = Field(
        description="Business identifier for this dispensation",
        default=None,
    )
    basedOn: Optional[ListType[Reference]] = Field(
        description="The order or request that this dispense is fulfilling",
        default=None,
    )
    partOf: Optional[ListType[Reference]] = Field(
        description="The bigger event that this dispense is a part of",
        default=None,
    )
    status: Optional[fhir.code] = Field(
        description="preparation | in-progress | cancelled | on-hold | completed | entered-in-error | stopped | declined | unknown",
        default=None,
    )
    statusReason: Optional[CodeableReference] = Field(
        description="Why a dispense was or was not performed",
        default=None,
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description="Type of device dispense",
        default=None,
    )
    device: Optional[CodeableReference] = Field(
        description="What device was supplied",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="Who the dispense is for",
        default=None,
    )
    receiver: Optional[Reference] = Field(
        description="Who collected the device or where the medication was delivered",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="Encounter associated with event",
        default=None,
    )
    supportingInformation: Optional[ListType[Reference]] = Field(
        description="Information that supports the dispensing of the device",
        default=None,
    )
    performer: Optional[ListType[DeviceDispensePerformer]] = Field(
        description="Who performed event",
        default=None,
    )
    location: Optional[Reference] = Field(
        description="Where the dispense occurred",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Trial fill, partial fill, emergency fill, etc",
        default=None,
    )
    quantity: Optional[Quantity] = Field(
        description="Amount dispensed",
        default=None,
    )
    preparedDate: Optional[fhir.dateTime] = Field(
        description="When product was packaged and reviewed",
        default=None,
    )
    whenHandedOver: Optional[fhir.dateTime] = Field(
        description="When product was given out",
        default=None,
    )
    destination: Optional[Reference] = Field(
        description="Where the device was sent or should be sent",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Information about the dispense",
        default=None,
    )
    usageInstruction: Optional[fhir.markdown] = Field(
        description="Full representation of the usage instructions",
        default=None,
    )
    eventHistory: Optional[ListType[Reference]] = Field(
        description="A list of relevant lifecycle events",
        default=None,
    )
