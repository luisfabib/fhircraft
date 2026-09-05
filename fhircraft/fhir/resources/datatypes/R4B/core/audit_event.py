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
    Coding,
    Period,
    CodeableConcept,
    BackboneElement,
    Reference,
)
from .resource import Resource
from .domain_resource import DomainResource


class AuditEventAgentNetwork(BackboneElement):
    """
    Logical network location for application activity, if the activity has a network location.
    """

    address: Optional[fhir.string] = Field(
        description="Identifier for the network access point of the user device",
        default=None,
    )
    type: Optional[fhir.code] = Field(
        description="The type of network access point",
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
    who: Optional[Reference] = Field(
        description="Identifier of who",
        default=None,
    )
    altId: Optional[fhir.string] = Field(
        description="Alternative User identity",
        default=None,
    )
    name: Optional[fhir.string] = Field(
        description="Human friendly name for the agent",
        default=None,
    )
    requestor: fhir.boolean = Field(
        description="Whether user is initiator",
    )
    location: Optional[Reference] = Field(
        description="Where",
        default=None,
    )
    policy: Optional[ListType[fhir.uri]] = Field(
        description="Policy that authorized event",
        default=None,
    )
    media: Optional[Coding] = Field(
        description="Type of media",
        default=None,
    )
    network: Optional[AuditEventAgentNetwork] = Field(
        description="Logical network location for application activity",
        default=None,
    )
    purposeOfUse: Optional[ListType[CodeableConcept]] = Field(
        description="Reason given for this user",
        default=None,
    )


class AuditEventSource(BackboneElement):
    """
    The system that is reporting the event.
    """

    site: Optional[fhir.string] = Field(
        description="Logical source location within the enterprise",
        default=None,
    )
    observer: Reference = Field(
        description="The identity of source detecting the event",
    )
    type: Optional[ListType[Coding]] = Field(
        description="The type of source where event originated",
        default=None,
    )


class AuditEventEntityDetail(BackboneElement):
    """
    Tagged value pairs for conveying additional information about the entity.
    """

    type: fhir.string = Field(
        description="Name of the property",
    )
    valueString: Optional[fhir.string] = Field(
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
            field_types=[fhir.String, fhir.Base64Binary],
            field_name_base="value",
            required=True,
        )


class AuditEventEntity(BackboneElement):
    """
    Specific instances of data or objects that have been accessed.
    """

    what: Optional[Reference] = Field(
        description="Specific instance of resource",
        default=None,
    )
    type: Optional[Coding] = Field(
        description="Type of entity involved",
        default=None,
    )
    role: Optional[Coding] = Field(
        description="What role the entity played",
        default=None,
    )
    lifecycle: Optional[Coding] = Field(
        description="Life-cycle stage for the entity",
        default=None,
    )
    securityLabel: Optional[ListType[Coding]] = Field(
        description="Security labels on the entity",
        default=None,
    )
    name: Optional[fhir.string] = Field(
        description="Descriptor for entity",
        default=None,
    )
    description: Optional[fhir.string] = Field(
        description="Descriptive text",
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


class AuditEvent(DomainResource):
    """
    A record of an event made for purposes of maintaining a security log. Typical uses include detection of intrusion attempts and monitoring for inappropriate usage.
    """

    _abstract = False
    _type = "AuditEvent"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/AuditEvent"

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
    type: Coding = Field(
        description="Type/identifier of event",
    )
    subtype: Optional[ListType[Coding]] = Field(
        description="More specific type/id for the event",
        default=None,
    )
    action: Optional[fhir.code] = Field(
        description="Type of action performed during the event",
        default=None,
    )
    period: Optional[Period] = Field(
        description="When the activity occurred",
        default=None,
    )
    recorded: fhir.instant = Field(
        description="time when the event was recorded",
    )
    outcome: Optional[fhir.code] = Field(
        description="Whether the event succeeded or failed",
        default=None,
    )
    outcomeDesc: Optional[fhir.string] = Field(
        description="Description of the event outcome",
        default=None,
    )
    purposeOfEvent: Optional[ListType[CodeableConcept]] = Field(
        description="The purposeOfUse of the event",
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

    @model_validator(mode="after")
    def FHIR_sev_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("entity",),
            expression="name.empty() or query.empty()",
            human="Either a name or a query (NOT both)",
            key="sev-1",
            severity="error",
        )
