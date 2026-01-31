import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import String, Uri, Code

from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    BackboneElement,
    CodeableConcept,
    Reference,
    Range,
    Identifier,
    Quantity,
)
from .resource import Resource
from .domain_resource import DomainResource


class SubstanceReferenceInformationGene(BackboneElement):
    """
    Todo.
    """

    geneSequenceOrigin: Optional[CodeableConcept] = Field(
        description="Todo",
        default=None,
    )
    gene: Optional[CodeableConcept] = Field(
        description="Todo",
        default=None,
    )
    source: Optional[ListType[Reference]] = Field(
        description="Todo",
        default=None,
    )


class SubstanceReferenceInformationGeneElement(BackboneElement):
    """
    Todo.
    """

    type: Optional[CodeableConcept] = Field(
        description="Todo",
        default=None,
    )
    element: Optional[Identifier] = Field(
        description="Todo",
        default=None,
    )
    source: Optional[ListType[Reference]] = Field(
        description="Todo",
        default=None,
    )


class SubstanceReferenceInformationClassification(BackboneElement):
    """
    Todo.
    """

    domain: Optional[CodeableConcept] = Field(
        description="Todo",
        default=None,
    )
    classification: Optional[CodeableConcept] = Field(
        description="Todo",
        default=None,
    )
    subtype: Optional[ListType[CodeableConcept]] = Field(
        description="Todo",
        default=None,
    )
    source: Optional[ListType[Reference]] = Field(
        description="Todo",
        default=None,
    )


class SubstanceReferenceInformationTarget(BackboneElement):
    """
    Todo.
    """

    target: Optional[Identifier] = Field(
        description="Todo",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Todo",
        default=None,
    )
    interaction: Optional[CodeableConcept] = Field(
        description="Todo",
        default=None,
    )
    organism: Optional[CodeableConcept] = Field(
        description="Todo",
        default=None,
    )
    organismType: Optional[CodeableConcept] = Field(
        description="Todo",
        default=None,
    )
    amountQuantity: Optional[Quantity] = Field(
        description="Todo",
        default=None,
    )
    amountRange: Optional[Range] = Field(
        description="Todo",
        default=None,
    )
    amountString: Optional[String] = Field(
        description="Todo",
        default=None,
    )
    amountString_ext: Optional[Element] = Field(
        description="Placeholder element for amountString extensions",
        default=None,
        alias="_amountString",
    )
    amountType: Optional[CodeableConcept] = Field(
        description="Todo",
        default=None,
    )
    source: Optional[ListType[Reference]] = Field(
        description="Todo",
        default=None,
    )

    @property
    def amount(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="amount",
        )

    @model_validator(mode="after")
    def amount_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Quantity, Range, String],
            field_name_base="amount",
            required=False,
        )


class SubstanceReferenceInformation(DomainResource):
    """
    Todo.
    """

    _abstract = False
    _type = "SubstanceReferenceInformation"
    _canonical_url = (
        "http://hl7.org/fhir/StructureDefinition/SubstanceReferenceInformation"
    )

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
    comment: Optional[String] = Field(
        description="Todo",
        default=None,
    )
    comment_ext: Optional[Element] = Field(
        description="Placeholder element for comment extensions",
        default=None,
        alias="_comment",
    )
    gene: Optional[ListType[SubstanceReferenceInformationGene]] = Field(
        description="Todo",
        default=None,
    )
    geneElement: Optional[ListType[SubstanceReferenceInformationGeneElement]] = Field(
        description="Todo",
        default=None,
    )
    classification: Optional[ListType[SubstanceReferenceInformationClassification]] = (
        Field(
            description="Todo",
            default=None,
        )
    )
    target: Optional[ListType[SubstanceReferenceInformationTarget]] = Field(
        description="Todo",
        default=None,
    )
