import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import String, Uri, Code

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

    outerPackaging: Optional[Identifier] = Field(
        description="A number appearing on the outer packaging of a specific batch",
        default=None,
    )
    immediatePackaging: Optional[Identifier] = Field(
        description="A number appearing on the immediate packaging (and not the outer packaging)",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "immediatePackaging",
                "outerPackaging",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class MedicinalProductPackagedPackageItem(BackboneElement):
    """
    A packaging item, as a contained for medicine, possibly with other packaging items within.
    """

    identifier: Optional[ListType[Identifier]] = Field(
        description="Including possibly Data Carrier Identifier",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="The physical type of the container of the medicine",
        default=None,
    )
    quantity: Optional[Quantity] = Field(
        description="The quantity of this package in the medicinal product, at the current level of packaging. The outermost is always 1",
        default=None,
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

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "manufacturer",
                "shelfLifeStorage",
                "otherCharacteristics",
                "physicalCharacteristics",
                "packageItem",
                "manufacturedItem",
                "device",
                "alternateMaterial",
                "material",
                "quantity",
                "type",
                "identifier",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class MedicinalProductPackaged(DomainResource):
    """
    A medicinal product in a container or package.
    """

    _abstract = False
    _type = "MedicinalProductPackaged"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/MedicinalProductPackaged"

    id: Optional[String] = Field(
        description="Logical id of this artifact",
        default=None,
    )
    id_ext: Optional[Element] = Field(
        description="Placeholder element for id extensions",
        default=None,
        alias="_id",
    )
    meta: Optional[Meta] = Field(
        description="Metadata about the resource.",
        default_factory=lambda: Meta(
            profile=["http://hl7.org/fhir/StructureDefinition/MedicinalProductPackaged"]
        ),
    )
    implicitRules: Optional[Uri] = Field(
        description="A set of rules under which this content was created",
        default=None,
    )
    implicitRules_ext: Optional[Element] = Field(
        description="Placeholder element for implicitRules extensions",
        default=None,
        alias="_implicitRules",
    )
    language: Optional[Code] = Field(
        description="Language of the resource content",
        default=None,
    )
    language_ext: Optional[Element] = Field(
        description="Placeholder element for language extensions",
        default=None,
        alias="_language",
    )
    text: Optional[Narrative] = Field(
        description="Text summary of the resource, for human interpretation",
        default=None,
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
    subject: Optional[ListType[Reference]] = Field(
        description="The product with this is a pack for",
        default=None,
    )
    description: Optional[String] = Field(
        description="Textual description",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
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
    packageItem: Optional[ListType[MedicinalProductPackagedPackageItem]] = Field(
        description="A packaging item, as a contained for medicine, possibly with other packaging items within",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "packageItem",
                "batchIdentifier",
                "manufacturer",
                "marketingAuthorization",
                "marketingStatus",
                "legalStatusOfSupply",
                "description",
                "subject",
                "identifier",
                "modifierExtension",
                "extension",
                "text",
                "language",
                "implicitRules",
                "meta",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ext_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "modifierExtension",
                "extension",
            ),
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_dom_2_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="contained.contained.empty()",
            human="If the resource is contained in another resource, it SHALL NOT contain nested Resources",
            key="dom-2",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_dom_3_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="contained.where((('#'+id in (%resource.descendants().reference | %resource.descendants().ofType(canonical) | %resource.descendants().ofType(uri) | %resource.descendants().ofType(url))) or descendants().where(reference = '#').exists() or descendants().where(as(canonical) = '#').exists() or descendants().where(as(canonical) = '#').exists()).not()).trace('unmatched', id).empty()",
            human="If the resource is contained in another resource, it SHALL be referred to from elsewhere in the resource or SHALL refer to the containing resource",
            key="dom-3",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_dom_4_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="contained.meta.versionId.empty() and contained.meta.lastUpdated.empty()",
            human="If a resource is contained in another resource, it SHALL NOT have a meta.versionId or a meta.lastUpdated",
            key="dom-4",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_dom_5_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="contained.meta.security.empty()",
            human="If a resource is contained in another resource, it SHALL NOT have a security label",
            key="dom-5",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_dom_6_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="text.`div`.exists()",
            human="A resource should have narrative for robust management",
            key="dom-6",
            severity="warning",
        )
