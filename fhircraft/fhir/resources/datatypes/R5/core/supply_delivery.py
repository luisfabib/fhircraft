from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators


from ..primitive import *
from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    BackboneElement,
    Quantity,
    Period,
    Timing,
)
from .resource import Resource
from .domain_resource import DomainResource

class SupplyDeliverySuppliedItem(BackboneElement):
    """
    The item that is being delivered or has been supplied.
    """

    quantity: Optional[Quantity] = Field(
        description="Amount supplied",
        default=None,
    )
    itemCodeableConcept: Optional[CodeableConcept] = Field(
        description="Medication, Substance, Device or Biologically Derived Product supplied",
        default=None,
    )
    itemReference: Optional[Reference] = Field(
        description="Medication, Substance, Device or Biologically Derived Product supplied",
        default=None,
    )

    @property
    def item(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="item",
        )

    @model_validator(mode="after")
    def item_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[CodeableConcept, Reference],
            field_name_base="item",
            required=False,
        )

class SupplyDelivery(DomainResource):
    """
    Record of delivery of what is supplied.
    """

    _abstract = False
    _type = "SupplyDelivery"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/SupplyDelivery"

    identifier: Optional[ListType[Identifier]] = Field(
        description="External identifier",
        default=None,
    )
    basedOn: Optional[ListType[Reference]] = Field(
        description="Fulfills plan, proposal or order",
        default=None,
    )
    partOf: Optional[ListType[Reference]] = Field(
        description="Part of referenced event",
        default=None,
    )
    status: Optional[Code] = Field(
        description="in-progress | completed | abandoned | entered-in-error",
        default=None,
    )
    patient: Optional[Reference] = Field(
        description="Patient for whom the item is supplied",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Category of supply event",
        default=None,
    )
    suppliedItem: Optional[ListType[SupplyDeliverySuppliedItem]] = Field(
        description="The item that is delivered or supplied",
        default=None,
    )
    occurrenceDateTime: Optional[DateTime] = Field(
        description="When event occurred",
        default=None,
    )
    occurrencePeriod: Optional[Period] = Field(
        description="When event occurred",
        default=None,
    )
    occurrenceTiming: Optional[Timing] = Field(
        description="When event occurred",
        default=None,
    )
    supplier: Optional[Reference] = Field(
        description="The item supplier",
        default=None,
    )
    destination: Optional[Reference] = Field(
        description="Where the delivery was sent",
        default=None,
    )
    receiver: Optional[ListType[Reference]] = Field(
        description="Who received the delivery",
        default=None,
    )

    @property
    def occurrence(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="occurrence",
        )

    @model_validator(mode="after")
    def occurrence_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[DateTime, Period, Timing],
            field_name_base="occurrence",
            required=False,
        )
