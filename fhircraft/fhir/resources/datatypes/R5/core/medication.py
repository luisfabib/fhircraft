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
    Reference,
    Quantity,
    BackboneElement,
    CodeableReference,
    Ratio,
)
from .resource import Resource
from .domain_resource import DomainResource

class MedicationIngredient(BackboneElement):
    """
    Identifies a particular constituent of interest in the product.
    """

    item: Optional[CodeableReference] = Field(
        description="The ingredient (substance or medication) that the ingredient.strength relates to",
        default=None,
    )
    isActive: Optional[Boolean] = Field(
        description="Active ingredient indicator",
        default=None,
    )
    strengthRatio: Optional[Ratio] = Field(
        description="Quantity of ingredient present",
        default=None,
    )
    strengthCodeableConcept: Optional[CodeableConcept] = Field(
        description="Quantity of ingredient present",
        default=None,
    )
    strengthQuantity: Optional[Quantity] = Field(
        description="Quantity of ingredient present",
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
            field_types=[Ratio, CodeableConcept, Quantity],
            field_name_base="strength",
            required=False,
        )

class MedicationBatch(BackboneElement):
    """
    Information that only applies to packages (not products).
    """

    lotNumber: Optional[String] = Field(
        description="Identifier assigned to batch",
        default=None,
    )
    expirationDate: Optional[DateTime] = Field(
        description="When batch will expire",
        default=None,
    )

class Medication(DomainResource):
    """
    This resource is primarily used for the identification and definition of a medication, including ingredients, for the purposes of prescribing, dispensing, and administering a medication as well as for making statements about medication use.
    """

    _abstract = False
    _type = "Medication"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Medication"

    identifier: Optional[ListType[Identifier]] = Field(
        description="Business identifier for this medication",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="Codes that identify this medication",
        default=None,
    )
    status: Optional[Code] = Field(
        description="active | inactive | entered-in-error",
        default=None,
    )
    marketingAuthorizationHolder: Optional[Reference] = Field(
        description="Organization that has authorization to market medication",
        default=None,
    )
    doseForm: Optional[CodeableConcept] = Field(
        description="powder | tablets | capsule +",
        default=None,
    )
    totalVolume: Optional[Quantity] = Field(
        description="When the specified product code does not infer a package size, this is the specific amount of drug in the product",
        default=None,
    )
    ingredient: Optional[ListType[MedicationIngredient]] = Field(
        description="Active or inactive ingredient",
        default=None,
    )
    batch: Optional[MedicationBatch] = Field(
        description="Details about packaged medications",
        default=None,
    )
    definition: Optional[Reference] = Field(
        description="Knowledge about this medication",
        default=None,
    )
