from pydantic import Field, model_validator
from typing import Optional, List

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    Canonical,
    DateTime,
)

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

    performedActivity: Optional[List[CodeableReference]] = Field(
        description="Results of the activity (concept, or Appointment, Encounter, Procedure, etc.)",
        default=None,
    )
    progress: Optional[List[Annotation]] = Field(
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

    identifier: Optional[List[Identifier]] = Field(
        description="External Ids for this plan",
        default=None,
    )
    instantiatesCanonical: Optional[List[Canonical]] = Field(
        description="Instantiates FHIR protocol or definition",
        default=None,
    )
    instantiatesCanonical_ext: Optional[List[Optional[Element]]] = Field(
        description="Placeholder element for instantiatesCanonical extensions",
        default=None,
        alias="_instantiatesCanonical",
    )
    instantiatesUri: Optional[List[Uri]] = Field(
        description="Instantiates external protocol or definition",
        default=None,
    )
    instantiatesUri_ext: Optional[List[Optional[Element]]] = Field(
        description="Placeholder element for instantiatesUri extensions",
        default=None,
        alias="_instantiatesUri",
    )
    basedOn: Optional[List[Reference]] = Field(
        description="Fulfills plan, proposal or order",
        default=None,
    )
    replaces: Optional[List[Reference]] = Field(
        description="CarePlan replaced by this CarePlan",
        default=None,
    )
    partOf: Optional[List[Reference]] = Field(
        description="Part of referenced CarePlan",
        default=None,
    )
    status: Optional[Code] = Field(
        description="draft | active | on-hold | revoked | completed | entered-in-error | unknown",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    intent: Optional[Code] = Field(
        description="proposal | plan | order | option | directive",
        default=None,
    )
    intent_ext: Optional[Element] = Field(
        description="Placeholder element for intent extensions",
        default=None,
        alias="_intent",
    )
    category: Optional[List[CodeableConcept]] = Field(
        description="Type of plan",
        default=None,
    )
    title: Optional[String] = Field(
        description="Human-friendly name for the care plan",
        default=None,
    )
    title_ext: Optional[Element] = Field(
        description="Placeholder element for title extensions",
        default=None,
        alias="_title",
    )
    description: Optional[String] = Field(
        description="Summary of nature of plan",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
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
    created_ext: Optional[Element] = Field(
        description="Placeholder element for created extensions",
        default=None,
        alias="_created",
    )
    custodian: Optional[Reference] = Field(
        description="Who is the designated responsible party",
        default=None,
    )
    contributor: Optional[List[Reference]] = Field(
        description="Who provided the content of the care plan",
        default=None,
    )
    careTeam: Optional[List[Reference]] = Field(
        description="Who\u0027s involved in plan?",
        default=None,
    )
    addresses: Optional[List[CodeableReference]] = Field(
        description="Health issues this plan addresses",
        default=None,
    )
    supportingInfo: Optional[List[Reference]] = Field(
        description="Information considered as part of plan",
        default=None,
    )
    goal: Optional[List[Reference]] = Field(
        description="Desired outcome of plan",
        default=None,
    )
    activity: Optional[List[CarePlanActivity]] = Field(
        description="Action to occur or has occurred as part of plan",
        default=None,
    )
    note: Optional[List[Annotation]] = Field(
        description="Comments about the plan",
        default=None,
    )
