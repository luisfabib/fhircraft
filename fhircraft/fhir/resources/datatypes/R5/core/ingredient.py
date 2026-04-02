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
    Reference,
    CodeableConcept,
    BackboneElement,
    CodeableReference,
    Ratio,
    RatioRange,
    Quantity,
)
from .resource import Resource
from .domain_resource import DomainResource

class IngredientManufacturer(BackboneElement):
    """
    The organization(s) that manufacture this ingredient. Can be used to indicate:         1) Organizations we are aware of that manufacture this ingredient         2) Specific Manufacturer(s) currently being used         3) Set of organisations allowed to manufacture this ingredient for this product         Users must be clear on the application of context relevant to their use case.
    """

    role: Optional[Code] = Field(
        description="allowed | possible | actual",
        default=None,
    )
    manufacturer: Optional[Reference] = Field(
        description="An organization that manufactures this ingredient",
        default=None,
    )

class IngredientSubstanceStrengthReferenceStrength(BackboneElement):
    """
    Strength expressed in terms of a reference substance. For when the ingredient strength is additionally expressed as equivalent to the strength of some other closely related substance (e.g. salt vs. base). Reference strength represents the strength (quantitative composition) of the active moiety of the active substance. There are situations when the active substance and active moiety are different, therefore both a strength and a reference strength are needed.
    """

    substance: Optional[CodeableReference] = Field(
        description="Relevant reference substance",
        default=None,
    )
    strengthRatio: Optional[Ratio] = Field(
        description="Strength expressed in terms of a reference substance",
        default=None,
    )
    strengthRatioRange: Optional[RatioRange] = Field(
        description="Strength expressed in terms of a reference substance",
        default=None,
    )
    strengthQuantity: Optional[Quantity] = Field(
        description="Strength expressed in terms of a reference substance",
        default=None,
    )
    measurementPoint: Optional[String] = Field(
        description="When strength is measured at a particular point or distance",
        default=None,
    )
    country: Optional[ListType[CodeableConcept]] = Field(
        description="Where the strength range applies",
        default=None,
    )

    @property
    def strength(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="strength",
        )

    @model_validator(mode="after")
    def strength_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Ratio, RatioRange, Quantity],
            field_name_base="strength",
            required=True,
        )

class IngredientSubstanceStrength(BackboneElement):
    """
    The quantity of substance in the unit of presentation, or in the volume (or mass) of the single pharmaceutical product or manufactured item. The allowed repetitions do not represent different strengths, but are different representations - mathematically equivalent - of a single strength.
    """

    presentationRatio: Optional[Ratio] = Field(
        description="The quantity of substance in the unit of presentation",
        default=None,
    )
    presentationRatioRange: Optional[RatioRange] = Field(
        description="The quantity of substance in the unit of presentation",
        default=None,
    )
    presentationCodeableConcept: Optional[CodeableConcept] = Field(
        description="The quantity of substance in the unit of presentation",
        default=None,
    )
    presentationQuantity: Optional[Quantity] = Field(
        description="The quantity of substance in the unit of presentation",
        default=None,
    )
    textPresentation: Optional[String] = Field(
        description="Text of either the whole presentation strength or a part of it (rest being in Strength.presentation as a ratio)",
        default=None,
    )
    concentrationRatio: Optional[Ratio] = Field(
        description="The strength per unitary volume (or mass)",
        default=None,
    )
    concentrationRatioRange: Optional[RatioRange] = Field(
        description="The strength per unitary volume (or mass)",
        default=None,
    )
    concentrationCodeableConcept: Optional[CodeableConcept] = Field(
        description="The strength per unitary volume (or mass)",
        default=None,
    )
    concentrationQuantity: Optional[Quantity] = Field(
        description="The strength per unitary volume (or mass)",
        default=None,
    )
    textConcentration: Optional[String] = Field(
        description="Text of either the whole concentration strength or a part of it (rest being in Strength.concentration as a ratio)",
        default=None,
    )
    basis: Optional[CodeableConcept] = Field(
        description="A code that indicates if the strength is, for example, based on the ingredient substance as stated or on the substance base (when the ingredient is a salt)",
        default=None,
    )
    measurementPoint: Optional[String] = Field(
        description="When strength is measured at a particular point or distance",
        default=None,
    )
    country: Optional[ListType[CodeableConcept]] = Field(
        description="Where the strength range applies",
        default=None,
    )
    referenceStrength: Optional[
        ListType[IngredientSubstanceStrengthReferenceStrength]
    ] = Field(
        description="Strength expressed in terms of a reference substance",
        default=None,
    )

    @property
    def presentation(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="presentation",
        )

    @property
    def concentration(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="concentration",
        )

    @model_validator(mode="after")
    def presentation_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Ratio, RatioRange, CodeableConcept, Quantity],
            field_name_base="presentation",
            required=False,
        )

    @model_validator(mode="after")
    def concentration_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Ratio, RatioRange, CodeableConcept, Quantity],
            field_name_base="concentration",
            required=False,
        )

class IngredientSubstance(BackboneElement):
    """
    The substance that comprises this ingredient.
    """

    code: Optional[CodeableReference] = Field(
        description="A code or full resource that represents the ingredient substance",
        default=None,
    )
    strength: Optional[ListType[IngredientSubstanceStrength]] = Field(
        description="The quantity of substance, per presentation, or per volume or mass, and type of quantity",
        default=None,
    )

class Ingredient(DomainResource):
    """
    An ingredient of a manufactured item or pharmaceutical product.
    """

    _abstract = False
    _type = "Ingredient"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Ingredient"

    identifier: Optional[Identifier] = Field(
        description="An identifier or code by which the ingredient can be referenced",
        default=None,
    )
    status: Optional[Code] = Field(
        description="draft | active | retired | unknown",
        default=None,
    )
    for_: Optional[ListType[Reference]] = Field(
        description="The product which this ingredient is a constituent part of",
        default=None,
        alias="for",
    )
    role: Optional[CodeableConcept] = Field(
        description="Purpose of the ingredient within the product, e.g. active, inactive",
        default=None,
    )
    function: Optional[ListType[CodeableConcept]] = Field(
        description="Precise action within the drug product, e.g. antioxidant, alkalizing agent",
        default=None,
    )
    group: Optional[CodeableConcept] = Field(
        description="A classification of the ingredient according to where in the physical item it tends to be used, such the outer shell of a tablet, inner body or ink",
        default=None,
    )
    allergenicIndicator: Optional[Boolean] = Field(
        description="If the ingredient is a known or suspected allergen",
        default=None,
    )
    comment: Optional[Markdown] = Field(
        description="A place for providing any notes that are relevant to the component, e.g. removed during process, adjusted for loss on drying",
        default=None,
    )
    manufacturer: Optional[ListType[IngredientManufacturer]] = Field(
        description="An organization that manufactures this ingredient",
        default=None,
    )
    substance: Optional[IngredientSubstance] = Field(
        description="The substance that comprises this ingredient",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ing_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="Ingredient.where(allergenicIndicator=true).count() + Ingredient.substance.code.reference.count()  < 2",
            human="If an ingredient is noted as an allergen (allergenicIndicator) then its substance should be a code. If the substance is a SubstanceDefinition, then the allegen information should be documented in that resource",
            key="ing-1",
            severity="error",
        )
