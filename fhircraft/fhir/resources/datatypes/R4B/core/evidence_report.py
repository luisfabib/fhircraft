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
    UsageContext,
    Identifier,
    Reference,
    CodeableConcept,
    Annotation,
    RelatedArtifact,
    BackboneElement,
    Quantity,
    Range,
    Period,
    ContactDetail,
)
from .resource import Resource
from .domain_resource import DomainResource


class EvidenceReportSubjectCharacteristic(BackboneElement):
    """
    Characteristic.
    """

    code: Optional[CodeableConcept] = Field(
        description="Characteristic code",
        default=None,
    )
    valueReference: Optional[Reference] = Field(
        description="Characteristic value",
        default=None,
    )
    valueCodeableConcept: Optional[CodeableConcept] = Field(
        description="Characteristic value",
        default=None,
    )
    valueBoolean: Optional[fhir.boolean] = Field(
        description="Characteristic value",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="Characteristic value",
        default=None,
    )
    valueRange: Optional[Range] = Field(
        description="Characteristic value",
        default=None,
    )
    exclude: Optional[fhir.boolean] = Field(
        description="Is used to express not the characteristic",
        default=None,
    )
    period: Optional[Period] = Field(
        description="Timeframe for the characteristic",
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
            field_types=[Reference, CodeableConcept, fhir.Boolean, Quantity, Range],
            field_name_base="value",
            required=True,
        )


class EvidenceReportSubject(BackboneElement):
    """
    Specifies the subject or focus of the report. Answers "What is this report about?".
    """

    characteristic: Optional[ListType[EvidenceReportSubjectCharacteristic]] = Field(
        description="Characteristic",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Footnotes and/or explanatory notes",
        default=None,
    )


class EvidenceReportRelatesTo(BackboneElement):
    """
    Relationships that this composition has with other compositions or documents that already exist.
    """

    code: Optional[fhir.code] = Field(
        description="replaces | amends | appends | transforms | replacedWith | amendedWith | appendedWith | transformedWith",
        default=None,
    )
    targetIdentifier: Optional[Identifier] = Field(
        description="Target of the relationship",
        default=None,
    )
    targetReference: Optional[Reference] = Field(
        description="Target of the relationship",
        default=None,
    )

    @property
    def target(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="target",
        )

    @model_validator(mode="after")
    def target_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Identifier, Reference],
            field_name_base="target",
            required=True,
        )


class EvidenceReportSection(BackboneElement):
    """
    The root of the sections that make up the composition.
    """

    title: Optional[fhir.string] = Field(
        description="Label for section (e.g. for ToC)",
        default=None,
    )
    focus: Optional[CodeableConcept] = Field(
        description="Classification of section (recommended)",
        default=None,
    )
    focusReference: Optional[Reference] = Field(
        description="Classification of section by Resource",
        default=None,
    )
    author: Optional[ListType[Reference]] = Field(
        description="Who and/or what authored the section",
        default=None,
    )
    text: Optional[Narrative] = Field(
        description="Text summary of the section, for human interpretation",
        default=None,
    )
    mode: Optional[fhir.code] = Field(
        description="working | snapshot | changes",
        default=None,
    )
    orderedBy: Optional[CodeableConcept] = Field(
        description="Order of section entries",
        default=None,
    )
    entryClassifier: Optional[ListType[CodeableConcept]] = Field(
        description="Extensible classifiers as content",
        default=None,
    )
    entryReference: Optional[ListType[Reference]] = Field(
        description="Reference to resources as content",
        default=None,
    )
    entryQuantity: Optional[ListType[Quantity]] = Field(
        description="Quantity as content",
        default=None,
    )
    emptyReason: Optional[CodeableConcept] = Field(
        description="Why the section is empty",
        default=None,
    )
    section: Optional[ListType["EvidenceReportSection"]] = Field(
        description="Nested Section",
        default=None,
    )


class EvidenceReport(DomainResource):
    """
    The EvidenceReport Resource is a specialized container for a collection of resources and codable concepts, adapted to support compositions of Evidence, EvidenceVariable, and Citation resources and related concepts.
    """

    _abstract = False
    _type = "EvidenceReport"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/EvidenceReport"

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
    url: Optional[fhir.uri] = Field(
        description="canonical identifier for this EvidenceReport, represented as a globally unique URI",
        default=None,
    )
    status: Optional[fhir.code] = Field(
        description="draft | active | retired | unknown",
        default=None,
    )
    useContext: Optional[ListType[UsageContext]] = Field(
        description="The context that the content is intended to support",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Unique identifier for the evidence report",
        default=None,
    )
    relatedIdentifier: Optional[ListType[Identifier]] = Field(
        description="Identifiers for articles that may relate to more than one evidence report",
        default=None,
    )
    citeAsReference: Optional[Reference] = Field(
        description="Citation for this report",
        default=None,
    )
    citeAsMarkdown: Optional[fhir.markdown] = Field(
        description="Citation for this report",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Kind of report",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Used for footnotes and annotations",
        default=None,
    )
    relatedArtifact: Optional[ListType[RelatedArtifact]] = Field(
        description="Link, description or reference to artifact associated with the report",
        default=None,
    )
    subject: Optional[EvidenceReportSubject] = Field(
        description="Focus of the report",
        default=None,
    )
    publisher: Optional[fhir.string] = Field(
        description="Name of the publisher (organization or individual)",
        default=None,
    )
    contact: Optional[ListType[ContactDetail]] = Field(
        description="Contact details for the publisher",
        default=None,
    )
    author: Optional[ListType[ContactDetail]] = Field(
        description="Who authored the content",
        default=None,
    )
    editor: Optional[ListType[ContactDetail]] = Field(
        description="Who edited the content",
        default=None,
    )
    reviewer: Optional[ListType[ContactDetail]] = Field(
        description="Who reviewed the content",
        default=None,
    )
    endorser: Optional[ListType[ContactDetail]] = Field(
        description="Who endorsed the content",
        default=None,
    )
    relatesTo: Optional[ListType[EvidenceReportRelatesTo]] = Field(
        description="Relationships to other compositions/documents",
        default=None,
    )
    section: Optional[ListType[EvidenceReportSection]] = Field(
        description="Composition is broken into sections",
        default=None,
    )

    @property
    def citeAs(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="citeAs",
        )

    @model_validator(mode="after")
    def citeAs_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Reference, fhir.Markdown],
            field_name_base="citeAs",
            required=False,
        )

    @model_validator(mode="after")
    def FHIR_cnl_0_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.exists() implies name.matches('[A-Z]([A-Za-z0-9_]){0,254}')",
            human="Name should be usable as an identifier for the module by machine processing applications such as code generation",
            key="cnl-0",
            severity="warning",
        )
