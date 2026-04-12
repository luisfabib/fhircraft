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

    valueBoolean: Optional[fhir.boolean] = Field(
        description="Single-valued answer to the question",
        default=None,
    )
    valueDecimal: Optional[fhir.decimal] = Field(
        description="Single-valued answer to the question",
        default=None,
    )
    valueInteger: Optional[fhir.integer] = Field(
        description="Single-valued answer to the question",
        default=None,
    )
    valueDate: Optional[fhir.date_] = Field(
        description="Single-valued answer to the question",
        default=None,
    )
    valueDateTime: Optional[fhir.dateTime] = Field(
        description="Single-valued answer to the question",
        default=None,
    )
    valueTime: Optional[fhir.time_] = Field(
        description="Single-valued answer to the question",
        default=None,
    )
    valueString: Optional[fhir.string] = Field(
        description="Single-valued answer to the question",
        default=None,
    )
    valueUri: Optional[fhir.uri] = Field(
        description="Single-valued answer to the question",
        default=None,
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
        description="Child items of question",
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


class QuestionnaireResponseItem(BackboneElement):
    """
    A group or question item from the original questionnaire for which answers are provided.
    """

    linkId: Optional[fhir.string] = Field(
        description="Pointer to specific item from Questionnaire",
        default=None,
    )
    definition: Optional[fhir.uri] = Field(
        description="ElementDefinition - details for the item",
        default=None,
    )
    text: Optional[fhir.string] = Field(
        description="Name for group or question text",
        default=None,
    )
    answer: Optional[ListType[QuestionnaireResponseItemAnswer]] = Field(
        description="The response(s) to the question",
        default=None,
    )
    item: Optional[ListType["QuestionnaireResponseItem"]] = Field(
        description="Child items of group item",
        default=None,
    )


class QuestionnaireResponse(DomainResource):
    """
    A structured set of questions and their answers. The questions are ordered and grouped into coherent subsets, corresponding to the structure of the grouping of the questionnaire being responded to.
    """

    _abstract = False
    _type = "QuestionnaireResponse"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/QuestionnaireResponse"

    identifier: Optional[ListType[Identifier]] = Field(
        description="Business identifier for this set of answers",
        default=None,
    )
    basedOn: Optional[ListType[Reference]] = Field(
        description="Request fulfilled by this QuestionnaireResponse",
        default=None,
    )
    partOf: Optional[ListType[Reference]] = Field(
        description="Part of referenced event",
        default=None,
    )
    questionnaire: Optional[fhir.canonical] = Field(
        description="canonical URL of Questionnaire being answered",
        default=None,
    )
    status: Optional[fhir.code] = Field(
        description="in-progress | completed | amended | entered-in-error | stopped",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="The subject of the questions",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="Encounter the questionnaire response is part of",
        default=None,
    )
    authored: Optional[fhir.dateTime] = Field(
        description="Date the answers were gathered",
        default=None,
    )
    author: Optional[Reference] = Field(
        description="The individual or device that received and recorded the answers",
        default=None,
    )
    source: Optional[Reference] = Field(
        description="The individual or device that answered the questions",
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
            human="Item cannot contain both item and answer",
            key="qrs-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_qrs_2_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("item",),
            expression="repeat(answer|item).select(item.where(answer.value.exists()).linkId.isDistinct()).allTrue()",
            human="Repeated answers are combined in the answers array of a single item",
            key="qrs-2",
            severity="error",
        )
