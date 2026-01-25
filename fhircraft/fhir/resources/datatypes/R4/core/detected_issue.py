import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import String, Uri, Code, DateTime

from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    BackboneElement,
    Period,
)
from .resource import Resource
from .domain_resource import DomainResource


class DetectedIssueEvidence(BackboneElement):
    """
    Supporting evidence or manifestations that provide the basis for identifying the detected issue such as a GuidanceResponse or MeasureReport.
    """

    code: Optional[ListType[CodeableConcept]] = Field(
        description="Manifestation",
        default=None,
    )
    detail: Optional[ListType[Reference]] = Field(
        description="Supporting information",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "detail",
                "code",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class DetectedIssueMitigation(BackboneElement):
    """
    Indicates an action that has been taken or is committed to reduce or eliminate the likelihood of the risk identified by the detected issue from manifesting.  Can also reflect an observation of known mitigating factors that may reduce/eliminate the need for any action.
    """

    action: Optional[CodeableConcept] = Field(
        description="What mitigation?",
        default=None,
    )
    date: Optional[DateTime] = Field(
        description="Date committed",
        default=None,
    )
    date_ext: Optional[Element] = Field(
        description="Placeholder element for date extensions",
        default=None,
        alias="_date",
    )
    author: Optional[Reference] = Field(
        description="Who is committing?",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "author",
                "date",
                "action",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class DetectedIssue(DomainResource):
    """
    Indicates an actual or potential clinical issue with or between one or more active or proposed clinical actions for a patient; e.g. Drug-drug interaction, Ineffective treatment frequency, Procedure-condition conflict, etc.
    """

    _abstract = False
    _type = "DetectedIssue"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/DetectedIssue"

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
            profile=["http://hl7.org/fhir/StructureDefinition/DetectedIssue"]
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
        description="Unique id for the detected issue",
        default=None,
    )
    status: Optional[Code] = Field(
        description="registered | preliminary | final | amended +",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    code: Optional[CodeableConcept] = Field(
        description="Issue Category, e.g. drug-drug, duplicate therapy, etc.",
        default=None,
    )
    severity: Optional[Code] = Field(
        description="high | moderate | low",
        default=None,
    )
    severity_ext: Optional[Element] = Field(
        description="Placeholder element for severity extensions",
        default=None,
        alias="_severity",
    )
    patient: Optional[Reference] = Field(
        description="Associated patient",
        default=None,
    )
    identifiedDateTime: Optional[DateTime] = Field(
        description="When identified",
        default=None,
    )
    identifiedDateTime_ext: Optional[Element] = Field(
        description="Placeholder element for identifiedDateTime extensions",
        default=None,
        alias="_identifiedDateTime",
    )
    identifiedPeriod: Optional[Period] = Field(
        description="When identified",
        default=None,
    )
    author: Optional[Reference] = Field(
        description="The provider or device that identified the issue",
        default=None,
    )
    implicated: Optional[ListType[Reference]] = Field(
        description="Problem resource",
        default=None,
    )
    evidence: Optional[ListType[DetectedIssueEvidence]] = Field(
        description="Supporting evidence",
        default=None,
    )
    detail: Optional[String] = Field(
        description="Description and context",
        default=None,
    )
    detail_ext: Optional[Element] = Field(
        description="Placeholder element for detail extensions",
        default=None,
        alias="_detail",
    )
    reference: Optional[Uri] = Field(
        description="Authority for issue",
        default=None,
    )
    reference_ext: Optional[Element] = Field(
        description="Placeholder element for reference extensions",
        default=None,
        alias="_reference",
    )
    mitigation: Optional[ListType[DetectedIssueMitigation]] = Field(
        description="Step taken to address",
        default=None,
    )

    @property
    def identified(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="identified",
        )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "mitigation",
                "reference",
                "detail",
                "evidence",
                "implicated",
                "author",
                "patient",
                "severity",
                "code",
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
    def identified_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[DateTime, Period],
            field_name_base="identified",
            required=False,
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
