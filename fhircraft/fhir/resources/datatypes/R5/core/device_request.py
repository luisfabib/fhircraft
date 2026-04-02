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
    CodeableReference,
    BackboneElement,
    CodeableConcept,
    Quantity,
    Range,
    Period,
    Timing,
    Annotation,
)
from .resource import Resource
from .domain_resource import DomainResource

class DeviceRequestParameter(BackboneElement):
    """
    Specific parameters for the ordered item.  For example, the prism value for lenses.
    """

    code: Optional[CodeableConcept] = Field(
        description="Device detail",
        default=None,
    )
    valueCodeableConcept: Optional[CodeableConcept] = Field(
        description="Value of detail",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="Value of detail",
        default=None,
    )
    valueRange: Optional[Range] = Field(
        description="Value of detail",
        default=None,
    )
    valueBoolean: Optional[Boolean] = Field(
        description="Value of detail",
        default=None,
    )

    @property
    def value(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="value",
        )

    @model_validator(mode="after")
    def value_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[CodeableConcept, Quantity, Range, Boolean],
            field_name_base="value",
            required=False,
        )

class DeviceRequest(DomainResource):
    """
    Represents a request a device to be provided to a specific patient. The device may be an implantable device to be subsequently implanted, or an external assistive device, such as a walker, to be delivered and subsequently be used.
    """

    _abstract = False
    _type = "DeviceRequest"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/DeviceRequest"

    identifier: Optional[ListType[Identifier]] = Field(
        description="External Request identifier",
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
        description="What request fulfills",
        default=None,
    )
    replaces: Optional[ListType[Reference]] = Field(
        description="What request replaces",
        default=None,
    )
    groupIdentifier: Optional[Identifier] = Field(
        description="Identifier of composite request",
        default=None,
    )
    status: Optional[Code] = Field(
        description="draft | active | on-hold | revoked | completed | entered-in-error | unknown",
        default=None,
    )
    intent: Optional[Code] = Field(
        description="proposal | plan | directive | order | original-order | reflex-order | filler-order | instance-order | option",
        default=None,
    )
    priority: Optional[Code] = Field(
        description="routine | urgent | asap | stat",
        default=None,
    )
    doNotPerform: Optional[Boolean] = Field(
        description="True if the request is to stop or not to start using the device",
        default=None,
    )
    code: Optional[CodeableReference] = Field(
        description="Device requested",
        default=None,
    )
    quantity: Optional[Integer] = Field(
        description="Quantity of devices to supply",
        default=None,
    )
    parameter: Optional[ListType[DeviceRequestParameter]] = Field(
        description="Device details",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="Focus of request",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="Encounter motivating request",
        default=None,
    )
    occurrenceDateTime: Optional[DateTime] = Field(
        description="Desired time or schedule for use",
        default=None,
    )
    occurrencePeriod: Optional[Period] = Field(
        description="Desired time or schedule for use",
        default=None,
    )
    occurrenceTiming: Optional[Timing] = Field(
        description="Desired time or schedule for use",
        default=None,
    )
    authoredOn: Optional[DateTime] = Field(
        description="When recorded",
        default=None,
    )
    requester: Optional[Reference] = Field(
        description="Who/what submitted the device request",
        default=None,
    )
    performer: Optional[CodeableReference] = Field(
        description="Requested Filler",
        default=None,
    )
    reason: Optional[ListType[CodeableReference]] = Field(
        description="Coded/Linked Reason for request",
        default=None,
    )
    asNeeded: Optional[Boolean] = Field(
        description="PRN status of request",
        default=None,
    )
    asNeededFor: Optional[CodeableConcept] = Field(
        description="Device usage reason",
        default=None,
    )
    insurance: Optional[ListType[Reference]] = Field(
        description="Associated insurance coverage",
        default=None,
    )
    supportingInfo: Optional[ListType[Reference]] = Field(
        description="Additional clinical information",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Notes or comments",
        default=None,
    )
    relevantHistory: Optional[ListType[Reference]] = Field(
        description="Request provenance",
        default=None,
    )

    @property
    def occurrence(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="occurrence",
        )

    @model_validator(mode="after")
    def occurrence_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[DateTime, Period, Timing],
            field_name_base="occurrence",
            required=False,
        )
