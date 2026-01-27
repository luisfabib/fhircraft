import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import String, Uri, Code, Markdown

from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    ContactDetail,
    RelatedArtifact,
    Period,
    BackboneElement,
    Annotation,
)
from .resource import Resource
from .domain_resource import DomainResource


class ResearchStudyArm(BackboneElement):
    """
    Describes an expected sequence of events for one of the participants of a study.  E.g. Exposure to drug A, wash-out, exposure to drug B, wash-out, follow-up.
    """

    name: Optional[String] = Field(
        description="Label for study arm",
        default=None,
    )
    name_ext: Optional[Element] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    type: Optional[CodeableConcept] = Field(
        description="Categorization of study arm",
        default=None,
    )
    description: Optional[String] = Field(
        description="Short explanation of study path",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "description",
                "type",
                "name",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class ResearchStudyObjective(BackboneElement):
    """
    A goal that the study is aiming to achieve in terms of a scientific question to be answered by the analysis of data collected during the study.
    """

    name: Optional[String] = Field(
        description="Label for the objective",
        default=None,
    )
    name_ext: Optional[Element] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    type: Optional[CodeableConcept] = Field(
        description="primary | secondary | exploratory",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "type",
                "name",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class ResearchStudy(DomainResource):
    """
    A process where a researcher or organization plans and then executes a series of steps intended to increase the field of healthcare-related knowledge.  This includes studies of safety, efficacy, comparative effectiveness and other information about medications, devices, therapies and other interventional and investigative techniques.  A ResearchStudy involves the gathering of information about human or animal subjects.
    """

    _abstract = False
    _type = "ResearchStudy"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/ResearchStudy"

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
            profile=["http://hl7.org/fhir/StructureDefinition/ResearchStudy"]
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
        description="Business Identifier for study",
        default=None,
    )
    title: Optional[String] = Field(
        description="Name for this study",
        default=None,
    )
    title_ext: Optional[Element] = Field(
        description="Placeholder element for title extensions",
        default=None,
        alias="_title",
    )
    protocol: Optional[ListType[Reference]] = Field(
        description="Steps followed in executing study",
        default=None,
    )
    partOf: Optional[ListType[Reference]] = Field(
        description="Part of larger study",
        default=None,
    )
    status: Optional[Code] = Field(
        description="active | administratively-completed | approved | closed-to-accrual | closed-to-accrual-and-intervention | completed | disapproved | in-review | temporarily-closed-to-accrual | temporarily-closed-to-accrual-and-intervention | withdrawn",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    primaryPurposeType: Optional[CodeableConcept] = Field(
        description="treatment | prevention | diagnostic | supportive-care | screening | health-services-research | basic-science | device-feasibility",
        default=None,
    )
    phase: Optional[CodeableConcept] = Field(
        description="n-a | early-phase-1 | phase-1 | phase-1-phase-2 | phase-2 | phase-2-phase-3 | phase-3 | phase-4",
        default=None,
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description="Classifications for the study",
        default=None,
    )
    focus: Optional[ListType[CodeableConcept]] = Field(
        description="Drugs, devices, etc. under study",
        default=None,
    )
    condition: Optional[ListType[CodeableConcept]] = Field(
        description="Condition being studied",
        default=None,
    )
    contact: Optional[ListType[ContactDetail]] = Field(
        description="Contact details for the study",
        default=None,
    )
    relatedArtifact: Optional[ListType[RelatedArtifact]] = Field(
        description="References and dependencies",
        default=None,
    )
    keyword: Optional[ListType[CodeableConcept]] = Field(
        description="Used to search for the study",
        default=None,
    )
    location: Optional[ListType[CodeableConcept]] = Field(
        description="Geographic region(s) for study",
        default=None,
    )
    description: Optional[Markdown] = Field(
        description="What this is study doing",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    enrollment: Optional[ListType[Reference]] = Field(
        description="Inclusion \u0026 exclusion criteria",
        default=None,
    )
    period: Optional[Period] = Field(
        description="When the study began and ended",
        default=None,
    )
    sponsor: Optional[Reference] = Field(
        description="Organization that initiates and is legally responsible for the study",
        default=None,
    )
    principalInvestigator: Optional[Reference] = Field(
        description="Researcher who oversees multiple aspects of the study",
        default=None,
    )
    site: Optional[ListType[Reference]] = Field(
        description="Facility where study activities are conducted",
        default=None,
    )
    reasonStopped: Optional[CodeableConcept] = Field(
        description="accrual-goal-met | closed-due-to-toxicity | closed-due-to-lack-of-study-progress | temporarily-closed-per-study-design",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Comments made about the study",
        default=None,
    )
    arm: Optional[ListType[ResearchStudyArm]] = Field(
        description="Defined path through the study for a subject",
        default=None,
    )
    objective: Optional[ListType[ResearchStudyObjective]] = Field(
        description="A goal for the study",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "objective",
                "arm",
                "note",
                "reasonStopped",
                "site",
                "principalInvestigator",
                "sponsor",
                "period",
                "enrollment",
                "description",
                "location",
                "keyword",
                "relatedArtifact",
                "contact",
                "condition",
                "focus",
                "category",
                "phase",
                "primaryPurposeType",
                "status",
                "partOf",
                "protocol",
                "title",
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
            expression="contained.where((('#'+id in (%resource.descendants().reference | %resource.descendants().ofType(canonical) | %resource.descendants().ofType(uri) | %resource.descendants().ofType(url))) or descendants().where(reference = '#').exists() or descendants().where(as(canonical) = '#').exists() or descendants().where(as(canonical) = '#').exists()).not()).trace('unmatched', id).empty()",
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
