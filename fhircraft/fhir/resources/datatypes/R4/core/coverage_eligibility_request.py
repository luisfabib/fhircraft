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
    Money,
    Reference,
    Period,
    BackboneElement,
    Quantity,
)
from .resource import Resource
from .domain_resource import DomainResource

class CoverageEligibilityRequestSupportingInfo(BackboneElement):
    """
    Additional information codes regarding exceptions, special considerations, the condition, situation, prior or concurrent issues.
    """

    sequence: fhir.positiveInt = Field(
        description="Information instance identifier",
    )
    information: Reference = Field(
        description="Data to be provided",
    )
    appliesToAll: Optional[fhir.boolean] = Field(
        description="Applies to all items",
        default=None,
    )

class CoverageEligibilityRequestInsurance(BackboneElement):
    """
    Financial instruments for reimbursement for the health care products and services.
    """

    focal: Optional[fhir.boolean] = Field(
        description="Applicable coverage",
        default=None,
    )
    coverage: Reference = Field(
        description="Insurance information",
    )
    businessArrangement: Optional[fhir.string] = Field(
        description="Additional provider contract number",
        default=None,
    )

class CoverageEligibilityRequestItemDiagnosis(BackboneElement):
    """
    Patient diagnosis for which care is sought.
    """

    diagnosisCodeableConcept: Optional[CodeableConcept] = Field(
        description="Nature of illness or problem",
        default=None,
    )
    diagnosisReference: Optional[Reference] = Field(
        description="Nature of illness or problem",
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
            required=False,
        )

class CoverageEligibilityRequestItem(BackboneElement):
    """
    Service categories or billable services for which benefit details and/or an authorization prior to service delivery may be required by the payor.
    """

    supportingInfoSequence: Optional[ListType[fhir.positiveInt]] = Field(
        description="Applicable exception or supporting information",
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
    provider: Optional[Reference] = Field(
        description="Perfoming practitioner",
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
    facility: Optional[Reference] = Field(
        description="Servicing facility",
        default=None,
    )
    diagnosis: Optional[ListType[CoverageEligibilityRequestItemDiagnosis]] = Field(
        description="Applicable diagnosis",
        default=None,
    )
    detail: Optional[ListType[Reference]] = Field(
        description="Product or service details",
        default=None,
    )

class CoverageEligibilityRequest(DomainResource):
    """
    The CoverageEligibilityRequest provides patient and insurance coverage information to an insurer for them to respond, in the form of an CoverageEligibilityResponse, with information regarding whether the stated coverage is valid and in-force and optionally to provide the insurance details of the policy.
    """

    _abstract = False
    _type = "CoverageEligibilityRequest"
    _canonical_url = (
        "http://hl7.org/fhir/StructureDefinition/CoverageEligibilityRequest"
    )

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
        description="Business Identifier for coverage eligiblity request",
        default=None,
    )
    status: fhir.code = Field(
        description="active | cancelled | draft | entered-in-error",
    )
    priority: Optional[CodeableConcept] = Field(
        description="Desired processing priority",
        default=None,
    )
    purpose: ListType[fhir.code] = Field(
        description="auth-requirements | benefits | discovery | validation",
    )
    patient: Reference = Field(
        description="Intended recipient of products and services",
    )
    servicedDate: Optional[fhir.date_] = Field(
        description="Estimated date or dates of service",
        default=None,
    )
    servicedPeriod: Optional[Period] = Field(
        description="Estimated date or dates of service",
        default=None,
    )
    created: fhir.dateTime = Field(
        description="Creation date",
    )
    enterer: Optional[Reference] = Field(
        description="Author",
        default=None,
    )
    provider: Optional[Reference] = Field(
        description="Party responsible for the request",
        default=None,
    )
    insurer: Reference = Field(
        description="Coverage issuer",
    )
    facility: Optional[Reference] = Field(
        description="Servicing facility",
        default=None,
    )
    supportingInfo: Optional[ListType[CoverageEligibilityRequestSupportingInfo]] = (
        Field(
            description="Supporting information",
            default=None,
        )
    )
    insurance: Optional[ListType[CoverageEligibilityRequestInsurance]] = Field(
        description="Patient insurance information",
        default=None,
    )
    item: Optional[ListType[CoverageEligibilityRequestItem]] = Field(
        description="Item to be evaluated for eligibiity",
        default=None,
    )

    @property
    def serviced(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="serviced",
        )

    @model_validator(mode="after")
    def serviced_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.Date, Period],
            field_name_base="serviced",
            required=False,
        )
