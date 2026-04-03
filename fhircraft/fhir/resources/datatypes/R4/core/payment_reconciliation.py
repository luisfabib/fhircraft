import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)


from ..primitive import *
from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Period,
    CodeableConcept,
    Reference,
    Money,
    BackboneElement,
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
    text: Optional[String] = Field(
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
    period: Optional[Period] = Field(
        description="Period covered",
        default=None,
    )
    created: Optional[DateTime] = Field(
        description="Creation date",
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
    disposition: Optional[String] = Field(
        description="Disposition message",
        default=None,
    )
    paymentDate: Optional[Date] = Field(
        description="When payment issued",
        default=None,
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
