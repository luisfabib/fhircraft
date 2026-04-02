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
    ContactDetail,
    UsageContext,
    CodeableConcept,
    Period,
    Reference,
    BackboneElement,
    Money,
)
from .resource import Resource
from .domain_resource import DomainResource

class ChargeItemDefinitionApplicability(BackboneElement):
    """
    Expressions that describe applicability criteria for the billing code.
    """

    description: Optional[String] = Field(
        description="Natural language description of the condition",
        default=None,
    )
    language: Optional[String] = Field(
        description="Language of the expression",
        default=None,
    )

    expression: Optional[String] = Field(
        description="Boolean-valued expression",
        default=None,
    )

class ChargeItemDefinitionPropertyGroupApplicability(BackboneElement):
    """
    Expressions that describe applicability criteria for the priceComponent.
    """

    description: Optional[String] = Field(
        description="Natural language description of the condition",
        default=None,
    )
    language: Optional[String] = Field(
        description="Language of the expression",
        default=None,
    )

    expression: Optional[String] = Field(
        description="Boolean-valued expression",
        default=None,
    )

class ChargeItemDefinitionPropertyGroupPriceComponent(BackboneElement):
    """
    The price for a ChargeItem may be calculated as a base price with surcharges/deductions that apply in certain conditions. A ChargeItemDefinition resource that defines the prices, factors and conditions that apply to a billing code is currently under development. The priceComponent element can be used to offer transparency to the recipient of the Invoice of how the prices have been calculated.
    """

    type: Optional[Code] = Field(
        description="base | surcharge | deduction | discount | tax | informational",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="Code identifying the specific component",
        default=None,
    )
    factor: Optional[Decimal] = Field(
        description="Factor used for calculating this component",
        default=None,
    )
    amount: Optional[Money] = Field(
        description="Monetary amount associated with this component",
        default=None,
    )

class ChargeItemDefinitionPropertyGroup(BackboneElement):
    """
    Group of properties which are applicable under the same conditions. If no applicability rules are established for the group, then all properties always apply.
    """

    applicability: Optional[
        ListType[ChargeItemDefinitionPropertyGroupApplicability]
    ] = Field(
        description="Conditions under which the priceComponent is applicable",
        default=None,
    )
    priceComponent: Optional[
        ListType[ChargeItemDefinitionPropertyGroupPriceComponent]
    ] = Field(
        description="Components of total line item price",
        default=None,
    )

class ChargeItemDefinition(DomainResource):
    """
    The ChargeItemDefinition resource provides the properties that apply to the (billing) codes necessary to calculate costs and prices. The properties may differ largely depending on type and realm, therefore this resource gives only a rough structure and requires profiling for each type of billing code system.
    """

    _abstract = False
    _type = "ChargeItemDefinition"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/ChargeItemDefinition"

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
    url: Optional[Uri] = Field(
        description="Canonical identifier for this charge item definition, represented as a URI (globally unique)",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Additional identifier for the charge item definition",
        default=None,
    )
    version: Optional[String] = Field(
        description="Business version of the charge item definition",
        default=None,
    )
    title: Optional[String] = Field(
        description="Name for this charge item definition (human friendly)",
        default=None,
    )
    derivedFromUri: Optional[ListType[Uri]] = Field(
        description="Underlying externally-defined charge item definition",
        default=None,
    )
    partOf: Optional[ListType[Canonical]] = Field(
        description="A larger definition of which this particular definition is a component or step",
        default=None,
    )
    replaces: Optional[ListType[Canonical]] = Field(
        description="Completed or terminated request(s) whose function is taken by this new request",
        default=None,
    )
    status: Optional[Code] = Field(
        description="draft | active | retired | unknown",
        default=None,
    )
    experimental: Optional[Boolean] = Field(
        description="For testing purposes, not real usage",
        default=None,
    )
    date: Optional[DateTime] = Field(
        description="Date last changed",
        default=None,
    )
    publisher: Optional[String] = Field(
        description="Name of the publisher (organization or individual)",
        default=None,
    )
    contact: Optional[ListType[ContactDetail]] = Field(
        description="Contact details for the publisher",
        default=None,
    )
    description: Optional[Markdown] = Field(
        description="Natural language description of the charge item definition",
        default=None,
    )
    useContext: Optional[ListType[UsageContext]] = Field(
        description="The context that the content is intended to support",
        default=None,
    )
    jurisdiction: Optional[ListType[CodeableConcept]] = Field(
        description="Intended jurisdiction for charge item definition (if applicable)",
        default=None,
    )
    copyright: Optional[Markdown] = Field(
        description="Use and/or publishing restrictions",
        default=None,
    )
    approvalDate: Optional[Date] = Field(
        description="When the charge item definition was approved by publisher",
        default=None,
    )
    lastReviewDate: Optional[Date] = Field(
        description="When the charge item definition was last reviewed",
        default=None,
    )
    effectivePeriod: Optional[Period] = Field(
        description="When the charge item definition is expected to be used",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="Billing codes or product types this definition applies to",
        default=None,
    )
    instance: Optional[ListType[Reference]] = Field(
        description="Instances this definition applies to",
        default=None,
    )
    applicability: Optional[ListType[ChargeItemDefinitionApplicability]] = Field(
        description="Whether or not the billing code is applicable",
        default=None,
    )
    propertyGroup: Optional[ListType[ChargeItemDefinitionPropertyGroup]] = Field(
        description="Group of properties which are applicable under the same conditions",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_cid_0_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.exists() implies name.matches('[A-Z]([A-Za-z0-9_]){0,254}')",
            human="Name should be usable as an identifier for the module by machine processing applications such as code generation",
            key="cid-0",
            severity="warning",
        )
