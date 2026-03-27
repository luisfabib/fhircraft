import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    Canonical,
    Boolean,
    DateTime,
    Markdown,
    UnsignedInt,
)

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

    code: Optional[Code] = Field(
        description="Type of resource",
        default=None,
    )
    code_ext: Optional[Element] = Field(
        description="Placeholder element for code extensions",
        default=None,
        alias="_code",
    )
    profile: Optional[Canonical] = Field(
        description="Profile that must be adhered to by focus",
        default=None,
    )
    profile_ext: Optional[Element] = Field(
        description="Placeholder element for profile extensions",
        default=None,
        alias="_profile",
    )
    min: Optional[UnsignedInt] = Field(
        description="Minimum number of focuses of this type",
        default=None,
    )
    min_ext: Optional[Element] = Field(
        description="Placeholder element for min extensions",
        default=None,
        alias="_min",
    )
    max: Optional[String] = Field(
        description="Maximum number of focuses of this type",
        default=None,
    )
    max_ext: Optional[Element] = Field(
        description="Placeholder element for max extensions",
        default=None,
        alias="_max",
    )


class MessageDefinitionAllowedResponse(BackboneElement):
    """
    Indicates what types of messages may be sent as an application-level response to this message.
    """

    message: Optional[Canonical] = Field(
        description="Reference to allowed message definition response",
        default=None,
    )
    message_ext: Optional[Element] = Field(
        description="Placeholder element for message extensions",
        default=None,
        alias="_message",
    )
    situation: Optional[Markdown] = Field(
        description="When should this response be used",
        default=None,
    )
    situation_ext: Optional[Element] = Field(
        description="Placeholder element for situation extensions",
        default=None,
        alias="_situation",
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
    url: Optional[Uri] = Field(
        description="Business Identifier for a given MessageDefinition",
        default=None,
    )
    url_ext: Optional[Element] = Field(
        description="Placeholder element for url extensions",
        default=None,
        alias="_url",
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Primary key for the message definition on a given server",
        default=None,
    )
    version: Optional[String] = Field(
        description="Business version of the message definition",
        default=None,
    )
    version_ext: Optional[Element] = Field(
        description="Placeholder element for version extensions",
        default=None,
        alias="_version",
    )
    name: Optional[String] = Field(
        description="Name for this message definition (computer friendly)",
        default=None,
    )
    name_ext: Optional[Element] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    title: Optional[String] = Field(
        description="Name for this message definition (human friendly)",
        default=None,
    )
    title_ext: Optional[Element] = Field(
        description="Placeholder element for title extensions",
        default=None,
        alias="_title",
    )
    replaces: Optional[ListType[Canonical]] = Field(
        description="Takes the place of",
        default=None,
    )
    replaces_ext: Optional[Element] = Field(
        description="Placeholder element for replaces extensions",
        default=None,
        alias="_replaces",
    )
    status: Optional[Code] = Field(
        description="draft | active | retired | unknown",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    experimental: Optional[Boolean] = Field(
        description="For testing purposes, not real usage",
        default=None,
    )
    experimental_ext: Optional[Element] = Field(
        description="Placeholder element for experimental extensions",
        default=None,
        alias="_experimental",
    )
    date: Optional[DateTime] = Field(
        description="Date last changed",
        default=None,
    )
    date_ext: Optional[Element] = Field(
        description="Placeholder element for date extensions",
        default=None,
        alias="_date",
    )
    publisher: Optional[String] = Field(
        description="Name of the publisher (organization or individual)",
        default=None,
    )
    publisher_ext: Optional[Element] = Field(
        description="Placeholder element for publisher extensions",
        default=None,
        alias="_publisher",
    )
    contact: Optional[ListType[ContactDetail]] = Field(
        description="Contact details for the publisher",
        default=None,
    )
    description: Optional[Markdown] = Field(
        description="Natural language description of the message definition",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    useContext: Optional[ListType[UsageContext]] = Field(
        description="The context that the content is intended to support",
        default=None,
    )
    jurisdiction: Optional[ListType[CodeableConcept]] = Field(
        description="Intended jurisdiction for message definition (if applicable)",
        default=None,
    )
    purpose: Optional[Markdown] = Field(
        description="Why this message definition is defined",
        default=None,
    )
    purpose_ext: Optional[Element] = Field(
        description="Placeholder element for purpose extensions",
        default=None,
        alias="_purpose",
    )
    copyright: Optional[Markdown] = Field(
        description="Use and/or publishing restrictions",
        default=None,
    )
    copyright_ext: Optional[Element] = Field(
        description="Placeholder element for copyright extensions",
        default=None,
        alias="_copyright",
    )
    base: Optional[Canonical] = Field(
        description="Definition this one is based on",
        default=None,
    )
    base_ext: Optional[Element] = Field(
        description="Placeholder element for base extensions",
        default=None,
        alias="_base",
    )
    parent: Optional[ListType[Canonical]] = Field(
        description="Protocol/workflow this is part of",
        default=None,
    )
    parent_ext: Optional[Element] = Field(
        description="Placeholder element for parent extensions",
        default=None,
        alias="_parent",
    )
    eventCoding: Optional[Coding] = Field(
        description="Event code  or link to the EventDefinition",
        default=None,
    )
    eventUri: Optional[Uri] = Field(
        description="Event code  or link to the EventDefinition",
        default=None,
    )
    eventUri_ext: Optional[Element] = Field(
        description="Placeholder element for eventUri extensions",
        default=None,
        alias="_eventUri",
    )
    category: Optional[Code] = Field(
        description="consequence | currency | notification",
        default=None,
    )
    category_ext: Optional[Element] = Field(
        description="Placeholder element for category extensions",
        default=None,
        alias="_category",
    )
    focus: Optional[ListType[MessageDefinitionFocus]] = Field(
        description="Resource(s) that are the subject of the event",
        default=None,
    )
    responseRequired: Optional[Code] = Field(
        description="always | on-error | never | on-success",
        default=None,
    )
    responseRequired_ext: Optional[Element] = Field(
        description="Placeholder element for responseRequired extensions",
        default=None,
        alias="_responseRequired",
    )
    allowedResponse: Optional[ListType[MessageDefinitionAllowedResponse]] = Field(
        description="Responses to this message",
        default=None,
    )
    graph: Optional[ListType[Canonical]] = Field(
        description="Canonical reference to a GraphDefinition",
        default=None,
    )
    graph_ext: Optional[Element] = Field(
        description="Placeholder element for graph extensions",
        default=None,
        alias="_graph",
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
            field_types=[Coding, Uri],
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
