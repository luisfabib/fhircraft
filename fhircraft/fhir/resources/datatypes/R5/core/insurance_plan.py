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
    CodeableConcept,
    Period,
    Reference,
    ExtendedContactDetail,
    BackboneElement,
    Quantity,
    Money,
)
from .resource import Resource
from .domain_resource import DomainResource


class InsurancePlanCoverageBenefitLimit(BackboneElement):
    """
    The specific limits on the benefit.
    """

    value: Optional[Quantity] = Field(
        description="Maximum value allowed",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="Benefit limit details",
        default=None,
    )


class InsurancePlanCoverageBenefit(BackboneElement):
    """
    Specific benefits under this type of coverage.
    """

    type: CodeableConcept = Field(
        description="Type of benefit",
    )
    requirement: Optional[fhir.string] = Field(
        description="Referral requirements",
        default=None,
    )
    limit: Optional[ListType[InsurancePlanCoverageBenefitLimit]] = Field(
        description="Benefit limits",
        default=None,
    )


class InsurancePlanCoverage(BackboneElement):
    """
    Details about the coverage offered by the insurance product.
    """

    type: CodeableConcept = Field(
        description="Type of coverage",
    )
    network: Optional[ListType[Reference]] = Field(
        description="What networks provide coverage",
        default=None,
    )
    benefit: ListType[InsurancePlanCoverageBenefit] = Field(
        description="List of benefits",
        min_length=1,
    )


class InsurancePlanPlanGeneralCost(BackboneElement):
    """
    Overall costs associated with the plan.
    """

    type: Optional[CodeableConcept] = Field(
        description="Type of cost",
        default=None,
    )
    groupSize: Optional[fhir.positiveInt] = Field(
        description="Number of enrollees",
        default=None,
    )
    cost: Optional[Money] = Field(
        description="Cost value",
        default=None,
    )
    comment: Optional[fhir.string] = Field(
        description="Additional cost information",
        default=None,
    )


class InsurancePlanPlanSpecificCostBenefitCost(BackboneElement):
    """
    List of the costs associated with a specific benefit.
    """

    type: CodeableConcept = Field(
        description="Type of cost",
    )
    applicability: Optional[CodeableConcept] = Field(
        description="in-network | out-of-network | other",
        default=None,
    )
    qualifiers: Optional[ListType[CodeableConcept]] = Field(
        description="Additional information about the cost",
        default=None,
    )
    value: Optional[Quantity] = Field(
        description="The actual cost value",
        default=None,
    )


class InsurancePlanPlanSpecificCostBenefit(BackboneElement):
    """
    List of the specific benefits under this category of benefit.
    """

    type: CodeableConcept = Field(
        description="Type of specific benefit",
    )
    cost: Optional[ListType[InsurancePlanPlanSpecificCostBenefitCost]] = Field(
        description="List of the costs",
        default=None,
    )


class InsurancePlanPlanSpecificCost(BackboneElement):
    """
    Costs associated with the coverage provided by the product.
    """

    category: CodeableConcept = Field(
        description="General category of benefit",
    )
    benefit: Optional[ListType[InsurancePlanPlanSpecificCostBenefit]] = Field(
        description="Benefits list",
        default=None,
    )


class InsurancePlanPlan(BackboneElement):
    """
    Details about an insurance plan.
    """

    identifier: Optional[ListType[Identifier]] = Field(
        description="Business Identifier for Product",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Type of plan",
        default=None,
    )
    coverageArea: Optional[ListType[Reference]] = Field(
        description="Where product applies",
        default=None,
    )
    network: Optional[ListType[Reference]] = Field(
        description="What networks provide coverage",
        default=None,
    )
    generalCost: Optional[ListType[InsurancePlanPlanGeneralCost]] = Field(
        description="Overall costs",
        default=None,
    )
    specificCost: Optional[ListType[InsurancePlanPlanSpecificCost]] = Field(
        description="Specific costs",
        default=None,
    )


class InsurancePlan(DomainResource):
    """
    Details of a Health Insurance product/plan provided by an organization.
    """

    _abstract = False
    _type = "InsurancePlan"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/InsurancePlan"

    identifier: Optional[ListType[Identifier]] = Field(
        description="Business Identifier for Product",
        default=None,
    )
    status: Optional[fhir.code] = Field(
        description="draft | active | retired | unknown",
        default=None,
    )
    type: Optional[ListType[CodeableConcept]] = Field(
        description="Kind of product",
        default=None,
    )
    name: Optional[fhir.string] = Field(
        description="Official name",
        default=None,
    )
    alias: Optional[ListType[fhir.string]] = Field(
        description="Alternate names",
        default=None,
    )
    period: Optional[Period] = Field(
        description="When the product is available",
        default=None,
    )
    ownedBy: Optional[Reference] = Field(
        description="Product issuer",
        default=None,
    )
    administeredBy: Optional[Reference] = Field(
        description="Product administrator",
        default=None,
    )
    coverageArea: Optional[ListType[Reference]] = Field(
        description="Where product applies",
        default=None,
    )
    contact: Optional[ListType[ExtendedContactDetail]] = Field(
        description="Official contact details relevant to the health insurance plan/product",
        default=None,
    )
    endpoint: Optional[ListType[Reference]] = Field(
        description="Technical endpoint",
        default=None,
    )
    network: Optional[ListType[Reference]] = Field(
        description="What networks are Included",
        default=None,
    )
    coverage: Optional[ListType[InsurancePlanCoverage]] = Field(
        description="Coverage details",
        default=None,
    )
    plan: Optional[ListType[InsurancePlanPlan]] = Field(
        description="Plan details",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ipn_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(identifier.count() + name.count()) > 0",
            human="The organization SHALL at least have a name or an identifier, and possibly more than one",
            key="ipn-1",
            severity="error",
        )
