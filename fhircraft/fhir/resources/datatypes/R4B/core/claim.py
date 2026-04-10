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
    Quantity,
    Attachment,
    Address,
    Money,
)
from .resource import Resource
from .domain_resource import DomainResource


class ClaimRelated(BackboneElement):
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


class ClaimPayee(BackboneElement):
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


class ClaimCareTeam(BackboneElement):
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


class ClaimSupportingInfo(BackboneElement):
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
    reason: Optional[CodeableConcept] = Field(
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


class ClaimDiagnosis(BackboneElement):
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


class ClaimProcedure(BackboneElement):
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


class ClaimInsurance(BackboneElement):
    """
    Financial instruments for reimbursement for the health care products and services specified on the claim.
    """

    sequence: Optional[fhir.positiveInt] = Field(
        description="Insurance instance identifier",
        default=None,
    )
    focal: Optional[fhir.boolean] = Field(
        description="Coverage to be used for adjudication",
        default=None,
    )
    identifier: Optional[Identifier] = Field(
        description="Pre-assigned Claim number",
        default=None,
    )
    coverage: Optional[Reference] = Field(
        description="Insurance information",
        default=None,
    )
    businessArrangement: Optional[fhir.string] = Field(
        description="Additional provider contract number",
        default=None,
    )
    preAuthRef: Optional[ListType[fhir.string]] = Field(
        description="Prior authorization reference number",
        default=None,
    )
    claimResponse: Optional[Reference] = Field(
        description="Adjudication results",
        default=None,
    )


class ClaimAccident(BackboneElement):
    """
    Details of an accident which resulted in injuries which required the products and services listed in the claim.
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


class ClaimItemDetailSubDetail(BackboneElement):
    """
    A claim detail line. Either a simple (a product or service) or a 'group' of sub-details which are simple items.
    """

    sequence: Optional[fhir.positiveInt] = Field(
        description="Item instance identifier",
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


class ClaimItemDetail(BackboneElement):
    """
    A claim detail line. Either a simple (a product or service) or a 'group' of sub-details which are simple items.
    """

    sequence: Optional[fhir.positiveInt] = Field(
        description="Item instance identifier",
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
    subDetail: Optional[ListType[ClaimItemDetailSubDetail]] = Field(
        description="Product or service provided",
        default=None,
    )


class ClaimItem(BackboneElement):
    """
    A claim line. Either a simple  product or service or a 'group' of details which can each be a simple items or groups of sub-details.
    """

    sequence: Optional[fhir.positiveInt] = Field(
        description="Item instance identifier",
        default=None,
    )
    careTeamSequence: Optional[ListType[fhir.positiveInt]] = Field(
        description="Applicable careTeam members",
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
    detail: Optional[ListType[ClaimItemDetail]] = Field(
        description="Product or service provided",
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


class Claim(DomainResource):
    """
    A provider issued list of professional services and products which have been provided, or are to be provided, to a patient which is sent to an insurer for reimbursement.
    """

    _abstract = False
    _type = "Claim"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Claim"

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
        description="Business Identifier for claim",
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
        description="Resource creation date",
        default=None,
    )
    enterer: Optional[Reference] = Field(
        description="Author of the claim",
        default=None,
    )
    insurer: Optional[Reference] = Field(
        description="Target",
        default=None,
    )
    provider: Optional[Reference] = Field(
        description="Party responsible for the claim",
        default=None,
    )
    priority: Optional[CodeableConcept] = Field(
        description="Desired processing ugency",
        default=None,
    )
    fundsReserve: Optional[CodeableConcept] = Field(
        description="For whom to reserve funds",
        default=None,
    )
    related: Optional[ListType[ClaimRelated]] = Field(
        description="Prior or corollary claims",
        default=None,
    )
    prescription: Optional[Reference] = Field(
        description="Prescription authorizing services and products",
        default=None,
    )
    originalPrescription: Optional[Reference] = Field(
        description="Original prescription if superseded by fulfiller",
        default=None,
    )
    payee: Optional[ClaimPayee] = Field(
        description="Recipient of benefits payable",
        default=None,
    )
    referral: Optional[Reference] = Field(
        description="Treatment referral",
        default=None,
    )
    facility: Optional[Reference] = Field(
        description="Servicing facility",
        default=None,
    )
    careTeam: Optional[ListType[ClaimCareTeam]] = Field(
        description="Members of the care team",
        default=None,
    )
    supportingInfo: Optional[ListType[ClaimSupportingInfo]] = Field(
        description="Supporting information",
        default=None,
    )
    diagnosis: Optional[ListType[ClaimDiagnosis]] = Field(
        description="Pertinent diagnosis information",
        default=None,
    )
    procedure: Optional[ListType[ClaimProcedure]] = Field(
        description="Clinical procedures performed",
        default=None,
    )
    insurance: Optional[ListType[ClaimInsurance]] = Field(
        description="Patient insurance information",
        default=None,
    )
    accident: Optional[ClaimAccident] = Field(
        description="Details of the event",
        default=None,
    )
    item: Optional[ListType[ClaimItem]] = Field(
        description="Product or service provided",
        default=None,
    )
    total: Optional[Money] = Field(
        description="Total claim cost",
        default=None,
    )
