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
    Reference,
    Period,
    BackboneElement,
    CodeableConcept,
    Money,
)
from .resource import Resource
from .domain_resource import DomainResource


class CoverageEligibilityResponseInsuranceItemBenefit(BackboneElement):
    """
    Benefits used to date.
    """

    type: CodeableConcept = Field(
        description="Benefit classification",
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
    usedString: Optional[fhir.string] = Field(
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
            field_types=[fhir.UnsignedInt, fhir.String, Money],
            field_name_base="used",
            required=False,
        )


class CoverageEligibilityResponseInsuranceItem(BackboneElement):
    """
    Benefits and optionally current balances, and authorization details by category or service.
    """

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
        description="Performing practitioner",
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
    benefit: Optional[ListType[CoverageEligibilityResponseInsuranceItemBenefit]] = (
        Field(
            description="Benefit Summary",
            default=None,
        )
    )
    authorizationRequired: Optional[fhir.boolean] = Field(
        description="Authorization required flag",
        default=None,
    )
    authorizationSupporting: Optional[ListType[CodeableConcept]] = Field(
        description="Type of required supporting materials",
        default=None,
    )
    authorizationUrl: Optional[fhir.uri] = Field(
        description="Preauthorization requirements endpoint",
        default=None,
    )


class CoverageEligibilityResponseInsurance(BackboneElement):
    """
    Financial instruments for reimbursement for the health care products and services.
    """

    coverage: Reference = Field(
        description="Insurance information",
    )
    inforce: Optional[fhir.boolean] = Field(
        description="Coverage inforce indicator",
        default=None,
    )
    benefitPeriod: Optional[Period] = Field(
        description="When the benefits are applicable",
        default=None,
    )
    item: Optional[ListType[CoverageEligibilityResponseInsuranceItem]] = Field(
        description="Benefits and authorization details",
        default=None,
    )


class CoverageEligibilityResponseError(BackboneElement):
    """
    Errors encountered during the processing of the request.
    """

    code: CodeableConcept = Field(
        description="Error code detailing processing issues",
    )


class CoverageEligibilityResponse(DomainResource):
    """
    This resource provides eligibility and plan details from the processing of an CoverageEligibilityRequest resource.
    """

    _abstract = False
    _type = "CoverageEligibilityResponse"
    _canonical_url = (
        "http://hl7.org/fhir/StructureDefinition/CoverageEligibilityResponse"
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
    purpose: ListType[fhir.code] = Field(
        description="auth-requirements | benefits | discovery | validation",
     	min_length=1,
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
        description="Response creation date",
    )
    requestor: Optional[Reference] = Field(
        description="Party responsible for the request",
        default=None,
    )
    request: Reference = Field(
        description="Eligibility request reference",
    )
    outcome: fhir.code = Field(
        description="queued | complete | error | partial",
    )
    disposition: Optional[fhir.string] = Field(
        description="Disposition Message",
        default=None,
    )
    insurer: Reference = Field(
        description="Coverage issuer",
    )
    insurance: Optional[ListType[CoverageEligibilityResponseInsurance]] = Field(
        description="Patient insurance information",
        default=None,
    )
    preAuthRef: Optional[fhir.string] = Field(
        description="Preauthorization reference",
        default=None,
    )
    form: Optional[CodeableConcept] = Field(
        description="Printed form identifier",
        default=None,
    )
    error: Optional[ListType[CoverageEligibilityResponseError]] = Field(
        description="Processing errors",
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

    @model_validator(mode="after")
    def FHIR_ces_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("response.insurance.item",),
            expression="category.exists() xor productOrService.exists()",
            human="SHALL contain a category or a billcode but not both.",
            key="ces-1",
            severity="error",
        )
