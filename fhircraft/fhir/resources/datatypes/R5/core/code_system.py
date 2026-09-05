from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators


import fhircraft.fhir.resources.datatypes.R5.primitive as fhir
from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Coding,
    ContactDetail,
    UsageContext,
    CodeableConcept,
    Period,
    RelatedArtifact,
    BackboneElement,
)
from .resource import Resource
from .domain_resource import DomainResource


class CodeSystemFilter(BackboneElement):
    """
    A filter that can be used in a value set compose statement when selecting concepts using a filter.
    """

    code: fhir.code = Field(
        description="code that identifies the filter",
    )
    description: Optional[fhir.string] = Field(
        description="How or why the filter is used",
        default=None,
    )
    operator: ListType[fhir.code] = Field(
        description="= | is-a | descendent-of | is-not-a | regex | in | not-in | generalizes | child-of | descendent-leaf | exists",
        min_length=1,
    )
    value: fhir.string = Field(
        description="What to use for the value",
    )


class CodeSystemProperty(BackboneElement):
    """
    A property defines an additional slot through which additional information can be provided about a concept.
    """

    code: fhir.code = Field(
        description="Identifies the property on the concepts, and when referred to in operations",
    )
    uri: Optional[fhir.uri] = Field(
        description="Formal identifier for the property",
        default=None,
    )
    description: Optional[fhir.string] = Field(
        description="Why the property is defined, and/or what it conveys",
        default=None,
    )
    type: fhir.code = Field(
        description="code | Coding | string | integer | boolean | dateTime | decimal",
    )


class CodeSystemConceptDesignation(BackboneElement):
    """
    Additional representations for the concept - other languages, aliases, specialized purposes, used for particular purposes, etc.
    """

    language: Optional[fhir.code] = Field(
        description="Human language of the designation",
        default=None,
    )

    use: Optional[Coding] = Field(
        description="Details how this designation would be used",
        default=None,
    )
    additionalUse: Optional[ListType[Coding]] = Field(
        description="Additional ways how this designation would be used",
        default=None,
    )
    value: fhir.string = Field(
        description="The text value for this designation",
    )


class CodeSystemConceptProperty(BackboneElement):
    """
    A property value for this concept.
    """

    code: fhir.code = Field(
        description="Reference to CodeSystem.property.code",
    )
    valueCode: Optional[fhir.code] = Field(
        description="Value of the property for this concept",
        default=None,
    )
    valueCoding: Optional[Coding] = Field(
        description="Value of the property for this concept",
        default=None,
    )
    valueString: Optional[fhir.string] = Field(
        description="Value of the property for this concept",
        default=None,
    )
    valueInteger: Optional[fhir.integer] = Field(
        description="Value of the property for this concept",
        default=None,
    )
    valueBoolean: Optional[fhir.boolean] = Field(
        description="Value of the property for this concept",
        default=None,
    )
    valueDateTime: Optional[fhir.dateTime] = Field(
        description="Value of the property for this concept",
        default=None,
    )
    valueDecimal: Optional[fhir.decimal] = Field(
        description="Value of the property for this concept",
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
            field_types=[
                fhir.Code,
                Coding,
                fhir.String,
                fhir.Integer,
                fhir.Boolean,
                fhir.DateTime,
                fhir.Decimal,
            ],
            field_name_base="value",
            required=True,
        )


class CodeSystemConcept(BackboneElement):
    """
    Concepts that are in the code system. The concept definitions are inherently hierarchical, but the definitions must be consulted to determine what the meanings of the hierarchical relationships are.
    """

    code: fhir.code = Field(
        description="code that identifies concept",
    )
    display: Optional[fhir.string] = Field(
        description="Text to display to the user",
        default=None,
    )
    definition: Optional[fhir.string] = Field(
        description="Formal definition",
        default=None,
    )
    designation: Optional[ListType[CodeSystemConceptDesignation]] = Field(
        description="Additional representations for the concept",
        default=None,
    )
    property_: Optional[ListType[CodeSystemConceptProperty]] = Field(
        description="Property value for the concept",
        default=None,
        alias="property",
    )
    concept: Optional[ListType["CodeSystemConcept"]] = Field(
        description="Child Concepts (is-a/contains/categorizes)",
        default=None,
    )


class CodeSystem(DomainResource):
    """
    The CodeSystem resource is used to declare the existence of and describe a code system or code system supplement and its key properties, and optionally define a part or all of its content.
    """

    _abstract = False
    _type = "CodeSystem"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/CodeSystem"

    url: Optional[fhir.uri] = Field(
        description="canonical identifier for this code system, represented as a URI (globally unique) (Coding.system)",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Additional identifier for the code system (business identifier)",
        default=None,
    )
    version: Optional[fhir.string] = Field(
        description="Business version of the code system (Coding.version)",
        default=None,
    )
    versionAlgorithmString: Optional[fhir.string] = Field(
        description="How to compare versions",
        default=None,
    )
    versionAlgorithmCoding: Optional[Coding] = Field(
        description="How to compare versions",
        default=None,
    )
    name: Optional[fhir.string] = Field(
        description="Name for this code system (computer friendly)",
        default=None,
    )
    title: Optional[fhir.string] = Field(
        description="Name for this code system (human friendly)",
        default=None,
    )
    status: fhir.code = Field(
        description="draft | active | retired | unknown",
    )
    experimental: Optional[fhir.boolean] = Field(
        description="For testing purposes, not real usage",
        default=None,
    )
    date: Optional[fhir.dateTime] = Field(
        description="Date last changed",
        default=None,
    )
    publisher: Optional[fhir.string] = Field(
        description="Name of the publisher/steward (organization or individual)",
        default=None,
    )
    contact: Optional[ListType[ContactDetail]] = Field(
        description="Contact details for the publisher",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
        description="Natural language description of the code system",
        default=None,
    )
    useContext: Optional[ListType[UsageContext]] = Field(
        description="The context that the content is intended to support",
        default=None,
    )
    jurisdiction: Optional[ListType[CodeableConcept]] = Field(
        description="Intended jurisdiction for code system (if applicable)",
        default=None,
    )
    purpose: Optional[fhir.markdown] = Field(
        description="Why this code system is defined",
        default=None,
    )
    copyright: Optional[fhir.markdown] = Field(
        description="Use and/or publishing restrictions",
        default=None,
    )
    copyrightLabel: Optional[fhir.string] = Field(
        description="Copyright holder and year(s)",
        default=None,
    )
    approvalDate: Optional[fhir.date_] = Field(
        description="When the CodeSystem was approved by publisher",
        default=None,
    )
    lastReviewDate: Optional[fhir.date_] = Field(
        description="When the CodeSystem was last reviewed by the publisher",
        default=None,
    )
    effectivePeriod: Optional[Period] = Field(
        description="When the CodeSystem is expected to be used",
        default=None,
    )
    topic: Optional[ListType[CodeableConcept]] = Field(
        description="E.g. Education, Treatment, Assessment, etc",
        default=None,
    )
    author: Optional[ListType[ContactDetail]] = Field(
        description="Who authored the CodeSystem",
        default=None,
    )
    editor: Optional[ListType[ContactDetail]] = Field(
        description="Who edited the CodeSystem",
        default=None,
    )
    reviewer: Optional[ListType[ContactDetail]] = Field(
        description="Who reviewed the CodeSystem",
        default=None,
    )
    endorser: Optional[ListType[ContactDetail]] = Field(
        description="Who endorsed the CodeSystem",
        default=None,
    )
    relatedArtifact: Optional[ListType[RelatedArtifact]] = Field(
        description="Additional documentation, citations, etc",
        default=None,
    )
    caseSensitive: Optional[fhir.boolean] = Field(
        description="If code comparison is case sensitive",
        default=None,
    )
    valueSet: Optional[fhir.canonical] = Field(
        description="canonical reference to the value set with entire code system",
        default=None,
    )
    hierarchyMeaning: Optional[fhir.code] = Field(
        description="grouped-by | is-a | part-of | classified-with",
        default=None,
    )
    compositional: Optional[fhir.boolean] = Field(
        description="If code system defines a compositional grammar",
        default=None,
    )
    versionNeeded: Optional[fhir.boolean] = Field(
        description="If definitions are not stable",
        default=None,
    )
    content: fhir.code = Field(
        description="not-present | example | fragment | complete | supplement",
    )
    supplements: Optional[fhir.canonical] = Field(
        description="canonical URL of code System this adds designations and properties to",
        default=None,
    )
    count: Optional[fhir.unsignedInt] = Field(
        description="Total concepts in the code system",
        default=None,
    )
    filter: Optional[ListType[CodeSystemFilter]] = Field(
        description="Filter that can be used in a value set",
        default=None,
    )
    property_: Optional[ListType[CodeSystemProperty]] = Field(
        description="Additional information supplied about each concept",
        default=None,
        alias="property",
    )
    concept: Optional[ListType[CodeSystemConcept]] = Field(
        description="Concepts in the code system",
        default=None,
    )

    @property
    def versionAlgorithm(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="versionAlgorithm",
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

    @model_validator(mode="after")
    def versionAlgorithm_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.String, Coding],
            field_name_base="versionAlgorithm",
            required=False,
        )

    @model_validator(mode="after")
    def FHIR_cnl_0_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.exists() implies name.matches('^[A-Z]([A-Za-z0-9_]){1,254}$')",
            human="Name should be usable as an identifier for the module by machine processing applications such as code generation",
            key="cnl-0",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_csd_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="concept.exists() implies concept.code.combine(%resource.concept.descendants().concept.code).isDistinct()",
            human="Within a code system definition, all the codes SHALL be unique",
            key="csd-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_csd_2_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="concept.concept.exists() implies hierarchyMeaning.exists()",
            human="If there is an explicit hierarchy, a hierarchyMeaning should be provided",
            key="csd-2",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_csd_3_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="concept.where(property.code = 'parent' or property.code = 'child').exists() implies hierarchyMeaning.exists()",
            human="If there is an implicit hierarchy, a hierarchyMeaning should be provided",
            key="csd-3",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_csd_4_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="CodeSystem.content = 'supplement' implies CodeSystem.supplements.exists()",
            human="If the code system content = supplement, it must nominate what it's a supplement for",
            key="csd-4",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_csd_5_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("concept.designation",),
            expression="additionalUse.exists() implies use.exists()",
            human="Must have a value for concept.designation.use if concept.designation.additionalUse is present",
            key="csd-5",
            severity="error",
        )
