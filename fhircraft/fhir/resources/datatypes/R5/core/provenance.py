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
    Reference,
    Period,
    CodeableReference,
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
        description="The agent that participated in the event",
        default=None,
    )
    onBehalfOf: Optional[Reference] = Field(
        description="The agent that delegated",
        default=None,
    )

class ProvenanceEntityAgent(BackboneElement):
    """
    The entity is attributed to an agent to express the agent's responsibility for that entity, possibly along with other agents. This description can be understood as shorthand for saying that the agent was responsible for the activity which used the entity.
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
        description="The agent that participated in the event",
        default=None,
    )
    onBehalfOf: Optional[Reference] = Field(
        description="The agent that delegated",
        default=None,
    )

class ProvenanceEntity(BackboneElement):
    """
    An entity used in this activity.
    """

    role: Optional[Code] = Field(
        description="revision | quotation | source | instantiates | removal",
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
    authorization: Optional[ListType[CodeableReference]] = Field(
        description="Authorization (purposeOfUse) related to the event",
        default=None,
    )
    activity: Optional[CodeableConcept] = Field(
        description="Activity that occurred",
        default=None,
    )
    basedOn: Optional[ListType[Reference]] = Field(
        description="Workflow authorization within which this event occurred",
        default=None,
    )
    patient: Optional[Reference] = Field(
        description="The patient is the subject of the data created/updated (.target) by the activity",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="Encounter within which this event occurred or which the event is tightly associated",
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

    @model_validator(mode="after")
    def FHIR_prov_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("agent",),
            expression="who.resolve().exists() and onBehalfOf.resolve().exists() implies who.resolve() != onBehalfOf.resolve()",
            human="Who and onBehalfOf cannot be the same",
            key="prov-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_prov_2_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("agent",),
            expression="who.resolve().ofType(PractitionerRole).practitioner.resolve().exists() and onBehalfOf.resolve().ofType(Practitioner).exists() implies who.resolve().practitioner.resolve() != onBehalfOf.resolve()",
            human="If who is a PractitionerRole, onBehalfOf can't reference the same Practitioner",
            key="prov-2",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_prov_3_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("agent",),
            expression="who.resolve().ofType(Organization).exists() and onBehalfOf.resolve().ofType(PractitionerRole).organization.resolve().exists() implies who.resolve() != onBehalfOf.resolve().organization.resolve()",
            human="If who is an organization, onBehalfOf can't be a PractitionerRole within that organization",
            key="prov-3",
            severity="error",
        )
