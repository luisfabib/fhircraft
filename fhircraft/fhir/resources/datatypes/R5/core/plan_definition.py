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
    Coding,
    CodeableConcept,
    Reference,
    ContactDetail,
    UsageContext,
    Period,
    RelatedArtifact,
    BackboneElement,
    Quantity,
    Range,
    Ratio,
    Duration,
    TriggerDefinition,
    Expression,
    DataRequirement,
    Age,
    Timing,
    CodeableReference,
)
from .resource import Resource
from .domain_resource import DomainResource

class PlanDefinitionGoalTarget(BackboneElement):
    """
    Indicates what should be done and within what timeframe.
    """

    measure: Optional[CodeableConcept] = Field(
        description="The parameter whose value is to be tracked",
        default=None,
    )
    detailQuantity: Optional[Quantity] = Field(
        description="The target value to be achieved",
        default=None,
    )
    detailRange: Optional[Range] = Field(
        description="The target value to be achieved",
        default=None,
    )
    detailCodeableConcept: Optional[CodeableConcept] = Field(
        description="The target value to be achieved",
        default=None,
    )
    detailString: Optional[String] = Field(
        description="The target value to be achieved",
        default=None,
    )
    detailBoolean: Optional[Boolean] = Field(
        description="The target value to be achieved",
        default=None,
    )
    detailInteger: Optional[Integer] = Field(
        description="The target value to be achieved",
        default=None,
    )
    detailRatio: Optional[Ratio] = Field(
        description="The target value to be achieved",
        default=None,
    )
    due: Optional[Duration] = Field(
        description="Reach goal within",
        default=None,
    )

    @property
    def detail(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="detail",
        )

    @model_validator(mode="after")
    def detail_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[
                Quantity,
                Range,
                CodeableConcept,
                String,
                Boolean,
                Integer,
                Ratio,
            ],
            field_name_base="detail",
            required=False,
        )

class PlanDefinitionGoal(BackboneElement):
    """
    A goal describes an expected outcome that activities within the plan are intended to achieve. For example, weight loss, restoring an activity of daily living, obtaining herd immunity via immunization, meeting a process improvement objective, meeting the acceptance criteria for a test as specified by a quality specification, etc.
    """

    category: Optional[CodeableConcept] = Field(
        description="E.g. Treatment, dietary, behavioral",
        default=None,
    )
    description: Optional[CodeableConcept] = Field(
        description="Code or text describing the goal",
        default=None,
    )
    priority: Optional[CodeableConcept] = Field(
        description="high-priority | medium-priority | low-priority",
        default=None,
    )
    start: Optional[CodeableConcept] = Field(
        description="When goal pursuit begins",
        default=None,
    )
    addresses: Optional[ListType[CodeableConcept]] = Field(
        description="What does the goal address",
        default=None,
    )
    documentation: Optional[ListType[RelatedArtifact]] = Field(
        description="Supporting documentation for the goal",
        default=None,
    )
    target: Optional[ListType[PlanDefinitionGoalTarget]] = Field(
        description="Target outcome for the goal",
        default=None,
    )

class PlanDefinitionActorOption(BackboneElement):
    """
    The characteristics of the candidates that could serve as the actor.
    """

    type: Optional[Code] = Field(
        description="careteam | device | group | healthcareservice | location | organization | patient | practitioner | practitionerrole | relatedperson",
        default=None,
    )
    typeCanonical: Optional[Canonical] = Field(
        description="Who or what can participate",
        default=None,
    )
    typeReference: Optional[Reference] = Field(
        description="Who or what can participate",
        default=None,
    )
    role: Optional[CodeableConcept] = Field(
        description="E.g. Nurse, Surgeon, Parent",
        default=None,
    )

class PlanDefinitionActor(BackboneElement):
    """
    Actors represent the individuals or groups involved in the execution of the defined set of activities.
    """

    title: Optional[String] = Field(
        description="User-visible title",
        default=None,
    )
    description: Optional[Markdown] = Field(
        description="Describes the actor",
        default=None,
    )
    option: Optional[ListType[PlanDefinitionActorOption]] = Field(
        description="Who or what can be this actor",
        default=None,
    )

class PlanDefinitionActionCondition(BackboneElement):
    """
    An expression that describes applicability criteria or start/stop conditions for the action.
    """

    kind: Optional[Code] = Field(
        description="applicability | start | stop",
        default=None,
    )
    expression: Optional[Expression] = Field(
        description="Boolean-valued expression",
        default=None,
    )

class PlanDefinitionActionInput(BackboneElement):
    """
    Defines input data requirements for the action.
    """

    title: Optional[String] = Field(
        description="User-visible title",
        default=None,
    )
    requirement: Optional[DataRequirement] = Field(
        description="What data is provided",
        default=None,
    )
    relatedData: Optional[Id] = Field(
        description="What data is provided",
        default=None,
    )

class PlanDefinitionActionOutput(BackboneElement):
    """
    Defines the outputs of the action, if any.
    """

    title: Optional[String] = Field(
        description="User-visible title",
        default=None,
    )
    requirement: Optional[DataRequirement] = Field(
        description="What data is provided",
        default=None,
    )
    relatedData: Optional[String] = Field(
        description="What data is provided",
        default=None,
    )

class PlanDefinitionActionRelatedAction(BackboneElement):
    """
    A relationship to another action such as "before" or "30-60 minutes after start of".
    """

    targetId: Optional[Id] = Field(
        description="What action is this related to",
        default=None,
    )
    relationship: Optional[Code] = Field(
        description="before | before-start | before-end | concurrent | concurrent-with-start | concurrent-with-end | after | after-start | after-end",
        default=None,
    )
    endRelationship: Optional[Code] = Field(
        description="before | before-start | before-end | concurrent | concurrent-with-start | concurrent-with-end | after | after-start | after-end",
        default=None,
    )
    offsetDuration: Optional[Duration] = Field(
        description="Time offset for the relationship",
        default=None,
    )
    offsetRange: Optional[Range] = Field(
        description="Time offset for the relationship",
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

class PlanDefinitionActionParticipant(BackboneElement):
    """
    Indicates who should participate in performing the action described.
    """

    actorId: Optional[String] = Field(
        description="What actor",
        default=None,
    )
    type: Optional[Code] = Field(
        description="careteam | device | group | healthcareservice | location | organization | patient | practitioner | practitionerrole | relatedperson",
        default=None,
    )
    typeCanonical: Optional[Canonical] = Field(
        description="Who or what can participate",
        default=None,
    )
    typeReference: Optional[Reference] = Field(
        description="Who or what can participate",
        default=None,
    )
    role: Optional[CodeableConcept] = Field(
        description="E.g. Nurse, Surgeon, Parent",
        default=None,
    )
    function: Optional[CodeableConcept] = Field(
        description="E.g. Author, Reviewer, Witness, etc",
        default=None,
    )

class PlanDefinitionActionDynamicValue(BackboneElement):
    """
    Customizations that should be applied to the statically defined resource. For example, if the dosage of a medication must be computed based on the patient's weight, a customization would be used to specify an expression that calculated the weight, and the path on the resource that would contain the result.
    """

    path: Optional[String] = Field(
        description="The path to the element to be set dynamically",
        default=None,
    )
    expression: Optional[Expression] = Field(
        description="An expression that provides the dynamic value for the customization",
        default=None,
    )

class PlanDefinitionAction(BackboneElement):
    """
    An action or group of actions to be taken as part of the plan. For example, in clinical care, an action would be to prescribe a particular indicated medication, or perform a particular test as appropriate. In pharmaceutical quality, an action would be the test that needs to be performed on a drug product as defined in the quality specification.
    """

    linkId: Optional[String] = Field(
        description="Unique id for the action in the PlanDefinition",
        default=None,
    )
    prefix: Optional[String] = Field(
        description="User-visible prefix for the action (e.g. 1. or A.)",
        default=None,
    )
    title: Optional[String] = Field(
        description="User-visible title",
        default=None,
    )
    description: Optional[Markdown] = Field(
        description="Brief description of the action",
        default=None,
    )
    textEquivalent: Optional[Markdown] = Field(
        description="Static text equivalent of the action, used if the dynamic aspects cannot be interpreted by the receiving system",
        default=None,
    )
    priority: Optional[Code] = Field(
        description="routine | urgent | asap | stat",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="Code representing the meaning of the action or sub-actions",
        default=None,
    )
    reason: Optional[ListType[CodeableConcept]] = Field(
        description="Why the action should be performed",
        default=None,
    )
    documentation: Optional[ListType[RelatedArtifact]] = Field(
        description="Supporting documentation for the intended performer of the action",
        default=None,
    )
    goalId: Optional[ListType[Id]] = Field(
        description="What goals this action supports",
        default=None,
    )
    subjectCodeableConcept: Optional[CodeableConcept] = Field(
        description="Type of individual the action is focused on",
        default=None,
    )
    subjectReference: Optional[Reference] = Field(
        description="Type of individual the action is focused on",
        default=None,
    )
    subjectCanonical: Optional[Canonical] = Field(
        description="Type of individual the action is focused on",
        default=None,
    )
    trigger: Optional[ListType[TriggerDefinition]] = Field(
        description="When the action should be triggered",
        default=None,
    )
    condition: Optional[ListType[PlanDefinitionActionCondition]] = Field(
        description="Whether or not the action is applicable",
        default=None,
    )
    input: Optional[ListType[PlanDefinitionActionInput]] = Field(
        description="Input data requirements",
        default=None,
    )
    output: Optional[ListType[PlanDefinitionActionOutput]] = Field(
        description="Output data definition",
        default=None,
    )
    relatedAction: Optional[ListType[PlanDefinitionActionRelatedAction]] = Field(
        description="Relationship to another action",
        default=None,
    )
    timingAge: Optional[Age] = Field(
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
    location: Optional[CodeableReference] = Field(
        description="Where it should happen",
        default=None,
    )
    participant: Optional[ListType[PlanDefinitionActionParticipant]] = Field(
        description="Who should participate in the action",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="create | update | remove | fire-event",
        default=None,
    )
    groupingBehavior: Optional[Code] = Field(
        description="visual-group | logical-group | sentence-group",
        default=None,
    )
    selectionBehavior: Optional[Code] = Field(
        description="any | all | all-or-none | exactly-one | at-most-one | one-or-more",
        default=None,
    )
    requiredBehavior: Optional[Code] = Field(
        description="must | could | must-unless-documented",
        default=None,
    )
    precheckBehavior: Optional[Code] = Field(
        description="yes | no",
        default=None,
    )
    cardinalityBehavior: Optional[Code] = Field(
        description="single | multiple",
        default=None,
    )
    definitionCanonical: Optional[Canonical] = Field(
        description="Description of the activity to be performed",
        default=None,
    )
    definitionUri: Optional[Uri] = Field(
        description="Description of the activity to be performed",
        default=None,
    )
    transform: Optional[Canonical] = Field(
        description="Transform to apply the template",
        default=None,
    )
    dynamicValue: Optional[ListType[PlanDefinitionActionDynamicValue]] = Field(
        description="Dynamic aspects of the definition",
        default=None,
    )
    action: Optional[ListType["PlanDefinitionAction"]] = Field(
        description="A sub-action",
        default=None,
    )

    @property
    def subject(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="subject",
        )

    @property
    def timing(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="timing",
        )

    @property
    def definition(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="definition",
        )

    @model_validator(mode="after")
    def subject_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[CodeableConcept, Reference, Canonical],
            field_name_base="subject",
            required=False,
        )

    @model_validator(mode="after")
    def timing_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Age, Duration, Range, Timing],
            field_name_base="timing",
            required=False,
        )

    @model_validator(mode="after")
    def definition_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Canonical, Uri],
            field_name_base="definition",
            required=False,
        )

class PlanDefinition(DomainResource):
    """
    This resource allows for the definition of various types of plans as a sharable, consumable, and executable artifact. The resource is general enough to support the description of a broad range of clinical and non-clinical artifacts such as clinical decision support rules, order sets, protocols, and drug quality specifications.
    """

    _abstract = False
    _type = "PlanDefinition"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/PlanDefinition"

    url: Optional[Uri] = Field(
        description="Canonical identifier for this plan definition, represented as a URI (globally unique)",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Additional identifier for the plan definition",
        default=None,
    )
    version: Optional[String] = Field(
        description="Business version of the plan definition",
        default=None,
    )
    versionAlgorithmString: Optional[String] = Field(
        description="How to compare versions",
        default=None,
    )
    versionAlgorithmCoding: Optional[Coding] = Field(
        description="How to compare versions",
        default=None,
    )
    name: Optional[String] = Field(
        description="Name for this plan definition (computer friendly)",
        default=None,
    )
    title: Optional[String] = Field(
        description="Name for this plan definition (human friendly)",
        default=None,
    )
    subtitle: Optional[String] = Field(
        description="Subordinate title of the plan definition",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="order-set | clinical-protocol | eca-rule | workflow-definition",
        default=None,
    )
    status: Optional[Code] = Field(
        description="draft | active | retired | unknown",
        default=None,
    )
    experimental: Optional[Boolean] = Field(
        description="For testing purposes, not real usage",
        default=None,
    )
    subjectCodeableConcept: Optional[CodeableConcept] = Field(
        description="Type of individual the plan definition is focused on",
        default=None,
    )
    subjectReference: Optional[Reference] = Field(
        description="Type of individual the plan definition is focused on",
        default=None,
    )
    subjectCanonical: Optional[Canonical] = Field(
        description="Type of individual the plan definition is focused on",
        default=None,
    )
    date: Optional[DateTime] = Field(
        description="Date last changed",
        default=None,
    )
    publisher: Optional[String] = Field(
        description="Name of the publisher/steward (organization or individual)",
        default=None,
    )
    contact: Optional[ListType[ContactDetail]] = Field(
        description="Contact details for the publisher",
        default=None,
    )
    description: Optional[Markdown] = Field(
        description="Natural language description of the plan definition",
        default=None,
    )
    useContext: Optional[ListType[UsageContext]] = Field(
        description="The context that the content is intended to support",
        default=None,
    )
    jurisdiction: Optional[ListType[CodeableConcept]] = Field(
        description="Intended jurisdiction for plan definition (if applicable)",
        default=None,
    )
    purpose: Optional[Markdown] = Field(
        description="Why this plan definition is defined",
        default=None,
    )
    usage: Optional[Markdown] = Field(
        description="Describes the clinical usage of the plan",
        default=None,
    )
    copyright: Optional[Markdown] = Field(
        description="Use and/or publishing restrictions",
        default=None,
    )
    copyrightLabel: Optional[String] = Field(
        description="Copyright holder and year(s)",
        default=None,
    )
    approvalDate: Optional[Date] = Field(
        description="When the plan definition was approved by publisher",
        default=None,
    )
    lastReviewDate: Optional[Date] = Field(
        description="When the plan definition was last reviewed by the publisher",
        default=None,
    )
    effectivePeriod: Optional[Period] = Field(
        description="When the plan definition is expected to be used",
        default=None,
    )
    topic: Optional[ListType[CodeableConcept]] = Field(
        description="E.g. Education, Treatment, Assessment",
        default=None,
    )
    author: Optional[ListType[ContactDetail]] = Field(
        description="Who authored the content",
        default=None,
    )
    editor: Optional[ListType[ContactDetail]] = Field(
        description="Who edited the content",
        default=None,
    )
    reviewer: Optional[ListType[ContactDetail]] = Field(
        description="Who reviewed the content",
        default=None,
    )
    endorser: Optional[ListType[ContactDetail]] = Field(
        description="Who endorsed the content",
        default=None,
    )
    relatedArtifact: Optional[ListType[RelatedArtifact]] = Field(
        description="Additional documentation, citations",
        default=None,
    )
    library: Optional[ListType[Canonical]] = Field(
        description="Logic used by the plan definition",
        default=None,
    )
    goal: Optional[ListType[PlanDefinitionGoal]] = Field(
        description="What the plan is trying to accomplish",
        default=None,
    )
    actor: Optional[ListType[PlanDefinitionActor]] = Field(
        description="Actors within the plan",
        default=None,
    )
    action: Optional[ListType[PlanDefinitionAction]] = Field(
        description="Action defined by the plan",
        default=None,
    )
    asNeededBoolean: Optional[Boolean] = Field(
        description="Preconditions for service",
        default=None,
    )
    asNeededCodeableConcept: Optional[CodeableConcept] = Field(
        description="Preconditions for service",
        default=None,
    )

    @property
    def versionAlgorithm(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="versionAlgorithm",
        )

    @property
    def subject(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="subject",
        )

    @property
    def asNeeded(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="asNeeded",
        )

    @model_validator(mode="after")
    def versionAlgorithm_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[String, Coding],
            field_name_base="versionAlgorithm",
            required=False,
        )

    @model_validator(mode="after")
    def subject_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[CodeableConcept, Reference, Canonical],
            field_name_base="subject",
            required=False,
        )

    @model_validator(mode="after")
    def asNeeded_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Boolean, CodeableConcept],
            field_name_base="asNeeded",
            required=False,
        )

    @model_validator(mode="after")
    def FHIR_cnl_0_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.exists() implies name.matches('^[A-Z]([A-Za-z0-9_]){1,254}$')",
            human="Name should be usable as an identifier for the module by machine processing applications such as code generation",
            key="cnl-0",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_cnl_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("action.url",),
            expression="exists() implies matches('^[^|# ]+$')",
            human="URL should not contain | or # - these characters make processing canonical references problematic",
            key="cnl-1",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_pld_0_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("action.input",),
            expression="requirement.exists() xor relatedData.exists()",
            human="Input data elements must have a requirement or a relatedData, but not both",
            key="pld-0",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_pld_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("action.output",),
            expression="requirement.exists() xor relatedData.exists()",
            human="Output data element must have a requirement or a relatedData, but not both",
            key="pld-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_pld_3_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="%context.repeat(action).where((goalId in %context.goal.id).not()).exists().not()",
            human="goalid should reference the id of a goal definition",
            key="pld-3",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_pld_4_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="%context.repeat(action).relatedAction.where((targetId in %context.repeat(action).id).not()).exists().not()",
            human="targetId should reference the id of an action",
            key="pld-4",
            severity="warning",
        )
