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
    Annotation,
    BackboneElement,
    Money,
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


class InvoiceLineItemPriceComponent(BackboneElement):
    """
    The price for a ChargeItem may be calculated as a base price with surcharges/deductions that apply in certain conditions. A ChargeItemDefinition resource that defines the prices, factors and conditions that apply to a billing code is currently under development. The priceComponent element can be used to offer transparency to the recipient of the Invoice as to how the prices have been calculated.
    """

    type: fhir.code = Field(
        description="base | surcharge | deduction | discount | tax | informational",
    )
    code: Optional[CodeableConcept] = Field(
        description="code identifying the specific component",
        default=None,
    )
    factor: Optional[fhir.decimal] = Field(
        description="Factor used for calculating this component",
        default=None,
    )
    amount: Optional[Money] = Field(
        description="Monetary amount associated with this component",
        default=None,
    )


class InvoiceLineItem(BackboneElement):
    """
    Each line item represents one charge for goods and services rendered. Details such as date, code and amount are found in the referenced ChargeItem resource.
    """

    sequence: Optional[fhir.positiveInt] = Field(
        description="Sequence number of line item",
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
    priceComponent: Optional[ListType[InvoiceLineItemPriceComponent]] = Field(
        description="Components of total line item price",
        default=None,
    )

    @property
    def chargeItem(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="chargeItem",
        )

    @model_validator(mode="after")
    def chargeItem_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Reference, CodeableConcept],
            field_name_base="chargeItem",
            required=True,
        )


class InvoiceTotalPriceComponent(BackboneElement):
    """
    The total amount for the Invoice may be calculated as the sum of the line items with surcharges/deductions that apply in certain conditions.  The priceComponent element can be used to offer transparency to the recipient of the Invoice of how the total price was calculated.
    """

    type: Optional[fhir.code] = Field(
        description="base | surcharge | deduction | discount | tax | informational",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="code identifying the specific component",
        default=None,
    )
    factor: Optional[fhir.decimal] = Field(
        description="Factor used for calculating this component",
        default=None,
    )
    amount: Optional[Money] = Field(
        description="Monetary amount associated with this component",
        default=None,
    )


class Invoice(DomainResource):
    """
    Invoice containing collected ChargeItems from an Account with calculated individual and total price for Billing purpose.
    """

    _abstract = False
    _type = "Invoice"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Invoice"

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
        description="Invoice date / posting date",
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
    totalPriceComponent: Optional[ListType[InvoiceTotalPriceComponent]] = Field(
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
