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
    CodeableReference,
    CodeableConcept,
    BackboneElement,
    Timing,
    Quantity,
    Ratio,
    Annotation,
)
from .resource import Resource
from .domain_resource import DomainResource

class NutritionOrderOralDietSchedule(BackboneElement):
    """
    Schedule information for an oral diet.
    """

    timing: Optional[ListType[Timing]] = Field(
        description="Scheduled frequency of diet",
        default=None,
    )
    asNeeded: Optional[Boolean] = Field(
        description="Take \u0027as needed\u0027",
        default=None,
    )
    asNeededFor: Optional[CodeableConcept] = Field(
        description="Take \u0027as needed\u0027 for x",
        default=None,
    )

class NutritionOrderOralDietNutrient(BackboneElement):
    """
    Class that defines the quantity and type of nutrient modifications (for example carbohydrate, fiber or sodium) required for the oral diet.
    """

    modifier: Optional[CodeableConcept] = Field(
        description="Type of nutrient that is being modified",
        default=None,
    )
    amount: Optional[Quantity] = Field(
        description="Quantity of the specified nutrient",
        default=None,
    )

class NutritionOrderOralDietTexture(BackboneElement):
    """
    Class that describes any texture modifications required for the patient to safely consume various types of solid foods.
    """

    modifier: Optional[CodeableConcept] = Field(
        description="Code to indicate how to alter the texture of the foods, e.g. pureed",
        default=None,
    )
    foodType: Optional[CodeableConcept] = Field(
        description="Concepts that are used to identify an entity that is ingested for nutritional purposes",
        default=None,
    )

class NutritionOrderOralDiet(BackboneElement):
    """
    Diet given orally in contrast to enteral (tube) feeding.
    """

    type: Optional[ListType[CodeableConcept]] = Field(
        description="Type of oral diet or diet restrictions that describe what can be consumed orally",
        default=None,
    )
    schedule: Optional[NutritionOrderOralDietSchedule] = Field(
        description="Scheduling information for oral diets",
        default=None,
    )
    nutrient: Optional[ListType[NutritionOrderOralDietNutrient]] = Field(
        description="Required  nutrient modifications",
        default=None,
    )
    texture: Optional[ListType[NutritionOrderOralDietTexture]] = Field(
        description="Required  texture modifications",
        default=None,
    )
    fluidConsistencyType: Optional[ListType[CodeableConcept]] = Field(
        description="The required consistency of fluids and liquids provided to the patient",
        default=None,
    )
    instruction: Optional[String] = Field(
        description="Instructions or additional information about the oral diet",
        default=None,
    )

class NutritionOrderSupplementSchedule(BackboneElement):
    """
    Schedule information for a supplement.
    """

    timing: Optional[ListType[Timing]] = Field(
        description="Scheduled frequency of diet",
        default=None,
    )
    asNeeded: Optional[Boolean] = Field(
        description="Take \u0027as needed\u0027",
        default=None,
    )
    asNeededFor: Optional[CodeableConcept] = Field(
        description="Take \u0027as needed\u0027 for x",
        default=None,
    )

class NutritionOrderSupplement(BackboneElement):
    """
    Oral nutritional products given in order to add further nutritional value to the patient's diet.
    """

    type: Optional[CodeableReference] = Field(
        description="Type of supplement product requested",
        default=None,
    )
    productName: Optional[String] = Field(
        description="Product or brand name of the nutritional supplement",
        default=None,
    )
    schedule: Optional[NutritionOrderSupplementSchedule] = Field(
        description="Scheduling information for supplements",
        default=None,
    )
    quantity: Optional[Quantity] = Field(
        description="Amount of the nutritional supplement",
        default=None,
    )
    instruction: Optional[String] = Field(
        description="Instructions or additional information about the oral supplement",
        default=None,
    )

class NutritionOrderEnteralFormulaAdditive(BackboneElement):
    """
    Indicates modular components to be provided in addition or mixed with the base formula.
    """

    type: Optional[CodeableReference] = Field(
        description="Type of modular component to add to the feeding",
        default=None,
    )
    productName: Optional[String] = Field(
        description="Product or brand name of the modular additive",
        default=None,
    )
    quantity: Optional[Quantity] = Field(
        description="Amount of additive to be given or mixed in",
        default=None,
    )

class NutritionOrderEnteralFormulaAdministrationSchedule(BackboneElement):
    """
    Schedule information for an enteral formula.
    """

    timing: Optional[ListType[Timing]] = Field(
        description="Scheduled frequency of enteral formula",
        default=None,
    )
    asNeeded: Optional[Boolean] = Field(
        description="Take \u0027as needed\u0027",
        default=None,
    )
    asNeededFor: Optional[CodeableConcept] = Field(
        description="Take \u0027as needed\u0027 for x",
        default=None,
    )

class NutritionOrderEnteralFormulaAdministration(BackboneElement):
    """
    Formula administration instructions as structured data.  This repeating structure allows for changing the administration rate or volume over time for both bolus and continuous feeding.  An example of this would be an instruction to increase the rate of continuous feeding every 2 hours.
    """

    schedule: Optional[NutritionOrderEnteralFormulaAdministrationSchedule] = Field(
        description="Scheduling information for enteral formula products",
        default=None,
    )
    quantity: Optional[Quantity] = Field(
        description="The volume of formula to provide",
        default=None,
    )
    rateQuantity: Optional[Quantity] = Field(
        description="Speed with which the formula is provided per period of time",
        default=None,
    )
    rateRatio: Optional[Ratio] = Field(
        description="Speed with which the formula is provided per period of time",
        default=None,
    )

    @property
    def rate(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="rate",
        )

    @model_validator(mode="after")
    def rate_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Quantity, Ratio],
            field_name_base="rate",
            required=False,
        )

class NutritionOrderEnteralFormula(BackboneElement):
    """
    Feeding provided through the gastrointestinal tract via a tube, catheter, or stoma that delivers nutrition distal to the oral cavity.
    """

    baseFormulaType: Optional[CodeableReference] = Field(
        description="Type of enteral or infant formula",
        default=None,
    )
    baseFormulaProductName: Optional[String] = Field(
        description="Product or brand name of the enteral or infant formula",
        default=None,
    )
    deliveryDevice: Optional[ListType[CodeableReference]] = Field(
        description="Intended type of device for the administration",
        default=None,
    )
    additive: Optional[ListType[NutritionOrderEnteralFormulaAdditive]] = Field(
        description="Components to add to the feeding",
        default=None,
    )
    caloricDensity: Optional[Quantity] = Field(
        description="Amount of energy per specified volume that is required",
        default=None,
    )
    routeOfAdministration: Optional[CodeableConcept] = Field(
        description="How the formula should enter the patient\u0027s gastrointestinal tract",
        default=None,
    )
    administration: Optional[ListType[NutritionOrderEnteralFormulaAdministration]] = (
        Field(
            description="Formula feeding instruction as structured data",
            default=None,
        )
    )
    maxVolumeToDeliver: Optional[Quantity] = Field(
        description="Upper limit on formula volume per unit of time",
        default=None,
    )
    administrationInstruction: Optional[Markdown] = Field(
        description="Formula feeding instructions expressed as text",
        default=None,
    )

class NutritionOrder(DomainResource):
    """
    A request to supply a diet, formula feeding (enteral) or oral nutritional supplement to a patient/resident.
    """

    _abstract = False
    _type = "NutritionOrder"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/NutritionOrder"

    identifier: Optional[ListType[Identifier]] = Field(
        description="Identifiers assigned to this order",
        default=None,
    )
    instantiatesCanonical: Optional[ListType[Canonical]] = Field(
        description="Instantiates FHIR protocol or definition",
        default=None,
    )
    instantiatesUri: Optional[ListType[Uri]] = Field(
        description="Instantiates external protocol or definition",
        default=None,
    )
    instantiates: Optional[ListType[Uri]] = Field(
        description="Instantiates protocol or definition",
        default=None,
    )
    basedOn: Optional[ListType[Reference]] = Field(
        description="What this order fulfills",
        default=None,
    )
    groupIdentifier: Optional[Identifier] = Field(
        description="Composite Request ID",
        default=None,
    )
    status: Optional[Code] = Field(
        description="draft | active | on-hold | revoked | completed | entered-in-error | unknown",
        default=None,
    )
    intent: Optional[Code] = Field(
        description="proposal | plan | directive | order | original-order | reflex-order | filler-order | instance-order | option",
        default=None,
    )
    priority: Optional[Code] = Field(
        description="routine | urgent | asap | stat",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="Who requires the diet, formula or nutritional supplement",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="The encounter associated with this nutrition order",
        default=None,
    )
    supportingInformation: Optional[ListType[Reference]] = Field(
        description="Information to support fulfilling of the nutrition order",
        default=None,
    )
    dateTime: Optional[DateTime] = Field(
        description="Date and time the nutrition order was requested",
        default=None,
    )
    orderer: Optional[Reference] = Field(
        description="Who ordered the diet, formula or nutritional supplement",
        default=None,
    )
    performer: Optional[ListType[CodeableReference]] = Field(
        description="Who is desired to perform the administration of what is being ordered",
        default=None,
    )
    allergyIntolerance: Optional[ListType[Reference]] = Field(
        description="List of the patient\u0027s food and nutrition-related allergies and intolerances",
        default=None,
    )
    foodPreferenceModifier: Optional[ListType[CodeableConcept]] = Field(
        description="Order-specific modifier about the type of food that should be given",
        default=None,
    )
    excludeFoodModifier: Optional[ListType[CodeableConcept]] = Field(
        description="Order-specific modifier about the type of food that should not be given",
        default=None,
    )
    outsideFoodAllowed: Optional[Boolean] = Field(
        description="Capture when a food item is brought in by the patient and/or family",
        default=None,
    )
    oralDiet: Optional[NutritionOrderOralDiet] = Field(
        description="Oral diet components",
        default=None,
    )
    supplement: Optional[ListType[NutritionOrderSupplement]] = Field(
        description="Supplement components",
        default=None,
    )
    enteralFormula: Optional[NutritionOrderEnteralFormula] = Field(
        description="Enteral formula components",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Comments",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_nor_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="oralDiet.exists() or supplement.exists() or enteralFormula.exists()",
            human="Nutrition Order SHALL contain either Oral Diet , Supplement, or Enteral Formula class",
            key="nor-1",
            severity="warning",
        )
