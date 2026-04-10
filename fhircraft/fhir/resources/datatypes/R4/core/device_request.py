import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)


import fhircraft.fhir.resources.datatypes.R4.primitive as fhir
from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    Annotation,
    BackboneElement,
    Quantity,
    Range,
    Period,
    Timing,
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
    valueBoolean: Optional[fhir.boolean] = Field(
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
            field_types=[CodeableConcept, Quantity, Range, fhir.boolean],
            field_name_base="value",
            required=False,
        )


class DeviceRequest(DomainResource):
    """
    Represents a request for a patient to employ a medical device. The device may be an implantable device, or an external assistive device, such as a walker.
    """

    _abstract = False
    _type = "DeviceRequest"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/DeviceRequest"

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
        description="External Request identifier",
        default=None,
    )
    instantiatesCanonical: Optional[ListType[fhir.canonical]] = Field(
        description="Instantiates FHIR protocol or definition",
        default=None,
    )
    instantiatesUri: Optional[ListType[fhir.uri]] = Field(
        description="Instantiates external protocol or definition",
        default=None,
    )
    basedOn: Optional[ListType[Reference]] = Field(
        description="What request fulfills",
        default=None,
    )
    priorRequest: Optional[ListType[Reference]] = Field(
        description="What request replaces",
        default=None,
    )
    groupIdentifier: Optional[Identifier] = Field(
        description="Identifier of composite request",
        default=None,
    )
    status: Optional[fhir.code] = Field(
        description="draft | active | on-hold | revoked | completed | entered-in-error | unknown",
        default=None,
    )
    intent: Optional[fhir.code] = Field(
        description="proposal | plan | directive | order | original-order | reflex-order | filler-order | instance-order | option",
        default=None,
    )
    priority: Optional[fhir.code] = Field(
        description="routine | urgent | asap | stat",
        default=None,
    )
    codeReference: Optional[Reference] = Field(
        description="Device requested",
        default=None,
    )
    codeCodeableConcept: Optional[CodeableConcept] = Field(
        description="Device requested",
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
    occurrenceDateTime: Optional[fhir.dateTime] = Field(
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
    authoredOn: Optional[fhir.dateTime] = Field(
        description="When recorded",
        default=None,
    )
    requester: Optional[Reference] = Field(
        description="Who/what is requesting diagnostics",
        default=None,
    )
    performerType: Optional[CodeableConcept] = Field(
        description="Filler role",
        default=None,
    )
    performer: Optional[Reference] = Field(
        description="Requested Filler",
        default=None,
    )
    reasonCode: Optional[ListType[CodeableConcept]] = Field(
        description="Coded Reason for request",
        default=None,
    )
    reasonReference: Optional[ListType[Reference]] = Field(
        description="Linked Reason for request",
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
    def code(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="code",
        )

    @property
    def occurrence(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="occurrence",
        )

    @model_validator(mode="after")
    def code_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Reference, CodeableConcept],
            field_name_base="code",
            required=True,
        )

    @model_validator(mode="after")
    def occurrence_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.dateTime, Period, Timing],
            field_name_base="occurrence",
            required=False,
        )
