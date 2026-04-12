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
    Identifier,
    ContactDetail,
    UsageContext,
    CodeableConcept,
    Coding,
    BackboneElement,
)
from .resource import Resource
from .domain_resource import DomainResource


class MessageDefinitionFocus(BackboneElement):
    """
    Identifies the resource (or resources) that are being addressed by the event.  For example, the Encounter for an admit message or two Account records for a merge.
    """

    code: Optional[fhir.code] = Field(
        description="Type of resource",
        default=None,
    )
    profile: Optional[fhir.canonical] = Field(
        description="Profile that must be adhered to by focus",
        default=None,
    )
    min: Optional[fhir.unsignedInt] = Field(
        description="Minimum number of focuses of this type",
        default=None,
    )
    max: Optional[fhir.string] = Field(
        description="Maximum number of focuses of this type",
        default=None,
    )


class MessageDefinitionAllowedResponse(BackboneElement):
    """
    Indicates what types of messages may be sent as an application-level response to this message.
    """

    message: Optional[fhir.canonical] = Field(
        description="Reference to allowed message definition response",
        default=None,
    )
    situation: Optional[fhir.markdown] = Field(
        description="When should this response be used",
        default=None,
    )


class MessageDefinition(DomainResource):
    """
    Defines the characteristics of a message that can be shared between systems, including the type of event that initiates the message, the content to be transmitted and what response(s), if any, are permitted.
    """

    _abstract = False
    _type = "MessageDefinition"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/MessageDefinition"

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
    url: Optional[fhir.uri] = Field(
        description="Business Identifier for a given MessageDefinition",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Primary key for the message definition on a given server",
        default=None,
    )
    version: Optional[fhir.string] = Field(
        description="Business version of the message definition",
        default=None,
    )
    name: Optional[fhir.string] = Field(
        description="Name for this message definition (computer friendly)",
        default=None,
    )
    title: Optional[fhir.string] = Field(
        description="Name for this message definition (human friendly)",
        default=None,
    )
    replaces: Optional[ListType[fhir.canonical]] = Field(
        description="Takes the place of",
        default=None,
    )
    status: Optional[fhir.code] = Field(
        description="draft | active | retired | unknown",
        default=None,
    )
    experimental: Optional[fhir.boolean] = Field(
        description="For testing purposes, not real usage",
        default=None,
    )
    date: Optional[fhir.dateTime] = Field(
        description="Date last changed",
        default=None,
    )
    publisher: Optional[fhir.string] = Field(
        description="Name of the publisher (organization or individual)",
        default=None,
    )
    contact: Optional[ListType[ContactDetail]] = Field(
        description="Contact details for the publisher",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
        description="Natural language description of the message definition",
        default=None,
    )
    useContext: Optional[ListType[UsageContext]] = Field(
        description="The context that the content is intended to support",
        default=None,
    )
    jurisdiction: Optional[ListType[CodeableConcept]] = Field(
        description="Intended jurisdiction for message definition (if applicable)",
        default=None,
    )
    purpose: Optional[fhir.markdown] = Field(
        description="Why this message definition is defined",
        default=None,
    )
    copyright: Optional[fhir.markdown] = Field(
        description="Use and/or publishing restrictions",
        default=None,
    )
    base: Optional[fhir.canonical] = Field(
        description="Definition this one is based on",
        default=None,
    )
    parent: Optional[ListType[fhir.canonical]] = Field(
        description="Protocol/workflow this is part of",
        default=None,
    )
    eventCoding: Optional[Coding] = Field(
        description="Event code  or link to the EventDefinition",
        default=None,
    )
    eventUri: Optional[fhir.uri] = Field(
        description="Event code  or link to the EventDefinition",
        default=None,
    )
    category: Optional[fhir.code] = Field(
        description="consequence | currency | notification",
        default=None,
    )
    focus: Optional[ListType[MessageDefinitionFocus]] = Field(
        description="Resource(s) that are the subject of the event",
        default=None,
    )
    responseRequired: Optional[fhir.code] = Field(
        description="always | on-error | never | on-success",
        default=None,
    )
    allowedResponse: Optional[ListType[MessageDefinitionAllowedResponse]] = Field(
        description="Responses to this message",
        default=None,
    )
    graph: Optional[ListType[fhir.canonical]] = Field(
        description="canonical reference to a GraphDefinition",
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
            field_types=[Coding, fhir.Uri],
            field_name_base="event",
            required=True,
        )

    @model_validator(mode="after")
    def FHIR_md_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("focus",),
            expression="max='*' or (max.toInteger() > 0)",
            human="Max must be postive int or *",
            key="md-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_msd_0_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.exists() implies name.matches('[A-Z]([A-Za-z0-9_]){0,254}')",
            human="Name should be usable as an identifier for the module by machine processing applications such as code generation",
            key="msd-0",
            severity="warning",
        )
