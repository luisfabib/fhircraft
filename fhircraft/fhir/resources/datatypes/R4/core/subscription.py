import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    Instant,
    Url,
)

from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    BackboneElement,
    ContactPoint,
)
from .resource import Resource
from .domain_resource import DomainResource


class SubscriptionChannel(BackboneElement):
    """
    Details where to send notifications when resources are received that meet the criteria.
    """

    type: Optional[Code] = Field(
        description="rest-hook | websocket | email | sms | message",
        default=None,
    )
    type_ext: Optional[Element] = Field(
        description="Placeholder element for type extensions",
        default=None,
        alias="_type",
    )
    endpoint: Optional[Url] = Field(
        description="Where the channel points to",
        default=None,
    )
    endpoint_ext: Optional[Element] = Field(
        description="Placeholder element for endpoint extensions",
        default=None,
        alias="_endpoint",
    )
    payload: Optional[Code] = Field(
        description="MIME type to send, or omit for no payload",
        default=None,
    )
    payload_ext: Optional[Element] = Field(
        description="Placeholder element for payload extensions",
        default=None,
        alias="_payload",
    )
    header: Optional[ListType[String]] = Field(
        description="Usage depends on the channel type",
        default=None,
    )
    header_ext: Optional[Element] = Field(
        description="Placeholder element for header extensions",
        default=None,
        alias="_header",
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "header",
                "payload",
                "endpoint",
                "type",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class Subscription(DomainResource):
    """
    The subscription resource is used to define a push-based subscription from a server to another system. Once a subscription is registered with the server, the server checks every resource that is created or updated, and if the resource matches the given criteria, it sends a message on the defined "channel" so that another system can take an appropriate action.
    """

    _abstract = False
    _type = "Subscription"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Subscription"

    id: Optional[String] = Field(
        description="Logical id of this artifact",
        default=None,
    )
    id_ext: Optional[Element] = Field(
        description="Placeholder element for id extensions",
        default=None,
        alias="_id",
    )
    meta: Optional[Meta] = Field(
        description="Metadata about the resource.",
        default_factory=lambda: Meta(
            profile=["http://hl7.org/fhir/StructureDefinition/Subscription"]
        ),
    )
    implicitRules: Optional[Uri] = Field(
        description="A set of rules under which this content was created",
        default=None,
    )
    implicitRules_ext: Optional[Element] = Field(
        description="Placeholder element for implicitRules extensions",
        default=None,
        alias="_implicitRules",
    )
    language: Optional[Code] = Field(
        description="Language of the resource content",
        default=None,
    )
    language_ext: Optional[Element] = Field(
        description="Placeholder element for language extensions",
        default=None,
        alias="_language",
    )
    text: Optional[Narrative] = Field(
        description="Text summary of the resource, for human interpretation",
        default=None,
    )
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
    status: Optional[Code] = Field(
        description="requested | active | error | off",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    contact: Optional[ListType[ContactPoint]] = Field(
        description="Contact details for source (e.g. troubleshooting)",
        default=None,
    )
    end: Optional[Instant] = Field(
        description="When to automatically delete the subscription",
        default=None,
    )
    end_ext: Optional[Element] = Field(
        description="Placeholder element for end extensions",
        default=None,
        alias="_end",
    )
    reason: Optional[String] = Field(
        description="Description of why this subscription was created",
        default=None,
    )
    reason_ext: Optional[Element] = Field(
        description="Placeholder element for reason extensions",
        default=None,
        alias="_reason",
    )
    criteria: Optional[String] = Field(
        description="Rule for server push",
        default=None,
    )
    criteria_ext: Optional[Element] = Field(
        description="Placeholder element for criteria extensions",
        default=None,
        alias="_criteria",
    )
    error: Optional[String] = Field(
        description="Latest error note",
        default=None,
    )
    error_ext: Optional[Element] = Field(
        description="Placeholder element for error extensions",
        default=None,
        alias="_error",
    )
    channel: Optional[SubscriptionChannel] = Field(
        description="The channel on which to report matches to the criteria",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "channel",
                "error",
                "criteria",
                "reason",
                "end",
                "contact",
                "status",
                "modifierExtension",
                "extension",
                "text",
                "language",
                "implicitRules",
                "meta",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ext_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "modifierExtension",
                "extension",
            ),
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_dom_2_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="contained.contained.empty()",
            human="If the resource is contained in another resource, it SHALL NOT contain nested Resources",
            key="dom-2",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_dom_3_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="contained.where((('#'+id in (%resource.descendants().reference | %resource.descendants().ofType(canonical) | %resource.descendants().ofType(uri) | %resource.descendants().ofType(url))) or descendants().where(reference = '#').exists() or descendants().where(as(canonical) = '#').exists() or descendants().where(as(canonical) = '#').exists()).not()).trace('unmatched', id).empty()",
            human="If the resource is contained in another resource, it SHALL be referred to from elsewhere in the resource or SHALL refer to the containing resource",
            key="dom-3",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_dom_4_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="contained.meta.versionId.empty() and contained.meta.lastUpdated.empty()",
            human="If a resource is contained in another resource, it SHALL NOT have a meta.versionId or a meta.lastUpdated",
            key="dom-4",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_dom_5_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="contained.meta.security.empty()",
            human="If a resource is contained in another resource, it SHALL NOT have a security label",
            key="dom-5",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_dom_6_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="text.`div`.exists()",
            human="A resource should have narrative for robust management",
            key="dom-6",
            severity="warning",
        )
