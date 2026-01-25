import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import String, Uri, Code, Boolean

from fhircraft.fhir.resources.datatypes.R4B.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Period,
    Reference,
    CodeableConcept,
    ContactPoint,
)
from .resource import Resource
from .domain_resource import DomainResource


class OrganizationAffiliation(DomainResource):
    """
    Defines an affiliation/assotiation/relationship between 2 distinct oganizations, that is not a part-of relationship/sub-division relationship.
    """

    _abstract = False
    _type = "OrganizationAffiliation"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/OrganizationAffiliation"

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
            profile=["http://hl7.org/fhir/StructureDefinition/OrganizationAffiliation"]
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
        description="Business identifiers that are specific to this role",
        default=None,
    )
    active: Optional[Boolean] = Field(
        description="Whether this organization affiliation record is in active use",
        default=None,
    )
    active_ext: Optional[Element] = Field(
        description="Placeholder element for active extensions",
        default=None,
        alias="_active",
    )
    period: Optional[Period] = Field(
        description="The period during which the participatingOrganization is affiliated with the primary organization",
        default=None,
    )
    organization: Optional[Reference] = Field(
        description="Organization where the role is available",
        default=None,
    )
    participatingOrganization: Optional[Reference] = Field(
        description="Organization that provides/performs the role (e.g. providing services or is a member of)",
        default=None,
    )
    network: Optional[ListType[Reference]] = Field(
        description="Health insurance provider network in which the participatingOrganization provides the role\u0027s services (if defined) at the indicated locations (if defined)",
        default=None,
    )
    code: Optional[ListType[CodeableConcept]] = Field(
        description="Definition of the role the participatingOrganization plays",
        default=None,
    )
    specialty: Optional[ListType[CodeableConcept]] = Field(
        description="Specific specialty of the participatingOrganization in the context of the role",
        default=None,
    )
    location: Optional[ListType[Reference]] = Field(
        description="The location(s) at which the role occurs",
        default=None,
    )
    healthcareService: Optional[ListType[Reference]] = Field(
        description="Healthcare services provided through the role",
        default=None,
    )
    telecom: Optional[ListType[ContactPoint]] = Field(
        description="Contact details at the participatingOrganization relevant to this Affiliation",
        default=None,
    )
    endpoint: Optional[ListType[Reference]] = Field(
        description="Technical endpoints providing access to services operated for this role",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "endpoint",
                "telecom",
                "healthcareService",
                "location",
                "specialty",
                "code",
                "network",
                "participatingOrganization",
                "organization",
                "period",
                "active",
                "identifier",
                "modifierExtension",
                "extension",
                "text",
                "language",
                "implicitRules",
                "meta",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
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
