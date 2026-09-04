import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)


import fhircraft.fhir.resources.datatypes.R4.primitive as fhir
from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Reference,
    ProductShelfLife,
    CodeableConcept,
    MarketingStatus,
    BackboneElement,
    Quantity,
    ProdCharacteristic,
)
from .resource import Resource
from .domain_resource import DomainResource

class MedicinalProductPackagedBatchIdentifier(BackboneElement):
    """
    Batch numbering.
    """

    outerPackaging: Identifier = Field(
        description="A number appearing on the outer packaging of a specific batch",
    )
    immediatePackaging: Optional[Identifier] = Field(
        description="A number appearing on the immediate packaging (and not the outer packaging)",
        default=None,
    )

class MedicinalProductPackagedPackageItem(BackboneElement):
    """
    A packaging item, as a contained for medicine, possibly with other packaging items within.
    """

    identifier: Optional[ListType[Identifier]] = Field(
        description="Including possibly Data Carrier Identifier",
        default=None,
    )
    type: CodeableConcept = Field(
        description="The physical type of the container of the medicine",
    )
    quantity: Quantity = Field(
        description="The quantity of this package in the medicinal product, at the current level of packaging. The outermost is always 1",
    )
    material: Optional[ListType[CodeableConcept]] = Field(
        description="Material type of the package item",
        default=None,
    )
    alternateMaterial: Optional[ListType[CodeableConcept]] = Field(
        description="A possible alternate material for the packaging",
        default=None,
    )
    device: Optional[ListType[Reference]] = Field(
        description="A device accompanying a medicinal product",
        default=None,
    )
    manufacturedItem: Optional[ListType[Reference]] = Field(
        description="The manufactured item as contained in the packaged medicinal product",
        default=None,
    )
    packageItem: Optional[ListType["MedicinalProductPackagedPackageItem"]] = Field(
        description="Allows containers within containers",
        default=None,
    )
    physicalCharacteristics: Optional[ProdCharacteristic] = Field(
        description="Dimensions, color etc.",
        default=None,
    )
    otherCharacteristics: Optional[ListType[CodeableConcept]] = Field(
        description="Other codeable characteristics",
        default=None,
    )
    shelfLifeStorage: Optional[ListType[ProductShelfLife]] = Field(
        description="Shelf Life and storage information",
        default=None,
    )
    manufacturer: Optional[ListType[Reference]] = Field(
        description="Manufacturer of this Package Item",
        default=None,
    )

class MedicinalProductPackaged(DomainResource):
    """
    A medicinal product in a container or package.
    """

    _abstract = False
    _type = "MedicinalProductPackaged"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/MedicinalProductPackaged"

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
    subject: Optional[ListType[Reference]] = Field(
        description="The product with this is a pack for",
        default=None,
    )
    description: Optional[fhir.string] = Field(
        description="Textual description",
        default=None,
    )
    legalStatusOfSupply: Optional[CodeableConcept] = Field(
        description="The legal status of supply of the medicinal product as classified by the regulator",
        default=None,
    )
    marketingStatus: Optional[ListType[MarketingStatus]] = Field(
        description="Marketing information",
        default=None,
    )
    marketingAuthorization: Optional[Reference] = Field(
        description="Manufacturer of this Package Item",
        default=None,
    )
    manufacturer: Optional[ListType[Reference]] = Field(
        description="Manufacturer of this Package Item",
        default=None,
    )
    batchIdentifier: Optional[ListType[MedicinalProductPackagedBatchIdentifier]] = (
        Field(
            description="Batch numbering",
            default=None,
        )
    )
    packageItem: ListType[MedicinalProductPackagedPackageItem] = Field(
        description="A packaging item, as a contained for medicine, possibly with other packaging items within",
     	min_length=1,
	)
