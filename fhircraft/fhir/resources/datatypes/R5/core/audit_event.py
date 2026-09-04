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
    CodeableConcept,
    Period,
    BackboneElement,
    Coding,
    Reference,
    Quantity,
    Range,
    Ratio,
)
from .resource import Resource
from .domain_resource import DomainResource


class AuditEventOutcome(BackboneElement):
    """
    Indicates whether the event succeeded or failed. A free text descripiton can be given in outcome.text.
    """

    code: Coding = Field(
        description="Whether the event succeeded or failed",
    )
    detail: Optional[ListType[CodeableConcept]] = Field(
        description="Additional outcome detail",
        default=None,
    )


class AuditEventAgent(BackboneElement):
    """
    An actor taking an active role in the event or activity that is logged.
    """

    type: Optional[CodeableConcept] = Field(
        description="How agent participated",
        default=None,
    )
    role: Optional[ListType[CodeableConcept]] = Field(
        description="Agent role in the event",
        default=None,
    )
    who: Reference = Field(
        description="Identifier of who",
    )
    requestor: Optional[fhir.boolean] = Field(
        description="Whether user is initiator",
        default=None,
    )
    location: Optional[Reference] = Field(
        description="The agent location when the event occurred",
        default=None,
    )
    policy: Optional[ListType[fhir.uri]] = Field(
        description="Policy that authorized the agent participation in the event",
        default=None,
    )
    networkReference: Optional[Reference] = Field(
        description="This agent network location for the activity",
        default=None,
    )
    networkUri: Optional[fhir.uri] = Field(
        description="This agent network location for the activity",
        default=None,
    )
    networkString: Optional[fhir.string] = Field(
        description="This agent network location for the activity",
        default=None,
    )
    authorization: Optional[ListType[CodeableConcept]] = Field(
        description="Allowable authorization for this agent",
        default=None,
    )

    @property
    def network(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="network",
        )

    @model_validator(mode="after")
    def network_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Reference, fhir.Uri, fhir.String],
            field_name_base="network",
            required=False,
        )


class AuditEventSource(BackboneElement):
    """
    The actor that is reporting the event.
    """

    site: Optional[Reference] = Field(
        description="Logical source location within the enterprise",
        default=None,
    )
    observer: Reference = Field(
        description="The identity of source detecting the event",
    )
    type: Optional[ListType[CodeableConcept]] = Field(
        description="The type of source where event originated",
        default=None,
    )


class AuditEventEntityDetail(BackboneElement):
    """
    Tagged value pairs for conveying additional information about the entity.
    """

    type: CodeableConcept = Field(
        description="Name of the property",
    )
    valueQuantity: Optional[Quantity] = Field(
        description="Property value",
        default=None,
    )
    valueCodeableConcept: Optional[CodeableConcept] = Field(
        description="Property value",
        default=None,
    )
    valueString: Optional[fhir.string] = Field(
        description="Property value",
        default=None,
    )
    valueBoolean: Optional[fhir.boolean] = Field(
        description="Property value",
        default=None,
    )
    valueInteger: Optional[fhir.integer] = Field(
        description="Property value",
        default=None,
    )
    valueRange: Optional[Range] = Field(
        description="Property value",
        default=None,
    )
    valueRatio: Optional[Ratio] = Field(
        description="Property value",
        default=None,
    )
    valueTime: Optional[fhir.time_] = Field(
        description="Property value",
        default=None,
    )
    valueDateTime: Optional[fhir.dateTime] = Field(
        description="Property value",
        default=None,
    )
    valuePeriod: Optional[Period] = Field(
        description="Property value",
        default=None,
    )
    valueBase64Binary: Optional[fhir.base64Binary] = Field(
        description="Property value",
        default=None,
    )

    @property
    def value(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="value",
        )

    @model_validator(mode="after")
    def value_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[
                Quantity,
                CodeableConcept,
                fhir.String,
                fhir.Boolean,
                fhir.Integer,
                Range,
                Ratio,
                fhir.Time,
                fhir.DateTime,
                Period,
                fhir.Base64Binary,
            ],
            field_name_base="value",
            required=True,
        )


class AuditEventEntityAgent(BackboneElement):
    """
    The entity is attributed to an agent to express the agent's responsibility for that entity in the activity. This is most used to indicate when persistence media (the entity) are used by an agent. For example when importing data from a device, the device would be described in an entity, and the user importing data from that media would be indicated as the entity.agent.
    """

    type: Optional[CodeableConcept] = Field(
        description="How agent participated",
        default=None,
    )
    role: Optional[ListType[CodeableConcept]] = Field(
        description="Agent role in the event",
        default=None,
    )
    who: Optional[Reference] = Field(
        description="Identifier of who",
        default=None,
    )
    requestor: Optional[fhir.boolean] = Field(
        description="Whether user is initiator",
        default=None,
    )
    location: Optional[Reference] = Field(
        description="The agent location when the event occurred",
        default=None,
    )
    policy: Optional[ListType[fhir.uri]] = Field(
        description="Policy that authorized the agent participation in the event",
        default=None,
    )
    networkReference: Optional[Reference] = Field(
        description="This agent network location for the activity",
        default=None,
    )
    networkUri: Optional[fhir.uri] = Field(
        description="This agent network location for the activity",
        default=None,
    )
    networkString: Optional[fhir.string] = Field(
        description="This agent network location for the activity",
        default=None,
    )
    authorization: Optional[ListType[CodeableConcept]] = Field(
        description="Allowable authorization for this agent",
        default=None,
    )

    @property
    def network(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="network",
        )

    @model_validator(mode="after")
    def network_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Reference, fhir.Uri, fhir.String],
            field_name_base="network",
            required=False,
        )


class AuditEventEntity(BackboneElement):
    """
    Specific instances of data or objects that have been accessed.
    """

    what: Optional[Reference] = Field(
        description="Specific instance of resource",
        default=None,
    )
    role: Optional[CodeableConcept] = Field(
        description="What role the entity played",
        default=None,
    )
    securityLabel: Optional[ListType[CodeableConcept]] = Field(
        description="Security labels on the entity",
        default=None,
    )
    query: Optional[fhir.base64Binary] = Field(
        description="Query parameters",
        default=None,
    )
    detail: Optional[ListType[AuditEventEntityDetail]] = Field(
        description="Additional Information about the entity",
        default=None,
    )
    agent: Optional[ListType[AuditEventEntityAgent]] = Field(
        description="Entity is attributed to this agent",
        default=None,
    )


class AuditEvent(DomainResource):
    """
    A record of an event relevant for purposes such as operations, privacy, security, maintenance, and performance analysis.
    """

    _abstract = False
    _type = "AuditEvent"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/AuditEvent"

    category: Optional[ListType[CodeableConcept]] = Field(
        description="Type/identifier of event",
        default=None,
    )
    code: CodeableConcept = Field(
        description="Specific type of event",
    )
    action: Optional[fhir.code] = Field(
        description="Type of action performed during the event",
        default=None,
    )
    severity: Optional[fhir.code] = Field(
        description="emergency | alert | critical | error | warning | notice | informational | debug",
        default=None,
    )
    occurredPeriod: Optional[Period] = Field(
        description="When the activity occurred",
        default=None,
    )
    occurredDateTime: Optional[fhir.dateTime] = Field(
        description="When the activity occurred",
        default=None,
    )
    recorded: fhir.instant = Field(
        description="time when the event was recorded",
    )
    outcome: Optional[AuditEventOutcome] = Field(
        description="Whether the event succeeded or failed",
        default=None,
    )
    authorization: Optional[ListType[CodeableConcept]] = Field(
        description="Authorization related to the event",
        default=None,
    )
    basedOn: Optional[ListType[Reference]] = Field(
        description="Workflow authorization within which this event occurred",
        default=None,
    )
    patient: Optional[Reference] = Field(
        description="The patient is the subject of the data used/created/updated/deleted during the activity",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="Encounter within which this event occurred or which the event is tightly associated",
        default=None,
    )
    agent: ListType[AuditEventAgent] = Field(
        description="Actor involved in the event",
     	min_length=1,
	)
    source: AuditEventSource = Field(
        description="Audit Event Reporter",
    )
    entity: Optional[ListType[AuditEventEntity]] = Field(
        description="Data or objects used",
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
            field_types=[Period, fhir.DateTime],
            field_name_base="occurred",
            required=False,
        )
