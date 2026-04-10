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
    Money,
)
from .resource import Resource
from .domain_resource import DomainResource

class CoverageClass(BackboneElement):
    """
    A suite of underwriter specific classifiers.
    """

    type: Optional[CodeableConcept] = Field(
        description="Type of class such as \u0027group\u0027 or \u0027plan\u0027",
        default=None,
    )
    value: Optional[fhir.string] = Field(
        description="Value associated with the type",
        default=None,
    )
    name: Optional[fhir.string] = Field(
        description="Human readable description of the type and value",
        default=None,
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
            required=True,
        )

class Coverage(DomainResource):
    """
    Financial instrument which may be used to reimburse or pay for health care products and services. Includes both insurance and self-payment.
    """

    _abstract = False
    _type = "Coverage"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Coverage"

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
        description="Business Identifier for the coverage",
        default=None,
    )
    status: Optional[fhir.code] = Field(
        description="active | cancelled | draft | entered-in-error",
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
    subscriberId: Optional[fhir.string] = Field(
        description="ID assigned to the subscriber",
        default=None,
    )
    beneficiary: Optional[Reference] = Field(
        description="Plan beneficiary",
        default=None,
    )
    dependent: Optional[fhir.string] = Field(
        description="Dependent number",
        default=None,
    )
    relationship: Optional[CodeableConcept] = Field(
        description="Beneficiary relationship to the subscriber",
        default=None,
    )
    period: Optional[Period] = Field(
        description="Coverage start and end dates",
        default=None,
    )
    payor: Optional[ListType[Reference]] = Field(
        description="Issuer of the policy",
        default=None,
    )
    class_: Optional[ListType[CoverageClass]] = Field(
        description="Additional coverage classifications",
        default=None,
        alias="class",
    )
    order: Optional[fhir.positiveInt] = Field(
        description="Relative order of the coverage",
        default=None,
    )
    network: Optional[fhir.string] = Field(
        description="Insurer network",
        default=None,
    )
    costToBeneficiary: Optional[ListType[CoverageCostToBeneficiary]] = Field(
        description="Patient payments for services/products",
        default=None,
    )
    subrogation: Optional[fhir.boolean] = Field(
        description="Reimbursement to insurer",
        default=None,
    )
    contract: Optional[ListType[Reference]] = Field(
        description="Contract details",
        default=None,
    )
