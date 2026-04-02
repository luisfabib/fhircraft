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
    CodeableConcept,
    CodeableReference,
    Quantity,
    BackboneElement,
    Ratio,
    Reference,
)
from .resource import Resource
from .domain_resource import DomainResource

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

    identifier: Optional[ListType[Identifier]] = Field(
        description="Unique identifier",
        default=None,
    )
    instance: Optional[Boolean] = Field(
        description="Is this an instance of a substance or a kind of one",
        default=None,
    )
    status: Optional[Code] = Field(
        description="active | inactive | entered-in-error",
        default=None,
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description="What class/type of substance this is",
        default=None,
    )
    code: Optional[CodeableReference] = Field(
        description="What substance this is",
        default=None,
    )
    description: Optional[Markdown] = Field(
        description="Textual description of the substance, comments",
        default=None,
    )
    expiry: Optional[DateTime] = Field(
        description="When no longer valid to use",
        default=None,
    )
    quantity: Optional[Quantity] = Field(
        description="Amount of substance in the package",
        default=None,
    )
    ingredient: Optional[ListType[SubstanceIngredient]] = Field(
        description="Composition information about the substance",
        default=None,
    )
