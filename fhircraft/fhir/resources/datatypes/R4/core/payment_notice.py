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
    CodeableConcept,
    Reference,
    Money,
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
        description="Business Identifier for the payment noctice",
        default=None,
    )
    status: Optional[Code] = Field(
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
    created: Optional[DateTime] = Field(
        description="Creation date",
        default=None,
    )
    provider: Optional[Reference] = Field(
        description="Responsible practitioner",
        default=None,
    )
    payment: Optional[Reference] = Field(
        description="Payment reference",
        default=None,
    )
    paymentDate: Optional[Date] = Field(
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
