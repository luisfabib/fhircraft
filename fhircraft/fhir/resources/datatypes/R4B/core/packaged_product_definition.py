import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

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

from fhircraft.fhir.resources.datatypes.R4B.complex import (
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
    Duration,
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

class PackagedProductDefinitionPackageShelfLifeStorage(BackboneElement):
    """
    Shelf Life and storage information.
    """

    type: Optional[CodeableConcept] = Field(
        description="This describes the shelf life, taking into account various scenarios such as shelf life of the packaged Medicinal Product itself, shelf life after transformation where necessary and shelf life after the first opening of a bottle, etc. The shelf life type shall be specified using an appropriate controlled vocabulary The controlled term and the controlled term identifier shall be specified",
        default=None,
    )
    periodDuration: Optional[Duration] = Field(
        description="The shelf life time period can be specified using a numerical value for the period of time and its unit of time measurement The unit of measurement shall be specified in accordance with ISO 11240 and the resulting terminology The symbol and the symbol identifier shall be used",
        default=None,
    )
    periodString: Optional[String] = Field(
        description="The shelf life time period can be specified using a numerical value for the period of time and its unit of time measurement The unit of measurement shall be specified in accordance with ISO 11240 and the resulting terminology The symbol and the symbol identifier shall be used",
        default=None,
    )
    periodString_ext: Optional[Element] = Field(
        description="Placeholder element for periodString extensions",
        default=None,
        alias="_periodString",
    )
    specialPrecautionsForStorage: Optional[ListType[CodeableConcept]] = Field(
        description="Special precautions for storage, if any, can be specified using an appropriate controlled vocabulary. The controlled term and the controlled term identifier shall be specified",
        default=None,
    )

    @property
    def period(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="period",
        )

    @model_validator(mode="after")
    def period_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Duration, String],
            field_name_base="period",
            required=False,
        )

class PackagedProductDefinitionPackageProperty(BackboneElement):
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

class PackagedProductDefinitionPackageContainedItem(BackboneElement):
    """
    The item(s) within the packaging.
    """

    item: Optional[CodeableReference] = Field(
        description="The actual item(s) of medication, as manufactured, or a device, or other medically related item (food, biologicals, raw materials, medical fluids, gases etc.), as contained in the package",
        default=None,
    )
    amount: Optional[Quantity] = Field(
        description="The number of this type of item within this packaging",
        default=None,
    )

class PackagedProductDefinitionPackage(BackboneElement):
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
    shelfLifeStorage: Optional[
        ListType[PackagedProductDefinitionPackageShelfLifeStorage]
    ] = Field(
        description="Shelf Life and storage information",
        default=None,
    )
    manufacturer: Optional[ListType[Reference]] = Field(
        description="Manufacturer of this package Item (multiple means these are all possible manufacturers)",
        default=None,
    )
    property_: Optional[ListType[PackagedProductDefinitionPackageProperty]] = Field(
        description="General characteristics of this item",
        default=None,
        alias="property",
    )
    containedItem: Optional[ListType[PackagedProductDefinitionPackageContainedItem]] = (
        Field(
            description="The item(s) within the packaging",
            default=None,
        )
    )
    package: Optional[ListType["PackagedProductDefinitionPackage"]] = Field(
        description="Allows containers (and parts of containers) within containers, still a single packaged product",
        default=None,
    )

class PackagedProductDefinition(DomainResource):
    """
    A medically related item or items, in a container or package.
    """

    _abstract = False
    _type = "PackagedProductDefinition"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/PackagedProductDefinition"

    meta: Optional[Meta] = Field(
        description="Metadata about the resource.",
        default_factory=lambda: Meta(
            profile=[
                "http://hl7.org/fhir/StructureDefinition/PackagedProductDefinition"
            ]
        ),
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
        description="A unique identifier for this package as whole",
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
        description="A total of the complete count of contained items of a particular type/form, independent of sub-packaging or organization. This can be considered as the pack size",
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
    characteristic: Optional[ListType[CodeableConcept]] = Field(
        description='Allows the key features to be recorded, such as "hospital pack", "nurse prescribable"',
        default=None,
    )
    copackagedIndicator: Optional[Boolean] = Field(
        description="If the drug product is supplied with another item such as a diluent or adjuvant",
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
    package: Optional[PackagedProductDefinitionPackage] = Field(
        description="A packaging item, as a container for medically related items, possibly with other packaging items within, or a packaging component, such as bottle cap",
        default=None,
    )

