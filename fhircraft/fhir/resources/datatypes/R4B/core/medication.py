import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    Boolean,
    DateTime,
)

from fhircraft.fhir.resources.datatypes.R4B.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    Ratio,
    BackboneElement,
)
from .resource import Resource
from .domain_resource import DomainResource

class MedicationIngredient(BackboneElement):
    """
    Identifies a particular constituent of interest in the product.
    """

    itemCodeableConcept: Optional[CodeableConcept] = Field(
        description="The actual ingredient or content",
        default=None,
    )
    itemReference: Optional[Reference] = Field(
        description="The actual ingredient or content",
        default=None,
    )
    isActive: Optional[Boolean] = Field(
        description="Active ingredient indicator",
        default=None,
    )
    isActive_ext: Optional[Element] = Field(
        description="Placeholder element for isActive extensions",
        default=None,
        alias="_isActive",
    )
    strength: Optional[Ratio] = Field(
        description="Quantity of ingredient present",
        default=None,
    )

    @property
    def item(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="item",
        )

    @model_validator(mode="after")
    def item_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[CodeableConcept, Reference],
            field_name_base="item",
            required=True,
        )

class MedicationBatch(BackboneElement):
    """
    Information that only applies to packages (not products).
    """

    lotNumber: Optional[String] = Field(
        description="Identifier assigned to batch",
        default=None,
    )
    lotNumber_ext: Optional[Element] = Field(
        description="Placeholder element for lotNumber extensions",
        default=None,
        alias="_lotNumber",
    )
    expirationDate: Optional[DateTime] = Field(
        description="When batch will expire",
        default=None,
    )
    expirationDate_ext: Optional[Element] = Field(
        description="Placeholder element for expirationDate extensions",
        default=None,
        alias="_expirationDate",
    )

class Medication(DomainResource):
    """
    This resource is primarily used for the identification and definition of a medication for the purposes of prescribing, dispensing, and administering a medication as well as for making statements about medication use.
    """

    _abstract = False
    _type = "Medication"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Medication"

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
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    manufacturer: Optional[Reference] = Field(
        description="Manufacturer of the item",
        default=None,
    )
    form: Optional[CodeableConcept] = Field(
        description="powder | tablets | capsule +",
        default=None,
    )
    amount: Optional[Ratio] = Field(
        description="Amount of drug in package",
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

