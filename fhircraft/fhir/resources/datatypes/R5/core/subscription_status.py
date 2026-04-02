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
    BackboneElement,
    Reference,
    CodeableConcept,
)
from .resource import Resource
from .domain_resource import DomainResource

class SubscriptionStatusNotificationEvent(BackboneElement):
    """
    Detailed information about events relevant to this subscription notification.
    """

    eventNumber: Optional[Integer64] = Field(
        description="Sequencing index of this event",
        default=None,
    )
    timestamp: Optional[Instant] = Field(
        description="The instant this event occurred",
        default=None,
    )
    focus: Optional[Reference] = Field(
        description="Reference to the primary resource or information of this event",
        default=None,
    )
    additionalContext: Optional[ListType[Reference]] = Field(
        description="References related to the focus resource and/or context of this event",
        default=None,
    )

class SubscriptionStatus(DomainResource):
    """
    The SubscriptionStatus resource describes the state of a Subscription during notifications. It is not persisted.
    """

    _abstract = False
    _type = "SubscriptionStatus"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/SubscriptionStatus"

    status: Optional[Code] = Field(
        description="requested | active | error | off | entered-in-error",
        default=None,
    )
    type: Optional[Code] = Field(
        description="handshake | heartbeat | event-notification | query-status | query-event",
        default=None,
    )
    eventsSinceSubscriptionStart: Optional[Integer64] = Field(
        description="Events since the Subscription was created",
        default=None,
    )
    notificationEvent: Optional[ListType[SubscriptionStatusNotificationEvent]] = Field(
        description="Detailed information about any events relevant to this notification",
        default=None,
    )
    subscription: Optional[Reference] = Field(
        description="Reference to the Subscription responsible for this notification",
        default=None,
    )
    topic: Optional[Canonical] = Field(
        description="Reference to the SubscriptionTopic this notification relates to",
        default=None,
    )
    error: Optional[ListType[CodeableConcept]] = Field(
        description="List of errors on the subscription",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_sst_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(type = 'event-notification' or type = 'query-event') implies notificationEvent.exists()",
            human="Event notifications must contain events",
            key="sst-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_sst_2_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="type = 'query-status' implies status.exists()",
            human="Status messages must contain status",
            key="sst-2",
            severity="error",
        )
