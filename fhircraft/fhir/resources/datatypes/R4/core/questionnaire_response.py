import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    Canonical,
    DateTime,
    Boolean,
    Decimal,
    Integer,
    Date,
    Time,
)

from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Reference,
    BackboneElement,
    Attachment,
    Coding,
    Quantity,
)
from .resource import Resource
from .domain_resource import DomainResource


class QuestionnaireResponseItemAnswer(BackboneElement):
    """
    The respondent's answer(s) to the question.
    """

    valueBoolean: Optional[Boolean] = Field(
        description="Single-valued answer to the question",
        default=None,
    )
    valueBoolean_ext: Optional[Element] = Field(
        description="Placeholder element for valueBoolean extensions",
        default=None,
        alias="_valueBoolean",
    )
    valueDecimal: Optional[Decimal] = Field(
        description="Single-valued answer to the question",
        default=None,
    )
    valueDecimal_ext: Optional[Element] = Field(
        description="Placeholder element for valueDecimal extensions",
        default=None,
        alias="_valueDecimal",
    )
    valueInteger: Optional[Integer] = Field(
        description="Single-valued answer to the question",
        default=None,
    )
    valueInteger_ext: Optional[Element] = Field(
        description="Placeholder element for valueInteger extensions",
        default=None,
        alias="_valueInteger",
    )
    valueDate: Optional[Date] = Field(
        description="Single-valued answer to the question",
        default=None,
    )
    valueDate_ext: Optional[Element] = Field(
        description="Placeholder element for valueDate extensions",
        default=None,
        alias="_valueDate",
    )
    valueDateTime: Optional[DateTime] = Field(
        description="Single-valued answer to the question",
        default=None,
    )
    valueDateTime_ext: Optional[Element] = Field(
        description="Placeholder element for valueDateTime extensions",
        default=None,
        alias="_valueDateTime",
    )
    valueTime: Optional[Time] = Field(
        description="Single-valued answer to the question",
        default=None,
    )
    valueTime_ext: Optional[Element] = Field(
        description="Placeholder element for valueTime extensions",
        default=None,
        alias="_valueTime",
    )
    valueString: Optional[String] = Field(
        description="Single-valued answer to the question",
        default=None,
    )
    valueString_ext: Optional[Element] = Field(
        description="Placeholder element for valueString extensions",
        default=None,
        alias="_valueString",
    )
    valueUri: Optional[Uri] = Field(
        description="Single-valued answer to the question",
        default=None,
    )
    valueUri_ext: Optional[Element] = Field(
        description="Placeholder element for valueUri extensions",
        default=None,
        alias="_valueUri",
    )
    valueAttachment: Optional[Attachment] = Field(
        description="Single-valued answer to the question",
        default=None,
    )
    valueCoding: Optional[Coding] = Field(
        description="Single-valued answer to the question",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="Single-valued answer to the question",
        default=None,
    )
    valueReference: Optional[Reference] = Field(
        description="Single-valued answer to the question",
        default=None,
    )
    item: Optional[ListType["QuestionnaireResponseItem"]] = Field(
        description="Nested groups and questions",
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
            required=False,
        )


class QuestionnaireResponseItem(BackboneElement):
    """
    A group or question item from the original questionnaire for which answers are provided.
    """

    linkId: Optional[String] = Field(
        description="Pointer to specific item from Questionnaire",
        default=None,
    )
    linkId_ext: Optional[Element] = Field(
        description="Placeholder element for linkId extensions",
        default=None,
        alias="_linkId",
    )
    definition: Optional[Uri] = Field(
        description="ElementDefinition - details for the item",
        default=None,
    )
    definition_ext: Optional[Element] = Field(
        description="Placeholder element for definition extensions",
        default=None,
        alias="_definition",
    )
    text: Optional[String] = Field(
        description="Name for group or question text",
        default=None,
    )
    text_ext: Optional[Element] = Field(
        description="Placeholder element for text extensions",
        default=None,
        alias="_text",
    )
    answer: Optional[ListType[QuestionnaireResponseItemAnswer]] = Field(
        description="The response(s) to the question",
        default=None,
    )
    item: Optional[ListType["QuestionnaireResponseItem"]] = Field(
        description="Nested questionnaire response items",
        default=None,
    )


class QuestionnaireResponse(DomainResource):
    """
    A structured set of questions and their answers. The questions are ordered and grouped into coherent subsets, corresponding to the structure of the grouping of the questionnaire being responded to.
    """

    _abstract = False
    _type = "QuestionnaireResponse"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/QuestionnaireResponse"

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
    identifier: Optional[Identifier] = Field(
        description="Unique id for this set of answers",
        default=None,
    )
    basedOn: Optional[ListType[Reference]] = Field(
        description="Request fulfilled by this QuestionnaireResponse",
        default=None,
    )
    partOf: Optional[ListType[Reference]] = Field(
        description="Part of this action",
        default=None,
    )
    questionnaire: Optional[Canonical] = Field(
        description="Form being answered",
        default=None,
    )
    questionnaire_ext: Optional[Element] = Field(
        description="Placeholder element for questionnaire extensions",
        default=None,
        alias="_questionnaire",
    )
    status: Optional[Code] = Field(
        description="in-progress | completed | amended | entered-in-error | stopped",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    subject: Optional[Reference] = Field(
        description="The subject of the questions",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="Encounter created as part of",
        default=None,
    )
    authored: Optional[DateTime] = Field(
        description="Date the answers were gathered",
        default=None,
    )
    authored_ext: Optional[Element] = Field(
        description="Placeholder element for authored extensions",
        default=None,
        alias="_authored",
    )
    author: Optional[Reference] = Field(
        description="Person who received and recorded the answers",
        default=None,
    )
    source: Optional[Reference] = Field(
        description="The person who answered the questions",
        default=None,
    )
    item: Optional[ListType[QuestionnaireResponseItem]] = Field(
        description="Groups and questions",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_qrs_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("item",),
            expression="(answer.exists() and item.exists()).not()",
            human="Nested item can't be beneath both item and answer",
            key="qrs-1",
            severity="error",
        )


QuestionnaireResponseItemAnswer.model_rebuild()
