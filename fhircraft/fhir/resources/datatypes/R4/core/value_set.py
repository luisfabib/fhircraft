import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)


import fhircraft.fhir.resources.datatypes.R4.primitive as fhir
from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    ContactDetail,
    UsageContext,
    CodeableConcept,
    Coding,
    BackboneElement,
)
from .resource import Resource
from .domain_resource import DomainResource


class ValueSetComposeIncludeConceptDesignation(BackboneElement):
    """
    Additional representations for this concept when used in this value set - other languages, aliases, specialized purposes, used for particular purposes, etc.
    """

    language: Optional[fhir.code] = Field(
        description="Human language of the designation",
        default=None,
    )

    use: Optional[Coding] = Field(
        description="Types of uses of designations",
        default=None,
    )
    value: fhir.string = Field(
        description="The text value for this designation",
    )


class ValueSetComposeIncludeConcept(BackboneElement):
    """
    Specifies a concept to be included or excluded.
    """

    code: fhir.code = Field(
        description="code or expression from system",
    )
    display: Optional[fhir.string] = Field(
        description="Text to display for this code for this value set in this valueset",
        default=None,
    )
    designation: Optional[ListType[ValueSetComposeIncludeConceptDesignation]] = Field(
        description="Additional representations for this concept",
        default=None,
    )


class ValueSetComposeIncludeFilter(BackboneElement):
    """
    Select concepts by specify a matching criterion based on the properties (including relationships) defined by the system, or on filters defined by the system. If multiple filters are specified, they SHALL all be true.
    """

    property_: fhir.code = Field(
        description="A property/filter defined by the code system",
        alias="property",
    )
    op: fhir.code = Field(
        description="= | is-a | descendent-of | is-not-a | regex | in | not-in | generalizes | exists",
    )
    value: fhir.string = Field(
        description="code from the system, or regex criteria, or boolean value for exists",
    )


class ValueSetComposeInclude(BackboneElement):
    """
    Include one or more codes from a code system or other value set(s).
    """

    system: Optional[fhir.uri] = Field(
        description="The system the codes come from",
        default=None,
    )
    version: Optional[fhir.string] = Field(
        description="Specific version of the code system referred to",
        default=None,
    )
    concept: Optional[ListType[ValueSetComposeIncludeConcept]] = Field(
        description="A concept defined in the system",
        default=None,
    )
    filter: Optional[ListType[ValueSetComposeIncludeFilter]] = Field(
        description="Select codes/concepts by their properties (including relationships)",
        default=None,
    )
    valueSet: Optional[ListType[fhir.canonical]] = Field(
        description="Select the contents included in this value set",
        default=None,
    )


class ValueSetComposeExclude(BackboneElement):
    """
    Exclude one or more codes from the value set based on code system filters and/or other value sets.
    """

    system: Optional[fhir.uri] = Field(
        description="The system the codes come from",
        default=None,
    )
    version: Optional[fhir.string] = Field(
        description="Specific version of the code system referred to",
        default=None,
    )
    concept: Optional[ListType[ValueSetComposeIncludeConcept]] = Field(
        description="A concept defined in the system",
        default=None,
    )
    filter: Optional[ListType[ValueSetComposeIncludeFilter]] = Field(
        description="Select codes/concepts by their properties (including relationships)",
        default=None,
    )
    valueSet: Optional[ListType[fhir.canonical]] = Field(
        description="Select the contents included in this value set",
        default=None,
    )


class ValueSetCompose(BackboneElement):
    """
    A set of criteria that define the contents of the value set by including or excluding codes selected from the specified code system(s) that the value set draws from. This is also known as the Content Logical Definition (CLD).
    """

    lockedDate: Optional[fhir.date_] = Field(
        description="Fixed date for references with no specified version (transitive)",
        default=None,
    )
    inactive: Optional[fhir.boolean] = Field(
        description="Whether inactive codes are in the value set",
        default=None,
    )
    include: ListType[ValueSetComposeInclude] = Field(
        description="Include one or more codes from a code system or other value set(s)",
        min_length=1,
    )
    exclude: Optional[ListType[ValueSetComposeExclude]] = Field(
        description="Explicitly exclude codes from a code system or other value sets",
        default=None,
    )


class ValueSetExpansionParameter(BackboneElement):
    """
    A parameter that controlled the expansion process. These parameters may be used by users of expanded value sets to check whether the expansion is suitable for a particular purpose, or to pick the correct expansion.
    """

    name: fhir.string = Field(
        description="Name as assigned by the client or server",
    )
    valueString: Optional[fhir.string] = Field(
        description="Value of the named parameter",
        default=None,
    )
    valueBoolean: Optional[fhir.boolean] = Field(
        description="Value of the named parameter",
        default=None,
    )
    valueInteger: Optional[fhir.integer] = Field(
        description="Value of the named parameter",
        default=None,
    )
    valueDecimal: Optional[fhir.decimal] = Field(
        description="Value of the named parameter",
        default=None,
    )
    valueUri: Optional[fhir.uri] = Field(
        description="Value of the named parameter",
        default=None,
    )
    valueCode: Optional[fhir.code] = Field(
        description="Value of the named parameter",
        default=None,
    )
    valueDateTime: Optional[fhir.dateTime] = Field(
        description="Value of the named parameter",
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
                fhir.String,
                fhir.Boolean,
                fhir.Integer,
                fhir.Decimal,
                fhir.Uri,
                fhir.Code,
                fhir.DateTime,
            ],
            field_name_base="value",
            required=False,
        )


class ValueSetExpansionContainsDesignation(BackboneElement):
    """
    Additional representations for this item - other languages, aliases, specialized purposes, used for particular purposes, etc. These are relevant when the conditions of the expansion do not fix to a single correct representation.
    """

    language: Optional[fhir.code] = Field(
        description="Human language of the designation",
        default=None,
    )

    use: Optional[Coding] = Field(
        description="Types of uses of designations",
        default=None,
    )
    value: Optional[fhir.string] = Field(
        description="The text value for this designation",
        default=None,
    )


class ValueSetExpansionContains(BackboneElement):
    """
    The codes that are contained in the value set expansion.
    """

    system: Optional[fhir.uri] = Field(
        description="System value for the code",
        default=None,
    )
    abstract: Optional[fhir.boolean] = Field(
        description="If user cannot select this entry",
        default=None,
    )
    inactive: Optional[fhir.boolean] = Field(
        description="If concept is inactive in the code system",
        default=None,
    )
    version: Optional[fhir.string] = Field(
        description="Version in which this code/display is defined",
        default=None,
    )
    code: Optional[fhir.code] = Field(
        description="code - if blank, this is not a selectable code",
        default=None,
    )
    display: Optional[fhir.string] = Field(
        description="User display for the concept",
        default=None,
    )
    designation: Optional[ListType[ValueSetExpansionContainsDesignation]] = Field(
        description="Additional representations for this item",
        default=None,
    )
    contains: Optional[ListType["ValueSetExpansionContains"]] = Field(
        description="Codes contained under this entry",
        default=None,
    )


class ValueSetExpansion(BackboneElement):
    """
    A value set can also be "expanded", where the value set is turned into a simple collection of enumerated codes. This element holds the expansion, if it has been performed.
    """

    identifier: Optional[fhir.uri] = Field(
        description="Identifies the value set expansion (business identifier)",
        default=None,
    )
    timestamp: fhir.dateTime = Field(
        description="time ValueSet expansion happened",
    )
    total: Optional[fhir.integer] = Field(
        description="Total number of codes in the expansion",
        default=None,
    )
    offset: Optional[fhir.integer] = Field(
        description="Offset at which this resource starts",
        default=None,
    )
    parameter: Optional[ListType[ValueSetExpansionParameter]] = Field(
        description="Parameter that controlled the expansion process",
        default=None,
    )
    contains: Optional[ListType[ValueSetExpansionContains]] = Field(
        description="Codes in the value set",
        default=None,
    )


class ValueSet(DomainResource):
    """
    A ValueSet resource instance specifies a set of codes drawn from one or more code systems, intended for use in a particular context. Value sets link between `CodeSystem` definitions and their use in [coded elements](https://hl7.org/fhir/R4/terminologies.html).
    """

    _abstract = False
    _type = "ValueSet"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/ValueSet"

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
        description="canonical identifier for this value set, represented as a URI (globally unique)",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Additional identifier for the value set (business identifier)",
        default=None,
    )
    version: Optional[fhir.string] = Field(
        description="Business version of the value set",
        default=None,
    )
    name: Optional[fhir.string] = Field(
        description="Name for this value set (computer friendly)",
        default=None,
    )
    title: Optional[fhir.string] = Field(
        description="Name for this value set (human friendly)",
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
        description="Name of the publisher (organization or individual)",
        default=None,
    )
    contact: Optional[ListType[ContactDetail]] = Field(
        description="Contact details for the publisher",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
        description="Natural language description of the value set",
        default=None,
    )
    useContext: Optional[ListType[UsageContext]] = Field(
        description="The context that the content is intended to support",
        default=None,
    )
    jurisdiction: Optional[ListType[CodeableConcept]] = Field(
        description="Intended jurisdiction for value set (if applicable)",
        default=None,
    )
    immutable: Optional[fhir.boolean] = Field(
        description="Indicates whether or not any change to the content logical definition may occur",
        default=None,
    )
    purpose: Optional[fhir.markdown] = Field(
        description="Why this value set is defined",
        default=None,
    )
    copyright: Optional[fhir.markdown] = Field(
        description="Use and/or publishing restrictions",
        default=None,
    )
    compose: Optional[ValueSetCompose] = Field(
        description="Content logical definition of the value set (CLD)",
        default=None,
    )
    expansion: Optional[ValueSetExpansion] = Field(
        description='Used when the value set is "expanded"',
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_vsd_0_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.matches('[A-Z]([A-Za-z0-9_]){0,254}')",
            human="Name should be usable as an identifier for the module by machine processing applications such as code generation",
            key="vsd-0",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_vsd_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("compose.include",),
            expression="valueSet.exists() or system.exists()",
            human="A value set include/exclude SHALL have a value set or a system",
            key="vsd-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_vsd_2_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("compose.include",),
            expression="(concept.exists() or filter.exists()) implies system.exists()",
            human="A value set with concepts or filters SHALL include a system",
            key="vsd-2",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_vsd_3_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("compose.include",),
            expression="concept.empty() or filter.empty()",
            human="Cannot have both concept and filter",
            key="vsd-3",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_vsd_6_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("expansion.contains",),
            expression="code.exists() or display.exists()",
            human="SHALL have a code or a display",
            key="vsd-6",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_vsd_9_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("expansion.contains",),
            expression="code.exists() or abstract = true",
            human="Must have a code if not abstract",
            key="vsd-9",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_vsd_10_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("expansion.contains",),
            expression="code.empty() or system.exists()",
            human="Must have a system if a code is present",
            key="vsd-10",
            severity="error",
        )
