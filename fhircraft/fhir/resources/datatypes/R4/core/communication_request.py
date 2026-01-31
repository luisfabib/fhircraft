import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    Boolean,
    DateTime,
)

from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    BackboneElement,
    Annotation,
    Attachment,
    Period,
)
from .resource import Resource
from .domain_resource import DomainResource


class CommunicationRequestPayload(BackboneElement):
    """
    Text, attachment(s), or resource(s) to be communicated to the recipient.
    """

    contentString: Optional[String] = Field(
        description="Message part content",
        default=None,
    )
    contentString_ext: Optional[Element] = Field(
        description="Placeholder element for contentString extensions",
        default=None,
        alias="_contentString",
    )
    contentAttachment: Optional[Attachment] = Field(
        description="Message part content",
        default=None,
    )
    contentReference: Optional[Reference] = Field(
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
            field_types=[String, Attachment, Reference],
            field_name_base="content",
            required=True,
        )


class CommunicationRequest(DomainResource):
    """
    A request to convey information; e.g. the CDS system proposes that an alert be sent to a responsible provider, the CDS system proposes that the public health agency be notified about a reportable condition.
    """

    _abstract = False
    _type = "CommunicationRequest"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/CommunicationRequest"

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
        description="Unique identifier",
        default=None,
    )
    basedOn: Optional[ListType[Reference]] = Field(
        description="Fulfills plan or proposal",
        default=None,
    )
    replaces: Optional[ListType[Reference]] = Field(
        description="Request(s) replaced by this request",
        default=None,
    )
    groupIdentifier: Optional[Identifier] = Field(
        description="Composite request this is part of",
        default=None,
    )
    status: Optional[Code] = Field(
        description="draft | active | on-hold | revoked | completed | entered-in-error | unknown",
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
    category: Optional[ListType[CodeableConcept]] = Field(
        description="Message category",
        default=None,
    )
    priority: Optional[Code] = Field(
        description="routine | urgent | asap | stat",
        default=None,
    )
    priority_ext: Optional[Element] = Field(
        description="Placeholder element for priority extensions",
        default=None,
        alias="_priority",
    )
    doNotPerform: Optional[Boolean] = Field(
        description="True if request is prohibiting action",
        default=None,
    )
    doNotPerform_ext: Optional[Element] = Field(
        description="Placeholder element for doNotPerform extensions",
        default=None,
        alias="_doNotPerform",
    )
    medium: Optional[ListType[CodeableConcept]] = Field(
        description="A channel of communication",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="Focus of message",
        default=None,
    )
    about: Optional[ListType[Reference]] = Field(
        description="Resources that pertain to this communication request",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="Encounter created as part of",
        default=None,
    )
    payload: Optional[ListType[CommunicationRequestPayload]] = Field(
        description="Message payload",
        default=None,
    )
    occurrenceDateTime: Optional[DateTime] = Field(
        description="When scheduled",
        default=None,
    )
    occurrenceDateTime_ext: Optional[Element] = Field(
        description="Placeholder element for occurrenceDateTime extensions",
        default=None,
        alias="_occurrenceDateTime",
    )
    occurrencePeriod: Optional[Period] = Field(
        description="When scheduled",
        default=None,
    )
    authoredOn: Optional[DateTime] = Field(
        description="When request transitioned to being actionable",
        default=None,
    )
    authoredOn_ext: Optional[Element] = Field(
        description="Placeholder element for authoredOn extensions",
        default=None,
        alias="_authoredOn",
    )
    requester: Optional[Reference] = Field(
        description="Who/what is requesting service",
        default=None,
    )
    recipient: Optional[ListType[Reference]] = Field(
        description="Message recipient",
        default=None,
    )
    sender: Optional[Reference] = Field(
        description="Message sender",
        default=None,
    )
    reasonCode: Optional[ListType[CodeableConcept]] = Field(
        description="Why is communication needed?",
        default=None,
    )
    reasonReference: Optional[ListType[Reference]] = Field(
        description="Why is communication needed?",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Comments made about communication request",
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
            field_types=[DateTime, Period],
            field_name_base="occurrence",
            required=False,
        )
