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
    CodeableConcept,
    Reference,
    BackboneElement,
    CodeableReference,
    Ratio,
    Quantity,
    Attachment,
    Identifier,
    Annotation,
)
from .resource import Resource
from .domain_resource import DomainResource

class NutritionProductNutrient(BackboneElement):
    """
    The product's nutritional information expressed by the nutrients.
    """

    item: Optional[CodeableReference] = Field(
        description="The (relevant) nutrients in the product",
        default=None,
    )
    amount: Optional[ListType[Ratio]] = Field(
        description="The amount of nutrient expressed in one or more units: X per pack / per serving / per dose",
        default=None,
    )

class NutritionProductIngredient(BackboneElement):
    """
    Ingredients contained in this product.
    """

    item: Optional[CodeableReference] = Field(
        description="The ingredient contained in the product",
        default=None,
    )
    amount: Optional[ListType[Ratio]] = Field(
        description="The amount of ingredient that is in the product",
        default=None,
    )

class NutritionProductCharacteristic(BackboneElement):
    """
    Specifies descriptive properties of the nutrition product.
    """

    type: Optional[CodeableConcept] = Field(
        description="Code specifying the type of characteristic",
        default=None,
    )
    valueCodeableConcept: Optional[CodeableConcept] = Field(
        description="The value of the characteristic",
        default=None,
    )
    valueString: Optional[String] = Field(
        description="The value of the characteristic",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="The value of the characteristic",
        default=None,
    )
    valueBase64Binary: Optional[Base64Binary] = Field(
        description="The value of the characteristic",
        default=None,
    )
    valueAttachment: Optional[Attachment] = Field(
        description="The value of the characteristic",
        default=None,
    )
    valueBoolean: Optional[Boolean] = Field(
        description="The value of the characteristic",
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
                CodeableConcept,
                String,
                Quantity,
                Base64Binary,
                Attachment,
                Boolean,
            ],
            field_name_base="value",
            required=True,
        )

class NutritionProductInstance(BackboneElement):
    """
    Conveys instance-level information about this product item. One or several physical, countable instances or occurrences of the product.
    """

    quantity: Optional[Quantity] = Field(
        description="The amount of items or instances",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="The identifier for the physical instance, typically a serial number or manufacturer number",
        default=None,
    )
    name: Optional[String] = Field(
        description="The name for the specific product",
        default=None,
    )
    lotNumber: Optional[String] = Field(
        description="The identification of the batch or lot of the product",
        default=None,
    )
    expiry: Optional[DateTime] = Field(
        description="The expiry date or date and time for the product",
        default=None,
    )
    useBy: Optional[DateTime] = Field(
        description="The date until which the product is expected to be good for consumption",
        default=None,
    )
    biologicalSourceEvent: Optional[Identifier] = Field(
        description="An identifier that supports traceability to the event during which material in this product from one or more biological entities was obtained or pooled",
        default=None,
    )

class NutritionProduct(DomainResource):
    """
    A food or supplement that is consumed by patients.
    """

    _abstract = False
    _type = "NutritionProduct"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/NutritionProduct"

    code: Optional[CodeableConcept] = Field(
        description="A code that can identify the detailed nutrients and ingredients in a specific food product",
        default=None,
    )
    status: Optional[Code] = Field(
        description="active | inactive | entered-in-error",
        default=None,
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description="Broad product groups or categories used to classify the product, such as Legume and Legume Products, Beverages, or Beef Products",
        default=None,
    )
    manufacturer: Optional[ListType[Reference]] = Field(
        description="Manufacturer, representative or officially responsible for the product",
        default=None,
    )
    nutrient: Optional[ListType[NutritionProductNutrient]] = Field(
        description="The product\u0027s nutritional information expressed by the nutrients",
        default=None,
    )
    ingredient: Optional[ListType[NutritionProductIngredient]] = Field(
        description="Ingredients contained in this product",
        default=None,
    )
    knownAllergen: Optional[ListType[CodeableReference]] = Field(
        description="Known or suspected allergens that are a part of this product",
        default=None,
    )
    characteristic: Optional[ListType[NutritionProductCharacteristic]] = Field(
        description="Specifies descriptive properties of the nutrition product",
        default=None,
    )
    instance: Optional[ListType[NutritionProductInstance]] = Field(
        description="One or several physical instances or occurrences of the nutrition product",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Comments made about the product",
        default=None,
    )
