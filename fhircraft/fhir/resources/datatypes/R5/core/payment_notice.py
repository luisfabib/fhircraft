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
    Reference,
    Money,
    CodeableConcept,
)
from .resource import Resource
from .domain_resource import DomainResource

class PaymentNotice(DomainResource):
    """
    This resource provides the status of the payment for goods and services rendered, and the request and response resource references.
    """

    _abstract = False
    _type = "PaymentNotice"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/PaymentNotice"

    identifier: Optional[ListType[Identifier]] = Field(
        description="Business Identifier for the payment notice",
        default=None,
    )
    status: Optional[fhir.code] = Field(
        description="active | cancelled | draft | entered-in-error",
        default=None,
    )
    request: Optional[Reference] = Field(
        description="Request reference",
        default=None,
    )
    response: Optional[Reference] = Field(
        description="Response reference",
        default=None,
    )
    created: Optional[fhir.dateTime] = Field(
        description="Creation date",
        default=None,
    )
    reporter: Optional[Reference] = Field(
        description="Responsible practitioner",
        default=None,
    )
    payment: Optional[Reference] = Field(
        description="Payment reference",
        default=None,
    )
    paymentDate: Optional[fhir.date_] = Field(
        description="Payment or clearing date",
        default=None,
    )
    payee: Optional[Reference] = Field(
        description="Party being paid",
        default=None,
    )
    recipient: Optional[Reference] = Field(
        description="Party being notified",
        default=None,
    )
    amount: Optional[Money] = Field(
        description="Monetary amount of the payment",
        default=None,
    )
    paymentStatus: Optional[CodeableConcept] = Field(
        description="Issued or cleared Status of the payment",
        default=None,
    )
