from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    DateTime,
    Markdown,
    Boolean,
    Integer,
    Date,
)

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
    MarketingStatus,
    ProductShelfLife,
    Attachment,
    CodeableReference,
)
from .resource import Resource
from .domain_resource import DomainResource


class PackagedProductDefinitionLegalStatusOfSupply(BackboneElement):
    """
    The legal status of supply of the packaged item as classified by the regulator.
    """

    code: Optional[CodeableConcept] = Field(
        description="The actual status of supply. In what situation this package type may be supplied for use",
        default=None,
    )
    jurisdiction: Optional[CodeableConcept] = Field(
        description="The place where the legal status of supply applies",
        default=None,
    )


class PackagedProductDefinitionPackagingProperty(BackboneElement):
    """
    General characteristics of this item.
    """

    type: Optional[CodeableConcept] = Field(
        description="A code expressing the type of characteristic",
        default=None,
    )
    valueCodeableConcept: Optional[CodeableConcept] = Field(
        description="A value for the characteristic",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="A value for the characteristic",
        default=None,
    )
    valueDate: Optional[Date] = Field(
        description="A value for the characteristic",
        default=None,
    )
    valueDate_ext: Optional[Element] = Field(
        description="Placeholder element for valueDate extensions",
        default=None,
        alias="_valueDate",
    )
    valueBoolean: Optional[Boolean] = Field(
        description="A value for the characteristic",
        default=None,
    )
    valueBoolean_ext: Optional[Element] = Field(
        description="Placeholder element for valueBoolean extensions",
        default=None,
        alias="_valueBoolean",
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
            field_types=[CodeableConcept, Quantity, Date, Boolean, Attachment],
            field_name_base="value",
            required=False,
        )


class PackagedProductDefinitionPackagingContainedItem(BackboneElement):
    """
    The item(s) within the packaging.
    """

    item: Optional[CodeableReference] = Field(
        description="The actual item(s) of medication, as manufactured, or a device, or other medically related item (food, biologicals, raw materials, medical fluids, gases etc.), as contained in the package",
        default=None,
    )
    amount: Optional[Quantity] = Field(
        description="The number of this type of item within this packaging or for continuous items such as liquids it is the quantity (for example 25ml). See also PackagedProductDefinition.containedItemQuantity (especially the long definition)",
        default=None,
    )


class PackagedProductDefinitionPackaging(BackboneElement):
    """
    A packaging item, as a container for medically related items, possibly with other packaging items within, or a packaging component, such as bottle cap (which is not a device or a medication manufactured item).
    """

    identifier: Optional[ListType[Identifier]] = Field(
        description="An identifier that is specific to this particular part of the packaging. Including possibly a Data Carrier Identifier",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="The physical type of the container of the items",
        default=None,
    )
    componentPart: Optional[Boolean] = Field(
        description="Is this a part of the packaging (e.g. a cap or bottle stopper), rather than the packaging itself (e.g. a bottle or vial)",
        default=None,
    )
    componentPart_ext: Optional[Element] = Field(
        description="Placeholder element for componentPart extensions",
        default=None,
        alias="_componentPart",
    )
    quantity: Optional[Integer] = Field(
        description="The quantity of this level of packaging in the package that contains it (with the outermost level being 1)",
        default=None,
    )
    quantity_ext: Optional[Element] = Field(
        description="Placeholder element for quantity extensions",
        default=None,
        alias="_quantity",
    )
    material: Optional[ListType[CodeableConcept]] = Field(
        description="Material type of the package item",
        default=None,
    )
    alternateMaterial: Optional[ListType[CodeableConcept]] = Field(
        description="A possible alternate material for this part of the packaging, that is allowed to be used instead of the usual material",
        default=None,
    )
    shelfLifeStorage: Optional[ListType[ProductShelfLife]] = Field(
        description="Shelf Life and storage information",
        default=None,
    )
    manufacturer: Optional[ListType[Reference]] = Field(
        description="Manufacturer of this packaging item (multiple means these are all potential manufacturers)",
        default=None,
    )
    property_: Optional[ListType[PackagedProductDefinitionPackagingProperty]] = Field(
        description="General characteristics of this item",
        default=None,
        alias="property",
    )
    containedItem: Optional[
        ListType[PackagedProductDefinitionPackagingContainedItem]
    ] = Field(
        description="The item(s) within the packaging",
        default=None,
    )
    packaging: Optional[ListType["PackagedProductDefinitionPackaging"]] = Field(
        description="Allows containers (and parts of containers) within containers, still as a part of single packaged product",
        default=None,
    )


class PackagedProductDefinitionCharacteristic(BackboneElement):
    """
    Allows the key features to be recorded, such as "hospital pack", "nurse prescribable", "calendar pack".
    """

    type: Optional[CodeableConcept] = Field(
        description="A code expressing the type of characteristic",
        default=None,
    )
    valueCodeableConcept: Optional[CodeableConcept] = Field(
        description="A value for the characteristic",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="A value for the characteristic",
        default=None,
    )
    valueDate: Optional[Date] = Field(
        description="A value for the characteristic",
        default=None,
    )
    valueDate_ext: Optional[Element] = Field(
        description="Placeholder element for valueDate extensions",
        default=None,
        alias="_valueDate",
    )
    valueBoolean: Optional[Boolean] = Field(
        description="A value for the characteristic",
        default=None,
    )
    valueBoolean_ext: Optional[Element] = Field(
        description="Placeholder element for valueBoolean extensions",
        default=None,
        alias="_valueBoolean",
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
            field_types=[CodeableConcept, Quantity, Date, Boolean, Attachment],
            field_name_base="value",
            required=False,
        )


class PackagedProductDefinition(DomainResource):
    """
    A medically related item or items, in a container or package.
    """

    _abstract = False
    _type = "PackagedProductDefinition"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/PackagedProductDefinition"

    identifier: Optional[ListType[Identifier]] = Field(
        description="A unique identifier for this package as whole - not for the content of the package",
        default=None,
    )
    name: Optional[String] = Field(
        description="A name for this package. Typically as listed in a drug formulary, catalogue, inventory etc",
        default=None,
    )
    name_ext: Optional[Element] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    type: Optional[CodeableConcept] = Field(
        description="A high level category e.g. medicinal product, raw material, shipping container etc",
        default=None,
    )
    packageFor: Optional[ListType[Reference]] = Field(
        description="The product that this is a pack for",
        default=None,
    )
    status: Optional[CodeableConcept] = Field(
        description="The status within the lifecycle of this item. High level - not intended to duplicate details elsewhere e.g. legal status, or authorization/marketing status",
        default=None,
    )
    statusDate: Optional[DateTime] = Field(
        description="The date at which the given status became applicable",
        default=None,
    )
    statusDate_ext: Optional[Element] = Field(
        description="Placeholder element for statusDate extensions",
        default=None,
        alias="_statusDate",
    )
    containedItemQuantity: Optional[ListType[Quantity]] = Field(
        description="A total of the complete count of contained items of a particular type/form, independent of sub-packaging or organization. This can be considered as the pack size. See also packaging.containedItem.amount (especially the long definition)",
        default=None,
    )
    description: Optional[Markdown] = Field(
        description="Textual description. Note that this is not the name of the package or product",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    legalStatusOfSupply: Optional[
        ListType[PackagedProductDefinitionLegalStatusOfSupply]
    ] = Field(
        description="The legal status of supply of the packaged item as classified by the regulator",
        default=None,
    )
    marketingStatus: Optional[ListType[MarketingStatus]] = Field(
        description="Allows specifying that an item is on the market for sale, or that it is not available, and the dates and locations associated",
        default=None,
    )
    copackagedIndicator: Optional[Boolean] = Field(
        description="Identifies if the drug product is supplied with another item such as a diluent or adjuvant",
        default=None,
    )
    copackagedIndicator_ext: Optional[Element] = Field(
        description="Placeholder element for copackagedIndicator extensions",
        default=None,
        alias="_copackagedIndicator",
    )
    manufacturer: Optional[ListType[Reference]] = Field(
        description="Manufacturer of this package type (multiple means these are all possible manufacturers)",
        default=None,
    )
    attachedDocument: Optional[ListType[Reference]] = Field(
        description="Additional information or supporting documentation about the packaged product",
        default=None,
    )
    packaging: Optional[PackagedProductDefinitionPackaging] = Field(
        description="A packaging item, as a container for medically related items, possibly with other packaging items within, or a packaging component, such as bottle cap",
        default=None,
    )
    characteristic: Optional[ListType[PackagedProductDefinitionCharacteristic]] = Field(
        description='Allows the key features to be recorded, such as "hospital pack", "nurse prescribable"',
        default=None,
    )
