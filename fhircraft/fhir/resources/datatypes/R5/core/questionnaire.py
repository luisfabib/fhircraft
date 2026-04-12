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
    Coding,
    ContactDetail,
    UsageContext,
    CodeableConcept,
    Period,
    BackboneElement,
    Quantity,
    Reference,
    Attachment,
)
from .resource import Resource
from .domain_resource import DomainResource


class QuestionnaireItemEnableWhen(BackboneElement):
    """
    A constraint indicating that this item should only be enabled (displayed/allow answers to be captured) when the specified condition is true.
    """

    question: Optional[fhir.string] = Field(
        description="The linkId of question that determines whether item is enabled/disabled",
        default=None,
    )
    operator: Optional[fhir.code] = Field(
        description="exists | = | != | \u003e | \u003c | \u003e= | \u003c=",
        default=None,
    )
    answerBoolean: Optional[fhir.boolean] = Field(
        description="Value for question comparison based on operator",
        default=None,
    )
    answerDecimal: Optional[fhir.decimal] = Field(
        description="Value for question comparison based on operator",
        default=None,
    )
    answerInteger: Optional[fhir.integer] = Field(
        description="Value for question comparison based on operator",
        default=None,
    )
    answerDate: Optional[fhir.date_] = Field(
        description="Value for question comparison based on operator",
        default=None,
    )
    answerDateTime: Optional[fhir.dateTime] = Field(
        description="Value for question comparison based on operator",
        default=None,
    )
    answerTime: Optional[fhir.time_] = Field(
        description="Value for question comparison based on operator",
        default=None,
    )
    answerString: Optional[fhir.string] = Field(
        description="Value for question comparison based on operator",
        default=None,
    )
    answerCoding: Optional[Coding] = Field(
        description="Value for question comparison based on operator",
        default=None,
    )
    answerQuantity: Optional[Quantity] = Field(
        description="Value for question comparison based on operator",
        default=None,
    )
    answerReference: Optional[Reference] = Field(
        description="Value for question comparison based on operator",
        default=None,
    )

    @property
    def answer(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="answer",
        )

    @model_validator(mode="after")
    def answer_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[
                fhir.Boolean,
                fhir.Decimal,
                fhir.Integer,
                fhir.Date,
                fhir.DateTime,
                fhir.Time,
                fhir.String,
                Coding,
                Quantity,
                Reference,
            ],
            field_name_base="answer",
            required=True,
        )


class QuestionnaireItemAnswerOption(BackboneElement):
    """
    One of the permitted answers for the question.
    """

    valueInteger: Optional[fhir.integer] = Field(
        description="Answer value",
        default=None,
    )
    valueDate: Optional[fhir.date_] = Field(
        description="Answer value",
        default=None,
    )
    valueTime: Optional[fhir.time_] = Field(
        description="Answer value",
        default=None,
    )
    valueString: Optional[fhir.string] = Field(
        description="Answer value",
        default=None,
    )
    valueCoding: Optional[Coding] = Field(
        description="Answer value",
        default=None,
    )
    valueReference: Optional[Reference] = Field(
        description="Answer value",
        default=None,
    )
    initialSelected: Optional[fhir.boolean] = Field(
        description="Whether option is selected by default",
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
                fhir.Integer,
                fhir.Date,
                fhir.Time,
                fhir.String,
                Coding,
                Reference,
            ],
            field_name_base="value",
            required=True,
        )


class QuestionnaireItemInitial(BackboneElement):
    """
    One or more values that should be pre-populated in the answer when initially rendering the questionnaire for user input.
    """

    valueBoolean: Optional[fhir.boolean] = Field(
        description="Actual value for initializing the question",
        default=None,
    )
    valueDecimal: Optional[fhir.decimal] = Field(
        description="Actual value for initializing the question",
        default=None,
    )
    valueInteger: Optional[fhir.integer] = Field(
        description="Actual value for initializing the question",
        default=None,
    )
    valueDate: Optional[fhir.date_] = Field(
        description="Actual value for initializing the question",
        default=None,
    )
    valueDateTime: Optional[fhir.dateTime] = Field(
        description="Actual value for initializing the question",
        default=None,
    )
    valueTime: Optional[fhir.time_] = Field(
        description="Actual value for initializing the question",
        default=None,
    )
    valueString: Optional[fhir.string] = Field(
        description="Actual value for initializing the question",
        default=None,
    )
    valueUri: Optional[fhir.uri] = Field(
        description="Actual value for initializing the question",
        default=None,
    )
    valueAttachment: Optional[Attachment] = Field(
        description="Actual value for initializing the question",
        default=None,
    )
    valueCoding: Optional[Coding] = Field(
        description="Actual value for initializing the question",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="Actual value for initializing the question",
        default=None,
    )
    valueReference: Optional[Reference] = Field(
        description="Actual value for initializing the question",
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
                fhir.Boolean,
                fhir.Decimal,
                fhir.Integer,
                fhir.Date,
                fhir.DateTime,
                fhir.Time,
                fhir.String,
                fhir.Uri,
                Attachment,
                Coding,
                Quantity,
                Reference,
            ],
            field_name_base="value",
            required=True,
        )


class QuestionnaireItem(BackboneElement):
    """
    A particular question, question grouping or display text that is part of the questionnaire.
    """

    linkId: Optional[fhir.string] = Field(
        description="Unique id for item in questionnaire",
        default=None,
    )
    definition: Optional[fhir.uri] = Field(
        description="ElementDefinition - details for the item",
        default=None,
    )
    code: Optional[ListType[Coding]] = Field(
        description="Corresponding concept for this item in a terminology",
        default=None,
    )
    prefix: Optional[fhir.string] = Field(
        description='E.g. "1(a)", "2.5.3"',
        default=None,
    )
    text: Optional[fhir.string] = Field(
        description="Primary text for the item",
        default=None,
    )
    type: Optional[fhir.code] = Field(
        description="group | display | boolean | decimal | integer | date | dateTime +",
        default=None,
    )
    enableWhen: Optional[ListType[QuestionnaireItemEnableWhen]] = Field(
        description="Only allow data when",
        default=None,
    )
    enableBehavior: Optional[fhir.code] = Field(
        description="all | any",
        default=None,
    )
    disabledDisplay: Optional[fhir.code] = Field(
        description="hidden | protected",
        default=None,
    )
    required: Optional[fhir.boolean] = Field(
        description="Whether the item must be included in data results",
        default=None,
    )
    repeats: Optional[fhir.boolean] = Field(
        description="Whether the item may repeat",
        default=None,
    )
    readOnly: Optional[fhir.boolean] = Field(
        description="Don\u0027t allow human editing",
        default=None,
    )
    maxLength: Optional[fhir.integer] = Field(
        description="No more than these many characters",
        default=None,
    )
    answerConstraint: Optional[fhir.code] = Field(
        description="optionsOnly | optionsOrType | optionsOrString",
        default=None,
    )
    answerValueSet: Optional[fhir.canonical] = Field(
        description="ValueSet containing permitted answers",
        default=None,
    )
    answerOption: Optional[ListType[QuestionnaireItemAnswerOption]] = Field(
        description="Permitted answer",
        default=None,
    )
    initial: Optional[ListType[QuestionnaireItemInitial]] = Field(
        description="Initial value(s) when item is first rendered",
        default=None,
    )
    item: Optional[ListType["QuestionnaireItem"]] = Field(
        description="Nested questionnaire items",
        default=None,
    )


class Questionnaire(DomainResource):
    """
    A structured set of questions intended to guide the collection of answers from end-users. Questionnaires provide detailed control over order, presentation, phraseology and grouping to allow coherent, consistent data collection.
    """

    _abstract = False
    _type = "Questionnaire"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Questionnaire"

    url: Optional[fhir.uri] = Field(
        description="canonical identifier for this questionnaire, represented as an absolute URI (globally unique)",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Business identifier for questionnaire",
        default=None,
    )
    version: Optional[fhir.string] = Field(
        description="Business version of the questionnaire",
        default=None,
    )
    versionAlgorithmString: Optional[fhir.string] = Field(
        description="How to compare versions",
        default=None,
    )
    versionAlgorithmCoding: Optional[Coding] = Field(
        description="How to compare versions",
        default=None,
    )
    name: Optional[fhir.string] = Field(
        description="Name for this questionnaire (computer friendly)",
        default=None,
    )
    title: Optional[fhir.string] = Field(
        description="Name for this questionnaire (human friendly)",
        default=None,
    )
    derivedFrom: Optional[ListType[fhir.canonical]] = Field(
        description="Based on Questionnaire",
        default=None,
    )
    status: Optional[fhir.code] = Field(
        description="draft | active | retired | unknown",
        default=None,
    )
    experimental: Optional[fhir.boolean] = Field(
        description="For testing purposes, not real usage",
        default=None,
    )
    subjectType: Optional[ListType[fhir.code]] = Field(
        description="Resource that can be subject of QuestionnaireResponse",
        default=None,
    )
    date: Optional[fhir.dateTime] = Field(
        description="Date last changed",
        default=None,
    )
    publisher: Optional[fhir.string] = Field(
        description="Name of the publisher/steward (organization or individual)",
        default=None,
    )
    contact: Optional[ListType[ContactDetail]] = Field(
        description="Contact details for the publisher",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
        description="Natural language description of the questionnaire",
        default=None,
    )
    useContext: Optional[ListType[UsageContext]] = Field(
        description="The context that the content is intended to support",
        default=None,
    )
    jurisdiction: Optional[ListType[CodeableConcept]] = Field(
        description="Intended jurisdiction for questionnaire (if applicable)",
        default=None,
    )
    purpose: Optional[fhir.markdown] = Field(
        description="Why this questionnaire is defined",
        default=None,
    )
    copyright: Optional[fhir.markdown] = Field(
        description="Use and/or publishing restrictions",
        default=None,
    )
    copyrightLabel: Optional[fhir.string] = Field(
        description="Copyright holder and year(s)",
        default=None,
    )
    approvalDate: Optional[fhir.date_] = Field(
        description="When the questionnaire was approved by publisher",
        default=None,
    )
    lastReviewDate: Optional[fhir.date_] = Field(
        description="When the questionnaire was last reviewed by the publisher",
        default=None,
    )
    effectivePeriod: Optional[Period] = Field(
        description="When the questionnaire is expected to be used",
        default=None,
    )
    code: Optional[ListType[Coding]] = Field(
        description="Concept that represents the overall questionnaire",
        default=None,
    )
    item: Optional[ListType[QuestionnaireItem]] = Field(
        description="Questions and sections within the Questionnaire",
        default=None,
    )

    @property
    def versionAlgorithm(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="versionAlgorithm",
        )

    @model_validator(mode="after")
    def versionAlgorithm_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.String, Coding],
            field_name_base="versionAlgorithm",
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
            elements=("url",),
            expression="exists() implies matches('^[^|# ]+$')",
            human="URL should not contain | or # - these characters make processing canonical references problematic",
            key="cnl-1",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_que_2_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="descendants().linkId.isDistinct()",
            human="The link ids for groups and questions must be unique within the questionnaire",
            key="que-2",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_que_1a_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("item",),
            expression="(type='group' and %resource.status='complete') implies item.empty().not()",
            human="Group items must have nested items when Questionanire is complete",
            key="que-1a",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_que_1b_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("item",),
            expression="type='group' implies item.empty().not()",
            human="Groups should have items",
            key="que-1b",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_que_1c_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("item",),
            expression="type='display' implies item.empty()",
            human="Display items cannot have child items",
            key="que-1c",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_que_3_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("item",),
            expression="type!='display' or code.empty()",
            human='Display items cannot have a "code" asserted',
            key="que-3",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_que_4_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("item",),
            expression="answerOption.empty() or answerValueSet.empty()",
            human="A question cannot have both answerOption and answerValueSet",
            key="que-4",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_que_5_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("item",),
            expression="(type='coding' or type = 'decimal' or type = 'integer' or type = 'date' or type = 'dateTime' or type = 'time' or type = 'string' or type = 'quantity') or (answerValueSet.empty() and answerOption.empty())",
            human="Only coding, decimal, integer, date, dateTime, time, string or quantity  items can have answerOption or answerValueSet",
            key="que-5",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_que_6_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("item",),
            expression="type!='display' or (required.empty() and repeats.empty())",
            human="Required and repeat aren't permitted for display items",
            key="que-6",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_que_7_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("item.enableWhen",),
            expression="operator = 'exists' implies (answer is boolean)",
            human="If the operator is 'exists', the value must be a boolean",
            key="que-7",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_que_8_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("item",),
            expression="(type!='group' and type!='display') or initial.empty()",
            human="Initial values can't be specified for groups or display items",
            key="que-8",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_que_9_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("item",),
            expression="type!='display' or readOnly.empty()",
            human='Read-only can\'t be specified for "display" items',
            key="que-9",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_que_10_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("item",),
            expression="(type in ('boolean' | 'decimal' | 'integer' | 'string' | 'text' | 'url')) or answerConstraint='optionOrString' or maxLength.empty()",
            human="Maximum length can only be declared for simple question types",
            key="que-10",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_que_11_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("item",),
            expression="answerOption.empty() or initial.empty()",
            human="If one or more answerOption is present, initial cannot be present.  Use answerOption.initialSelected instead",
            key="que-11",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_que_12_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("item",),
            expression="enableWhen.count() > 1 implies enableBehavior.exists()",
            human="If there are more than one enableWhen, enableBehavior must be specified",
            key="que-12",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_que_13_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("item",),
            expression="repeats=true or initial.count() <= 1",
            human="Can only have multiple initial values for repeating items",
            key="que-13",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_que_14_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("item",),
            expression="answerConstraint.exists() implies answerOption.exists() or answerValueSet.exists()",
            human="Can only have answerConstraint if answerOption or answerValueSet are present.  (This is a warning because extensions may serve the same purpose)",
            key="que-14",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_que_15_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("item.linkId",),
            expression="$this.length() <= 255",
            human="Link ids should be 255 characters or less",
            key="que-15",
            severity="warning",
        )
