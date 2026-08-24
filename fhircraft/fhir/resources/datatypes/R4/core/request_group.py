import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)


import fhircraft.fhir.resources.datatypes.R4.primitive as fhir
from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    Annotation,
    Timing,
    BackboneElement,
    RelatedArtifact,
    Expression,
    Duration,
    Range,
    Age,
    Period,
)
from .resource import Resource
from .domain_resource import DomainResource


class RequestGroupActionCondition(BackboneElement):
    """
    An expression that describes applicability criteria, or start/stop conditions for the action.
    """

    kind: fhir.code = Field(
        description="applicability | start | stop",
    )
    expression: Optional[Expression] = Field(
        description="boolean-valued expression",
        default=None,
    )


class RequestGroupActionRelatedAction(BackboneElement):
    """
    A relationship to another action such as "before" or "30-60 minutes after start of".
    """

    actionId: fhir.id_ = Field(
        description="What action this is related to",
    )
    relationship: fhir.code = Field(
        description="before-start | before | before-end | concurrent-with-start | concurrent | concurrent-with-end | after-start | after | after-end",
    )
    offsetDuration: Optional[Duration] = Field(
        description="time offset for the relationship",
        default=None,
    )
    offsetRange: Optional[Range] = Field(
        description="time offset for the relationship",
        default=None,
    )

    @property
    def offset(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="offset",
        )

    @model_validator(mode="after")
    def offset_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Duration, Range],
            field_name_base="offset",
            required=False,
        )


class RequestGroupAction(BackboneElement):
    """
    The actions, if any, produced by the evaluation of the artifact.
    """

    prefix: Optional[fhir.string] = Field(
        description="User-visible prefix for the action (e.g. 1. or A.)",
        default=None,
    )
    title: Optional[fhir.string] = Field(
        description="User-visible title",
        default=None,
    )
    description: Optional[fhir.string] = Field(
        description="Short description of the action",
        default=None,
    )
    textEquivalent: Optional[fhir.string] = Field(
        description="Static text equivalent of the action, used if the dynamic aspects cannot be interpreted by the receiving system",
        default=None,
    )
    priority: Optional[fhir.code] = Field(
        description="routine | urgent | asap | stat",
        default=None,
    )
    code: Optional[ListType[CodeableConcept]] = Field(
        description="code representing the meaning of the action or sub-actions",
        default=None,
    )
    documentation: Optional[ListType[RelatedArtifact]] = Field(
        description="Supporting documentation for the intended performer of the action",
        default=None,
    )
    condition: Optional[ListType[RequestGroupActionCondition]] = Field(
        description="Whether or not the action is applicable",
        default=None,
    )
    relatedAction: Optional[ListType[RequestGroupActionRelatedAction]] = Field(
        description="Relationship to another action",
        default=None,
    )
    timingDateTime: Optional[fhir.dateTime] = Field(
        description="When the action should take place",
        default=None,
    )
    timingAge: Optional[Age] = Field(
        description="When the action should take place",
        default=None,
    )
    timingPeriod: Optional[Period] = Field(
        description="When the action should take place",
        default=None,
    )
    timingDuration: Optional[Duration] = Field(
        description="When the action should take place",
        default=None,
    )
    timingRange: Optional[Range] = Field(
        description="When the action should take place",
        default=None,
    )
    timingTiming: Optional[Timing] = Field(
        description="When the action should take place",
        default=None,
    )
    participant: Optional[ListType[Reference]] = Field(
        description="Who should perform the action",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="create | update | remove | fire-event",
        default=None,
    )
    groupingBehavior: Optional[fhir.code] = Field(
        description="visual-group | logical-group | sentence-group",
        default=None,
    )
    selectionBehavior: Optional[fhir.code] = Field(
        description="any | all | all-or-none | exactly-one | at-most-one | one-or-more",
        default=None,
    )
    requiredBehavior: Optional[fhir.code] = Field(
        description="must | could | must-unless-documented",
        default=None,
    )
    precheckBehavior: Optional[fhir.code] = Field(
        description="yes | no",
        default=None,
    )
    cardinalityBehavior: Optional[fhir.code] = Field(
        description="single | multiple",
        default=None,
    )
    resource: Optional[Reference] = Field(
        description="The target of the action",
        default=None,
    )
    action: Optional[ListType["RequestGroupAction"]] = Field(
        description="Sub action",
        default=None,
    )

    @property
    def timing(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="timing",
        )

    @model_validator(mode="after")
    def timing_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.DateTime, Age, Period, Duration, Range, Timing],
            field_name_base="timing",
            required=False,
        )


class RequestGroup(DomainResource):
    """
    A group of related requests that can be used to capture intended activities that have inter-dependencies such as "give this medication after that one".
    """

    _abstract = False
    _type = "RequestGroup"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/RequestGroup"

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
        description="Business identifier",
        default=None,
    )
    instantiatesCanonical: Optional[ListType[fhir.canonical]] = Field(
        description="Instantiates FHIR protocol or definition",
        default=None,
    )
    instantiatesUri: Optional[ListType[fhir.uri]] = Field(
        description="Instantiates external protocol or definition",
        default=None,
    )
    basedOn: Optional[ListType[Reference]] = Field(
        description="Fulfills plan, proposal, or order",
        default=None,
    )
    replaces: Optional[ListType[Reference]] = Field(
        description="Request(s) replaced by this request",
        default=None,
    )
    groupIdentifier: Optional[Identifier] = Field(
        description="Composite request this is part of",
        default=None,
    )
    status: fhir.code = Field(
        description="draft | active | on-hold | revoked | completed | entered-in-error | unknown",
    )
    intent: fhir.code = Field(
        description="proposal | plan | directive | order | original-order | reflex-order | filler-order | instance-order | option",
    )
    priority: Optional[fhir.code] = Field(
        description="routine | urgent | asap | stat",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="What\u0027s being requested/ordered",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="Who the request group is about",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="Created as part of",
        default=None,
    )
    authoredOn: Optional[fhir.dateTime] = Field(
        description="When the request group was authored",
        default=None,
    )
    author: Optional[Reference] = Field(
        description="Device or practitioner that authored the request group",
        default=None,
    )
    reasonCode: Optional[ListType[CodeableConcept]] = Field(
        description="Why the request group is needed",
        default=None,
    )
    reasonReference: Optional[ListType[Reference]] = Field(
        description="Why the request group is needed",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Additional notes about the response",
        default=None,
    )
    action: Optional[ListType[RequestGroupAction]] = Field(
        description="Proposed actions, if any",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_rqg_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("action",),
            expression="resource.exists() != action.exists()",
            human="Must have resource or action but not both",
            key="rqg-1",
            severity="error",
        )
