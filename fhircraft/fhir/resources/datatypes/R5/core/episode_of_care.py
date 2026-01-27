from pydantic import Field, model_validator
from typing import Optional, List

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from fhircraft.fhir.resources.datatypes.primitives import String, Uri, Code

from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    BackboneElement,
    Period,
    CodeableConcept,
    CodeableReference,
    Reference,
)
from .resource import Resource
from .domain_resource import DomainResource


class EpisodeOfCareStatusHistory(BackboneElement):
    """
    The history of statuses that the EpisodeOfCare has been through (without requiring processing the history of the resource).
    """

    status: Optional[Code] = Field(
        description="planned | waitlist | active | onhold | finished | cancelled | entered-in-error",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    period: Optional[Period] = Field(
        description="Duration the EpisodeOfCare was in the specified status",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "period",
                "status",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class EpisodeOfCareReason(BackboneElement):
    """
    The list of medical reasons that are expected to be addressed during the episode of care.
    """

    use: Optional[CodeableConcept] = Field(
        description="What the reason value should be used for/as",
        default=None,
    )
    value: Optional[List[CodeableReference]] = Field(
        description="Medical reason to be addressed",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "value",
                "use",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class EpisodeOfCareDiagnosis(BackboneElement):
    """
    The list of medical conditions that were addressed during the episode of care.
    """

    condition: Optional[List[CodeableReference]] = Field(
        description="The medical condition that was addressed during the episode of care",
        default=None,
    )
    use: Optional[CodeableConcept] = Field(
        description="Role that this diagnosis has within the episode of care (e.g. admission, billing, discharge \u2026)",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "use",
                "condition",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class EpisodeOfCare(DomainResource):
    """
    An association between a patient and an organization / healthcare provider(s) during which time encounters may occur. The managing organization assumes a level of responsibility for the patient during this time.
    """

    _abstract = False
    _type = "EpisodeOfCare"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/EpisodeOfCare"

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
            profile=["http://hl7.org/fhir/StructureDefinition/EpisodeOfCare"]
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
    contained: Optional[List[Resource]] = Field(
        description="Contained, inline Resources",
        default=None,
    )
    extension: Optional[List[Extension]] = Field(
        description="Additional content defined by implementations",
        default=None,
    )
    modifierExtension: Optional[List[Extension]] = Field(
        description="Extensions that cannot be ignored",
        default=None,
    )
    identifier: Optional[List[Identifier]] = Field(
        description="Business Identifier(s) relevant for this EpisodeOfCare",
        default=None,
    )
    status: Optional[Code] = Field(
        description="planned | waitlist | active | onhold | finished | cancelled | entered-in-error",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    statusHistory: Optional[List[EpisodeOfCareStatusHistory]] = Field(
        description="Past list of status codes (the current status may be included to cover the start date of the status)",
        default=None,
    )
    type: Optional[List[CodeableConcept]] = Field(
        description="Type/class  - e.g. specialist referral, disease management",
        default=None,
    )
    reason: Optional[List[EpisodeOfCareReason]] = Field(
        description="The list of medical reasons that are expected to be addressed during the episode of care",
        default=None,
    )
    diagnosis: Optional[List[EpisodeOfCareDiagnosis]] = Field(
        description="The list of medical conditions that were addressed during the episode of care",
        default=None,
    )
    patient: Optional[Reference] = Field(
        description="The patient who is the focus of this episode of care",
        default=None,
    )
    managingOrganization: Optional[Reference] = Field(
        description="Organization that assumes responsibility for care coordination",
        default=None,
    )
    period: Optional[Period] = Field(
        description="Interval during responsibility is assumed",
        default=None,
    )
    referralRequest: Optional[List[Reference]] = Field(
        description="Originating Referral Request(s)",
        default=None,
    )
    careManager: Optional[Reference] = Field(
        description="Care manager/care coordinator for the patient",
        default=None,
    )
    careTeam: Optional[List[Reference]] = Field(
        description="Other practitioners facilitating this episode of care",
        default=None,
    )
    account: Optional[List[Reference]] = Field(
        description="The set of accounts that may be used for billing for this EpisodeOfCare",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "account",
                "careTeam",
                "careManager",
                "referralRequest",
                "period",
                "managingOrganization",
                "patient",
                "diagnosis",
                "reason",
                "type",
                "statusHistory",
                "status",
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
            expression="contained.where((('#'+id in (%resource.descendants().reference | %resource.descendants().ofType(canonical) | %resource.descendants().ofType(uri) | %resource.descendants().ofType(url))) or descendants().where(reference = '#').exists() or descendants().where(ofType(canonical) = '#').exists() or descendants().where(ofType(canonical) = '#').exists()).not()).trace('unmatched', id).empty()",
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
