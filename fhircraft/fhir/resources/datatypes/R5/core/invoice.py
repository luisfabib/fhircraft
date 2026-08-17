from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators


import fhircraft.fhir.resources.datatypes.R5.primitive as fhir
from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    Period,
    BackboneElement,
    MonetaryComponent,
    Money,
    Annotation,
)
from .resource import Resource
from .domain_resource import DomainResource

class InvoiceParticipant(BackboneElement):
    """
    Indicates who or what performed or participated in the charged service.
    """

    role: Optional[CodeableConcept] = Field(
        description="Type of involvement in creation of this Invoice",
        default=None,
    )
    actor: Reference = Field(
        description="Individual who was involved",
    )

class InvoiceLineItem(BackboneElement):
    """
    Each line item represents one charge for goods and services rendered. Details such.ofType(date), code and amount are found in the referenced ChargeItem resource.
    """

    sequence: Optional[fhir.positiveInt] = Field(
        description="Sequence number of line item",
        default=None,
    )
    servicedDate: Optional[fhir.date_] = Field(
        description="Service data or period",
        default=None,
    )
    servicedPeriod: Optional[Period] = Field(
        description="Service data or period",
        default=None,
    )
    chargeItemReference: Optional[Reference] = Field(
        description="Reference to ChargeItem containing details of this line item or an inline billing code",
        default=None,
    )
    chargeItemCodeableConcept: Optional[CodeableConcept] = Field(
        description="Reference to ChargeItem containing details of this line item or an inline billing code",
        default=None,
    )
    priceComponent: Optional[ListType[MonetaryComponent]] = Field(
        description="Components of total line item price",
        default=None,
    )

    @property
    def serviced(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="serviced",
        )

    @property
    def chargeItem(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="chargeItem",
        )

    @model_validator(mode="after")
    def serviced_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.Date, Period],
            field_name_base="serviced",
            required=False,
        )

    @model_validator(mode="after")
    def chargeItem_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Reference, CodeableConcept],
            field_name_base="chargeItem",
            required=True,
        )

class Invoice(DomainResource):
    """
    Invoice containing collected ChargeItems from an Account with calculated individual and total price for Billing purpose.
    """

    _abstract = False
    _type = "Invoice"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Invoice"

    identifier: Optional[ListType[Identifier]] = Field(
        description="Business Identifier for item",
        default=None,
    )
    status: fhir.code = Field(
        description="draft | issued | balanced | cancelled | entered-in-error",
    )
    cancelledReason: Optional[fhir.string] = Field(
        description="Reason for cancellation of this Invoice",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Type of Invoice",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="Recipient(s) of goods and services",
        default=None,
    )
    recipient: Optional[Reference] = Field(
        description="Recipient of this invoice",
        default=None,
    )
    date: Optional[fhir.dateTime] = Field(
        description="DEPRICATED",
        default=None,
    )
    creation: Optional[fhir.dateTime] = Field(
        description="When posted",
        default=None,
    )
    periodDate: Optional[fhir.date_] = Field(
        description="Billing date or period",
        default=None,
    )
    periodPeriod: Optional[Period] = Field(
        description="Billing date or period",
        default=None,
    )
    participant: Optional[ListType[InvoiceParticipant]] = Field(
        description="Participant in creation of this Invoice",
        default=None,
    )
    issuer: Optional[Reference] = Field(
        description="Issuing Organization of Invoice",
        default=None,
    )
    account: Optional[Reference] = Field(
        description="Account that is being balanced",
        default=None,
    )
    lineItem: Optional[ListType[InvoiceLineItem]] = Field(
        description="Line items of this Invoice",
        default=None,
    )
    totalPriceComponent: Optional[ListType[MonetaryComponent]] = Field(
        description="Components of Invoice total",
        default=None,
    )
    totalNet: Optional[Money] = Field(
        description="Net total of this Invoice",
        default=None,
    )
    totalGross: Optional[Money] = Field(
        description="Gross total of this Invoice",
        default=None,
    )
    paymentTerms: Optional[fhir.markdown] = Field(
        description="Payment details",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Comments made about the invoice",
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
            field_types=[fhir.Date, Period],
            field_name_base="period",
            required=False,
        )
