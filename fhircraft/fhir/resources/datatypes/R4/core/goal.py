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
    CodeableConcept,
    Annotation,
    Reference,
    BackboneElement,
    Quantity,
    Range,
    Ratio,
    Duration,
)
from .resource import Resource
from .domain_resource import DomainResource

class GoalTarget(BackboneElement):
    """
    Indicates what should be done by when.
    """

    measure: Optional[CodeableConcept] = Field(
        description="The parameter whose value is being tracked",
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
    detailString: Optional[fhir.string] = Field(
        description="The target value to be achieved",
        default=None,
    )
    detailBoolean: Optional[fhir.boolean] = Field(
        description="The target value to be achieved",
        default=None,
    )
    detailInteger: Optional[fhir.integer] = Field(
        description="The target value to be achieved",
        default=None,
    )
    detailRatio: Optional[Ratio] = Field(
        description="The target value to be achieved",
        default=None,
    )
    dueDate: Optional[fhir.date_] = Field(
        description="Reach goal on or before",
        default=None,
    )
    dueDuration: Optional[Duration] = Field(
        description="Reach goal on or before",
        default=None,
    )

    @property
    def detail(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="detail",
        )

    @property
    def due(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="due",
        )

    @model_validator(mode="after")
    def detail_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[
                Quantity,
                Range,
                CodeableConcept,
                fhir.String,
                fhir.Boolean,
                fhir.Integer,
                Ratio,
            ],
            field_name_base="detail",
            required=False,
        )

    @model_validator(mode="after")
    def due_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.Date, Duration],
            field_name_base="due",
            required=False,
        )

class Goal(DomainResource):
    """
    Describes the intended objective(s) for a patient, group or organization care, for example, weight loss, restoring an activity of daily living, obtaining herd immunity via immunization, meeting a process improvement objective, etc.
    """

    _abstract = False
    _type = "Goal"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Goal"

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
        description="External Ids for this goal",
        default=None,
    )
    lifecycleStatus: fhir.code = Field(
        description="proposed | planned | accepted | active | on-hold | completed | cancelled | entered-in-error | rejected",
    )
    achievementStatus: Optional[CodeableConcept] = Field(
        description="in-progress | improving | worsening | no-change | achieved | sustaining | not-achieved | no-progress | not-attainable",
        default=None,
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description="E.g. Treatment, dietary, behavioral, etc.",
        default=None,
    )
    priority: Optional[CodeableConcept] = Field(
        description="high-priority | medium-priority | low-priority",
        default=None,
    )
    description: CodeableConcept = Field(
        description="code or text describing goal",
    )
    subject: Reference = Field(
        description="Who this goal is intended for",
    )
    startDate: Optional[fhir.date_] = Field(
        description="When goal pursuit begins",
        default=None,
    )
    startCodeableConcept: Optional[CodeableConcept] = Field(
        description="When goal pursuit begins",
        default=None,
    )
    target: Optional[ListType[GoalTarget]] = Field(
        description="Target outcome for the goal",
        default=None,
    )
    statusDate: Optional[fhir.date_] = Field(
        description="When goal status took effect",
        default=None,
    )
    statusReason: Optional[fhir.string] = Field(
        description="Reason for current status",
        default=None,
    )
    expressedBy: Optional[Reference] = Field(
        description="Who\u0027s responsible for creating Goal?",
        default=None,
    )
    addresses: Optional[ListType[Reference]] = Field(
        description="Issues addressed by this goal",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Comments about the goal",
        default=None,
    )
    outcomeCode: Optional[ListType[CodeableConcept]] = Field(
        description="What result was achieved regarding the goal?",
        default=None,
    )
    outcomeReference: Optional[ListType[Reference]] = Field(
        description="Observation that resulted from goal",
        default=None,
    )

    @property
    def start(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="start",
        )

    @model_validator(mode="after")
    def FHIR_gol_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("target",),
            expression="(detail.exists() and measure.exists()) or detail.exists().not()",
            human="Goal.target.measure is required if Goal.target.detail is populated",
            key="gol-1",
            severity="error",
        )

    @model_validator(mode="after")
    def start_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.Date, CodeableConcept],
            field_name_base="start",
            required=False,
        )
