from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    DateTime,
    Boolean,
    Integer,
)

from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Coding,
    CodeableConcept,
    Reference,
    Identifier,
    BackboneElement,
    Period,
    Range,
    Quantity,
    Ratio,
    Attachment,
)
from .resource import Resource
from .domain_resource import DomainResource


class BiologicallyDerivedProductCollection(BackboneElement):
    """
    How this product was collected.
    """

    collector: Optional[Reference] = Field(
        description="Individual performing collection",
        default=None,
    )
    source: Optional[Reference] = Field(
        description="The patient who underwent the medical procedure to collect the product or the organization that facilitated the collection",
        default=None,
    )
    collectedDateTime: Optional[DateTime] = Field(
        description="Time of product collection",
        default=None,
    )
    collectedDateTime_ext: Optional[Element] = Field(
        description="Placeholder element for collectedDateTime extensions",
        default=None,
        alias="_collectedDateTime",
    )
    collectedPeriod: Optional[Period] = Field(
        description="Time of product collection",
        default=None,
    )

    @property
    def collected(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="collected",
        )

    @model_validator(mode="after")
    def collected_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[DateTime, Period],
            field_name_base="collected",
            required=False,
        )


class BiologicallyDerivedProductProperty(BackboneElement):
    """
    A property that is specific to this BiologicallyDerviedProduct instance.
    """

    type: Optional[CodeableConcept] = Field(
        description="Code that specifies the property",
        default=None,
    )
    valueBoolean: Optional[Boolean] = Field(
        description="Property values",
        default=None,
    )
    valueBoolean_ext: Optional[Element] = Field(
        description="Placeholder element for valueBoolean extensions",
        default=None,
        alias="_valueBoolean",
    )
    valueInteger: Optional[Integer] = Field(
        description="Property values",
        default=None,
    )
    valueInteger_ext: Optional[Element] = Field(
        description="Placeholder element for valueInteger extensions",
        default=None,
        alias="_valueInteger",
    )
    valueCodeableConcept: Optional[CodeableConcept] = Field(
        description="Property values",
        default=None,
    )
    valuePeriod: Optional[Period] = Field(
        description="Property values",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="Property values",
        default=None,
    )
    valueRange: Optional[Range] = Field(
        description="Property values",
        default=None,
    )
    valueRatio: Optional[Ratio] = Field(
        description="Property values",
        default=None,
    )
    valueString: Optional[String] = Field(
        description="Property values",
        default=None,
    )
    valueString_ext: Optional[Element] = Field(
        description="Placeholder element for valueString extensions",
        default=None,
        alias="_valueString",
    )
    valueAttachment: Optional[Attachment] = Field(
        description="Property values",
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
                Boolean,
                Integer,
                CodeableConcept,
                Period,
                Quantity,
                Range,
                Ratio,
                String,
                Attachment,
            ],
            field_name_base="value",
            required=True,
        )


class BiologicallyDerivedProduct(DomainResource):
    """
    A biological material originating from a biological entity intended to be transplanted or infused into another (possibly the same) biological entity.
    """

    _abstract = False
    _type = "BiologicallyDerivedProduct"
    _canonical_url = (
        "http://hl7.org/fhir/StructureDefinition/BiologicallyDerivedProduct"
    )

    productCategory: Optional[Coding] = Field(
        description="organ | tissue | fluid | cells | biologicalAgent",
        default=None,
    )
    productCode: Optional[CodeableConcept] = Field(
        description="A code that identifies the kind of this biologically derived product",
        default=None,
    )
    parent: Optional[ListType[Reference]] = Field(
        description="The parent biologically-derived product",
        default=None,
    )
    request: Optional[ListType[Reference]] = Field(
        description="Request to obtain and/or infuse this product",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Instance identifier",
        default=None,
    )
    biologicalSourceEvent: Optional[Identifier] = Field(
        description="An identifier that supports traceability to the event during which material in this product from one or more biological entities was obtained or pooled",
        default=None,
    )
    processingFacility: Optional[ListType[Reference]] = Field(
        description="Processing facilities responsible for the labeling and distribution of this biologically derived product",
        default=None,
    )
    division: Optional[String] = Field(
        description="A unique identifier for an aliquot of a product",
        default=None,
    )
    division_ext: Optional[Element] = Field(
        description="Placeholder element for division extensions",
        default=None,
        alias="_division",
    )
    productStatus: Optional[Coding] = Field(
        description="available | unavailable",
        default=None,
    )
    expirationDate: Optional[DateTime] = Field(
        description="Date, and where relevant time, of expiration",
        default=None,
    )
    expirationDate_ext: Optional[Element] = Field(
        description="Placeholder element for expirationDate extensions",
        default=None,
        alias="_expirationDate",
    )
    collection: Optional[BiologicallyDerivedProductCollection] = Field(
        description="How this product was collected",
        default=None,
    )
    storageTempRequirements: Optional[Range] = Field(
        description="Product storage temperature requirements",
        default=None,
    )
    property_: Optional[ListType[BiologicallyDerivedProductProperty]] = Field(
        description="A property that is specific to this BiologicallyDerviedProduct instance",
        default=None,
        alias="property",
    )
