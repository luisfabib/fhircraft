import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)


import fhircraft.fhir.resources.datatypes.R4B.primitive as fhir
from fhircraft.fhir.resources.datatypes.R4B.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    Period,
    BackboneElement,
    Money,
    Address,
    Quantity,
    Attachment,
)
from .resource import Resource
from .domain_resource import DomainResource


class ClaimResponseItemAdjudication(BackboneElement):
    """
    If this item is a group then the values here are a summary of the adjudication of the detail items. If this item is a simple product or service then this is the result of the adjudication of this item.
    """

    category: CodeableConcept = Field(
        description="Type of adjudication information",
    )
    reason: Optional[CodeableConcept] = Field(
        description="Explanation of adjudication outcome",
        default=None,
    )
    amount: Optional[Money] = Field(
        description="Monetary amount",
        default=None,
    )
    value: Optional[fhir.decimal] = Field(
        description="Non-monetary value",
        default=None,
    )


class ClaimResponseItemDetailAdjudication(BackboneElement):
    """
    The adjudication results.
    """

    category: Optional[CodeableConcept] = Field(
        description="Type of adjudication information",
        default=None,
    )
    reason: Optional[CodeableConcept] = Field(
        description="Explanation of adjudication outcome",
        default=None,
    )
    amount: Optional[Money] = Field(
        description="Monetary amount",
        default=None,
    )
    value: Optional[fhir.decimal] = Field(
        description="Non-monetary value",
        default=None,
    )


class ClaimResponseItemDetailSubDetail(BackboneElement):
    """
    A sub-detail adjudication of a simple product or service.
    """

    subDetailSequence: fhir.positiveInt = Field(
        description="Claim sub-detail instance identifier",
    )
    noteNumber: Optional[ListType[fhir.positiveInt]] = Field(
        description="Applicable note numbers",
        default=None,
    )
    adjudication: Optional[ListType[ClaimResponseItemAdjudication]] = Field(
        description="Subdetail level adjudication details",
        default=None,
    )


class ClaimResponseItemDetail(BackboneElement):
    """
    A claim detail. Either a simple (a product or service) or a 'group' of sub-details which are simple items.
    """

    detailSequence: fhir.positiveInt = Field(
        description="Claim detail instance identifier",
    )
    noteNumber: Optional[ListType[fhir.positiveInt]] = Field(
        description="Applicable note numbers",
        default=None,
    )
    adjudication: ListType[ClaimResponseItemDetailAdjudication] = Field(
        description="Detail level adjudication details",
        min_length=1,
    )
    subDetail: Optional[ListType[ClaimResponseItemDetailSubDetail]] = Field(
        description="Adjudication for claim sub-details",
        default=None,
    )


class ClaimResponseItem(BackboneElement):
    """
    A claim line. Either a simple (a product or service) or a 'group' of details which can also be a simple items or groups of sub-details.
    """

    itemSequence: fhir.positiveInt = Field(
        description="Claim item instance identifier",
    )
    noteNumber: Optional[ListType[fhir.positiveInt]] = Field(
        description="Applicable note numbers",
        default=None,
    )
    adjudication: ListType[ClaimResponseItemAdjudication] = Field(
        description="Adjudication details",
        min_length=1,
    )
    detail: Optional[ListType[ClaimResponseItemDetail]] = Field(
        description="Adjudication for claim details",
        default=None,
    )


class ClaimResponseAddItemDetailSubDetail(BackboneElement):
    """
    The third-tier service adjudications for payor added services.
    """

    productOrService: CodeableConcept = Field(
        description="Billing, service, product, or drug code",
    )
    modifier: Optional[ListType[CodeableConcept]] = Field(
        description="Service/Product billing modifiers",
        default=None,
    )
    quantity: Optional[Quantity] = Field(
        description="Count of products or services",
        default=None,
    )
    unitPrice: Optional[Money] = Field(
        description="Fee, charge or cost per item",
        default=None,
    )
    factor: Optional[fhir.decimal] = Field(
        description="Price scaling factor",
        default=None,
    )
    net: Optional[Money] = Field(
        description="Total item cost",
        default=None,
    )
    noteNumber: Optional[ListType[fhir.positiveInt]] = Field(
        description="Applicable note numbers",
        default=None,
    )
    adjudication: ListType[ClaimResponseItemAdjudication] = Field(
        description="Added items detail adjudication",
        min_length=1,
    )


class ClaimResponseAddItemDetail(BackboneElement):
    """
    The second-tier service adjudications for payor added services.
    """

    productOrService: CodeableConcept = Field(
        description="Billing, service, product, or drug code",
    )
    modifier: Optional[ListType[CodeableConcept]] = Field(
        description="Service/Product billing modifiers",
        default=None,
    )
    quantity: Optional[Quantity] = Field(
        description="Count of products or services",
        default=None,
    )
    unitPrice: Optional[Money] = Field(
        description="Fee, charge or cost per item",
        default=None,
    )
    factor: Optional[fhir.decimal] = Field(
        description="Price scaling factor",
        default=None,
    )
    net: Optional[Money] = Field(
        description="Total item cost",
        default=None,
    )
    noteNumber: Optional[ListType[fhir.positiveInt]] = Field(
        description="Applicable note numbers",
        default=None,
    )
    adjudication: ListType[ClaimResponseItemAdjudication] = Field(
        description="Added items detail adjudication",
        min_length=1,
    )
    subDetail: Optional[ListType[ClaimResponseAddItemDetailSubDetail]] = Field(
        description="Insurer added line items",
        default=None,
    )


class ClaimResponseAddItem(BackboneElement):
    """
    The first-tier service adjudications for payor added product or service lines.
    """

    itemSequence: Optional[ListType[fhir.positiveInt]] = Field(
        description="Item sequence number",
        default=None,
    )
    detailSequence: Optional[ListType[fhir.positiveInt]] = Field(
        description="Detail sequence number",
        default=None,
    )
    subdetailSequence: Optional[ListType[fhir.positiveInt]] = Field(
        description="Subdetail sequence number",
        default=None,
    )
    provider: Optional[ListType[Reference]] = Field(
        description="Authorized providers",
        default=None,
    )
    productOrService: CodeableConcept = Field(
        description="Billing, service, product, or drug code",
    )
    modifier: Optional[ListType[CodeableConcept]] = Field(
        description="Service/Product billing modifiers",
        default=None,
    )
    programCode: Optional[ListType[CodeableConcept]] = Field(
        description="Program the product or service is provided under",
        default=None,
    )
    servicedDate: Optional[fhir.date_] = Field(
        description="Date or dates of service or product delivery",
        default=None,
    )
    servicedPeriod: Optional[Period] = Field(
        description="Date or dates of service or product delivery",
        default=None,
    )
    locationCodeableConcept: Optional[CodeableConcept] = Field(
        description="Place of service or where product was supplied",
        default=None,
    )
    locationAddress: Optional[Address] = Field(
        description="Place of service or where product was supplied",
        default=None,
    )
    locationReference: Optional[Reference] = Field(
        description="Place of service or where product was supplied",
        default=None,
    )
    quantity: Optional[Quantity] = Field(
        description="Count of products or services",
        default=None,
    )
    unitPrice: Optional[Money] = Field(
        description="Fee, charge or cost per item",
        default=None,
    )
    factor: Optional[fhir.decimal] = Field(
        description="Price scaling factor",
        default=None,
    )
    net: Optional[Money] = Field(
        description="Total item cost",
        default=None,
    )
    bodySite: Optional[CodeableConcept] = Field(
        description="Anatomical location",
        default=None,
    )
    subSite: Optional[ListType[CodeableConcept]] = Field(
        description="Anatomical sub-location",
        default=None,
    )
    noteNumber: Optional[ListType[fhir.positiveInt]] = Field(
        description="Applicable note numbers",
        default=None,
    )
    adjudication: ListType[ClaimResponseItemAdjudication] = Field(
        description="Added items adjudication",
        min_length=1,
    )
    detail: Optional[ListType[ClaimResponseAddItemDetail]] = Field(
        description="Insurer added line details",
        default=None,
    )

    @property
    def serviced(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="serviced",
        )

    @property
    def location(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="location",
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
    def location_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[CodeableConcept, Address, Reference],
            field_name_base="location",
            required=False,
        )


class ClaimResponseTotal(BackboneElement):
    """
    Categorized monetary totals for the adjudication.
    """

    category: CodeableConcept = Field(
        description="Type of adjudication information",
    )
    amount: Money = Field(
        description="Financial total for the category",
    )


class ClaimResponsePayment(BackboneElement):
    """
    Payment details for the adjudication of the claim.
    """

    type: CodeableConcept = Field(
        description="Partial or complete payment",
    )
    adjustment: Optional[Money] = Field(
        description="Payment adjustment for non-claim issues",
        default=None,
    )
    adjustmentReason: Optional[CodeableConcept] = Field(
        description="Explanation for the adjustment",
        default=None,
    )
    date: Optional[fhir.date_] = Field(
        description="Expected date of payment",
        default=None,
    )
    amount: Money = Field(
        description="Payable amount after adjustment",
    )
    identifier: Optional[Identifier] = Field(
        description="Business identifier for the payment",
        default=None,
    )


class ClaimResponseProcessNote(BackboneElement):
    """
    A note that describes or explains adjudication results in a human readable form.
    """

    number: Optional[fhir.positiveInt] = Field(
        description="Note instance identifier",
        default=None,
    )
    type: Optional[fhir.code] = Field(
        description="display | print | printoper",
        default=None,
    )
    text: fhir.string = Field(
        description="Note explanatory text",
    )
    language: Optional[CodeableConcept] = Field(
        description="Language of the text",
        default=None,
    )


class ClaimResponseInsurance(BackboneElement):
    """
    Financial instruments for reimbursement for the health care products and services specified on the claim.
    """

    sequence: fhir.positiveInt = Field(
        description="Insurance instance identifier",
    )
    focal: fhir.boolean = Field(
        description="Coverage to be used for adjudication",
    )
    coverage: Reference = Field(
        description="Insurance information",
    )
    businessArrangement: Optional[fhir.string] = Field(
        description="Additional provider contract number",
        default=None,
    )
    claimResponse: Optional[Reference] = Field(
        description="Adjudication results",
        default=None,
    )


class ClaimResponseError(BackboneElement):
    """
    Errors encountered during the processing of the adjudication.
    """

    itemSequence: Optional[fhir.positiveInt] = Field(
        description="Item sequence number",
        default=None,
    )
    detailSequence: Optional[fhir.positiveInt] = Field(
        description="Detail sequence number",
        default=None,
    )
    subDetailSequence: Optional[fhir.positiveInt] = Field(
        description="Subdetail sequence number",
        default=None,
    )
    code: CodeableConcept = Field(
        description="Error code detailing processing issues",
    )


class ClaimResponse(DomainResource):
    """
    This resource provides the adjudication details from the processing of a Claim resource.
    """

    _abstract = False
    _type = "ClaimResponse"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/ClaimResponse"

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
        description="Business Identifier for a claim response",
        default=None,
    )
    status: fhir.code = Field(
        description="active | cancelled | draft | entered-in-error",
    )
    type: CodeableConcept = Field(
        description="More granular claim type",
    )
    subType: Optional[CodeableConcept] = Field(
        description="More granular claim type",
        default=None,
    )
    use: fhir.code = Field(
        description="claim | preauthorization | predetermination",
    )
    patient: Reference = Field(
        description="The recipient of the products and services",
    )
    created: fhir.dateTime = Field(
        description="Response creation date",
    )
    insurer: Reference = Field(
        description="Party responsible for reimbursement",
    )
    requestor: Optional[Reference] = Field(
        description="Party responsible for the claim",
        default=None,
    )
    request: Optional[Reference] = Field(
        description="id_ of resource triggering adjudication",
        default=None,
    )
    outcome: fhir.code = Field(
        description="queued | complete | error | partial",
    )
    disposition: Optional[fhir.string] = Field(
        description="Disposition Message",
        default=None,
    )
    preAuthRef: Optional[fhir.string] = Field(
        description="Preauthorization reference",
        default=None,
    )
    preAuthPeriod: Optional[Period] = Field(
        description="Preauthorization reference effective period",
        default=None,
    )
    payeeType: Optional[CodeableConcept] = Field(
        description="Party to be paid any benefits payable",
        default=None,
    )
    item: Optional[ListType[ClaimResponseItem]] = Field(
        description="Adjudication for claim line items",
        default=None,
    )
    addItem: Optional[ListType[ClaimResponseAddItem]] = Field(
        description="Insurer added line items",
        default=None,
    )
    adjudication: Optional[ListType[ClaimResponseItemAdjudication]] = Field(
        description="Header-level adjudication",
        default=None,
    )
    total: Optional[ListType[ClaimResponseTotal]] = Field(
        description="Adjudication totals",
        default=None,
    )
    payment: Optional[ClaimResponsePayment] = Field(
        description="Payment Details",
        default=None,
    )
    fundsReserve: Optional[CodeableConcept] = Field(
        description="Funds reserved status",
        default=None,
    )
    formCode: Optional[CodeableConcept] = Field(
        description="Printed form identifier",
        default=None,
    )
    form: Optional[Attachment] = Field(
        description="Printed reference or actual form",
        default=None,
    )
    processNote: Optional[ListType[ClaimResponseProcessNote]] = Field(
        description="Note concerning adjudication",
        default=None,
    )
    communicationRequest: Optional[ListType[Reference]] = Field(
        description="Request for additional information",
        default=None,
    )
    insurance: Optional[ListType[ClaimResponseInsurance]] = Field(
        description="Patient insurance information",
        default=None,
    )
    error: Optional[ListType[ClaimResponseError]] = Field(
        description="Processing errors",
        default=None,
    )
