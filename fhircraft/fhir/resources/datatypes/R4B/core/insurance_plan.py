import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import String, Uri, Code, PositiveInt

from fhircraft.fhir.resources.datatypes.R4B.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    CodeableConcept,
    Period,
    Reference,
    BackboneElement,
    HumanName,
    ContactPoint,
    Address,
    Quantity,
    Money,
)
from .resource import Resource
from .domain_resource import DomainResource


class InsurancePlanContact(BackboneElement):
    """
    The contact for the health insurance product for a certain purpose.
    """

    purpose: Optional[CodeableConcept] = Field(
        description="The type of contact",
        default=None,
    )
    name: Optional[HumanName] = Field(
        description="A name associated with the contact",
        default=None,
    )
    telecom: Optional[ListType[ContactPoint]] = Field(
        description="Contact details (telephone, email, etc.)  for a contact",
        default=None,
    )
    address: Optional[Address] = Field(
        description="Visiting or postal addresses for the contact",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "address",
                "telecom",
                "name",
                "purpose",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


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

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "code",
                "value",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class InsurancePlanCoverageBenefit(BackboneElement):
    """
    Specific benefits under this type of coverage.
    """

    type: Optional[CodeableConcept] = Field(
        description="Type of benefit",
        default=None,
    )
    requirement: Optional[String] = Field(
        description="Referral requirements",
        default=None,
    )
    requirement_ext: Optional[Element] = Field(
        description="Placeholder element for requirement extensions",
        default=None,
        alias="_requirement",
    )
    limit: Optional[ListType[InsurancePlanCoverageBenefitLimit]] = Field(
        description="Benefit limits",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "limit",
                "requirement",
                "type",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )


class InsurancePlanCoverage(BackboneElement):
    """
    Details about the coverage offered by the insurance product.
    """

    type: Optional[CodeableConcept] = Field(
        description="Type of coverage",
        default=None,
    )
    network: Optional[ListType[Reference]] = Field(
        description="What networks provide coverage",
        default=None,
    )
    benefit: Optional[ListType[InsurancePlanCoverageBenefit]] = Field(
        description="List of benefits",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "benefit",
                "network",
                "type",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )


class InsurancePlanPlanGeneralCost(BackboneElement):
    """
    Overall costs associated with the plan.
    """

    type: Optional[CodeableConcept] = Field(
        description="Type of cost",
        default=None,
    )
    groupSize: Optional[PositiveInt] = Field(
        description="Number of enrollees",
        default=None,
    )
    groupSize_ext: Optional[Element] = Field(
        description="Placeholder element for groupSize extensions",
        default=None,
        alias="_groupSize",
    )
    cost: Optional[Money] = Field(
        description="Cost value",
        default=None,
    )
    comment: Optional[String] = Field(
        description="Additional cost information",
        default=None,
    )
    comment_ext: Optional[Element] = Field(
        description="Placeholder element for comment extensions",
        default=None,
        alias="_comment",
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "comment",
                "cost",
                "groupSize",
                "type",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class InsurancePlanPlanSpecificCostBenefitCost(BackboneElement):
    """
    List of the costs associated with a specific benefit.
    """

    type: Optional[CodeableConcept] = Field(
        description="Type of cost",
        default=None,
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

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "value",
                "qualifiers",
                "applicability",
                "type",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class InsurancePlanPlanSpecificCostBenefit(BackboneElement):
    """
    List of the specific benefits under this category of benefit.
    """

    type: Optional[CodeableConcept] = Field(
        description="Type of specific benefit",
        default=None,
    )
    cost: Optional[ListType[InsurancePlanPlanSpecificCostBenefitCost]] = Field(
        description="List of the costs",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "cost",
                "type",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )


class InsurancePlanPlanSpecificCost(BackboneElement):
    """
    Costs associated with the coverage provided by the product.
    """

    category: Optional[CodeableConcept] = Field(
        description="General category of benefit",
        default=None,
    )
    benefit: Optional[ListType[InsurancePlanPlanSpecificCostBenefit]] = Field(
        description="Benefits list",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "benefit",
                "category",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
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

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "specificCost",
                "generalCost",
                "network",
                "coverageArea",
                "type",
                "identifier",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )


class InsurancePlan(DomainResource):
    """
    Details of a Health Insurance product/plan provided by an organization.
    """

    _abstract = False
    _type = "InsurancePlan"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/InsurancePlan"

    id: Optional[String] = Field(
        description="Logical id of this artifact",
        default=None,
    )
    id_ext: Optional[Element] = Field(
        description="Placeholder element for id extensions",
        default=None,
        alias="_id",
    )
    meta: Optional[Meta] = Field(
        description="Metadata about the resource.",
        default_factory=lambda: Meta(
            profile=["http://hl7.org/fhir/StructureDefinition/InsurancePlan"]
        ),
    )
    implicitRules: Optional[Uri] = Field(
        description="A set of rules under which this content was created",
        default=None,
    )
    implicitRules_ext: Optional[Element] = Field(
        description="Placeholder element for implicitRules extensions",
        default=None,
        alias="_implicitRules",
    )
    language: Optional[Code] = Field(
        description="Language of the resource content",
        default=None,
    )
    language_ext: Optional[Element] = Field(
        description="Placeholder element for language extensions",
        default=None,
        alias="_language",
    )
    text: Optional[Narrative] = Field(
        description="Text summary of the resource, for human interpretation",
        default=None,
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
        description="Business Identifier for Product",
        default=None,
    )
    status: Optional[Code] = Field(
        description="draft | active | retired | unknown",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    type: Optional[ListType[CodeableConcept]] = Field(
        description="Kind of product",
        default=None,
    )
    name: Optional[String] = Field(
        description="Official name",
        default=None,
    )
    name_ext: Optional[Element] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    alias: Optional[ListType[String]] = Field(
        description="Alternate names",
        default=None,
    )
    alias_ext: Optional[Element] = Field(
        description="Placeholder element for alias extensions",
        default=None,
        alias="_alias",
    )
    period: Optional[Period] = Field(
        description="When the product is available",
        default=None,
    )
    ownedBy: Optional[Reference] = Field(
        description="Plan issuer",
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
    contact: Optional[ListType[InsurancePlanContact]] = Field(
        description="Contact for the product",
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
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "plan",
                "coverage",
                "network",
                "endpoint",
                "contact",
                "coverageArea",
                "administeredBy",
                "ownedBy",
                "period",
                "alias",
                "name",
                "type",
                "status",
                "identifier",
                "modifierExtension",
                "extension",
                "text",
                "language",
                "implicitRules",
                "meta",
            ),
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_dom_r4b_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("contained",),
            expression="($this is Citation or $this is Evidence or $this is EvidenceReport or $this is EvidenceVariable or $this is MedicinalProductDefinition or $this is PackagedProductDefinition or $this is AdministrableProductDefinition or $this is Ingredient or $this is ClinicalUseDefinition or $this is RegulatedAuthorization or $this is SubstanceDefinition or $this is SubscriptionStatus or $this is SubscriptionTopic) implies (%resource is Citation or %resource is Evidence or %resource is EvidenceReport or %resource is EvidenceVariable or %resource is MedicinalProductDefinition or %resource is PackagedProductDefinition or %resource is AdministrableProductDefinition or %resource is Ingredient or %resource is ClinicalUseDefinition or %resource is RegulatedAuthorization or %resource is SubstanceDefinition or %resource is SubscriptionStatus or %resource is SubscriptionTopic)",
            human="Containing new R4B resources within R4 resources may cause interoperability issues if instances are shared with R4 systems",
            key="dom-r4b",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_ext_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "modifierExtension",
                "extension",
            ),
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_dom_2_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="contained.contained.empty()",
            human="If the resource is contained in another resource, it SHALL NOT contain nested Resources",
            key="dom-2",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_dom_3_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="contained.where(((id.exists() and ('#'+id in (%resource.descendants().reference | %resource.descendants().ofType(canonical) | %resource.descendants().ofType(uri) | %resource.descendants().ofType(url)))) or descendants().where(reference = '#').exists() or descendants().where(as(canonical) = '#').exists() or descendants().where(as(uri) = '#').exists()).not()).trace('unmatched', id).empty()",
            human="If the resource is contained in another resource, it SHALL be referred to from elsewhere in the resource or SHALL refer to the containing resource",
            key="dom-3",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_dom_4_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="contained.meta.versionId.empty() and contained.meta.lastUpdated.empty()",
            human="If a resource is contained in another resource, it SHALL NOT have a meta.versionId or a meta.lastUpdated",
            key="dom-4",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_dom_5_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="contained.meta.security.empty()",
            human="If a resource is contained in another resource, it SHALL NOT have a security label",
            key="dom-5",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_dom_6_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="text.`div`.exists()",
            human="A resource should have narrative for robust management",
            key="dom-6",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_ipn_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(identifier.count() + name.count()) > 0",
            human="The organization SHALL at least have a name or an idendtifier, and possibly more than one",
            key="ipn-1",
            severity="error",
        )
