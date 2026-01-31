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
    Boolean,
    UnsignedInt,
)

from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Reference,
    BackboneElement,
    CodeableConcept,
    Period,
    Money,
)
from .resource import Resource
from .domain_resource import DomainResource


class CoverageEligibilityResponseEvent(BackboneElement):
    """
    Information code for an event with a corresponding date or period.
    """

    type: Optional[CodeableConcept] = Field(
        description="Specific event",
        default=None,
    )
    whenDateTime: Optional[DateTime] = Field(
        description="Occurance date or period",
        default=None,
    )
    whenDateTime_ext: Optional[Element] = Field(
        description="Placeholder element for whenDateTime extensions",
        default=None,
        alias="_whenDateTime",
    )
    whenPeriod: Optional[Period] = Field(
        description="Occurance date or period",
        default=None,
    )

    @property
    def when(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="when",
        )

    @model_validator(mode="after")
    def when_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[DateTime, Period],
            field_name_base="when",
            required=True,
        )


class CoverageEligibilityResponseInsuranceItemBenefit(BackboneElement):
    """
    Benefits used to date.
    """

    type: Optional[CodeableConcept] = Field(
        description="Benefit classification",
        default=None,
    )
    allowedUnsignedInt: Optional[UnsignedInt] = Field(
        description="Benefits allowed",
        default=None,
    )
    allowedUnsignedInt_ext: Optional[Element] = Field(
        description="Placeholder element for allowedUnsignedInt extensions",
        default=None,
        alias="_allowedUnsignedInt",
    )
    allowedString: Optional[String] = Field(
        description="Benefits allowed",
        default=None,
    )
    allowedString_ext: Optional[Element] = Field(
        description="Placeholder element for allowedString extensions",
        default=None,
        alias="_allowedString",
    )
    allowedMoney: Optional[Money] = Field(
        description="Benefits allowed",
        default=None,
    )
    usedUnsignedInt: Optional[UnsignedInt] = Field(
        description="Benefits used",
        default=None,
    )
    usedUnsignedInt_ext: Optional[Element] = Field(
        description="Placeholder element for usedUnsignedInt extensions",
        default=None,
        alias="_usedUnsignedInt",
    )
    usedString: Optional[String] = Field(
        description="Benefits used",
        default=None,
    )
    usedString_ext: Optional[Element] = Field(
        description="Placeholder element for usedString extensions",
        default=None,
        alias="_usedString",
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
            field_types=[UnsignedInt, String, Money],
            field_name_base="allowed",
            required=False,
        )

    @model_validator(mode="after")
    def used_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[UnsignedInt, String, Money],
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
    excluded: Optional[Boolean] = Field(
        description="Excluded from the plan",
        default=None,
    )
    excluded_ext: Optional[Element] = Field(
        description="Placeholder element for excluded extensions",
        default=None,
        alias="_excluded",
    )
    name: Optional[String] = Field(
        description="Short name for the benefit",
        default=None,
    )
    name_ext: Optional[Element] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    description: Optional[String] = Field(
        description="Description of the benefit or services covered",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
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
    authorizationRequired: Optional[Boolean] = Field(
        description="Authorization required flag",
        default=None,
    )
    authorizationRequired_ext: Optional[Element] = Field(
        description="Placeholder element for authorizationRequired extensions",
        default=None,
        alias="_authorizationRequired",
    )
    authorizationSupporting: Optional[ListType[CodeableConcept]] = Field(
        description="Type of required supporting materials",
        default=None,
    )
    authorizationUrl: Optional[Uri] = Field(
        description="Preauthorization requirements endpoint",
        default=None,
    )
    authorizationUrl_ext: Optional[Element] = Field(
        description="Placeholder element for authorizationUrl extensions",
        default=None,
        alias="_authorizationUrl",
    )


class CoverageEligibilityResponseInsurance(BackboneElement):
    """
    Financial instruments for reimbursement for the health care products and services.
    """

    coverage: Optional[Reference] = Field(
        description="Insurance information",
        default=None,
    )
    inforce: Optional[Boolean] = Field(
        description="Coverage inforce indicator",
        default=None,
    )
    inforce_ext: Optional[Element] = Field(
        description="Placeholder element for inforce extensions",
        default=None,
        alias="_inforce",
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

    code: Optional[CodeableConcept] = Field(
        description="Error code detailing processing issues",
        default=None,
    )
    expression: Optional[ListType[String]] = Field(
        description="FHIRPath of element(s) related to issue",
        default=None,
    )
    expression_ext: Optional[ListType[Optional[Element]]] = Field(
        description="Placeholder element for expression extensions",
        default=None,
        alias="_expression",
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

    identifier: Optional[ListType[Identifier]] = Field(
        description="Business Identifier for coverage eligiblity request",
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
    purpose: Optional[ListType[Code]] = Field(
        description="auth-requirements | benefits | discovery | validation",
        default=None,
    )
    purpose_ext: Optional[ListType[Optional[Element]]] = Field(
        description="Placeholder element for purpose extensions",
        default=None,
        alias="_purpose",
    )
    patient: Optional[Reference] = Field(
        description="Intended recipient of products and services",
        default=None,
    )
    event: Optional[ListType[CoverageEligibilityResponseEvent]] = Field(
        description="Event information",
        default=None,
    )
    servicedDate: Optional[Date] = Field(
        description="Estimated date or dates of service",
        default=None,
    )
    servicedDate_ext: Optional[Element] = Field(
        description="Placeholder element for servicedDate extensions",
        default=None,
        alias="_servicedDate",
    )
    servicedPeriod: Optional[Period] = Field(
        description="Estimated date or dates of service",
        default=None,
    )
    created: Optional[DateTime] = Field(
        description="Response creation date",
        default=None,
    )
    created_ext: Optional[Element] = Field(
        description="Placeholder element for created extensions",
        default=None,
        alias="_created",
    )
    requestor: Optional[Reference] = Field(
        description="Party responsible for the request",
        default=None,
    )
    request: Optional[Reference] = Field(
        description="Eligibility request reference",
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
        description="Disposition Message",
        default=None,
    )
    disposition_ext: Optional[Element] = Field(
        description="Placeholder element for disposition extensions",
        default=None,
        alias="_disposition",
    )
    insurer: Optional[Reference] = Field(
        description="Coverage issuer",
        default=None,
    )
    insurance: Optional[ListType[CoverageEligibilityResponseInsurance]] = Field(
        description="Patient insurance information",
        default=None,
    )
    preAuthRef: Optional[String] = Field(
        description="Preauthorization reference",
        default=None,
    )
    preAuthRef_ext: Optional[Element] = Field(
        description="Placeholder element for preAuthRef extensions",
        default=None,
        alias="_preAuthRef",
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
            field_types=[Date, Period],
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
