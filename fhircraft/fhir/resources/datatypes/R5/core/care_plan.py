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
    Reference,
    CodeableConcept,
    Period,
    CodeableReference,
    BackboneElement,
    Annotation,
)
from .resource import Resource
from .domain_resource import DomainResource

class CarePlanActivity(BackboneElement):
    """
    Identifies an action that has occurred or is a planned action to occur as part of the plan. For example, a medication to be used, lab tests to perform, self-monitoring that has occurred, education etc.
    """

    performedActivity: Optional[ListType[CodeableReference]] = Field(
        description="Results of the activity (concept, or Appointment, Encounter, Procedure, etc.)",
        default=None,
    )
    progress: Optional[ListType[Annotation]] = Field(
        description="Comments about the activity status/progress",
        default=None,
    )
    plannedActivityReference: Optional[Reference] = Field(
        description="Activity that is intended to be part of the care plan",
        default=None,
    )

class CarePlan(DomainResource):
    """
    Describes the intention of how one or more practitioners intend to deliver care for a particular patient, group or community for a period of time, possibly limited to care for a specific condition or set of conditions.
    """

    _abstract = False
    _type = "CarePlan"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/CarePlan"

    identifier: Optional[ListType[Identifier]] = Field(
        description="External Ids for this plan",
        default=None,
    )
    instantiatesCanonical: Optional[ListType[Canonical]] = Field(
        description="Instantiates FHIR protocol or definition",
        default=None,
    )
    instantiatesUri: Optional[ListType[Uri]] = Field(
        description="Instantiates external protocol or definition",
        default=None,
    )
    basedOn: Optional[ListType[Reference]] = Field(
        description="Fulfills plan, proposal or order",
        default=None,
    )
    replaces: Optional[ListType[Reference]] = Field(
        description="CarePlan replaced by this CarePlan",
        default=None,
    )
    partOf: Optional[ListType[Reference]] = Field(
        description="Part of referenced CarePlan",
        default=None,
    )
    status: Optional[Code] = Field(
        description="draft | active | on-hold | revoked | completed | entered-in-error | unknown",
        default=None,
    )
    intent: Optional[Code] = Field(
        description="proposal | plan | order | option | directive",
        default=None,
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description="Type of plan",
        default=None,
    )
    title: Optional[String] = Field(
        description="Human-friendly name for the care plan",
        default=None,
    )
    description: Optional[String] = Field(
        description="Summary of nature of plan",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="Who the care plan is for",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="The Encounter during which this CarePlan was created",
        default=None,
    )
    period: Optional[Period] = Field(
        description="Time period plan covers",
        default=None,
    )
    created: Optional[DateTime] = Field(
        description="Date record was first recorded",
        default=None,
    )
    custodian: Optional[Reference] = Field(
        description="Who is the designated responsible party",
        default=None,
    )
    contributor: Optional[ListType[Reference]] = Field(
        description="Who provided the content of the care plan",
        default=None,
    )
    careTeam: Optional[ListType[Reference]] = Field(
        description="Who\u0027s involved in plan?",
        default=None,
    )
    addresses: Optional[ListType[CodeableReference]] = Field(
        description="Health issues this plan addresses",
        default=None,
    )
    supportingInfo: Optional[ListType[Reference]] = Field(
        description="Information considered as part of plan",
        default=None,
    )
    goal: Optional[ListType[Reference]] = Field(
        description="Desired outcome of plan",
        default=None,
    )
    activity: Optional[ListType[CarePlanActivity]] = Field(
        description="Action to occur or has occurred as part of plan",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Comments about the plan",
        default=None,
    )
