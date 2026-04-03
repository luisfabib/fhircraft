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
    Period,
    BackboneElement,
)
from .resource import Resource
from .domain_resource import DomainResource

class SubscriptionTopicResourceTriggerQueryCriteria(BackboneElement):
    """
    The FHIR query based rules that the server should use to determine when to trigger a notification for this subscription topic.
    """

    previous: Optional[String] = Field(
        description="Rule applied to previous resource state",
        default=None,
    )
    resultForCreate: Optional[Code] = Field(
        description="test-passes | test-fails",
        default=None,
    )
    current: Optional[String] = Field(
        description="Rule applied to current resource state",
        default=None,
    )
    resultForDelete: Optional[Code] = Field(
        description="test-passes | test-fails",
        default=None,
    )
    requireBoth: Optional[Boolean] = Field(
        description="Both must be true flag",
        default=None,
    )

class SubscriptionTopicResourceTrigger(BackboneElement):
    """
    A definition of a resource-based event that triggers a notification based on the SubscriptionTopic. The criteria may be just a human readable description and/or a full FHIR search string or FHIRPath expression. Multiple triggers are considered OR joined (e.g., a resource update matching ANY of the definitions will trigger a notification).
    """

    description: Optional[Markdown] = Field(
        description="Text representation of the resource trigger",
        default=None,
    )
    resource: Optional[Uri] = Field(
        description="Data Type or Resource (reference to definition) for this trigger definition",
        default=None,
    )
    supportedInteraction: Optional[ListType[Code]] = Field(
        description="create | update | delete",
        default=None,
    )
    queryCriteria: Optional[SubscriptionTopicResourceTriggerQueryCriteria] = Field(
        description="Query based trigger rule",
        default=None,
    )
    fhirPathCriteria: Optional[String] = Field(
        description="FHIRPath based trigger rule",
        default=None,
    )

class SubscriptionTopicEventTrigger(BackboneElement):
    """
    Event definition which can be used to trigger the SubscriptionTopic.
    """

    description: Optional[Markdown] = Field(
        description="Text representation of the event trigger",
        default=None,
    )
    event: Optional[CodeableConcept] = Field(
        description="Event which can trigger a notification from the SubscriptionTopic",
        default=None,
    )
    resource: Optional[Uri] = Field(
        description="Data Type or Resource (reference to definition) for this trigger definition",
        default=None,
    )

class SubscriptionTopicCanFilterBy(BackboneElement):
    """
    List of properties by which Subscriptions on the SubscriptionTopic can be filtered. May be defined Search Parameters (e.g., Encounter.patient) or parameters defined within this SubscriptionTopic context (e.g., hub.event).
    """

    description: Optional[Markdown] = Field(
        description="Description of this filter parameter",
        default=None,
    )
    resource: Optional[Uri] = Field(
        description="URL of the triggering Resource that this filter applies to",
        default=None,
    )
    filterParameter: Optional[String] = Field(
        description="Human-readable and computation-friendly name for a filter parameter usable by subscriptions on this topic, via Subscription.filterBy.filterParameter",
        default=None,
    )
    filterDefinition: Optional[Uri] = Field(
        description="Canonical URL for a filterParameter definition",
        default=None,
    )
    comparator: Optional[ListType[Code]] = Field(
        description="eq | ne | gt | lt | ge | le | sa | eb | ap",
        default=None,
    )
    modifier: Optional[ListType[Code]] = Field(
        description="missing | exact | contains | not | text | in | not-in | below | above | type | identifier | of-type | code-text | text-advanced | iterate",
        default=None,
    )

class SubscriptionTopicNotificationShape(BackboneElement):
    """
    List of properties to describe the shape (e.g., resources) included in notifications from this Subscription Topic.
    """

    resource: Optional[Uri] = Field(
        description="URL of the Resource that is the focus (main) resource in a notification shape",
        default=None,
    )
    include: Optional[ListType[String]] = Field(
        description="Include directives, rooted in the resource for this shape",
        default=None,
    )
    revInclude: Optional[ListType[String]] = Field(
        description="Reverse include directives, rooted in the resource for this shape",
        default=None,
    )

class SubscriptionTopic(DomainResource):
    """
    Describes a stream of resource state changes identified by trigger criteria and annotated with labels useful to filter projections from this topic.
    """

    _abstract = False
    _type = "SubscriptionTopic"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/SubscriptionTopic"

    url: Optional[Uri] = Field(
        description="Canonical identifier for this subscription topic, represented as an absolute URI (globally unique)",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Business identifier for subscription topic",
        default=None,
    )
    version: Optional[String] = Field(
        description="Business version of the subscription topic",
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
        description="Name for this subscription topic (computer friendly)",
        default=None,
    )
    title: Optional[String] = Field(
        description="Name for this subscription topic (human friendly)",
        default=None,
    )
    derivedFrom: Optional[ListType[Canonical]] = Field(
        description="Based on FHIR protocol or definition",
        default=None,
    )
    status: Optional[Code] = Field(
        description="draft | active | retired | unknown",
        default=None,
    )
    experimental: Optional[Boolean] = Field(
        description="If for testing purposes, not real usage",
        default=None,
    )
    date: Optional[DateTime] = Field(
        description="Date status first applied",
        default=None,
    )
    publisher: Optional[String] = Field(
        description="The name of the individual or organization that published the SubscriptionTopic",
        default=None,
    )
    contact: Optional[ListType[ContactDetail]] = Field(
        description="Contact details for the publisher",
        default=None,
    )
    description: Optional[Markdown] = Field(
        description="Natural language description of the SubscriptionTopic",
        default=None,
    )
    useContext: Optional[ListType[UsageContext]] = Field(
        description="Content intends to support these contexts",
        default=None,
    )
    jurisdiction: Optional[ListType[CodeableConcept]] = Field(
        description="Intended jurisdiction of the SubscriptionTopic (if applicable)",
        default=None,
    )
    purpose: Optional[Markdown] = Field(
        description="Why this SubscriptionTopic is defined",
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
    approvalDate: Optional[Date] = Field(
        description="When SubscriptionTopic is/was approved by publisher",
        default=None,
    )
    lastReviewDate: Optional[Date] = Field(
        description="Date the Subscription Topic was last reviewed by the publisher",
        default=None,
    )
    effectivePeriod: Optional[Period] = Field(
        description="The effective date range for the SubscriptionTopic",
        default=None,
    )
    resourceTrigger: Optional[ListType[SubscriptionTopicResourceTrigger]] = Field(
        description="Definition of a resource-based trigger for the subscription topic",
        default=None,
    )
    eventTrigger: Optional[ListType[SubscriptionTopicEventTrigger]] = Field(
        description="Event definitions the SubscriptionTopic",
        default=None,
    )
    canFilterBy: Optional[ListType[SubscriptionTopicCanFilterBy]] = Field(
        description="Properties by which a Subscription can filter notifications from the SubscriptionTopic",
        default=None,
    )
    notificationShape: Optional[ListType[SubscriptionTopicNotificationShape]] = Field(
        description="Properties for describing the shape of notifications generated by this topic",
        default=None,
    )

    @property
    def versionAlgorithm(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="versionAlgorithm",
        )

    @model_validator(mode="after")
    def versionAlgorithm_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[String, Coding],
            field_name_base="versionAlgorithm",
            required=False,
        )
