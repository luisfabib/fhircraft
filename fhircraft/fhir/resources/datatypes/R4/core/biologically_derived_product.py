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
    collectedDateTime: Optional[fhir.dateTime] = Field(
        description="time of product collection",
        default=None,
    )
    collectedPeriod: Optional[Period] = Field(
        description="time of product collection",
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
            field_types=[fhir.DateTime, Period],
            field_name_base="collected",
            required=False,
        )

class BiologicallyDerivedProductProcessing(BackboneElement):
    """
    Any processing of the product during collection that does not change the fundamental nature of the product. For example adding anti-coagulants during the collection of Peripheral Blood Stem Cells.
    """

    description: Optional[fhir.string] = Field(
        description="Description of of processing",
        default=None,
    )
    procedure: Optional[CodeableConcept] = Field(
        description="Procesing code",
        default=None,
    )
    additive: Optional[Reference] = Field(
        description="Substance added during processing",
        default=None,
    )
    timeDateTime: Optional[fhir.dateTime] = Field(
        description="time of processing",
        default=None,
    )
    timePeriod: Optional[Period] = Field(
        description="time of processing",
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
            field_types=[fhir.DateTime, Period],
            field_name_base="time",
            required=False,
        )

class BiologicallyDerivedProductManipulation(BackboneElement):
    """
    Any manipulation of product post-collection that is intended to alter the product.  For example a buffy-coat enrichment or CD8 reduction of Peripheral Blood Stem Cells to make it more suitable for infusion.
    """

    description: Optional[fhir.string] = Field(
        description="Description of manipulation",
        default=None,
    )
    timeDateTime: Optional[fhir.dateTime] = Field(
        description="time of manipulation",
        default=None,
    )
    timePeriod: Optional[Period] = Field(
        description="time of manipulation",
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
            field_types=[fhir.DateTime, Period],
            field_name_base="time",
            required=False,
        )

class BiologicallyDerivedProductStorage(BackboneElement):
    """
    Product storage.
    """

    description: Optional[fhir.string] = Field(
        description="Description of storage",
        default=None,
    )
    temperature: Optional[fhir.decimal] = Field(
        description="Storage temperature",
        default=None,
    )
    scale: Optional[fhir.code] = Field(
        description="farenheit | celsius | kelvin",
        default=None,
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
    productCategory: Optional[fhir.code] = Field(
        description="organ | tissue | fluid | cells | biologicalAgent",
        default=None,
    )
    productCode: Optional[CodeableConcept] = Field(
        description="What this biologically derived product is",
        default=None,
    )
    status: Optional[fhir.code] = Field(
        description="available | unavailable",
        default=None,
    )
    request: Optional[ListType[Reference]] = Field(
        description="Procedure request",
        default=None,
    )
    quantity: Optional[fhir.integer] = Field(
        description="The amount of this biologically derived product",
        default=None,
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
