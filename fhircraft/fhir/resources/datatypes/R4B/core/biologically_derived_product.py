import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    Integer,
    DateTime,
    Decimal,
)

from fhircraft.fhir.resources.datatypes.R4B.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    BackboneElement,
    Period,
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
        description="Who is product from",
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


class BiologicallyDerivedProductProcessing(BackboneElement):
    """
    Any processing of the product during collection that does not change the fundamental nature of the product. For example adding anti-coagulants during the collection of Peripheral Blood Stem Cells.
    """

    description: Optional[String] = Field(
        description="Description of of processing",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    procedure: Optional[CodeableConcept] = Field(
        description="Procesing code",
        default=None,
    )
    additive: Optional[Reference] = Field(
        description="Substance added during processing",
        default=None,
    )
    timeDateTime: Optional[DateTime] = Field(
        description="Time of processing",
        default=None,
    )
    timeDateTime_ext: Optional[Element] = Field(
        description="Placeholder element for timeDateTime extensions",
        default=None,
        alias="_timeDateTime",
    )
    timePeriod: Optional[Period] = Field(
        description="Time of processing",
        default=None,
    )

    @property
    def time(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="time",
        )

    @model_validator(mode="after")
    def time_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[DateTime, Period],
            field_name_base="time",
            required=False,
        )


class BiologicallyDerivedProductManipulation(BackboneElement):
    """
    Any manipulation of product post-collection that is intended to alter the product.  For example a buffy-coat enrichment or CD8 reduction of Peripheral Blood Stem Cells to make it more suitable for infusion.
    """

    description: Optional[String] = Field(
        description="Description of manipulation",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    timeDateTime: Optional[DateTime] = Field(
        description="Time of manipulation",
        default=None,
    )
    timeDateTime_ext: Optional[Element] = Field(
        description="Placeholder element for timeDateTime extensions",
        default=None,
        alias="_timeDateTime",
    )
    timePeriod: Optional[Period] = Field(
        description="Time of manipulation",
        default=None,
    )

    @property
    def time(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="time",
        )

    @model_validator(mode="after")
    def time_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[DateTime, Period],
            field_name_base="time",
            required=False,
        )


class BiologicallyDerivedProductStorage(BackboneElement):
    """
    Product storage.
    """

    description: Optional[String] = Field(
        description="Description of storage",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    temperature: Optional[Decimal] = Field(
        description="Storage temperature",
        default=None,
    )
    temperature_ext: Optional[Element] = Field(
        description="Placeholder element for temperature extensions",
        default=None,
        alias="_temperature",
    )
    scale: Optional[Code] = Field(
        description="farenheit | celsius | kelvin",
        default=None,
    )
    scale_ext: Optional[Element] = Field(
        description="Placeholder element for scale extensions",
        default=None,
        alias="_scale",
    )
    duration: Optional[Period] = Field(
        description="Storage timeperiod",
        default=None,
    )


class BiologicallyDerivedProduct(DomainResource):
    """
        A material substance originating from a biological entity intended to be transplanted or infused
    into another (possibly the same) biological entity.
    """

    _abstract = False
    _type = "BiologicallyDerivedProduct"
    _canonical_url = (
        "http://hl7.org/fhir/StructureDefinition/BiologicallyDerivedProduct"
    )

    meta: Optional[Meta] = Field(
        description="Metadata about the resource.",
        default_factory=lambda: Meta(
            profile=[
                "http://hl7.org/fhir/StructureDefinition/BiologicallyDerivedProduct"
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
        description="External ids for this item",
        default=None,
    )
    productCategory: Optional[Code] = Field(
        description="organ | tissue | fluid | cells | biologicalAgent",
        default=None,
    )
    productCategory_ext: Optional[Element] = Field(
        description="Placeholder element for productCategory extensions",
        default=None,
        alias="_productCategory",
    )
    productCode: Optional[CodeableConcept] = Field(
        description="What this biologically derived product is",
        default=None,
    )
    status: Optional[Code] = Field(
        description="available | unavailable",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    request: Optional[ListType[Reference]] = Field(
        description="Procedure request",
        default=None,
    )
    quantity: Optional[Integer] = Field(
        description="The amount of this biologically derived product",
        default=None,
    )
    quantity_ext: Optional[Element] = Field(
        description="Placeholder element for quantity extensions",
        default=None,
        alias="_quantity",
    )
    parent: Optional[ListType[Reference]] = Field(
        description="BiologicallyDerivedProduct parent",
        default=None,
    )
    collection: Optional[BiologicallyDerivedProductCollection] = Field(
        description="How this product was collected",
        default=None,
    )
    processing: Optional[ListType[BiologicallyDerivedProductProcessing]] = Field(
        description="Any processing of the product during collection",
        default=None,
    )
    manipulation: Optional[BiologicallyDerivedProductManipulation] = Field(
        description="Any manipulation of product post-collection",
        default=None,
    )
    storage: Optional[ListType[BiologicallyDerivedProductStorage]] = Field(
        description="Product storage",
        default=None,
    )
