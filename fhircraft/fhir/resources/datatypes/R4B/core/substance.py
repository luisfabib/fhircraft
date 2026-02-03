import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import String, Uri, Code, DateTime

from fhircraft.fhir.resources.datatypes.R4B.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    CodeableConcept,
    BackboneElement,
    Quantity,
    Ratio,
    Reference,
)
from .resource import Resource
from .domain_resource import DomainResource


class SubstanceInstance(BackboneElement):
    """
    Substance may be used to describe a kind of substance, or a specific package/container of the substance: an instance.
    """

    identifier: Optional[Identifier] = Field(
        description="Identifier of the package/container",
        default=None,
    )
    expiry: Optional[DateTime] = Field(
        description="When no longer valid to use",
        default=None,
    )
    expiry_ext: Optional[Element] = Field(
        description="Placeholder element for expiry extensions",
        default=None,
        alias="_expiry",
    )
    quantity: Optional[Quantity] = Field(
        description="Amount of substance in the package",
        default=None,
    )


class SubstanceIngredient(BackboneElement):
    """
    A substance can be composed of other substances.
    """

    quantity: Optional[Ratio] = Field(
        description="Optional amount (concentration)",
        default=None,
    )
    substanceCodeableConcept: Optional[CodeableConcept] = Field(
        description="A component of the substance",
        default=None,
    )
    substanceReference: Optional[Reference] = Field(
        description="A component of the substance",
        default=None,
    )

    @property
    def substance(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="substance",
        )

    @model_validator(mode="after")
    def substance_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[CodeableConcept, Reference],
            field_name_base="substance",
            required=True,
        )


class Substance(DomainResource):
    """
    A homogeneous material with a definite composition.
    """

    _abstract = False
    _type = "Substance"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Substance"

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
        description="Unique identifier",
        default=None,
    )
    status: Optional[Code] = Field(
        description="active | inactive | entered-in-error",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description="What class/type of substance this is",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="What substance this is",
        default=None,
    )
    description: Optional[String] = Field(
        description="Textual description of the substance, comments",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    instance: Optional[ListType[SubstanceInstance]] = Field(
        description="If this describes a specific package/container of the substance",
        default=None,
    )
    ingredient: Optional[ListType[SubstanceIngredient]] = Field(
        description="Composition information about the substance",
        default=None,
    )
