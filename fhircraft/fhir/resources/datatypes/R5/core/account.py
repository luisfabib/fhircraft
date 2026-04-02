from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators
from ..primitive import *
from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    Identifier,
    CodeableConcept,
    Reference,
    Period,
    BackboneElement,
    CodeableReference,
    Money,
)
from .domain_resource import DomainResource

class AccountCoverage(BackboneElement):
    """
    The party(s) that are responsible for covering the payment of this account, and what order should they be applied to the account.
    """

    coverage: Optional[Reference] = Field(
        description="The party(s), such as insurances, that may contribute to the payment of this account",
        default=None,
    )
    priority: Optional[PositiveInt] = Field(
        description="The priority of the coverage in the context of this account",
        default=None,
    )

class AccountGuarantor(BackboneElement):
    """
    The parties responsible for balancing the account if other payment options fall short.
    """

    party: Optional[Reference] = Field(
        description="Responsible entity",
        default=None,
    )
    onHold: Optional[Boolean] = Field(
        description="Credit or other hold applied",
        default=None,
    )
    period: Optional[Period] = Field(
        description="Guarantee account during",
        default=None,
    )

class AccountDiagnosis(BackboneElement):
    """
    When using an account for billing a specific Encounter the set of diagnoses that are relevant for billing are stored here on the account where they are able to be sequenced appropriately prior to processing to produce claim(s).
    """

    sequence: Optional[PositiveInt] = Field(
        description="Ranking of the diagnosis (for each type)",
        default=None,
    )
    condition: Optional[CodeableReference] = Field(
        description="The diagnosis relevant to the account",
        default=None,
    )
    dateOfDiagnosis: Optional[DateTime] = Field(
        description="Date of the diagnosis (when coded diagnosis)",
        default=None,
    )
    type: Optional[ListType[CodeableConcept]] = Field(
        description="Type that this diagnosis has relevant to the account (e.g. admission, billing, discharge \u2026)",
        default=None,
    )
    onAdmission: Optional[Boolean] = Field(
        description="Diagnosis present on Admission",
        default=None,
    )
    packageCode: Optional[ListType[CodeableConcept]] = Field(
        description="Package Code specific for billing",
        default=None,
    )

class AccountProcedure(BackboneElement):
    """
    When using an account for billing a specific Encounter the set of procedures that are relevant for billing are stored here on the account where they are able to be sequenced appropriately prior to processing to produce claim(s).
    """

    sequence: Optional[PositiveInt] = Field(
        description="Ranking of the procedure (for each type)",
        default=None,
    )
    code: Optional[CodeableReference] = Field(
        description="The procedure relevant to the account",
        default=None,
    )
    dateOfService: Optional[DateTime] = Field(
        description="Date of the procedure (when coded procedure)",
        default=None,
    )
    type: Optional[ListType[CodeableConcept]] = Field(
        description="How this procedure value should be used in charging the account",
        default=None,
    )
    packageCode: Optional[ListType[CodeableConcept]] = Field(
        description="Package Code specific for billing",
        default=None,
    )
    device: Optional[ListType[Reference]] = Field(
        description="Any devices that were associated with the procedure",
        default=None,
    )

class AccountRelatedAccount(BackboneElement):
    """
    Other associated accounts related to this account.
    """

    relationship: Optional[CodeableConcept] = Field(
        description="Relationship of the associated Account",
        default=None,
    )
    account: Optional[Reference] = Field(
        description="Reference to an associated Account",
        default=None,
    )

class AccountBalance(BackboneElement):
    """
        The calculated account balances - these are calculated and processed by the finance system.

    The balances with a `term` that is not current are usually generated/updated by an invoicing or similar process.
    """

    aggregate: Optional[CodeableConcept] = Field(
        description="Who is expected to pay this part of the balance",
        default=None,
    )
    term: Optional[CodeableConcept] = Field(
        description="current | 30 | 60 | 90 | 120",
        default=None,
    )
    estimate: Optional[Boolean] = Field(
        description="Estimated balance",
        default=None,
    )
    amount: Optional[Money] = Field(
        description="Calculated amount",
        default=None,
    )

class Account(DomainResource):
    """
    A financial tool for tracking value accrued for a particular purpose.  In the healthcare field, used to track charges for a patient, cost centers, etc.
    """

    _abstract = False
    _type = "Account"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Account"

    identifier: Optional[ListType[Identifier]] = Field(
        description="Account number",
        default=None,
    )
    status: Optional[Code] = Field(
        description="active | inactive | entered-in-error | on-hold | unknown",
        default=None,
    )
    billingStatus: Optional[CodeableConcept] = Field(
        description="Tracks the lifecycle of the account through the billing process",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="E.g. patient, expense, depreciation",
        default=None,
    )
    name: Optional[String] = Field(
        description="Human-readable label",
        default=None,
    )
    subject: Optional[ListType[Reference]] = Field(
        description="The entity that caused the expenses",
        default=None,
    )
    servicePeriod: Optional[Period] = Field(
        description="Transaction window",
        default=None,
    )
    coverage: Optional[ListType[AccountCoverage]] = Field(
        description="The party(s) that are responsible for covering the payment of this account, and what order should they be applied to the account",
        default=None,
    )
    owner: Optional[Reference] = Field(
        description="Entity managing the Account",
        default=None,
    )
    description: Optional[Markdown] = Field(
        description="Explanation of purpose/use",
        default=None,
    )
    guarantor: Optional[ListType[AccountGuarantor]] = Field(
        description="The parties ultimately responsible for balancing the Account",
        default=None,
    )
    diagnosis: Optional[ListType[AccountDiagnosis]] = Field(
        description="The ListType of diagnoses relevant to this account",
        default=None,
    )
    procedure: Optional[ListType[AccountProcedure]] = Field(
        description="The ListType of procedures relevant to this account",
        default=None,
    )
    relatedAccount: Optional[ListType[AccountRelatedAccount]] = Field(
        description="Other associated accounts related to this account",
        default=None,
    )
    currency: Optional[CodeableConcept] = Field(
        description="The base or default currency",
        default=None,
    )
    balance: Optional[ListType[AccountBalance]] = Field(
        description="Calculated account balance(s)",
        default=None,
    )
    calculatedAt: Optional[Instant] = Field(
        description="Time the balance amount was calculated",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_act_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("diagnosis",),
            expression="condition.reference.empty().not() implies dateOfDiagnosis.empty()",
            human="The dateOfDiagnosis is not valid when using a reference to a diagnosis",
            key="act-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_act_2_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("procedure",),
            expression="code.reference.empty().not() implies dateOfService.empty()",
            human="The dateOfService is not valid when using a reference to a procedure",
            key="act-2",
            severity="error",
        )
