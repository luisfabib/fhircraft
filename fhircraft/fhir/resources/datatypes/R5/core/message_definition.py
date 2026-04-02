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
    Coding,
    ContactDetail,
    UsageContext,
    CodeableConcept,
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
    profile: Optional[Canonical] = Field(
        description="Profile that must be adhered to by focus",
        default=None,
    )
    min: Optional[UnsignedInt] = Field(
        description="Minimum number of focuses of this type",
        default=None,
    )
    max: Optional[String] = Field(
        description="Maximum number of focuses of this type",
        default=None,
    )

class MessageDefinitionAllowedResponse(BackboneElement):
    """
    Indicates what types of messages may be sent as an application-level response to this message.
    """

    message: Optional[Canonical] = Field(
        description="Reference to allowed message definition response",
        default=None,
    )
    situation: Optional[Markdown] = Field(
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

    url: Optional[Uri] = Field(
        description="The cannonical URL for a given MessageDefinition",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Business Identifier for a given MessageDefinition",
        default=None,
    )
    version: Optional[String] = Field(
        description="Business version of the message definition",
        default=None,
    )
    versionAlgorithmString: Optional[String] = Field(
        description="How to compare versions",
        default=None,
    )
    versionAlgorithmCoding: Optional[Coding] = Field(
        description="How to compare versions",
        default=None,
    )
    name: Optional[String] = Field(
        description="Name for this message definition (computer friendly)",
        default=None,
    )
    title: Optional[String] = Field(
        description="Name for this message definition (human friendly)",
        default=None,
    )
    replaces: Optional[ListType[Canonical]] = Field(
        description="Takes the place of",
        default=None,
    )
    status: Optional[Code] = Field(
        description="draft | active | retired | unknown",
        default=None,
    )
    experimental: Optional[Boolean] = Field(
        description="For testing purposes, not real usage",
        default=None,
    )
    date: Optional[DateTime] = Field(
        description="Date last changed",
        default=None,
    )
    publisher: Optional[String] = Field(
        description="Name of the publisher/steward (organization or individual)",
        default=None,
    )
    contact: Optional[ListType[ContactDetail]] = Field(
        description="Contact details for the publisher",
        default=None,
    )
    description: Optional[Markdown] = Field(
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
    purpose: Optional[Markdown] = Field(
        description="Why this message definition is defined",
        default=None,
    )
    copyright: Optional[Markdown] = Field(
        description="Use and/or publishing restrictions",
        default=None,
    )
    copyrightLabel: Optional[String] = Field(
        description="Copyright holder and year(s)",
        default=None,
    )
    base: Optional[Canonical] = Field(
        description="Definition this one is based on",
        default=None,
    )
    parent: Optional[ListType[Canonical]] = Field(
        description="Protocol/workflow this is part of",
        default=None,
    )
    eventCoding: Optional[Coding] = Field(
        description="Event code  or link to the EventDefinition",
        default=None,
    )
    eventUri: Optional[Uri] = Field(
        description="Event code  or link to the EventDefinition",
        default=None,
    )
    category: Optional[Code] = Field(
        description="consequence | currency | notification",
        default=None,
    )
    focus: Optional[ListType[MessageDefinitionFocus]] = Field(
        description="Resource(s) that are the subject of the event",
        default=None,
    )
    responseRequired: Optional[Code] = Field(
        description="always | on-error | never | on-success",
        default=None,
    )
    allowedResponse: Optional[ListType[MessageDefinitionAllowedResponse]] = Field(
        description="Responses to this message",
        default=None,
    )
    graph: Optional[Canonical] = Field(
        description="Canonical reference to a GraphDefinition",
        default=None,
    )

    @property
    def versionAlgorithm(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="versionAlgorithm",
        )

    @property
    def event(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="event",
        )

    @model_validator(mode="after")
    def versionAlgorithm_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[String, Coding],
            field_name_base="versionAlgorithm",
            required=False,
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
    def FHIR_cnl_0_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.exists() implies name.matches('^[A-Z]([A-Za-z0-9_]){1,254}$')",
            human="Name should be usable as an identifier for the module by machine processing applications such as code generation",
            key="cnl-0",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_cnl_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("url",),
            expression="exists() implies matches('^[^|# ]+$')",
            human="URL should not contain | or # - these characters make processing canonical references problematic",
            key="cnl-1",
            severity="warning",
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
