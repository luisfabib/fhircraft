from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    PositiveInt,
    Boolean,
)

from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    BackboneElement,
    Reference,
    CodeableConcept,
    Period,
    Quantity,
    Money,
)
from .resource import Resource
from .domain_resource import DomainResource


class CoveragePaymentBy(BackboneElement):
    """
    Link to the paying party and optionally what specifically they will be responsible to pay.
    """

    party: Optional[Reference] = Field(
        description="Parties performing self-payment",
        default=None,
    )
    responsibility: Optional[String] = Field(
        description="Party\u0027s responsibility",
        default=None,
    )
    responsibility_ext: Optional[Element] = Field(
        description="Placeholder element for responsibility extensions",
        default=None,
        alias="_responsibility",
    )


class CoverageClass(BackboneElement):
    """
    A suite of underwriter specific classifiers.
    """

    type: Optional[CodeableConcept] = Field(
        description="Type of class such as \u0027group\u0027 or \u0027plan\u0027",
        default=None,
    )
    value: Optional[Identifier] = Field(
        description="Value associated with the type",
        default=None,
    )
    name: Optional[String] = Field(
        description="Human readable description of the type and value",
        default=None,
    )
    name_ext: Optional[Element] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )


class CoverageCostToBeneficiaryException(BackboneElement):
    """
    A suite of codes indicating exceptions or reductions to patient costs and their effective periods.
    """

    type: Optional[CodeableConcept] = Field(
        description="Exception category",
        default=None,
    )
    period: Optional[Period] = Field(
        description="The effective period of the exception",
        default=None,
    )


class CoverageCostToBeneficiary(BackboneElement):
    """
    A suite of codes indicating the cost category and associated amount which have been detailed in the policy and may have been  included on the health card.
    """

    type: Optional[CodeableConcept] = Field(
        description="Cost category",
        default=None,
    )
    category: Optional[CodeableConcept] = Field(
        description="Benefit classification",
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
    valueQuantity: Optional[Quantity] = Field(
        description="The amount or percentage due from the beneficiary",
        default=None,
    )
    valueMoney: Optional[Money] = Field(
        description="The amount or percentage due from the beneficiary",
        default=None,
    )
    exception: Optional[ListType[CoverageCostToBeneficiaryException]] = Field(
        description="Exceptions for patient payments",
        default=None,
    )

    @property
    def value(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="value",
        )

    @model_validator(mode="after")
    def value_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Quantity, Money],
            field_name_base="value",
            required=False,
        )


class Coverage(DomainResource):
    """
    Financial instrument which may be used to reimburse or pay for health care products and services. Includes both insurance and self-payment.
    """

    _abstract = False
    _type = "Coverage"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Coverage"

    identifier: Optional[ListType[Identifier]] = Field(
        description="Business identifier(s) for this coverage",
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
    kind: Optional[Code] = Field(
        description="insurance | self-pay | other",
        default=None,
    )
    kind_ext: Optional[Element] = Field(
        description="Placeholder element for kind extensions",
        default=None,
        alias="_kind",
    )
    paymentBy: Optional[ListType[CoveragePaymentBy]] = Field(
        description="Self-pay parties and responsibility",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Coverage category such as medical or accident",
        default=None,
    )
    policyHolder: Optional[Reference] = Field(
        description="Owner of the policy",
        default=None,
    )
    subscriber: Optional[Reference] = Field(
        description="Subscriber to the policy",
        default=None,
    )
    subscriberId: Optional[ListType[Identifier]] = Field(
        description="ID assigned to the subscriber",
        default=None,
    )
    beneficiary: Optional[Reference] = Field(
        description="Plan beneficiary",
        default=None,
    )
    dependent: Optional[String] = Field(
        description="Dependent number",
        default=None,
    )
    dependent_ext: Optional[Element] = Field(
        description="Placeholder element for dependent extensions",
        default=None,
        alias="_dependent",
    )
    relationship: Optional[CodeableConcept] = Field(
        description="Beneficiary relationship to the subscriber",
        default=None,
    )
    period: Optional[Period] = Field(
        description="Coverage start and end dates",
        default=None,
    )
    insurer: Optional[Reference] = Field(
        description="Issuer of the policy",
        default=None,
    )
    class_: Optional[ListType[CoverageClass]] = Field(
        description="Additional coverage classifications",
        default=None,
        alias="class",
    )
    order: Optional[PositiveInt] = Field(
        description="Relative order of the coverage",
        default=None,
    )
    order_ext: Optional[Element] = Field(
        description="Placeholder element for order extensions",
        default=None,
        alias="_order",
    )
    network: Optional[String] = Field(
        description="Insurer network",
        default=None,
    )
    network_ext: Optional[Element] = Field(
        description="Placeholder element for network extensions",
        default=None,
        alias="_network",
    )
    costToBeneficiary: Optional[ListType[CoverageCostToBeneficiary]] = Field(
        description="Patient payments for services/products",
        default=None,
    )
    subrogation: Optional[Boolean] = Field(
        description="Reimbursement to insurer",
        default=None,
    )
    subrogation_ext: Optional[Element] = Field(
        description="Placeholder element for subrogation extensions",
        default=None,
        alias="_subrogation",
    )
    contract: Optional[ListType[Reference]] = Field(
        description="Contract details",
        default=None,
    )
    insurancePlan: Optional[Reference] = Field(
        description="Insurance plan details",
        default=None,
    )
