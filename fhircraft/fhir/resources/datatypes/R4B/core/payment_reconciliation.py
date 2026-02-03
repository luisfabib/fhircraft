import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    DateTime,
    Date,
)

from fhircraft.fhir.resources.datatypes.R4B.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Period,
    Reference,
    Money,
    BackboneElement,
    CodeableConcept,
)
from .resource import Resource
from .domain_resource import DomainResource


class PaymentReconciliationDetail(BackboneElement):
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
    type: Optional[CodeableConcept] = Field(
        description="Category of payment",
        default=None,
    )
    request: Optional[Reference] = Field(
        description="Request giving rise to the payment",
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
        description="Business Identifier for a payment reconciliation",
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
    paymentDate: Optional[Date] = Field(
        description="When payment issued",
        default=None,
    )
    paymentDate_ext: Optional[Element] = Field(
        description="Placeholder element for paymentDate extensions",
        default=None,
        alias="_paymentDate",
    )
    paymentAmount: Optional[Money] = Field(
        description="Total amount of Payment",
        default=None,
    )
    paymentIdentifier: Optional[Identifier] = Field(
        description="Business identifier for the payment",
        default=None,
    )
    detail: Optional[ListType[PaymentReconciliationDetail]] = Field(
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
