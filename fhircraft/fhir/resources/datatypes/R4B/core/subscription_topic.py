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
    Period,
    BackboneElement,
)
from .resource import Resource
from .domain_resource import DomainResource


class SubscriptionTopicResourceTriggerQueryCriteria(BackboneElement):
    """
    The FHIR query based rules that the server should use to determine when to trigger a notification for this subscription topic.
    """

    previous: Optional[fhir.string] = Field(
        description="Rule applied to previous resource state",
        default=None,
    )
    resultForCreate: Optional[fhir.code] = Field(
        description="test-passes | test-fails",
        default=None,
    )
    current: Optional[fhir.string] = Field(
        description="Rule applied to current resource state",
        default=None,
    )
    resultForDelete: Optional[fhir.code] = Field(
        description="test-passes | test-fails",
        default=None,
    )
    requireBoth: Optional[fhir.boolean] = Field(
        description="Both must be true flag",
        default=None,
    )


class SubscriptionTopicResourceTrigger(BackboneElement):
    """
    A definition of a resource-based event that triggers a notification based on the SubscriptionTopic. The criteria may be just a human readable description and/or a full FHIR search string or FHIRPath expression. Multiple triggers are considered OR joined (e.g., a resource update matching ANY of the definitions will trigger a notification).
    """

    description: Optional[fhir.markdown] = Field(
        description="Text representation of the resource trigger",
        default=None,
    )
    resource: fhir.uri = Field(
        description="Data Type or Resource (reference to definition) for this trigger definition",
    )
    supportedInteraction: Optional[ListType[fhir.code]] = Field(
        description="create | update | delete",
        default=None,
    )
    queryCriteria: Optional[SubscriptionTopicResourceTriggerQueryCriteria] = Field(
        description="Query based trigger rule",
        default=None,
    )
    fhirPathCriteria: Optional[fhir.string] = Field(
        description="FHIRPath based trigger rule",
        default=None,
    )


class SubscriptionTopicEventTrigger(BackboneElement):
    """
    Event definition which can be used to trigger the SubscriptionTopic.
    """

    description: Optional[fhir.markdown] = Field(
        description="Text representation of the event trigger",
        default=None,
    )
    event: CodeableConcept = Field(
        description="Event which can trigger a notification from the SubscriptionTopic",
    )
    resource: fhir.uri = Field(
        description="Data Type or Resource (reference to definition) for this trigger definition",
    )


class SubscriptionTopicCanFilterBy(BackboneElement):
    """
    List of properties by which Subscriptions on the SubscriptionTopic can be filtered. May be defined Search Parameters (e.g., Encounter.patient) or parameters defined within this SubscriptionTopic context (e.g., hub.event).
    """

    description: Optional[fhir.markdown] = Field(
        description="Description of this filter parameter",
        default=None,
    )
    resource: Optional[fhir.uri] = Field(
        description="URL of the triggering Resource that this filter applies to",
        default=None,
    )
    filterParameter: fhir.string = Field(
        description="Human-readable and computation-friendly name for a filter parameter usable by subscriptions on this topic, via Subscription.filterBy.filterParameter",
    )
    filterDefinition: Optional[fhir.uri] = Field(
        description="canonical URL for a filterParameter definition",
        default=None,
    )
    modifier: Optional[ListType[fhir.code]] = Field(
        description="= | eq | ne | gt | lt | ge | le | sa | eb | ap | above | below | in | not-in | of-type",
        default=None,
    )


class SubscriptionTopicNotificationShape(BackboneElement):
    """
    List of properties to describe the shape (e.g., resources) included in notifications from this Subscription Topic.
    """

    resource: fhir.uri = Field(
        description="URL of the Resource that is the focus (main) resource in a notification shape",
    )
    include: Optional[ListType[fhir.string]] = Field(
        description="Include directives, rooted in the resource for this shape",
        default=None,
    )
    revInclude: Optional[ListType[fhir.string]] = Field(
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
    url: fhir.uri = Field(
        description="canonical identifier for this subscription topic definition, represented as a URI (globally unique)",
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Business Identifier for this subscription topic",
        default=None,
    )
    version: Optional[fhir.string] = Field(
        description="Business version of the subscription topic",
        default=None,
    )
    title: Optional[fhir.string] = Field(
        description="Name for this subscription topic (Human friendly)",
        default=None,
    )
    derivedFrom: Optional[ListType[fhir.canonical]] = Field(
        description="Based on FHIR protocol or definition",
        default=None,
    )
    status: fhir.code = Field(
        description="draft | active | retired | unknown",
    )
    experimental: Optional[fhir.boolean] = Field(
        description="If for testing purposes, not real usage",
        default=None,
    )
    date: Optional[fhir.dateTime] = Field(
        description="Date status first applied",
        default=None,
    )
    publisher: Optional[fhir.string] = Field(
        description="The name of the individual or organization that published the SubscriptionTopic",
        default=None,
    )
    contact: Optional[ListType[ContactDetail]] = Field(
        description="Contact details for the publisher",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
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
    purpose: Optional[fhir.markdown] = Field(
        description="Why this SubscriptionTopic is defined",
        default=None,
    )
    copyright: Optional[fhir.markdown] = Field(
        description="Use and/or publishing restrictions",
        default=None,
    )
    approvalDate: Optional[fhir.date_] = Field(
        description="When SubscriptionTopic is/was approved by publisher",
        default=None,
    )
    lastReviewDate: Optional[fhir.date_] = Field(
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
