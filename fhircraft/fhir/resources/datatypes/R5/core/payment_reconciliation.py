from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    DateTime,
    Date,
    PositiveInt,
)

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
    targetItemString: Optional[String] = Field(
        description="Sub-element of the subject",
        default=None,
    )
    targetItemString_ext: Optional[Element] = Field(
        description="Placeholder element for targetItemString extensions",
        default=None,
        alias="_targetItemString",
    )
    targetItemIdentifier: Optional[Identifier] = Field(
        description="Sub-element of the subject",
        default=None,
    )
    targetItemPositiveInt: Optional[PositiveInt] = Field(
        description="Sub-element of the subject",
        default=None,
    )
    targetItemPositiveInt_ext: Optional[Element] = Field(
        description="Placeholder element for targetItemPositiveInt extensions",
        default=None,
        alias="_targetItemPositiveInt",
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
    date: Optional[Date] = Field(
        description="Date of commitment to pay",
        default=None,
    )
    date_ext: Optional[Element] = Field(
        description="Placeholder element for date extensions",
        default=None,
        alias="_date",
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
            field_types=[String, Identifier, PositiveInt],
            field_name_base="targetItem",
            required=False,
        )


class PaymentReconciliationProcessNote(BackboneElement):
    """
    A note that describes or explains the processing in a human readable form.
    """

    type: Optional[Code] = Field(
        description="display | print | printoper",
        default=None,
    )
    type_ext: Optional[Element] = Field(
        description="Placeholder element for type extensions",
        default=None,
        alias="_type",
    )
    text: Optional[String] = Field(
        description="Note explanatory text",
        default=None,
    )
    text_ext: Optional[Element] = Field(
        description="Placeholder element for text extensions",
        default=None,
        alias="_text",
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
    status: Optional[Code] = Field(
        description="active | cancelled | draft | entered-in-error",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    kind: Optional[CodeableConcept] = Field(
        description="Workflow originating payment",
        default=None,
    )
    period: Optional[Period] = Field(
        description="Period covered",
        default=None,
    )
    created: Optional[DateTime] = Field(
        description="Creation date",
        default=None,
    )
    created_ext: Optional[Element] = Field(
        description="Placeholder element for created extensions",
        default=None,
        alias="_created",
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
    outcome: Optional[Code] = Field(
        description="queued | complete | error | partial",
        default=None,
    )
    outcome_ext: Optional[Element] = Field(
        description="Placeholder element for outcome extensions",
        default=None,
        alias="_outcome",
    )
    disposition: Optional[String] = Field(
        description="Disposition message",
        default=None,
    )
    disposition_ext: Optional[Element] = Field(
        description="Placeholder element for disposition extensions",
        default=None,
        alias="_disposition",
    )
    date: Optional[Date] = Field(
        description="When payment issued",
        default=None,
    )
    date_ext: Optional[Element] = Field(
        description="Placeholder element for date extensions",
        default=None,
        alias="_date",
    )
    location: Optional[Reference] = Field(
        description="Where payment collected",
        default=None,
    )
    method: Optional[CodeableConcept] = Field(
        description="Payment instrument",
        default=None,
    )
    cardBrand: Optional[String] = Field(
        description="Type of card",
        default=None,
    )
    cardBrand_ext: Optional[Element] = Field(
        description="Placeholder element for cardBrand extensions",
        default=None,
        alias="_cardBrand",
    )
    accountNumber: Optional[String] = Field(
        description="Digits for verification",
        default=None,
    )
    accountNumber_ext: Optional[Element] = Field(
        description="Placeholder element for accountNumber extensions",
        default=None,
        alias="_accountNumber",
    )
    expirationDate: Optional[Date] = Field(
        description="Expiration year-month",
        default=None,
    )
    expirationDate_ext: Optional[Element] = Field(
        description="Placeholder element for expirationDate extensions",
        default=None,
        alias="_expirationDate",
    )
    processor: Optional[String] = Field(
        description="Processor name",
        default=None,
    )
    processor_ext: Optional[Element] = Field(
        description="Placeholder element for processor extensions",
        default=None,
        alias="_processor",
    )
    referenceNumber: Optional[String] = Field(
        description="Check number or payment reference",
        default=None,
    )
    referenceNumber_ext: Optional[Element] = Field(
        description="Placeholder element for referenceNumber extensions",
        default=None,
        alias="_referenceNumber",
    )
    authorization: Optional[String] = Field(
        description="Authorization number",
        default=None,
    )
    authorization_ext: Optional[Element] = Field(
        description="Placeholder element for authorization extensions",
        default=None,
        alias="_authorization",
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
