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
    Identifier,
    BackboneElement,
    Period,
    CodeableConcept,
    Reference,
)
from .resource import Resource
from .domain_resource import DomainResource

class EpisodeOfCareStatusHistory(BackboneElement):
    """
    The history of statuses that the EpisodeOfCare has been through (without requiring processing the history of the resource).
    """

    status: Optional[Code] = Field(
        description="planned | waitlist | active | onhold | finished | cancelled | entered-in-error",
        default=None,
    )
    period: Optional[Period] = Field(
        description="Duration the EpisodeOfCare was in the specified status",
        default=None,
    )

class EpisodeOfCareDiagnosis(BackboneElement):
    """
    The list of diagnosis relevant to this episode of care.
    """

    condition: Optional[Reference] = Field(
        description="Conditions/problems/diagnoses this episode of care is for",
        default=None,
    )
    role: Optional[CodeableConcept] = Field(
        description="Role that this diagnosis has within the episode of care (e.g. admission, billing, discharge \u2026)",
        default=None,
    )
    rank: Optional[PositiveInt] = Field(
        description="Ranking of the diagnosis (for each role type)",
        default=None,
    )

class EpisodeOfCare(DomainResource):
    """
    An association between a patient and an organization / healthcare provider(s) during which time encounters may occur. The managing organization assumes a level of responsibility for the patient during this time.
    """

    _abstract = False
    _type = "EpisodeOfCare"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/EpisodeOfCare"

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
    identifier: Optional[ListType[Identifier]] = Field(
        description="Business Identifier(s) relevant for this EpisodeOfCare",
        default=None,
    )
    status: Optional[Code] = Field(
        description="planned | waitlist | active | onhold | finished | cancelled | entered-in-error",
        default=None,
    )
    statusHistory: Optional[ListType[EpisodeOfCareStatusHistory]] = Field(
        description="Past list of status codes (the current status may be included to cover the start date of the status)",
        default=None,
    )
    type: Optional[ListType[CodeableConcept]] = Field(
        description="Type/class  - e.g. specialist referral, disease management",
        default=None,
    )
    diagnosis: Optional[ListType[EpisodeOfCareDiagnosis]] = Field(
        description="The list of diagnosis relevant to this episode of care",
        default=None,
    )
    patient: Optional[Reference] = Field(
        description="The patient who is the focus of this episode of care",
        default=None,
    )
    managingOrganization: Optional[Reference] = Field(
        description="Organization that assumes care",
        default=None,
    )
    period: Optional[Period] = Field(
        description="Interval during responsibility is assumed",
        default=None,
    )
    referralRequest: Optional[ListType[Reference]] = Field(
        description="Originating Referral Request(s)",
        default=None,
    )
    careManager: Optional[Reference] = Field(
        description="Care manager/care coordinator for the patient",
        default=None,
    )
    team: Optional[ListType[Reference]] = Field(
        description="Other practitioners facilitating this episode of care",
        default=None,
    )
    account: Optional[ListType[Reference]] = Field(
        description="The set of accounts that may be used for billing for this EpisodeOfCare",
        default=None,
    )
