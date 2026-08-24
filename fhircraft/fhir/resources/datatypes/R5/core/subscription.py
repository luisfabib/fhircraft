from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators


import fhircraft.fhir.resources.datatypes.R5.primitive as fhir
from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    ContactPoint,
    Reference,
    BackboneElement,
    Coding,
)
from .resource import Resource
from .domain_resource import DomainResource

class SubscriptionFilterBy(BackboneElement):
    """
    The filter properties to be applied to narrow the subscription topic stream.  When multiple filters are applied, evaluates to true if all the conditions applicable to that resource are met; otherwise it returns false (i.e., logical AND).
    """

    resourceType: Optional[fhir.string] = Field(
        description="Allowed Resource (reference to definition) for this Subscription filter",
        default=None,
    )
    filterParameter: fhir.string = Field(
        description="Filter label defined in SubscriptionTopic",
    )
    comparator: Optional[fhir.code] = Field(
        description="eq | ne | gt | lt | ge | le | sa | eb | ap",
        default=None,
    )
    modifier: Optional[fhir.code] = Field(
        description="missing | exact | contains | not | text | in | not-in | below | above | type | identifier | of-type | code-text | text-advanced | iterate",
        default=None,
    )
    value: fhir.string = Field(
        description="Literal value or resource path",
    )

class SubscriptionParameter(BackboneElement):
    """
    Channel-dependent information to send as part of the notification (e.g., HTTP Headers).
    """

    name: fhir.string = Field(
        description="Name (key) of the parameter",
    )
    value: fhir.string = Field(
        description="Value of the parameter to use or pass through",
    )

class Subscription(DomainResource):
    """
    The subscription resource describes a particular client's request to be notified about a SubscriptionTopic.
    """

    _abstract = False
    _type = "Subscription"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Subscription"

    identifier: Optional[ListType[Identifier]] = Field(
        description="Additional identifiers (business identifier)",
        default=None,
    )
    name: Optional[fhir.string] = Field(
        description="Human readable name for this subscription",
        default=None,
    )
    status: fhir.code = Field(
        description="requested | active | error | off | entered-in-error",
    )
    topic: fhir.canonical = Field(
        description="Reference to the subscription topic being subscribed to",
    )
    contact: Optional[ListType[ContactPoint]] = Field(
        description="Contact details for source (e.g. troubleshooting)",
        default=None,
    )
    end: Optional[fhir.instant] = Field(
        description="When to automatically delete the subscription",
        default=None,
    )
    managingEntity: Optional[Reference] = Field(
        description="Entity responsible for Subscription changes",
        default=None,
    )
    reason: Optional[fhir.string] = Field(
        description="Description of why this subscription was created",
        default=None,
    )
    filterBy: Optional[ListType[SubscriptionFilterBy]] = Field(
        description="Criteria for narrowing the subscription topic stream",
        default=None,
    )
    channelType: Coding = Field(
        description="Channel type for notifications",
    )
    endpoint: Optional[fhir.url] = Field(
        description="Where the channel points to",
        default=None,
    )
    parameter: Optional[ListType[SubscriptionParameter]] = Field(
        description="Channel type",
        default=None,
    )
    heartbeatPeriod: Optional[fhir.unsignedInt] = Field(
        description="Interval in seconds to send \u0027heartbeat\u0027 notification",
        default=None,
    )
    timeout: Optional[fhir.unsignedInt] = Field(
        description="Timeout in seconds to attempt notification delivery",
        default=None,
    )
    contentType: Optional[fhir.code] = Field(
        description="MIME type to send, or omit for no payload",
        default=None,
    )
    content: Optional[fhir.code] = Field(
        description="empty | id-only | full-resource",
        default=None,
    )
    maxCount: Optional[fhir.positiveInt] = Field(
        description="Maximum number of events that can be combined in a single notification",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_scr_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("filterBy",),
            expression="(comparator.exists() and modifier.exists()).not()",
            human="Subscription filters may only contain a modifier or a comparator",
            key="scr-1",
            severity="error",
        )
