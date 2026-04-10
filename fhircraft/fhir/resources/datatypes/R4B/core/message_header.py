import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)


import fhircraft.fhir.resources.datatypes.R4B.primitive as fhir
from fhircraft.fhir.resources.datatypes.R4B.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Coding,
    BackboneElement,
    Reference,
    ContactPoint,
    CodeableConcept,
)
from .resource import Resource
from .domain_resource import DomainResource


class MessageHeaderDestination(BackboneElement):
    """
    The destination application which the message is intended for.
    """

    name: Optional[fhir.string] = Field(
        description="Name of system",
        default=None,
    )
    target: Optional[Reference] = Field(
        description="Particular delivery destination within the destination",
        default=None,
    )
    endpoint: Optional[fhir.url] = Field(
        description="Actual destination address or id",
        default=None,
    )
    receiver: Optional[Reference] = Field(
        description='Intended "real-world" recipient for the data',
        default=None,
    )


class MessageHeaderSource(BackboneElement):
    """
    The source application from which this message originated.
    """

    name: Optional[fhir.string] = Field(
        description="Name of system",
        default=None,
    )
    software: Optional[fhir.string] = Field(
        description="Name of software running the system",
        default=None,
    )
    version: Optional[fhir.string] = Field(
        description="Version of software running",
        default=None,
    )
    contact: Optional[ContactPoint] = Field(
        description="Human contact for problems",
        default=None,
    )
    endpoint: Optional[fhir.url] = Field(
        description="Actual message source address or id",
        default=None,
    )


class MessageHeaderResponse(BackboneElement):
    """
    Information about the message that this message is a response to.  Only present if this message is a response.
    """

    identifier: Optional[fhir.id_] = Field(
        description="id_ of original message",
        default=None,
    )
    code: Optional[fhir.code] = Field(
        description="ok | transient-error | fatal-error",
        default=None,
    )
    details: Optional[Reference] = Field(
        description="Specific list of hints/warnings/errors",
        default=None,
    )


class MessageHeader(DomainResource):
    """
    The header for a message exchange that is either requesting or responding to an action.  The reference(s) that are the subject of the action as well as other information related to the action are typically transmitted in a bundle in which the MessageHeader resource instance is the first resource in the bundle.
    """

    _abstract = False
    _type = "MessageHeader"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/MessageHeader"

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
    eventCoding: Optional[Coding] = Field(
        description="code for the event this message represents or link to event definition",
        default=None,
    )
    eventUri: Optional[fhir.uri] = Field(
        description="code for the event this message represents or link to event definition",
        default=None,
    )
    destination: Optional[ListType[MessageHeaderDestination]] = Field(
        description="Message destination application(s)",
        default=None,
    )
    sender: Optional[Reference] = Field(
        description="Real world sender of the message",
        default=None,
    )
    enterer: Optional[Reference] = Field(
        description="The source of the data entry",
        default=None,
    )
    author: Optional[Reference] = Field(
        description="The source of the decision",
        default=None,
    )
    source: Optional[MessageHeaderSource] = Field(
        description="Message source application",
        default=None,
    )
    responsible: Optional[Reference] = Field(
        description="Final responsibility for event",
        default=None,
    )
    reason: Optional[CodeableConcept] = Field(
        description="Cause of event",
        default=None,
    )
    response: Optional[MessageHeaderResponse] = Field(
        description="If this is a reply to prior message",
        default=None,
    )
    focus: Optional[ListType[Reference]] = Field(
        description="The actual content of the message",
        default=None,
    )
    definition: Optional[fhir.canonical] = Field(
        description="Link to the definition for this message",
        default=None,
    )

    @property
    def event(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="event",
        )

    @model_validator(mode="after")
    def event_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Coding, fhir.uri],
            field_name_base="event",
            required=True,
        )
