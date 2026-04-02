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
    Reference,
    Period,
    CodeableConcept,
    BackboneElement,
    Signature,
)
from .resource import Resource
from .domain_resource import DomainResource

class ProvenanceAgent(BackboneElement):
    """
    An actor taking a role in an activity  for which it can be assigned some degree of responsibility for the activity taking place.
    """

    type: Optional[CodeableConcept] = Field(
        description="How the agent participated",
        default=None,
    )
    role: Optional[ListType[CodeableConcept]] = Field(
        description="What the agents role was",
        default=None,
    )
    who: Optional[Reference] = Field(
        description="Who participated",
        default=None,
    )
    onBehalfOf: Optional[Reference] = Field(
        description="Who the agent is representing",
        default=None,
    )

class ProvenanceEntityAgent(BackboneElement):
    """
    The entity is attributed to an agent to express the agent's responsibility for that entity, possibly along with other agents. This description can be understood as shorthand for saying that the agent was responsible for the activity which generated the entity.
    """

    type: Optional[CodeableConcept] = Field(
        description="How the agent participated",
        default=None,
    )
    role: Optional[ListType[CodeableConcept]] = Field(
        description="What the agents role was",
        default=None,
    )
    who: Optional[Reference] = Field(
        description="Who participated",
        default=None,
    )
    onBehalfOf: Optional[Reference] = Field(
        description="Who the agent is representing",
        default=None,
    )

class ProvenanceEntity(BackboneElement):
    """
    An entity used in this activity.
    """

    role: Optional[Code] = Field(
        description="derivation | revision | quotation | source | removal",
        default=None,
    )
    what: Optional[Reference] = Field(
        description="Identity of entity",
        default=None,
    )
    agent: Optional[ListType[ProvenanceEntityAgent]] = Field(
        description="Entity is attributed to this agent",
        default=None,
    )

class Provenance(DomainResource):
    """
    Provenance of a resource is a record that describes entities and processes involved in producing and delivering or otherwise influencing that resource. Provenance provides a critical foundation for assessing authenticity, enabling trust, and allowing reproducibility. Provenance assertions are a form of contextual metadata and can themselves become important records with their own provenance. Provenance statement indicates clinical significance in terms of confidence in authenticity, reliability, and trustworthiness, integrity, and stage in lifecycle (e.g. Document Completion - has the artifact been legally authenticated), all of which may impact security, privacy, and trust policies.
    """

    _abstract = False
    _type = "Provenance"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Provenance"

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
    target: Optional[ListType[Reference]] = Field(
        description="Target Reference(s) (usually version specific)",
        default=None,
    )
    occurredPeriod: Optional[Period] = Field(
        description="When the activity occurred",
        default=None,
    )
    occurredDateTime: Optional[DateTime] = Field(
        description="When the activity occurred",
        default=None,
    )
    recorded: Optional[Instant] = Field(
        description="When the activity was recorded / updated",
        default=None,
    )
    policy: Optional[ListType[Uri]] = Field(
        description="Policy or plan the activity was defined by",
        default=None,
    )
    location: Optional[Reference] = Field(
        description="Where the activity occurred, if relevant",
        default=None,
    )
    reason: Optional[ListType[CodeableConcept]] = Field(
        description="Reason the activity is occurring",
        default=None,
    )
    activity: Optional[CodeableConcept] = Field(
        description="Activity that occurred",
        default=None,
    )
    agent: Optional[ListType[ProvenanceAgent]] = Field(
        description="Actor involved",
        default=None,
    )
    entity: Optional[ListType[ProvenanceEntity]] = Field(
        description="An entity used in this activity",
        default=None,
    )
    signature: Optional[ListType[Signature]] = Field(
        description="Signature on target",
        default=None,
    )

    @property
    def occurred(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="occurred",
        )

    @model_validator(mode="after")
    def occurred_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Period, DateTime],
            field_name_base="occurred",
            required=False,
        )
