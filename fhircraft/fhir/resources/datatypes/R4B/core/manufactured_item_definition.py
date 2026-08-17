import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)


import fhircraft.fhir.resources.datatypes.R4B.primitive as fhir
from fhircraft.fhir.resources.datatypes.R4B.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    BackboneElement,
    Quantity,
    Attachment,
)
from .resource import Resource
from .domain_resource import DomainResource

class ManufacturedItemDefinitionProperty(BackboneElement):
    """
    General characteristics of this item.
    """

    type: CodeableConcept = Field(
        description="A code expressing the type of characteristic",
    )
    valueCodeableConcept: Optional[CodeableConcept] = Field(
        description="A value for the characteristic",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="A value for the characteristic",
        default=None,
    )
    valueDate: Optional[fhir.date_] = Field(
        description="A value for the characteristic",
        default=None,
    )
    valueBoolean: Optional[fhir.boolean] = Field(
        description="A value for the characteristic",
        default=None,
    )
    valueAttachment: Optional[Attachment] = Field(
        description="A value for the characteristic",
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
            field_types=[CodeableConcept, Quantity, fhir.Date, fhir.Boolean, Attachment],
            field_name_base="value",
            required=False,
        )

class ManufacturedItemDefinition(DomainResource):
    """
    The definition and characteristics of a medicinal manufactured item, such as a tablet or capsule, as contained in a packaged medicinal product.
    """

    _abstract = False
    _type = "ManufacturedItemDefinition"
    _canonical_url = (
        "http://hl7.org/fhir/StructureDefinition/ManufacturedItemDefinition"
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
    identifier: Optional[ListType[Identifier]] = Field(
        description="Unique identifier",
        default=None,
    )
    status: fhir.code = Field(
        description="draft | active | retired | unknown",
    )
    manufacturedDoseForm: CodeableConcept = Field(
        description="Dose form as manufactured (before any necessary transformation)",
    )
    unitOfPresentation: Optional[CodeableConcept] = Field(
        description="The \u201creal world\u201d units in which the quantity of the item is described",
        default=None,
    )
    manufacturer: Optional[ListType[Reference]] = Field(
        description='Manufacturer of the item (Note that this should be named "manufacturer" but it currently causes technical issues)',
        default=None,
    )
    ingredient: Optional[ListType[CodeableConcept]] = Field(
        description="The ingredients of this manufactured item. Only needed if these are not specified by incoming references from the Ingredient resource",
        default=None,
    )
    property_: Optional[ListType[ManufacturedItemDefinitionProperty]] = Field(
        description="General characteristics of this item",
        default=None,
        alias="property",
    )
