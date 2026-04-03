import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)


from ..primitive import *
from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    ContactDetail,
    Coding,
    UsageContext,
    CodeableConcept,
    BackboneElement,
)
from .resource import Resource
from .domain_resource import DomainResource

class CodeSystemFilter(BackboneElement):
    """
    A filter that can be used in a value set compose statement when selecting concepts using a filter.
    """

    code: Optional[Code] = Field(
        description="Code that identifies the filter",
        default=None,
    )
    description: Optional[String] = Field(
        description="How or why the filter is used",
        default=None,
    )
    operator: Optional[ListType[Code]] = Field(
        description="= | is-a | descendent-of | is-not-a | regex | in | not-in | generalizes | exists",
        default=None,
    )
    value: Optional[String] = Field(
        description="What to use for the value",
        default=None,
    )

class CodeSystemProperty(BackboneElement):
    """
    A property defines an additional slot through which additional information can be provided about a concept.
    """

    code: Optional[Code] = Field(
        description="Identifies the property on the concepts, and when referred to in operations",
        default=None,
    )
    uri: Optional[Uri] = Field(
        description="Formal identifier for the property",
        default=None,
    )
    description: Optional[String] = Field(
        description="Why the property is defined, and/or what it conveys",
        default=None,
    )
    type: Optional[Code] = Field(
        description="code | Coding | string | integer | boolean | dateTime | decimal",
        default=None,
    )

class CodeSystemConceptDesignation(BackboneElement):
    """
    Additional representations for the concept - other languages, aliases, specialized purposes, used for particular purposes, etc.
    """

    language: Optional[Code] = Field(
        description="Human language of the designation",
        default=None,
    )

    use: Optional[Coding] = Field(
        description="Details how this designation would be used",
        default=None,
    )
    value: Optional[String] = Field(
        description="The text value for this designation",
        default=None,
    )

class CodeSystemConceptProperty(BackboneElement):
    """
    A property value for this concept.
    """

    code: Optional[Code] = Field(
        description="Reference to CodeSystem.property.code",
        default=None,
    )
    valueCode: Optional[Code] = Field(
        description="Value of the property for this concept",
        default=None,
    )
    valueCoding: Optional[Coding] = Field(
        description="Value of the property for this concept",
        default=None,
    )
    valueString: Optional[String] = Field(
        description="Value of the property for this concept",
        default=None,
    )
    valueInteger: Optional[Integer] = Field(
        description="Value of the property for this concept",
        default=None,
    )
    valueBoolean: Optional[Boolean] = Field(
        description="Value of the property for this concept",
        default=None,
    )
    valueDateTime: Optional[DateTime] = Field(
        description="Value of the property for this concept",
        default=None,
    )
    valueDecimal: Optional[Decimal] = Field(
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
            field_types=[Code, Coding, String, Integer, Boolean, DateTime, Decimal],
            field_name_base="value",
            required=True,
        )

class CodeSystemConcept(BackboneElement):
    """
    Concepts that are in the code system. The concept definitions are inherently hierarchical, but the definitions must be consulted to determine what the meanings of the hierarchical relationships are.
    """

    code: Optional[Code] = Field(
        description="Code that identifies concept",
        default=None,
    )
    display: Optional[String] = Field(
        description="Text to display to the user",
        default=None,
    )
    definition: Optional[String] = Field(
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
        description="Canonical identifier for this code system, represented as a URI (globally unique) (Coding.system)",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Additional identifier for the code system (business identifier)",
        default=None,
    )
    version: Optional[String] = Field(
        description="Business version of the code system (Coding.version)",
        default=None,
    )
    name: Optional[String] = Field(
        description="Name for this code system (computer friendly)",
        default=None,
    )
    title: Optional[String] = Field(
        description="Name for this code system (human friendly)",
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
    purpose: Optional[Markdown] = Field(
        description="Why this code system is defined",
        default=None,
    )
    copyright: Optional[Markdown] = Field(
        description="Use and/or publishing restrictions",
        default=None,
    )
    caseSensitive: Optional[Boolean] = Field(
        description="If code comparison is case sensitive",
        default=None,
    )
    valueSet: Optional[Canonical] = Field(
        description="Canonical reference to the value set with entire code system",
        default=None,
    )
    hierarchyMeaning: Optional[Code] = Field(
        description="grouped-by | is-a | part-of | classified-with",
        default=None,
    )
    compositional: Optional[Boolean] = Field(
        description="If code system defines a compositional grammar",
        default=None,
    )
    versionNeeded: Optional[Boolean] = Field(
        description="If definitions are not stable",
        default=None,
    )
    content: Optional[Code] = Field(
        description="not-present | example | fragment | complete | supplement",
        default=None,
    )
    supplements: Optional[Canonical] = Field(
        description="Canonical URL of Code System this adds designations and properties to",
        default=None,
    )
    count: Optional[UnsignedInt] = Field(
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

    @model_validator(mode="after")
    def FHIR_csd_0_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.matches('[A-Z]([A-Za-z0-9_]){0,254}')",
            human="Name should be usable as an identifier for the module by machine processing applications such as code generation",
            key="csd-0",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_csd_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="concept.code.combine($this.descendants().concept.code).isDistinct()",
            human="Within a code system definition, all the codes SHALL be unique",
            key="csd-1",
            severity="error",
        )
