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

from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Reference,
    Annotation,
    CodeableConcept,
    BackboneElement,
    Attachment,
)
from .resource import Resource
from .domain_resource import DomainResource


class CommunicationPayload(BackboneElement):
    """
    Text, attachment(s), or resource(s) that was communicated to the recipient.
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


class Communication(DomainResource):
    """
    An occurrence of information being transmitted; e.g. an alert that was sent to a responsible provider, a public health agency that was notified about a reportable condition.
    """

    _abstract = False
    _type = "Communication"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Communication"

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
        description="Request fulfilled by this communication",
        default=None,
    )
    partOf: Optional[ListType[Reference]] = Field(
        description="Part of this action",
        default=None,
    )
    inResponseTo: Optional[ListType[Reference]] = Field(
        description="Reply to",
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
        description="Encounter created as part of",
        default=None,
    )
    sent: Optional[DateTime] = Field(
        description="When sent",
        default=None,
    )
    sent_ext: Optional[Element] = Field(
        description="Placeholder element for sent extensions",
        default=None,
        alias="_sent",
    )
    received: Optional[DateTime] = Field(
        description="When received",
        default=None,
    )
    received_ext: Optional[Element] = Field(
        description="Placeholder element for received extensions",
        default=None,
        alias="_received",
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
        description="Indication for message",
        default=None,
    )
    reasonReference: Optional[ListType[Reference]] = Field(
        description="Why was communication done?",
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
