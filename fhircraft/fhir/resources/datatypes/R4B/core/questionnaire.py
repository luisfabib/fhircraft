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
    Identifier,
    ContactDetail,
    UsageContext,
    CodeableConcept,
    Period,
    Coding,
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

    question: Optional[String] = Field(
        description="Question that determines whether item is enabled",
        default=None,
    )
    operator: Optional[Code] = Field(
        description="exists | = | != | \u003e | \u003c | \u003e= | \u003c=",
        default=None,
    )
    answerBoolean: Optional[Boolean] = Field(
        description="Value for question comparison based on operator",
        default=None,
    )
    answerDecimal: Optional[Decimal] = Field(
        description="Value for question comparison based on operator",
        default=None,
    )
    answerInteger: Optional[Integer] = Field(
        description="Value for question comparison based on operator",
        default=None,
    )
    answerDate: Optional[Date] = Field(
        description="Value for question comparison based on operator",
        default=None,
    )
    answerDateTime: Optional[DateTime] = Field(
        description="Value for question comparison based on operator",
        default=None,
    )
    answerTime: Optional[Time] = Field(
        description="Value for question comparison based on operator",
        default=None,
    )
    answerString: Optional[String] = Field(
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
                Boolean,
                Decimal,
                Integer,
                Date,
                DateTime,
                Time,
                String,
                Coding,
                Quantity,
                Reference,
            ],
            field_name_base="answer",
            required=True,
        )

class QuestionnaireItemAnswerOption(BackboneElement):
    """
    One of the permitted answers for a "choice" or "open-choice" question.
    """

    valueInteger: Optional[Integer] = Field(
        description="Answer value",
        default=None,
    )
    valueDate: Optional[Date] = Field(
        description="Answer value",
        default=None,
    )
    valueTime: Optional[Time] = Field(
        description="Answer value",
        default=None,
    )
    valueString: Optional[String] = Field(
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
    initialSelected: Optional[Boolean] = Field(
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
            field_types=[Integer, Date, Time, String, Coding, Reference],
            field_name_base="value",
            required=True,
        )

class QuestionnaireItemInitial(BackboneElement):
    """
    One or more values that should be pre-populated in the answer when initially rendering the questionnaire for user input.
    """

    valueBoolean: Optional[Boolean] = Field(
        description="Actual value for initializing the question",
        default=None,
    )
    valueDecimal: Optional[Decimal] = Field(
        description="Actual value for initializing the question",
        default=None,
    )
    valueInteger: Optional[Integer] = Field(
        description="Actual value for initializing the question",
        default=None,
    )
    valueDate: Optional[Date] = Field(
        description="Actual value for initializing the question",
        default=None,
    )
    valueDateTime: Optional[DateTime] = Field(
        description="Actual value for initializing the question",
        default=None,
    )
    valueTime: Optional[Time] = Field(
        description="Actual value for initializing the question",
        default=None,
    )
    valueString: Optional[String] = Field(
        description="Actual value for initializing the question",
        default=None,
    )
    valueUri: Optional[Uri] = Field(
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
                Boolean,
                Decimal,
                Integer,
                Date,
                DateTime,
                Time,
                String,
                Uri,
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

    linkId: Optional[String] = Field(
        description="Unique id for item in questionnaire",
        default=None,
    )
    definition: Optional[Uri] = Field(
        description="ElementDefinition - details for the item",
        default=None,
    )
    code: Optional[ListType[Coding]] = Field(
        description="Corresponding concept for this item in a terminology",
        default=None,
    )
    prefix: Optional[String] = Field(
        description='E.g. "1(a)", "2.5.3"',
        default=None,
    )
    text: Optional[String] = Field(
        description="Primary text for the item",
        default=None,
    )
    type: Optional[Code] = Field(
        description="group | display | boolean | decimal | integer | date | dateTime +",
        default=None,
    )
    enableWhen: Optional[ListType[QuestionnaireItemEnableWhen]] = Field(
        description="Only allow data when",
        default=None,
    )
    enableBehavior: Optional[Code] = Field(
        description="all | any",
        default=None,
    )
    required: Optional[Boolean] = Field(
        description="Whether the item must be included in data results",
        default=None,
    )
    repeats: Optional[Boolean] = Field(
        description="Whether the item may repeat",
        default=None,
    )
    readOnly: Optional[Boolean] = Field(
        description="Don\u0027t allow human editing",
        default=None,
    )
    maxLength: Optional[Integer] = Field(
        description="No more than this many characters",
        default=None,
    )
    answerValueSet: Optional[Canonical] = Field(
        description="Valueset containing permitted answers",
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
    url: Optional[Uri] = Field(
        description="Canonical identifier for this questionnaire, represented as a URI (globally unique)",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Additional identifier for the questionnaire",
        default=None,
    )
    version: Optional[String] = Field(
        description="Business version of the questionnaire",
        default=None,
    )
    name: Optional[String] = Field(
        description="Name for this questionnaire (computer friendly)",
        default=None,
    )
    title: Optional[String] = Field(
        description="Name for this questionnaire (human friendly)",
        default=None,
    )
    derivedFrom: Optional[ListType[Canonical]] = Field(
        description="Instantiates protocol or definition",
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
    subjectType: Optional[ListType[Code]] = Field(
        description="Resource that can be subject of QuestionnaireResponse",
        default=None,
    )
    date: Optional[DateTime] = Field(
        description="Date last changed",
        default=None,
    )
    publisher: Optional[String] = Field(
        description="Name of the publisher (organization or individual)",
        default=None,
    )
    contact: Optional[ListType[ContactDetail]] = Field(
        description="Contact details for the publisher",
        default=None,
    )
    description: Optional[Markdown] = Field(
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
    purpose: Optional[Markdown] = Field(
        description="Why this questionnaire is defined",
        default=None,
    )
    copyright: Optional[Markdown] = Field(
        description="Use and/or publishing restrictions",
        default=None,
    )
    approvalDate: Optional[Date] = Field(
        description="When the questionnaire was approved by publisher",
        default=None,
    )
    lastReviewDate: Optional[Date] = Field(
        description="When the questionnaire was last reviewed",
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

    @model_validator(mode="after")
    def FHIR_que_0_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.exists() implies name.matches('[A-Z]([A-Za-z0-9_]){0,254}')",
            human="Name should be usable as an identifier for the module by machine processing applications such as code generation",
            key="que-0",
            severity="warning",
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
    def FHIR_que_2_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="descendants().linkId.isDistinct()",
            human="The link ids for groups and questions must be unique within the questionnaire",
            key="que-2",
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
            expression="(type ='choice' or type = 'open-choice' or type = 'decimal' or type = 'integer' or type = 'date' or type = 'dateTime' or type = 'time' or type = 'string' or type = 'quantity') or (answerValueSet.empty() and answerOption.empty())",
            human="Only 'choice' and 'open-choice' items can have answerValueSet",
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
            expression="(type in ('boolean' | 'decimal' | 'integer' | 'string' | 'text' | 'url' | 'open-choice')) or maxLength.empty()",
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
            human="If one or more answerOption is present, initial[x] must be missing",
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
