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
    BackboneElement,
    Period,
    CodeableConcept,
    CodeableReference,
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

class EpisodeOfCareReason(BackboneElement):
    """
    The list of medical reasons that are expected to be addressed during the episode of care.
    """

    use: Optional[CodeableConcept] = Field(
        description="What the reason value should be used for/as",
        default=None,
    )
    value: Optional[ListType[CodeableReference]] = Field(
        description="Medical reason to be addressed",
        default=None,
    )

class EpisodeOfCareDiagnosis(BackboneElement):
    """
    The list of medical conditions that were addressed during the episode of care.
    """

    condition: Optional[ListType[CodeableReference]] = Field(
        description="The medical condition that was addressed during the episode of care",
        default=None,
    )
    use: Optional[CodeableConcept] = Field(
        description="Role that this diagnosis has within the episode of care (e.g. admission, billing, discharge \u2026)",
        default=None,
    )

class EpisodeOfCare(DomainResource):
    """
    An association between a patient and an organization / healthcare provider(s) during which time encounters may occur. The managing organization assumes a level of responsibility for the patient during this time.
    """

    _abstract = False
    _type = "EpisodeOfCare"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/EpisodeOfCare"

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
    reason: Optional[ListType[EpisodeOfCareReason]] = Field(
        description="The list of medical reasons that are expected to be addressed during the episode of care",
        default=None,
    )
    diagnosis: Optional[ListType[EpisodeOfCareDiagnosis]] = Field(
        description="The list of medical conditions that were addressed during the episode of care",
        default=None,
    )
    patient: Optional[Reference] = Field(
        description="The patient who is the focus of this episode of care",
        default=None,
    )
    managingOrganization: Optional[Reference] = Field(
        description="Organization that assumes responsibility for care coordination",
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
    careTeam: Optional[ListType[Reference]] = Field(
        description="Other practitioners facilitating this episode of care",
        default=None,
    )
    account: Optional[ListType[Reference]] = Field(
        description="The set of accounts that may be used for billing for this EpisodeOfCare",
        default=None,
    )
