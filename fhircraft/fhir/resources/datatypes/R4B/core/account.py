import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from ..primitive import *

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
)
from .resource import Resource
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

class Account(DomainResource):
    """
    A financial tool for tracking value accrued for a particular purpose.  In the healthcare field, used to track charges for a patient, cost centers, etc.
    """

    _abstract = False
    _type = "Account"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Account"

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
        description="Account number",
        default=None,
    )
    status: Optional[Code] = Field(
        description="active | inactive | entered-in-error | on-hold | unknown",
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
    description: Optional[String] = Field(
        description="Explanation of purpose/use",
        default=None,
    )
    guarantor: Optional[ListType[AccountGuarantor]] = Field(
        description="The parties ultimately responsible for balancing the Account",
        default=None,
    )
    partOf: Optional[Reference] = Field(
        description="Reference to a parent Account",
        default=None,
    )
