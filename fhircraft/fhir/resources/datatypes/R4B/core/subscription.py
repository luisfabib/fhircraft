import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from ..primitive import *

from fhircraft.fhir.resources.datatypes.R4B.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    ContactPoint,
    BackboneElement,
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
    endpoint: Optional[Url] = Field(
        description="Where the channel points to",
        default=None,
    )
    payload: Optional[Code] = Field(
        description="MIME type to send, or omit for no payload",
        default=None,
    )
    header: Optional[ListType[String]] = Field(
        description="Usage depends on the channel type",
        default=None,
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
    contact: Optional[ListType[ContactPoint]] = Field(
        description="Contact details for source (e.g. troubleshooting)",
        default=None,
    )
    end: Optional[Instant] = Field(
        description="When to automatically delete the subscription",
        default=None,
    )
    reason: Optional[String] = Field(
        description="Description of why this subscription was created",
        default=None,
    )
    criteria: Optional[String] = Field(
        description="Rule for server push",
        default=None,
    )
    error: Optional[String] = Field(
        description="Latest error note",
        default=None,
    )
    channel: Optional[SubscriptionChannel] = Field(
        description="The channel on which to report matches to the criteria",
        default=None,
    )
