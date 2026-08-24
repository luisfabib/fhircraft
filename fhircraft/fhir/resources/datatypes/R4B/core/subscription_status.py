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

    eventNumber: fhir.string = Field(
        description="Event number",
    )
    timestamp: Optional[fhir.instant] = Field(
        description="The instant this event occurred",
        default=None,
    )
    focus: Optional[Reference] = Field(
        description="The focus of this event",
        default=None,
    )
    additionalContext: Optional[ListType[Reference]] = Field(
        description="Additional context for this event",
        default=None,
    )

class SubscriptionStatus(DomainResource):
    """
    The SubscriptionStatus resource describes the state of a Subscription during notifications.
    """

    _abstract = False
    _type = "SubscriptionStatus"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/SubscriptionStatus"

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
    status: Optional[fhir.code] = Field(
        description="requested | active | error | off | entered-in-error",
        default=None,
    )
    type: fhir.code = Field(
        description="handshake | heartbeat | event-notification | query-status | query-event",
    )
    eventsSinceSubscriptionStart: Optional[fhir.string] = Field(
        description="Events since the Subscription was created",
        default=None,
    )
    notificationEvent: Optional[ListType[SubscriptionStatusNotificationEvent]] = Field(
        description="Detailed information about any events relevant to this notification",
        default=None,
    )
    subscription: Reference = Field(
        description="Reference to the Subscription responsible for this notification",
    )
    topic: Optional[fhir.canonical] = Field(
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
            expression="type = 'event-notification' implies (notificationEvent.exists() and notificationEvent.first().exists())",
            human="events listed in event notifications",
            key="sst-1",
            severity="error",
        )
