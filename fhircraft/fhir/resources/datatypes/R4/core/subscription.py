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


class Subscription(DomainResource):
    """
    The subscription resource is used to define a push-based subscription from a server to another system. Once a subscription is registered with the server, the server checks every resource that is created or updated, and if the resource matches the given criteria, it sends a message on the defined "channel" so that another system can take an appropriate action.
    """

    _abstract = False
    _type = "Subscription"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Subscription"

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
