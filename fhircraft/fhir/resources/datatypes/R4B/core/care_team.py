import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import String, Uri, Code

from fhircraft.fhir.resources.datatypes.R4B.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    Period,
    BackboneElement,
    ContactPoint,
    Annotation,
)
from .resource import Resource
from .domain_resource import DomainResource


class CareTeamParticipant(BackboneElement):
    """
    Identifies all people and organizations who are expected to be involved in the care team.
    """

    role: Optional[ListType[CodeableConcept]] = Field(
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
    period: Optional[Period] = Field(
        description="Time period of participant",
        default=None,
    )


class CareTeam(DomainResource):
    """
    The Care Team includes all the people and organizations who plan to participate in the coordination and delivery of care for a patient.
    """

    _abstract = False
    _type = "CareTeam"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/CareTeam"

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
        description="External Ids for this team",
        default=None,
    )
    status: Optional[Code] = Field(
        description="proposed | active | suspended | inactive | entered-in-error",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description="Type of team",
        default=None,
    )
    name: Optional[String] = Field(
        description="Name of the team, such as crisis assessment team",
        default=None,
    )
    name_ext: Optional[Element] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    subject: Optional[Reference] = Field(
        description="Who care team is for",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="Encounter created as part of",
        default=None,
    )
    period: Optional[Period] = Field(
        description="Time period team covers",
        default=None,
    )
    participant: Optional[ListType[CareTeamParticipant]] = Field(
        description="Members of the team",
        default=None,
    )
    reasonCode: Optional[ListType[CodeableConcept]] = Field(
        description="Why the care team exists",
        default=None,
    )
    reasonReference: Optional[ListType[Reference]] = Field(
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
            expression="onBehalfOf.exists() implies (member.resolve().iif(empty(), true, ofType(Practitioner).exists()))",
            human="CareTeam.participant.onBehalfOf can only be populated when CareTeam.participant.member is a Practitioner",
            key="ctm-1",
            severity="error",
        )
