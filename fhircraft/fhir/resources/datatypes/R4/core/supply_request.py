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
    Quantity,
    BackboneElement,
    Range,
    Period,
    Timing,
)
from .resource import Resource
from .domain_resource import DomainResource


class SupplyRequestParameter(BackboneElement):
    """
    Specific parameters for the ordered item.  For example, the size of the indicated item.
    """

    code: Optional[CodeableConcept] = Field(
        description="Item detail",
        default=None,
    )
    valueCodeableConcept: Optional[CodeableConcept] = Field(
        description="Value of detail",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="Value of detail",
        default=None,
    )
    valueRange: Optional[Range] = Field(
        description="Value of detail",
        default=None,
    )
    valueBoolean: Optional[fhir.boolean] = Field(
        description="Value of detail",
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
            field_types=[CodeableConcept, Quantity, Range, fhir.boolean],
            field_name_base="value",
            required=False,
        )


class SupplyRequest(DomainResource):
    """
    A record of a request for a medication, substance or device used in the healthcare setting.
    """

    _abstract = False
    _type = "SupplyRequest"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/SupplyRequest"

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
        description="Business Identifier for SupplyRequest",
        default=None,
    )
    status: Optional[fhir.code] = Field(
        description="draft | active | suspended +",
        default=None,
    )
    category: Optional[CodeableConcept] = Field(
        description="The kind of supply (central, non-stock, etc.)",
        default=None,
    )
    priority: Optional[fhir.code] = Field(
        description="routine | urgent | asap | stat",
        default=None,
    )
    itemCodeableConcept: Optional[CodeableConcept] = Field(
        description="Medication, Substance, or Device requested to be supplied",
        default=None,
    )
    itemReference: Optional[Reference] = Field(
        description="Medication, Substance, or Device requested to be supplied",
        default=None,
    )
    quantity: Optional[Quantity] = Field(
        description="The requested amount of the item indicated",
        default=None,
    )
    parameter: Optional[ListType[SupplyRequestParameter]] = Field(
        description="Ordered item details",
        default=None,
    )
    occurrenceDateTime: Optional[fhir.dateTime] = Field(
        description="When the request should be fulfilled",
        default=None,
    )
    occurrencePeriod: Optional[Period] = Field(
        description="When the request should be fulfilled",
        default=None,
    )
    occurrenceTiming: Optional[Timing] = Field(
        description="When the request should be fulfilled",
        default=None,
    )
    authoredOn: Optional[fhir.dateTime] = Field(
        description="When the request was made",
        default=None,
    )
    requester: Optional[Reference] = Field(
        description="Individual making the request",
        default=None,
    )
    supplier: Optional[ListType[Reference]] = Field(
        description="Who is intended to fulfill the request",
        default=None,
    )
    reasonCode: Optional[ListType[CodeableConcept]] = Field(
        description="The reason why the supply item was requested",
        default=None,
    )
    reasonReference: Optional[ListType[Reference]] = Field(
        description="The reason why the supply item was requested",
        default=None,
    )
    deliverFrom: Optional[Reference] = Field(
        description="The origin of the supply",
        default=None,
    )
    deliverTo: Optional[Reference] = Field(
        description="The destination of the supply",
        default=None,
    )

    @property
    def item(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="item",
        )

    @property
    def occurrence(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="occurrence",
        )

    @model_validator(mode="after")
    def item_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[CodeableConcept, Reference],
            field_name_base="item",
            required=True,
        )

    @model_validator(mode="after")
    def occurrence_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.dateTime, Period, Timing],
            field_name_base="occurrence",
            required=False,
        )
