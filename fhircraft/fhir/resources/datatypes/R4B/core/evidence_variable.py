import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    DateTime,
    Markdown,
    Boolean,
    Canonical,
)

from fhircraft.fhir.resources.datatypes.R4B.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Annotation,
    UsageContext,
    ContactDetail,
    RelatedArtifact,
    BackboneElement,
    Reference,
    CodeableConcept,
    Expression,
    Quantity,
    Range,
)
from .resource import Resource
from .domain_resource import DomainResource


class EvidenceVariableCharacteristicTimeFromStart(BackboneElement):
    """
    Indicates duration, period, or point of observation from the participant's study entry.
    """

    description: Optional[String] = Field(
        description="Human readable description",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    quantity: Optional[Quantity] = Field(
        description="Used to express the observation at a defined amount of time after the study start",
        default=None,
    )
    range: Optional[Range] = Field(
        description="Used to express the observation within a period after the study start",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Used for footnotes or explanatory notes",
        default=None,
    )


class EvidenceVariableCharacteristic(BackboneElement):
    """
    A characteristic that defines the members of the evidence element. Multiple characteristics are applied with "and" semantics.
    """

    description: Optional[String] = Field(
        description="Natural language description of the characteristic",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    definitionReference: Optional[Reference] = Field(
        description="What code or expression defines members?",
        default=None,
    )
    definitionCanonical: Optional[Canonical] = Field(
        description="What code or expression defines members?",
        default=None,
    )
    definitionCanonical_ext: Optional[Element] = Field(
        description="Placeholder element for definitionCanonical extensions",
        default=None,
        alias="_definitionCanonical",
    )
    definitionCodeableConcept: Optional[CodeableConcept] = Field(
        description="What code or expression defines members?",
        default=None,
    )
    definitionExpression: Optional[Expression] = Field(
        description="What code or expression defines members?",
        default=None,
    )
    method: Optional[CodeableConcept] = Field(
        description="Method used for describing characteristic",
        default=None,
    )
    device: Optional[Reference] = Field(
        description="Device used for determining characteristic",
        default=None,
    )
    exclude: Optional[Boolean] = Field(
        description="Whether the characteristic includes or excludes members",
        default=None,
    )
    exclude_ext: Optional[Element] = Field(
        description="Placeholder element for exclude extensions",
        default=None,
        alias="_exclude",
    )
    timeFromStart: Optional[EvidenceVariableCharacteristicTimeFromStart] = Field(
        description="Observation time from study start",
        default=None,
    )
    groupMeasure: Optional[Code] = Field(
        description="mean | median | mean-of-mean | mean-of-median | median-of-mean | median-of-median",
        default=None,
    )
    groupMeasure_ext: Optional[Element] = Field(
        description="Placeholder element for groupMeasure extensions",
        default=None,
        alias="_groupMeasure",
    )

    @property
    def definition(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="definition",
        )

    @model_validator(mode="after")
    def definition_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Reference, Canonical, CodeableConcept, Expression],
            field_name_base="definition",
            required=True,
        )


class EvidenceVariableCategory(BackboneElement):
    """
    A grouping (or set of values) described along with other groupings to specify the set of groupings allowed for the variable.
    """

    name: Optional[String] = Field(
        description="Description of the grouping",
        default=None,
    )
    name_ext: Optional[Element] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    valueCodeableConcept: Optional[CodeableConcept] = Field(
        description="Definition of the grouping",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="Definition of the grouping",
        default=None,
    )
    valueRange: Optional[Range] = Field(
        description="Definition of the grouping",
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
            field_types=[CodeableConcept, Quantity, Range],
            field_name_base="value",
            required=False,
        )


class EvidenceVariable(DomainResource):
    """
    The EvidenceVariable resource describes an element that knowledge (Evidence) is about.
    """

    _abstract = False
    _type = "EvidenceVariable"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/EvidenceVariable"

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
        description="Canonical identifier for this evidence variable, represented as a URI (globally unique)",
        default=None,
    )
    url_ext: Optional[Element] = Field(
        description="Placeholder element for url extensions",
        default=None,
        alias="_url",
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Additional identifier for the evidence variable",
        default=None,
    )
    version: Optional[String] = Field(
        description="Business version of the evidence variable",
        default=None,
    )
    version_ext: Optional[Element] = Field(
        description="Placeholder element for version extensions",
        default=None,
        alias="_version",
    )
    name: Optional[String] = Field(
        description="Name for this evidence variable (computer friendly)",
        default=None,
    )
    name_ext: Optional[Element] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    title: Optional[String] = Field(
        description="Name for this evidence variable (human friendly)",
        default=None,
    )
    title_ext: Optional[Element] = Field(
        description="Placeholder element for title extensions",
        default=None,
        alias="_title",
    )
    shortTitle: Optional[String] = Field(
        description="Title for use in informal contexts",
        default=None,
    )
    shortTitle_ext: Optional[Element] = Field(
        description="Placeholder element for shortTitle extensions",
        default=None,
        alias="_shortTitle",
    )
    subtitle: Optional[String] = Field(
        description="Subordinate title of the EvidenceVariable",
        default=None,
    )
    subtitle_ext: Optional[Element] = Field(
        description="Placeholder element for subtitle extensions",
        default=None,
        alias="_subtitle",
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
    date: Optional[DateTime] = Field(
        description="Date last changed",
        default=None,
    )
    date_ext: Optional[Element] = Field(
        description="Placeholder element for date extensions",
        default=None,
        alias="_date",
    )
    description: Optional[Markdown] = Field(
        description="Natural language description of the evidence variable",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Used for footnotes or explanatory notes",
        default=None,
    )
    useContext: Optional[ListType[UsageContext]] = Field(
        description="The context that the content is intended to support",
        default=None,
    )
    publisher: Optional[String] = Field(
        description="Name of the publisher (organization or individual)",
        default=None,
    )
    publisher_ext: Optional[Element] = Field(
        description="Placeholder element for publisher extensions",
        default=None,
        alias="_publisher",
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
    relatedArtifact: Optional[ListType[RelatedArtifact]] = Field(
        description="Additional documentation, citations, etc.",
        default=None,
    )
    actual: Optional[Boolean] = Field(
        description="Actual or conceptual",
        default=None,
    )
    actual_ext: Optional[Element] = Field(
        description="Placeholder element for actual extensions",
        default=None,
        alias="_actual",
    )
    characteristicCombination: Optional[Code] = Field(
        description="intersection | union",
        default=None,
    )
    characteristicCombination_ext: Optional[Element] = Field(
        description="Placeholder element for characteristicCombination extensions",
        default=None,
        alias="_characteristicCombination",
    )
    characteristic: Optional[ListType[EvidenceVariableCharacteristic]] = Field(
        description="What defines the members of the evidence element",
        default=None,
    )
    handling: Optional[Code] = Field(
        description="continuous | dichotomous | ordinal | polychotomous",
        default=None,
    )
    handling_ext: Optional[Element] = Field(
        description="Placeholder element for handling extensions",
        default=None,
        alias="_handling",
    )
    category: Optional[ListType[EvidenceVariableCategory]] = Field(
        description="A grouping for ordinal or polychotomous variables",
        default=None,
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
