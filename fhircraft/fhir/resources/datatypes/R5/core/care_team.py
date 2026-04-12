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
    CodeableConcept,
    Reference,
    Period,
    BackboneElement,
    Timing,
    CodeableReference,
    ContactPoint,
    Annotation,
)
from .resource import Resource
from .domain_resource import DomainResource

class CareTeamParticipant(BackboneElement):
    """
    Identifies all people and organizations who are expected to be involved in the care team.
    """

    role: Optional[CodeableConcept] = Field(
        description="Type of involvement",
        default=None,
    )
    member: Optional[Reference] = Field(
        description="Who is involved",
        default=None,
    )
    onBehalfOf: Optional[Reference] = Field(
        description="Organization of the practitioner",
        default=None,
    )
    coveragePeriod: Optional[Period] = Field(
        description="When the member is generally available within this care team",
        default=None,
    )
    coverageTiming: Optional[Timing] = Field(
        description="When the member is generally available within this care team",
        default=None,
    )

    @property
    def coverage(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="coverage",
        )

    @model_validator(mode="after")
    def coverage_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Period, Timing],
            field_name_base="coverage",
            required=False,
        )

class CareTeam(DomainResource):
    """
    The Care Team includes all the people and organizations who plan to participate in the coordination and delivery of care.
    """

    _abstract = False
    _type = "CareTeam"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/CareTeam"

    identifier: Optional[ListType[Identifier]] = Field(
        description="External Ids for this team",
        default=None,
    )
    status: Optional[fhir.code] = Field(
        description="proposed | active | suspended | inactive | entered-in-error",
        default=None,
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description="Type of team",
        default=None,
    )
    name: Optional[fhir.string] = Field(
        description="Name of the team, such as crisis assessment team",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="Who care team is for",
        default=None,
    )
    period: Optional[Period] = Field(
        description="time period team covers",
        default=None,
    )
    participant: Optional[ListType[CareTeamParticipant]] = Field(
        description="Members of the team",
        default=None,
    )
    reason: Optional[ListType[CodeableReference]] = Field(
        description="Why the care team exists",
        default=None,
    )
    managingOrganization: Optional[ListType[Reference]] = Field(
        description="Organization responsible for the care team",
        default=None,
    )
    telecom: Optional[ListType[ContactPoint]] = Field(
        description="A contact detail for the care team (that applies to all members)",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Comments made about the CareTeam",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ctm_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("participant",),
            expression="onBehalfOf.exists() implies (member.resolve() is Practitioner)",
            human="CareTeam.participant.onBehalfOf can only be populated when CareTeam.participant.member is a Practitioner",
            key="ctm-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ctm_2_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("participant",),
            expression="role.exists() or member.exists()",
            human="CareTeam.participant.role or CareTeam.participant.member exists",
            key="ctm-2",
            severity="warning",
        )
