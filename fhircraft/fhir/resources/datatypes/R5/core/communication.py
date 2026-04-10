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
    CodeableReference,
    BackboneElement,
    Attachment,
    Annotation,
)
from .resource import Resource
from .domain_resource import DomainResource

class CommunicationPayload(BackboneElement):
    """
    Text, attachment(s), or resource(s) that was communicated to the recipient.
    """

    contentAttachment: Optional[Attachment] = Field(
        description="Message part content",
        default=None,
    )
    contentReference: Optional[Reference] = Field(
        description="Message part content",
        default=None,
    )
    contentCodeableConcept: Optional[CodeableConcept] = Field(
        description="Message part content",
        default=None,
    )

    @property
    def content(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="content",
        )

    @model_validator(mode="after")
    def content_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Attachment, Reference, CodeableConcept],
            field_name_base="content",
            required=True,
        )

class Communication(DomainResource):
    """
    A clinical or business level record of information being transmitted or shared; e.g. an alert that was sent to a responsible provider, a public health agency communication to a provider/reporter in response to a case report for a reportable condition.
    """

    _abstract = False
    _type = "Communication"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Communication"

    identifier: Optional[ListType[Identifier]] = Field(
        description="Unique identifier",
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
        description="Request fulfilled by this communication",
        default=None,
    )
    partOf: Optional[ListType[Reference]] = Field(
        description="Part of referenced event (e.g. Communication, Procedure)",
        default=None,
    )
    inResponseTo: Optional[ListType[Reference]] = Field(
        description="Reply to",
        default=None,
    )
    status: Optional[fhir.code] = Field(
        description="preparation | in-progress | not-done | on-hold | stopped | completed | entered-in-error | unknown",
        default=None,
    )
    statusReason: Optional[CodeableConcept] = Field(
        description="Reason for current status",
        default=None,
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description="Message category",
        default=None,
    )
    priority: Optional[fhir.code] = Field(
        description="routine | urgent | asap | stat",
        default=None,
    )
    medium: Optional[ListType[CodeableConcept]] = Field(
        description="A channel of communication",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="Focus of message",
        default=None,
    )
    topic: Optional[CodeableConcept] = Field(
        description="Description of the purpose/content",
        default=None,
    )
    about: Optional[ListType[Reference]] = Field(
        description="Resources that pertain to this communication",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="The Encounter during which this Communication was created",
        default=None,
    )
    sent: Optional[fhir.dateTime] = Field(
        description="When sent",
        default=None,
    )
    received: Optional[fhir.dateTime] = Field(
        description="When received",
        default=None,
    )
    recipient: Optional[ListType[Reference]] = Field(
        description="Who the information is shared with",
        default=None,
    )
    sender: Optional[Reference] = Field(
        description="Who shares the information",
        default=None,
    )
    reason: Optional[ListType[CodeableReference]] = Field(
        description="Indication for message",
        default=None,
    )
    payload: Optional[ListType[CommunicationPayload]] = Field(
        description="Message payload",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Comments made about the communication",
        default=None,
    )
