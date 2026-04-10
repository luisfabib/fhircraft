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
    Money,
    CodeableConcept,
    Reference,
    Period,
    BackboneElement,
    Quantity,
    Attachment,
    Coding,
    Address,
)
from .resource import Resource
from .domain_resource import DomainResource


class ExplanationOfBenefitRelated(BackboneElement):
    """
    Other claims which are related to this claim such as prior submissions or claims for related services or for the same event.
    """

    claim: Optional[Reference] = Field(
        description="Reference to the related claim",
        default=None,
    )
    relationship: Optional[CodeableConcept] = Field(
        description="How the reference claim is related",
        default=None,
    )
    reference: Optional[Identifier] = Field(
        description="File or case reference",
        default=None,
    )


class ExplanationOfBenefitPayee(BackboneElement):
    """
    The party to be reimbursed for cost of the products and services according to the terms of the policy.
    """

    type: Optional[CodeableConcept] = Field(
        description="Category of recipient",
        default=None,
    )
    party: Optional[Reference] = Field(
        description="Recipient reference",
        default=None,
    )


class ExplanationOfBenefitCareTeam(BackboneElement):
    """
    The members of the team who provided the products and services.
    """

    sequence: Optional[fhir.positiveInt] = Field(
        description="Order of care team",
        default=None,
    )
    provider: Optional[Reference] = Field(
        description="Practitioner or organization",
        default=None,
    )
    responsible: Optional[fhir.boolean] = Field(
        description="Indicator of the lead practitioner",
        default=None,
    )
    role: Optional[CodeableConcept] = Field(
        description="Function within the team",
        default=None,
    )
    qualification: Optional[CodeableConcept] = Field(
        description="Practitioner credential or specialization",
        default=None,
    )


class ExplanationOfBenefitSupportingInfo(BackboneElement):
    """
    Additional information codes regarding exceptions, special considerations, the condition, situation, prior or concurrent issues.
    """

    sequence: Optional[fhir.positiveInt] = Field(
        description="Information instance identifier",
        default=None,
    )
    category: Optional[CodeableConcept] = Field(
        description="Classification of the supplied information",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="Type of information",
        default=None,
    )
    timingDate: Optional[fhir.date_] = Field(
        description="When it occurred",
        default=None,
    )
    timingPeriod: Optional[Period] = Field(
        description="When it occurred",
        default=None,
    )
    valueBoolean: Optional[fhir.boolean] = Field(
        description="Data to be provided",
        default=None,
    )
    valueString: Optional[fhir.string] = Field(
        description="Data to be provided",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="Data to be provided",
        default=None,
    )
    valueAttachment: Optional[Attachment] = Field(
        description="Data to be provided",
        default=None,
    )
    valueReference: Optional[Reference] = Field(
        description="Data to be provided",
        default=None,
    )
    reason: Optional[Coding] = Field(
        description="Explanation for the information",
        default=None,
    )

    @property
    def timing(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="timing",
        )

    @property
    def value(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="value",
        )

    @model_validator(mode="after")
    def timing_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.Date, Period],
            field_name_base="timing",
            required=False,
        )

    @model_validator(mode="after")
    def value_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.Boolean, fhir.String, Quantity, Attachment, Reference],
            field_name_base="value",
            required=False,
        )


class ExplanationOfBenefitDiagnosis(BackboneElement):
    """
    Information about diagnoses relevant to the claim items.
    """

    sequence: Optional[fhir.positiveInt] = Field(
        description="Diagnosis instance identifier",
        default=None,
    )
    diagnosisCodeableConcept: Optional[CodeableConcept] = Field(
        description="Nature of illness or problem",
        default=None,
    )
    diagnosisReference: Optional[Reference] = Field(
        description="Nature of illness or problem",
        default=None,
    )
    type: Optional[ListType[CodeableConcept]] = Field(
        description="Timing or nature of the diagnosis",
        default=None,
    )
    onAdmission: Optional[CodeableConcept] = Field(
        description="Present on admission",
        default=None,
    )
    packageCode: Optional[CodeableConcept] = Field(
        description="Package billing code",
        default=None,
    )

    @property
    def diagnosis(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="diagnosis",
        )

    @model_validator(mode="after")
    def diagnosis_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[CodeableConcept, Reference],
            field_name_base="diagnosis",
            required=True,
        )


class ExplanationOfBenefitProcedure(BackboneElement):
    """
    Procedures performed on the patient relevant to the billing items with the claim.
    """

    sequence: Optional[fhir.positiveInt] = Field(
        description="Procedure instance identifier",
        default=None,
    )
    type: Optional[ListType[CodeableConcept]] = Field(
        description="Category of Procedure",
        default=None,
    )
    date: Optional[fhir.dateTime] = Field(
        description="When the procedure was performed",
        default=None,
    )
    procedureCodeableConcept: Optional[CodeableConcept] = Field(
        description="Specific clinical procedure",
        default=None,
    )
    procedureReference: Optional[Reference] = Field(
        description="Specific clinical procedure",
        default=None,
    )
    udi: Optional[ListType[Reference]] = Field(
        description="Unique device identifier",
        default=None,
    )

    @property
    def procedure(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="procedure",
        )

    @model_validator(mode="after")
    def procedure_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[CodeableConcept, Reference],
            field_name_base="procedure",
            required=True,
        )


class ExplanationOfBenefitInsurance(BackboneElement):
    """
    Financial instruments for reimbursement for the health care products and services specified on the claim.
    """

    focal: Optional[fhir.boolean] = Field(
        description="Coverage to be used for adjudication",
        default=None,
    )
    coverage: Optional[Reference] = Field(
        description="Insurance information",
        default=None,
    )
    preAuthRef: Optional[ListType[fhir.string]] = Field(
        description="Prior authorization reference number",
        default=None,
    )


class ExplanationOfBenefitAccident(BackboneElement):
    """
    Details of a accident which resulted in injuries which required the products and services listed in the claim.
    """

    date: Optional[fhir.date_] = Field(
        description="When the incident occurred",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="The nature of the accident",
        default=None,
    )
    locationAddress: Optional[Address] = Field(
        description="Where the event occurred",
        default=None,
    )
    locationReference: Optional[Reference] = Field(
        description="Where the event occurred",
        default=None,
    )

    @property
    def location(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="location",
        )

    @model_validator(mode="after")
    def location_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Address, Reference],
            field_name_base="location",
            required=False,
        )


class ExplanationOfBenefitItemAdjudication(BackboneElement):
    """
    If this item is a group then the values here are a summary of the adjudication of the detail items. If this item is a simple product or service then this is the result of the adjudication of this item.
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
        description="Non-monitary value",
        default=None,
    )


class ExplanationOfBenefitItemDetailAdjudication(BackboneElement):
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
        description="Non-monitary value",
        default=None,
    )


class ExplanationOfBenefitItemDetailSubDetail(BackboneElement):
    """
    Third-tier of goods and services.
    """

    sequence: Optional[fhir.positiveInt] = Field(
        description="Product or service provided",
        default=None,
    )
    revenue: Optional[CodeableConcept] = Field(
        description="Revenue or cost center code",
        default=None,
    )
    category: Optional[CodeableConcept] = Field(
        description="Benefit classification",
        default=None,
    )
    productOrService: Optional[CodeableConcept] = Field(
        description="Billing, service, product, or drug code",
        default=None,
    )
    modifier: Optional[ListType[CodeableConcept]] = Field(
        description="Service/Product billing modifiers",
        default=None,
    )
    programCode: Optional[ListType[CodeableConcept]] = Field(
        description="Program the product or service is provided under",
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
    udi: Optional[ListType[Reference]] = Field(
        description="Unique device identifier",
        default=None,
    )
    noteNumber: Optional[ListType[fhir.positiveInt]] = Field(
        description="Applicable note numbers",
        default=None,
    )
    adjudication: Optional[ListType[ExplanationOfBenefitItemAdjudication]] = Field(
        description="Subdetail level adjudication details",
        default=None,
    )


class ExplanationOfBenefitItemDetail(BackboneElement):
    """
    Second-tier of goods and services.
    """

    sequence: Optional[fhir.positiveInt] = Field(
        description="Product or service provided",
        default=None,
    )
    revenue: Optional[CodeableConcept] = Field(
        description="Revenue or cost center code",
        default=None,
    )
    category: Optional[CodeableConcept] = Field(
        description="Benefit classification",
        default=None,
    )
    productOrService: Optional[CodeableConcept] = Field(
        description="Billing, service, product, or drug code",
        default=None,
    )
    modifier: Optional[ListType[CodeableConcept]] = Field(
        description="Service/Product billing modifiers",
        default=None,
    )
    programCode: Optional[ListType[CodeableConcept]] = Field(
        description="Program the product or service is provided under",
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
    udi: Optional[ListType[Reference]] = Field(
        description="Unique device identifier",
        default=None,
    )
    noteNumber: Optional[ListType[fhir.positiveInt]] = Field(
        description="Applicable note numbers",
        default=None,
    )
    adjudication: Optional[ListType[ExplanationOfBenefitItemDetailAdjudication]] = (
        Field(
            description="Detail level adjudication details",
            default=None,
        )
    )
    subDetail: Optional[ListType[ExplanationOfBenefitItemDetailSubDetail]] = Field(
        description="Additional items",
        default=None,
    )


class ExplanationOfBenefitItem(BackboneElement):
    """
    A claim line. Either a simple (a product or service) or a 'group' of details which can also be a simple items or groups of sub-details.
    """

    sequence: Optional[fhir.positiveInt] = Field(
        description="Item instance identifier",
        default=None,
    )
    careTeamSequence: Optional[ListType[fhir.positiveInt]] = Field(
        description="Applicable care team members",
        default=None,
    )
    diagnosisSequence: Optional[ListType[fhir.positiveInt]] = Field(
        description="Applicable diagnoses",
        default=None,
    )
    procedureSequence: Optional[ListType[fhir.positiveInt]] = Field(
        description="Applicable procedures",
        default=None,
    )
    informationSequence: Optional[ListType[fhir.positiveInt]] = Field(
        description="Applicable exception and supporting information",
        default=None,
    )
    revenue: Optional[CodeableConcept] = Field(
        description="Revenue or cost center code",
        default=None,
    )
    category: Optional[CodeableConcept] = Field(
        description="Benefit classification",
        default=None,
    )
    productOrService: Optional[CodeableConcept] = Field(
        description="Billing, service, product, or drug code",
        default=None,
    )
    modifier: Optional[ListType[CodeableConcept]] = Field(
        description="Product or service billing modifiers",
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
    udi: Optional[ListType[Reference]] = Field(
        description="Unique device identifier",
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
    encounter: Optional[ListType[Reference]] = Field(
        description="Encounters related to this billed item",
        default=None,
    )
    noteNumber: Optional[ListType[fhir.positiveInt]] = Field(
        description="Applicable note numbers",
        default=None,
    )
    adjudication: Optional[ListType[ExplanationOfBenefitItemAdjudication]] = Field(
        description="Adjudication details",
        default=None,
    )
    detail: Optional[ListType[ExplanationOfBenefitItemDetail]] = Field(
        description="Additional items",
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


class ExplanationOfBenefitAddItemDetailSubDetail(BackboneElement):
    """
    The third-tier service adjudications for payor added services.
    """

    productOrService: Optional[CodeableConcept] = Field(
        description="Billing, service, product, or drug code",
        default=None,
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
    adjudication: Optional[ListType[ExplanationOfBenefitItemAdjudication]] = Field(
        description="Added items adjudication",
        default=None,
    )


class ExplanationOfBenefitAddItemDetail(BackboneElement):
    """
    The second-tier service adjudications for payor added services.
    """

    productOrService: Optional[CodeableConcept] = Field(
        description="Billing, service, product, or drug code",
        default=None,
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
    adjudication: Optional[ListType[ExplanationOfBenefitItemAdjudication]] = Field(
        description="Added items adjudication",
        default=None,
    )
    subDetail: Optional[ListType[ExplanationOfBenefitAddItemDetailSubDetail]] = Field(
        description="Insurer added line items",
        default=None,
    )


class ExplanationOfBenefitAddItem(BackboneElement):
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
    subDetailSequence: Optional[ListType[fhir.positiveInt]] = Field(
        description="Subdetail sequence number",
        default=None,
    )
    provider: Optional[ListType[Reference]] = Field(
        description="Authorized providers",
        default=None,
    )
    productOrService: Optional[CodeableConcept] = Field(
        description="Billing, service, product, or drug code",
        default=None,
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
    adjudication: Optional[ListType[ExplanationOfBenefitItemAdjudication]] = Field(
        description="Added items adjudication",
        default=None,
    )
    detail: Optional[ListType[ExplanationOfBenefitAddItemDetail]] = Field(
        description="Insurer added line items",
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


class ExplanationOfBenefitTotal(BackboneElement):
    """
    Categorized monetary totals for the adjudication.
    """

    category: Optional[CodeableConcept] = Field(
        description="Type of adjudication information",
        default=None,
    )
    amount: Optional[Money] = Field(
        description="Financial total for the category",
        default=None,
    )


class ExplanationOfBenefitPayment(BackboneElement):
    """
    Payment details for the adjudication of the claim.
    """

    type: Optional[CodeableConcept] = Field(
        description="Partial or complete payment",
        default=None,
    )
    adjustment: Optional[Money] = Field(
        description="Payment adjustment for non-claim issues",
        default=None,
    )
    adjustmentReason: Optional[CodeableConcept] = Field(
        description="Explanation for the variance",
        default=None,
    )
    date: Optional[fhir.date_] = Field(
        description="Expected date of payment",
        default=None,
    )
    amount: Optional[Money] = Field(
        description="Payable amount after adjustment",
        default=None,
    )
    identifier: Optional[Identifier] = Field(
        description="Business identifier for the payment",
        default=None,
    )


class ExplanationOfBenefitProcessNote(BackboneElement):
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
    text: Optional[fhir.string] = Field(
        description="Note explanatory text",
        default=None,
    )
    language: Optional[CodeableConcept] = Field(
        description="Language of the text",
        default=None,
    )


class ExplanationOfBenefitBenefitBalanceFinancial(BackboneElement):
    """
    Benefits Used to date.
    """

    type: Optional[CodeableConcept] = Field(
        description="Benefit classification",
        default=None,
    )
    allowedUnsignedInt: Optional[fhir.unsignedInt] = Field(
        description="Benefits allowed",
        default=None,
    )
    allowedString: Optional[fhir.string] = Field(
        description="Benefits allowed",
        default=None,
    )
    allowedMoney: Optional[Money] = Field(
        description="Benefits allowed",
        default=None,
    )
    usedUnsignedInt: Optional[fhir.unsignedInt] = Field(
        description="Benefits used",
        default=None,
    )
    usedMoney: Optional[Money] = Field(
        description="Benefits used",
        default=None,
    )

    @property
    def allowed(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="allowed",
        )

    @property
    def used(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="used",
        )

    @model_validator(mode="after")
    def allowed_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.UnsignedInt, fhir.String, Money],
            field_name_base="allowed",
            required=False,
        )

    @model_validator(mode="after")
    def used_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.UnsignedInt, Money],
            field_name_base="used",
            required=False,
        )


class ExplanationOfBenefitBenefitBalance(BackboneElement):
    """
    Balance by Benefit Category.
    """

    category: Optional[CodeableConcept] = Field(
        description="Benefit classification",
        default=None,
    )
    excluded: Optional[fhir.boolean] = Field(
        description="Excluded from the plan",
        default=None,
    )
    name: Optional[fhir.string] = Field(
        description="Short name for the benefit",
        default=None,
    )
    description: Optional[fhir.string] = Field(
        description="Description of the benefit or services covered",
        default=None,
    )
    network: Optional[CodeableConcept] = Field(
        description="In or out of network",
        default=None,
    )
    unit: Optional[CodeableConcept] = Field(
        description="Individual or family",
        default=None,
    )
    term: Optional[CodeableConcept] = Field(
        description="Annual or lifetime",
        default=None,
    )
    financial: Optional[ListType[ExplanationOfBenefitBenefitBalanceFinancial]] = Field(
        description="Benefit Summary",
        default=None,
    )


class ExplanationOfBenefit(DomainResource):
    """
    This resource provides: the claim details; adjudication details from the processing of a Claim; and optionally account balance information, for informing the subscriber of the benefits provided.
    """

    _abstract = False
    _type = "ExplanationOfBenefit"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/ExplanationOfBenefit"

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
        description="Business Identifier for the resource",
        default=None,
    )
    status: Optional[fhir.code] = Field(
        description="active | cancelled | draft | entered-in-error",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Category or discipline",
        default=None,
    )
    subType: Optional[CodeableConcept] = Field(
        description="More granular claim type",
        default=None,
    )
    use: Optional[fhir.code] = Field(
        description="claim | preauthorization | predetermination",
        default=None,
    )
    patient: Optional[Reference] = Field(
        description="The recipient of the products and services",
        default=None,
    )
    billablePeriod: Optional[Period] = Field(
        description="Relevant time frame for the claim",
        default=None,
    )
    created: Optional[fhir.dateTime] = Field(
        description="Response creation date",
        default=None,
    )
    enterer: Optional[Reference] = Field(
        description="Author of the claim",
        default=None,
    )
    insurer: Optional[Reference] = Field(
        description="Party responsible for reimbursement",
        default=None,
    )
    provider: Optional[Reference] = Field(
        description="Party responsible for the claim",
        default=None,
    )
    priority: Optional[CodeableConcept] = Field(
        description="Desired processing urgency",
        default=None,
    )
    fundsReserveRequested: Optional[CodeableConcept] = Field(
        description="For whom to reserve funds",
        default=None,
    )
    fundsReserve: Optional[CodeableConcept] = Field(
        description="Funds reserved status",
        default=None,
    )
    related: Optional[ListType[ExplanationOfBenefitRelated]] = Field(
        description="Prior or corollary claims",
        default=None,
    )
    prescription: Optional[Reference] = Field(
        description="Prescription authorizing services or products",
        default=None,
    )
    originalPrescription: Optional[Reference] = Field(
        description="Original prescription if superceded by fulfiller",
        default=None,
    )
    payee: Optional[ExplanationOfBenefitPayee] = Field(
        description="Recipient of benefits payable",
        default=None,
    )
    referral: Optional[Reference] = Field(
        description="Treatment Referral",
        default=None,
    )
    facility: Optional[Reference] = Field(
        description="Servicing Facility",
        default=None,
    )
    claim: Optional[Reference] = Field(
        description="Claim reference",
        default=None,
    )
    claimResponse: Optional[Reference] = Field(
        description="Claim response reference",
        default=None,
    )
    outcome: Optional[fhir.code] = Field(
        description="queued | complete | error | partial",
        default=None,
    )
    disposition: Optional[fhir.string] = Field(
        description="Disposition Message",
        default=None,
    )
    preAuthRef: Optional[ListType[fhir.string]] = Field(
        description="Preauthorization reference",
        default=None,
    )
    preAuthRefPeriod: Optional[ListType[Period]] = Field(
        description="Preauthorization in-effect period",
        default=None,
    )
    careTeam: Optional[ListType[ExplanationOfBenefitCareTeam]] = Field(
        description="Care Team members",
        default=None,
    )
    supportingInfo: Optional[ListType[ExplanationOfBenefitSupportingInfo]] = Field(
        description="Supporting information",
        default=None,
    )
    diagnosis: Optional[ListType[ExplanationOfBenefitDiagnosis]] = Field(
        description="Pertinent diagnosis information",
        default=None,
    )
    procedure: Optional[ListType[ExplanationOfBenefitProcedure]] = Field(
        description="Clinical procedures performed",
        default=None,
    )
    precedence: Optional[fhir.positiveInt] = Field(
        description="Precedence (primary, secondary, etc.)",
        default=None,
    )
    insurance: Optional[ListType[ExplanationOfBenefitInsurance]] = Field(
        description="Patient insurance information",
        default=None,
    )
    accident: Optional[ExplanationOfBenefitAccident] = Field(
        description="Details of the event",
        default=None,
    )
    item: Optional[ListType[ExplanationOfBenefitItem]] = Field(
        description="Product or service provided",
        default=None,
    )
    addItem: Optional[ListType[ExplanationOfBenefitAddItem]] = Field(
        description="Insurer added line items",
        default=None,
    )
    adjudication: Optional[ListType[ExplanationOfBenefitItemAdjudication]] = Field(
        description="Header-level adjudication",
        default=None,
    )
    total: Optional[ListType[ExplanationOfBenefitTotal]] = Field(
        description="Adjudication totals",
        default=None,
    )
    payment: Optional[ExplanationOfBenefitPayment] = Field(
        description="Payment Details",
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
    processNote: Optional[ListType[ExplanationOfBenefitProcessNote]] = Field(
        description="Note concerning adjudication",
        default=None,
    )
    benefitPeriod: Optional[Period] = Field(
        description="When the benefits are applicable",
        default=None,
    )
    benefitBalance: Optional[ListType[ExplanationOfBenefitBenefitBalance]] = Field(
        description="Balance by Benefit Category",
        default=None,
    )
