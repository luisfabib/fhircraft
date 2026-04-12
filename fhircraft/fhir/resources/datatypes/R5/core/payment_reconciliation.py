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
    Period,
    Reference,
    Money,
    BackboneElement,
)
from .resource import Resource
from .domain_resource import DomainResource


class PaymentReconciliationAllocation(BackboneElement):
    """
    Distribution of the payment amount for a previously acknowledged payable.
    """

    identifier: Optional[Identifier] = Field(
        description="Business identifier of the payment detail",
        default=None,
    )
    predecessor: Optional[Identifier] = Field(
        description="Business identifier of the prior payment detail",
        default=None,
    )
    target: Optional[Reference] = Field(
        description="Subject of the payment",
        default=None,
    )
    targetItemString: Optional[fhir.string] = Field(
        description="Sub-element of the subject",
        default=None,
    )
    targetItemIdentifier: Optional[Identifier] = Field(
        description="Sub-element of the subject",
        default=None,
    )
    targetItemPositiveInt: Optional[fhir.positiveInt] = Field(
        description="Sub-element of the subject",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="Applied-to encounter",
        default=None,
    )
    account: Optional[Reference] = Field(
        description="Applied-to account",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Category of payment",
        default=None,
    )
    submitter: Optional[Reference] = Field(
        description="Submitter of the request",
        default=None,
    )
    response: Optional[Reference] = Field(
        description="Response committing to a payment",
        default=None,
    )
    date: Optional[fhir.date_] = Field(
        description="Date of commitment to pay",
        default=None,
    )
    responsible: Optional[Reference] = Field(
        description="Contact for the response",
        default=None,
    )
    payee: Optional[Reference] = Field(
        description="Recipient of the payment",
        default=None,
    )
    amount: Optional[Money] = Field(
        description="Amount allocated to this payable",
        default=None,
    )

    @property
    def targetItem(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="targetItem",
        )

    @model_validator(mode="after")
    def targetItem_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.String, Identifier, fhir.PositiveInt],
            field_name_base="targetItem",
            required=False,
        )


class PaymentReconciliationProcessNote(BackboneElement):
    """
    A note that describes or explains the processing in a human readable form.
    """

    type: Optional[fhir.code] = Field(
        description="display | print | printoper",
        default=None,
    )
    text: Optional[fhir.string] = Field(
        description="Note explanatory text",
        default=None,
    )


class PaymentReconciliation(DomainResource):
    """
    This resource provides the details including amount of a payment and allocates the payment items being paid.
    """

    _abstract = False
    _type = "PaymentReconciliation"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/PaymentReconciliation"

    identifier: Optional[ListType[Identifier]] = Field(
        description="Business Identifier for a payment reconciliation",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Category of payment",
        default=None,
    )
    status: Optional[fhir.code] = Field(
        description="active | cancelled | draft | entered-in-error",
        default=None,
    )
    kind: Optional[CodeableConcept] = Field(
        description="Workflow originating payment",
        default=None,
    )
    period: Optional[Period] = Field(
        description="Period covered",
        default=None,
    )
    created: Optional[fhir.dateTime] = Field(
        description="Creation date",
        default=None,
    )
    enterer: Optional[Reference] = Field(
        description="Who entered the payment",
        default=None,
    )
    issuerType: Optional[CodeableConcept] = Field(
        description="Nature of the source",
        default=None,
    )
    paymentIssuer: Optional[Reference] = Field(
        description="Party generating payment",
        default=None,
    )
    request: Optional[Reference] = Field(
        description="Reference to requesting resource",
        default=None,
    )
    requestor: Optional[Reference] = Field(
        description="Responsible practitioner",
        default=None,
    )
    outcome: Optional[fhir.code] = Field(
        description="queued | complete | error | partial",
        default=None,
    )
    disposition: Optional[fhir.string] = Field(
        description="Disposition message",
        default=None,
    )
    date: Optional[fhir.date_] = Field(
        description="When payment issued",
        default=None,
    )
    location: Optional[Reference] = Field(
        description="Where payment collected",
        default=None,
    )
    method: Optional[CodeableConcept] = Field(
        description="Payment instrument",
        default=None,
    )
    cardBrand: Optional[fhir.string] = Field(
        description="Type of card",
        default=None,
    )
    accountNumber: Optional[fhir.string] = Field(
        description="Digits for verification",
        default=None,
    )
    expirationDate: Optional[fhir.date_] = Field(
        description="Expiration year-month",
        default=None,
    )
    processor: Optional[fhir.string] = Field(
        description="Processor name",
        default=None,
    )
    referenceNumber: Optional[fhir.string] = Field(
        description="Check number or payment reference",
        default=None,
    )
    authorization: Optional[fhir.string] = Field(
        description="Authorization number",
        default=None,
    )
    tenderedAmount: Optional[Money] = Field(
        description="Amount offered by the issuer",
        default=None,
    )
    returnedAmount: Optional[Money] = Field(
        description="Amount returned by the receiver",
        default=None,
    )
    amount: Optional[Money] = Field(
        description="Total amount of Payment",
        default=None,
    )
    paymentIdentifier: Optional[Identifier] = Field(
        description="Business identifier for the payment",
        default=None,
    )
    allocation: Optional[ListType[PaymentReconciliationAllocation]] = Field(
        description="Settlement particulars",
        default=None,
    )
    formCode: Optional[CodeableConcept] = Field(
        description="Printed form identifier",
        default=None,
    )
    processNote: Optional[ListType[PaymentReconciliationProcessNote]] = Field(
        description="Note concerning processing",
        default=None,
    )
