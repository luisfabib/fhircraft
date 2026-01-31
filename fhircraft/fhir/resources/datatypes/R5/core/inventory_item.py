from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    Integer,
    Decimal,
    Boolean,
    Url,
    DateTime,
)

from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    CodeableConcept,
    BackboneElement,
    Coding,
    Reference,
    Quantity,
    Ratio,
    Range,
    Annotation,
    Address,
    Duration,
)
from .resource import Resource
from .domain_resource import DomainResource


class InventoryItemName(BackboneElement):
    """
    The item name(s) - the brand name, or common name, functional name, generic name.
    """

    nameType: Optional[Coding] = Field(
        description="The type of name e.g. \u0027brand-name\u0027, \u0027functional-name\u0027, \u0027common-name\u0027",
        default=None,
    )
    language: Optional[Code] = Field(
        description="The language used to express the item name",
        default=None,
    )

    name: Optional[String] = Field(
        description="The name or designation of the item",
        default=None,
    )
    name_ext: Optional[ListType[Optional[Element]]] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )


class InventoryItemResponsibleOrganization(BackboneElement):
    """
    Organization(s) responsible for the product.
    """

    role: Optional[CodeableConcept] = Field(
        description="The role of the organization e.g. manufacturer, distributor, or other",
        default=None,
    )
    organization: Optional[Reference] = Field(
        description="An organization that is associated with the item",
        default=None,
    )


class InventoryItemDescription(BackboneElement):
    """
    The descriptive characteristics of the inventory item.
    """

    language: Optional[Code] = Field(
        description="The language that is used in the item description",
        default=None,
    )

    description: Optional[String] = Field(
        description="Textual description of the item",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )


class InventoryItemAssociation(BackboneElement):
    """
    Association with other items or products.
    """

    associationType: Optional[CodeableConcept] = Field(
        description="The type of association between the device and the other item",
        default=None,
    )
    relatedItem: Optional[Reference] = Field(
        description="The related item or product",
        default=None,
    )
    quantity: Optional[Ratio] = Field(
        description="The quantity of the product in this product",
        default=None,
    )


class InventoryItemCharacteristic(BackboneElement):
    """
    The descriptive or identifying characteristics of the item.
    """

    characteristicType: Optional[CodeableConcept] = Field(
        description="The characteristic that is being defined",
        default=None,
    )
    valueString: Optional[String] = Field(
        description="The value of the attribute",
        default=None,
    )
    valueString_ext: Optional[Element] = Field(
        description="Placeholder element for valueString extensions",
        default=None,
        alias="_valueString",
    )
    valueInteger: Optional[Integer] = Field(
        description="The value of the attribute",
        default=None,
    )
    valueInteger_ext: Optional[Element] = Field(
        description="Placeholder element for valueInteger extensions",
        default=None,
        alias="_valueInteger",
    )
    valueDecimal: Optional[Decimal] = Field(
        description="The value of the attribute",
        default=None,
    )
    valueDecimal_ext: Optional[Element] = Field(
        description="Placeholder element for valueDecimal extensions",
        default=None,
        alias="_valueDecimal",
    )
    valueBoolean: Optional[Boolean] = Field(
        description="The value of the attribute",
        default=None,
    )
    valueBoolean_ext: Optional[Element] = Field(
        description="Placeholder element for valueBoolean extensions",
        default=None,
        alias="_valueBoolean",
    )
    valueUrl: Optional[Url] = Field(
        description="The value of the attribute",
        default=None,
    )
    valueUrl_ext: Optional[Element] = Field(
        description="Placeholder element for valueUrl extensions",
        default=None,
        alias="_valueUrl",
    )
    valueDateTime: Optional[DateTime] = Field(
        description="The value of the attribute",
        default=None,
    )
    valueDateTime_ext: Optional[Element] = Field(
        description="Placeholder element for valueDateTime extensions",
        default=None,
        alias="_valueDateTime",
    )
    valueQuantity: Optional[Quantity] = Field(
        description="The value of the attribute",
        default=None,
    )
    valueRange: Optional[Range] = Field(
        description="The value of the attribute",
        default=None,
    )
    valueRatio: Optional[Ratio] = Field(
        description="The value of the attribute",
        default=None,
    )
    valueAnnotation: Optional[Annotation] = Field(
        description="The value of the attribute",
        default=None,
    )
    valueAddress: Optional[Address] = Field(
        description="The value of the attribute",
        default=None,
    )
    valueDuration: Optional[Duration] = Field(
        description="The value of the attribute",
        default=None,
    )
    valueCodeableConcept: Optional[CodeableConcept] = Field(
        description="The value of the attribute",
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
                String,
                Integer,
                Decimal,
                Boolean,
                Url,
                DateTime,
                Quantity,
                Range,
                Ratio,
                Annotation,
                Address,
                Duration,
                CodeableConcept,
            ],
            field_name_base="value",
            required=True,
        )


class InventoryItemInstance(BackboneElement):
    """
    Instances or occurrences of the product.
    """

    identifier: Optional[ListType[Identifier]] = Field(
        description="The identifier for the physical instance, typically a serial number",
        default=None,
    )
    lotNumber: Optional[String] = Field(
        description="The lot or batch number of the item",
        default=None,
    )
    lotNumber_ext: Optional[Element] = Field(
        description="Placeholder element for lotNumber extensions",
        default=None,
        alias="_lotNumber",
    )
    expiry: Optional[DateTime] = Field(
        description="The expiry date or date and time for the product",
        default=None,
    )
    expiry_ext: Optional[Element] = Field(
        description="Placeholder element for expiry extensions",
        default=None,
        alias="_expiry",
    )
    subject: Optional[Reference] = Field(
        description="The subject that the item is associated with",
        default=None,
    )
    location: Optional[Reference] = Field(
        description="The location that the item is associated with",
        default=None,
    )


class InventoryItem(DomainResource):
    """
    functional description of an inventory item used in inventory and supply-related workflows.
    """

    _abstract = False
    _type = "InventoryItem"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/InventoryItem"

    identifier: Optional[ListType[Identifier]] = Field(
        description="Business identifier for the inventory item",
        default=None,
    )
    status: Optional[Code] = Field(
        description="active | inactive | entered-in-error | unknown",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description="Category or class of the item",
        default=None,
    )
    code: Optional[ListType[CodeableConcept]] = Field(
        description="Code designating the specific type of item",
        default=None,
    )
    name: Optional[ListType[InventoryItemName]] = Field(
        description="The item name(s) - the brand name, or common name, functional name, generic name or others",
        default=None,
    )
    responsibleOrganization: Optional[
        ListType[InventoryItemResponsibleOrganization]
    ] = Field(
        description="Organization(s) responsible for the product",
        default=None,
    )
    description: Optional[InventoryItemDescription] = Field(
        description="Descriptive characteristics of the item",
        default=None,
    )
    inventoryStatus: Optional[ListType[CodeableConcept]] = Field(
        description="The usage status like recalled, in use, discarded",
        default=None,
    )
    baseUnit: Optional[CodeableConcept] = Field(
        description="The base unit of measure - the unit in which the product is used or counted",
        default=None,
    )
    netContent: Optional[Quantity] = Field(
        description="Net content or amount present in the item",
        default=None,
    )
    association: Optional[ListType[InventoryItemAssociation]] = Field(
        description="Association with other items or products",
        default=None,
    )
    characteristic: Optional[ListType[InventoryItemCharacteristic]] = Field(
        description="Characteristic of the item",
        default=None,
    )
    instance: Optional[InventoryItemInstance] = Field(
        description="Instances or occurrences of the product",
        default=None,
    )
    productReference: Optional[Reference] = Field(
        description="Link to a product resource used in clinical workflows",
        default=None,
    )
