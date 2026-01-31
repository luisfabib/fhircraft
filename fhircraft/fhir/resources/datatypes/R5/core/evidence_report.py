from pydantic import Field, model_validator
from typing import Optional, List

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    Markdown,
    Boolean,
)

from fhircraft.fhir.resources.datatypes.R5.complex import (
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
    valueBoolean: Optional[Boolean] = Field(
        description="Characteristic value",
        default=None,
    )
    valueBoolean_ext: Optional[Element] = Field(
        description="Placeholder element for valueBoolean extensions",
        default=None,
        alias="_valueBoolean",
    )
    valueQuantity: Optional[Quantity] = Field(
        description="Characteristic value",
        default=None,
    )
    valueRange: Optional[Range] = Field(
        description="Characteristic value",
        default=None,
    )
    exclude: Optional[Boolean] = Field(
        description="Is used to express not the characteristic",
        default=None,
    )
    exclude_ext: Optional[Element] = Field(
        description="Placeholder element for exclude extensions",
        default=None,
        alias="_exclude",
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
            field_types=[Reference, CodeableConcept, Boolean, Quantity, Range],
            field_name_base="value",
            required=True,
        )


class EvidenceReportSubject(BackboneElement):
    """
    Specifies the subject or focus of the report. Answers "What is this report about?".
    """

    characteristic: Optional[List[EvidenceReportSubjectCharacteristic]] = Field(
        description="Characteristic",
        default=None,
    )
    note: Optional[List[Annotation]] = Field(
        description="Footnotes and/or explanatory notes",
        default=None,
    )


class EvidenceReportRelatesToTarget(BackboneElement):
    """
    The target composition/document of this relationship.
    """

    url: Optional[Uri] = Field(
        description="Target of the relationship URL",
        default=None,
    )
    url_ext: Optional[Element] = Field(
        description="Placeholder element for url extensions",
        default=None,
        alias="_url",
    )
    identifier: Optional[Identifier] = Field(
        description="Target of the relationship Identifier",
        default=None,
    )
    display: Optional[Markdown] = Field(
        description="Target of the relationship Display",
        default=None,
    )
    display_ext: Optional[Element] = Field(
        description="Placeholder element for display extensions",
        default=None,
        alias="_display",
    )
    resource: Optional[Reference] = Field(
        description="Target of the relationship Resource reference",
        default=None,
    )


class EvidenceReportRelatesTo(BackboneElement):
    """
    Relationships that this composition has with other compositions or documents that already exist.
    """

    code: Optional[Code] = Field(
        description="replaces | amends | appends | transforms | replacedWith | amendedWith | appendedWith | transformedWith",
        default=None,
    )
    code_ext: Optional[Element] = Field(
        description="Placeholder element for code extensions",
        default=None,
        alias="_code",
    )
    target: Optional[EvidenceReportRelatesToTarget] = Field(
        description="Target of the relationship",
        default=None,
    )


class EvidenceReportSection(BackboneElement):
    """
    The root of the sections that make up the composition.
    """

    title: Optional[String] = Field(
        description="Label for section (e.g. for ToC)",
        default=None,
    )
    title_ext: Optional[Element] = Field(
        description="Placeholder element for title extensions",
        default=None,
        alias="_title",
    )
    focus: Optional[CodeableConcept] = Field(
        description="Classification of section (recommended)",
        default=None,
    )
    focusReference: Optional[Reference] = Field(
        description="Classification of section by Resource",
        default=None,
    )
    author: Optional[List[Reference]] = Field(
        description="Who and/or what authored the section",
        default=None,
    )
    text: Optional[Narrative] = Field(
        description="Text summary of the section, for human interpretation",
        default=None,
    )
    mode: Optional[Code] = Field(
        description="working | snapshot | changes",
        default=None,
    )
    mode_ext: Optional[Element] = Field(
        description="Placeholder element for mode extensions",
        default=None,
        alias="_mode",
    )
    orderedBy: Optional[CodeableConcept] = Field(
        description="Order of section entries",
        default=None,
    )
    entryClassifier: Optional[List[CodeableConcept]] = Field(
        description="Extensible classifiers as content",
        default=None,
    )
    entryReference: Optional[List[Reference]] = Field(
        description="Reference to resources as content",
        default=None,
    )
    entryQuantity: Optional[List[Quantity]] = Field(
        description="Quantity as content",
        default=None,
    )
    emptyReason: Optional[CodeableConcept] = Field(
        description="Why the section is empty",
        default=None,
    )
    section: Optional[List["EvidenceReportSection"]] = Field(
        description="Nested Section",
        default=None,
    )


class EvidenceReport(DomainResource):
    """
    The EvidenceReport Resource is a specialized container for a collection of resources and codeable concepts, adapted to support compositions of Evidence, EvidenceVariable, and Citation resources and related concepts.
    """

    _abstract = False
    _type = "EvidenceReport"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/EvidenceReport"

    url: Optional[Uri] = Field(
        description="Canonical identifier for this EvidenceReport, represented as a globally unique URI",
        default=None,
    )
    url_ext: Optional[Element] = Field(
        description="Placeholder element for url extensions",
        default=None,
        alias="_url",
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
    useContext: Optional[List[UsageContext]] = Field(
        description="The context that the content is intended to support",
        default=None,
    )
    identifier: Optional[List[Identifier]] = Field(
        description="Unique identifier for the evidence report",
        default=None,
    )
    relatedIdentifier: Optional[List[Identifier]] = Field(
        description="Identifiers for articles that may relate to more than one evidence report",
        default=None,
    )
    citeAsReference: Optional[Reference] = Field(
        description="Citation for this report",
        default=None,
    )
    citeAsMarkdown: Optional[Markdown] = Field(
        description="Citation for this report",
        default=None,
    )
    citeAsMarkdown_ext: Optional[Element] = Field(
        description="Placeholder element for citeAsMarkdown extensions",
        default=None,
        alias="_citeAsMarkdown",
    )
    type: Optional[CodeableConcept] = Field(
        description="Kind of report",
        default=None,
    )
    note: Optional[List[Annotation]] = Field(
        description="Used for footnotes and annotations",
        default=None,
    )
    relatedArtifact: Optional[List[RelatedArtifact]] = Field(
        description="Link, description or reference to artifact associated with the report",
        default=None,
    )
    subject: Optional[EvidenceReportSubject] = Field(
        description="Focus of the report",
        default=None,
    )
    publisher: Optional[String] = Field(
        description="Name of the publisher/steward (organization or individual)",
        default=None,
    )
    publisher_ext: Optional[Element] = Field(
        description="Placeholder element for publisher extensions",
        default=None,
        alias="_publisher",
    )
    contact: Optional[List[ContactDetail]] = Field(
        description="Contact details for the publisher",
        default=None,
    )
    author: Optional[List[ContactDetail]] = Field(
        description="Who authored the content",
        default=None,
    )
    editor: Optional[List[ContactDetail]] = Field(
        description="Who edited the content",
        default=None,
    )
    reviewer: Optional[List[ContactDetail]] = Field(
        description="Who reviewed the content",
        default=None,
    )
    endorser: Optional[List[ContactDetail]] = Field(
        description="Who endorsed the content",
        default=None,
    )
    relatesTo: Optional[List[EvidenceReportRelatesTo]] = Field(
        description="Relationships to other compositions/documents",
        default=None,
    )
    section: Optional[List[EvidenceReportSection]] = Field(
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
            field_types=[Reference, Markdown],
            field_name_base="citeAs",
            required=False,
        )

    @model_validator(mode="after")
    def FHIR_cnl_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("url",),
            expression="exists() implies matches('^[^|# ]+$')",
            human="URL should not contain | or # - these characters make processing canonical references problematic",
            key="cnl-1",
            severity="warning",
        )
