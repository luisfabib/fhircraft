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
    CodeableConcept,
    Period,
    BackboneElement,
    CodeableReference,
    Timing,
    Quantity,
    Annotation,
)
from .resource import Resource
from .domain_resource import DomainResource


class NutritionIntakeConsumedItem(BackboneElement):
    """
    What food or fluid product or item was consumed.
    """

    type: CodeableConcept = Field(
        description="The type of food or fluid product",
    )
    nutritionProduct: CodeableReference = Field(
        description="code that identifies the food or fluid product that was consumed",
    )
    schedule: Optional[Timing] = Field(
        description="Scheduled frequency of consumption",
        default=None,
    )
    amount: Optional[Quantity] = Field(
        description="Quantity of the specified food",
        default=None,
    )
    rate: Optional[Quantity] = Field(
        description="Rate at which enteral feeding was administered",
        default=None,
    )
    notConsumed: Optional[fhir.boolean] = Field(
        description="Flag to indicate if the food or fluid item was refused or otherwise not consumed",
        default=None,
    )
    notConsumedReason: Optional[CodeableConcept] = Field(
        description="Reason food or fluid was not consumed",
        default=None,
    )


class NutritionIntakeIngredientLabel(BackboneElement):
    """
    Total nutrient amounts for the whole meal, product, serving, etc.
    """

    nutrient: CodeableReference = Field(
        description="Total nutrient consumed",
    )
    amount: Quantity = Field(
        description="Total amount of nutrient consumed",
    )


class NutritionIntakePerformer(BackboneElement):
    """
    Who performed the intake and how they were involved.
    """

    function: Optional[CodeableConcept] = Field(
        description="Type of performer",
        default=None,
    )
    actor: Reference = Field(
        description="Who performed the intake",
    )


class NutritionIntake(DomainResource):
    """
    A record of food or fluid that is being consumed by a patient.  A NutritionIntake may indicate that the patient may be consuming the food or fluid now or has consumed the food or fluid in the past.  The source of this information can be the patient, significant other (such as a family member or spouse), or a clinician.  A common scenario where this information is captured is during the history taking process during a patient visit or stay or through an app that tracks food or fluids consumed.   The consumption information may come from sources such as the patient's memory, from a nutrition label,  or from a clinician documenting observed intake.
    """

    _abstract = False
    _type = "NutritionIntake"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/NutritionIntake"

    identifier: Optional[ListType[Identifier]] = Field(
        description="External identifier",
        default=None,
    )
    instantiatesCanonical: Optional[ListType[fhir.canonical]] = Field(
        description="Instantiates FHIR protocol or definition",
        default=None,
    )
    instantiatesUri: Optional[ListType[fhir.uri]] = Field(
        description="Instantiates external protocol or definition",
        default=None,
    )
    basedOn: Optional[ListType[Reference]] = Field(
        description="Fulfils plan, proposal or order",
        default=None,
    )
    partOf: Optional[ListType[Reference]] = Field(
        description="Part of referenced event",
        default=None,
    )
    status: fhir.code = Field(
        description="preparation | in-progress | not-done | on-hold | stopped | completed | entered-in-error | unknown",
    )
    statusReason: Optional[ListType[CodeableConcept]] = Field(
        description="Reason for current status",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="code representing an overall type of nutrition intake",
        default=None,
    )
    subject: Reference = Field(
        description="Who is/was consuming the food or fluid",
    )
    encounter: Optional[Reference] = Field(
        description="Encounter associated with NutritionIntake",
        default=None,
    )
    occurrenceDateTime: Optional[fhir.dateTime] = Field(
        description="The date/time or interval when the food or fluid is/was consumed",
        default=None,
    )
    occurrencePeriod: Optional[Period] = Field(
        description="The date/time or interval when the food or fluid is/was consumed",
        default=None,
    )
    recorded: Optional[fhir.dateTime] = Field(
        description="When the intake was recorded",
        default=None,
    )
    reportedBoolean: Optional[fhir.boolean] = Field(
        description="Person or organization that provided the information about the consumption of this food or fluid",
        default=None,
    )
    reportedReference: Optional[Reference] = Field(
        description="Person or organization that provided the information about the consumption of this food or fluid",
        default=None,
    )
    consumedItem: ListType[NutritionIntakeConsumedItem] = Field(
        description="What food or fluid product or item was consumed",
        min_length=1,
    )
    ingredientLabel: Optional[ListType[NutritionIntakeIngredientLabel]] = Field(
        description="Total nutrient for the whole meal, product, serving",
        default=None,
    )
    performer: Optional[ListType[NutritionIntakePerformer]] = Field(
        description="Who was performed in the intake",
        default=None,
    )
    location: Optional[Reference] = Field(
        description="Where the intake occurred",
        default=None,
    )
    derivedFrom: Optional[ListType[Reference]] = Field(
        description="Additional supporting information",
        default=None,
    )
    reason: Optional[ListType[CodeableReference]] = Field(
        description="Reason for why the food or fluid is /was consumed",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Further information about the consumption",
        default=None,
    )

    @property
    def occurrence(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="occurrence",
        )

    @property
    def reported(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="reported",
        )

    @model_validator(mode="after")
    def occurrence_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.DateTime, Period],
            field_name_base="occurrence",
            required=False,
        )

    @model_validator(mode="after")
    def reported_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.Boolean, Reference],
            field_name_base="reported",
            required=False,
        )
