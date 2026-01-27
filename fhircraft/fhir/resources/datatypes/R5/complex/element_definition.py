from typing import List, Optional

from pydantic import Field, model_validator
from fhircraft.fhir.resources.validators import (
    get_type_choice_value_by_base,
    validate_element_constraint,
    validate_model_constraint,
    validate_type_choice_element,
)

from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R5.complex import (
    Address,
    Age,
    Annotation,
    Attachment,
    BackboneType,
    CodeableConcept,
    CodeableReference,
    Coding,
    ContactDetail,
    ContactPoint,
    Count,
    DataRequirement,
    Dosage,
    Element,
    Expression,
    Money,
    Period,
    Quantity,
    Range,
    Ratio,
    RatioRange,
    Reference,
    SampledData,
    Signature,
    Timing,
    Distance,
    Duration,
    HumanName,
    Identifier,
    Meta,
    ParameterDefinition,
    RelatedArtifact,
    TriggerDefinition,
    UsageContext,
    ExtendedContactDetail,
    Availability,
)


class ElementDefinitionSlicingDiscriminator(Element):
    """
    Designates which child elements are used to discriminate between the slices when processing an instance. If one or more discriminators are provided, the value of the child elements in the instance data SHALL completely distinguish which slice the element in the resource matches based on the allowed values for those elements in each of the slices.
    """

    _type = "ElementDefinitionSlicingDiscriminator"

    type: Optional[Code] = Field(
        description="value | exists | type | profile | position",
        default=None,
    )
    type_ext: Optional[List[Optional[Element]]] = Field(
        description="Placeholder element for type extensions",
        default=None,
        alias="_type",
    )
    path: Optional[String] = Field(
        description="Path to element value",
        default=None,
    )
    path_ext: Optional[Element] = Field(
        description="Placeholder element for path extensions",
        default=None,
        alias="_path",
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return validate_element_constraint(
            self,
            elements=(
                "path",
                "type",
                "extension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class ElementDefinitionSlicing(Element):
    """
    Indicates that the element is sliced into a set of alternative definitions (i.e. in a structure definition, there are multiple different constraints on a single element in the base resource). Slicing can be used in any resource that has cardinality ..* on the base resource, or any resource with a choice of types. The set of slices is any elements that come after this in the element sequence that have the same path, until a shorter path occurs (the shorter path terminates the set).
    """

    _type = "ElementDefinitionSlicing"

    discriminator: Optional[List[ElementDefinitionSlicingDiscriminator]] = Field(
        description="Element values that are used to distinguish the slices",
        default=None,
    )
    description: Optional[String] = Field(
        description="Text description of how slicing works (or not)",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    ordered: Optional[Boolean] = Field(
        description="If elements must be in same order as slices",
        default=None,
    )
    ordered_ext: Optional[Element] = Field(
        description="Placeholder element for ordered extensions",
        default=None,
        alias="_ordered",
    )
    rules: Optional[Code] = Field(
        description="closed | open | openAtEnd",
        default=None,
    )
    rules_ext: Optional[Element] = Field(
        description="Placeholder element for rules extensions",
        default=None,
        alias="_rules",
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return validate_element_constraint(
            self,
            elements=(
                "rules",
                "ordered",
                "description",
                "discriminator",
                "extension",
                "extension",
                "extension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class ElementDefinitionBase(Element):
    """
    Information about the base definition of the element, provided to make it unnecessary for tools to trace the deviation of the element through the derived and related profiles. When the element definition is not the original definition of an element - e.g. either in a constraint on another type, or for elements from a super type in a snap shot - then the information in provided in the element definition may be different to the base definition. On the original definition of the element, it will be same.
    """

    _type = "ElementDefinitionBase"

    path: Optional[String] = Field(
        description="Path that identifies the base element",
        default=None,
    )
    path_ext: Optional[Element] = Field(
        description="Placeholder element for path extensions",
        default=None,
        alias="_path",
    )
    min: Optional[UnsignedInt] = Field(
        description="Min cardinality of the base element",
        default=None,
    )
    min_ext: Optional[Element] = Field(
        description="Placeholder element for min extensions",
        default=None,
        alias="_min",
    )
    max: Optional[String] = Field(
        description="Max cardinality of the base element",
        default=None,
    )
    max_ext: Optional[Element] = Field(
        description="Placeholder element for max extensions",
        default=None,
        alias="_max",
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return validate_element_constraint(
            self,
            elements=(
                "max",
                "min",
                "path",
                "extension",
                "extension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class ElementDefinitionType(Element):
    """
    The data type or resource that the value of this element is permitted to be.
    """

    _type = "ElementDefinitionType"

    code: Optional[Uri] = Field(
        description="Data type or Resource (reference to definition)",
        default=None,
    )
    code_ext: Optional[List[Optional[Element]]] = Field(
        description="Placeholder element for code extensions",
        default=None,
        alias="_code",
    )
    profile: Optional[List[Canonical]] = Field(
        description="Profiles (StructureDefinition or IG) - one must apply",
        default=None,
    )
    profile_ext: Optional[List[Optional[Element]]] = Field(
        description="Placeholder element for profile extensions",
        default=None,
        alias="_profile",
    )
    targetProfile: Optional[List[Canonical]] = Field(
        description="Profile (StructureDefinition or IG) on the Reference/canonical target - one must apply",
        default=None,
    )
    targetProfile_ext: Optional[List[Optional[Element]]] = Field(
        description="Placeholder element for targetProfile extensions",
        default=None,
        alias="_targetProfile",
    )
    aggregation: Optional[List[Code]] = Field(
        description="contained | referenced | bundled - how aggregated",
        default=None,
    )
    aggregation_ext: Optional[List[Optional[Element]]] = Field(
        description="Placeholder element for aggregation extensions",
        default=None,
        alias="_aggregation",
    )
    versioning: Optional[Code] = Field(
        description="either | independent | specific",
        default=None,
    )
    versioning_ext: Optional[Element] = Field(
        description="Placeholder element for versioning extensions",
        default=None,
        alias="_versioning",
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return validate_element_constraint(
            self,
            elements=(
                "versioning",
                "aggregation",
                "targetProfile",
                "profile",
                "code",
                "extension",
                "extension",
                "extension",
                "extension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class ElementDefinitionExample(Element):
    """
    A sample value for this element demonstrating the type of information that would typically be found in the element.
    """

    _type = "ElementDefinitionExample"

    label: Optional[String] = Field(
        description="Describes the purpose of this example",
        default=None,
    )
    label_ext: Optional[Element] = Field(
        description="Placeholder element for label extensions",
        default=None,
        alias="_label",
    )
    valueBase64Binary: Optional[Base64Binary] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueBase64Binary_ext: Optional[Element] = Field(
        description="Placeholder element for valueBase64Binary extensions",
        default=None,
        alias="_valueBase64Binary",
    )
    valueBoolean: Optional[Boolean] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueBoolean_ext: Optional[Element] = Field(
        description="Placeholder element for valueBoolean extensions",
        default=None,
        alias="_valueBoolean",
    )
    valueCanonical: Optional[Canonical] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueCanonical_ext: Optional[Element] = Field(
        description="Placeholder element for valueCanonical extensions",
        default=None,
        alias="_valueCanonical",
    )
    valueCode: Optional[Code] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueCode_ext: Optional[Element] = Field(
        description="Placeholder element for valueCode extensions",
        default=None,
        alias="_valueCode",
    )
    valueDate: Optional[Date] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueDate_ext: Optional[Element] = Field(
        description="Placeholder element for valueDate extensions",
        default=None,
        alias="_valueDate",
    )
    valueDateTime: Optional[DateTime] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueDateTime_ext: Optional[Element] = Field(
        description="Placeholder element for valueDateTime extensions",
        default=None,
        alias="_valueDateTime",
    )
    valueDecimal: Optional[Decimal] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueDecimal_ext: Optional[Element] = Field(
        description="Placeholder element for valueDecimal extensions",
        default=None,
        alias="_valueDecimal",
    )
    valueId: Optional[Id] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueId_ext: Optional[Element] = Field(
        description="Placeholder element for valueId extensions",
        default=None,
        alias="_valueId",
    )
    valueInstant: Optional[Instant] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueInstant_ext: Optional[Element] = Field(
        description="Placeholder element for valueInstant extensions",
        default=None,
        alias="_valueInstant",
    )
    valueInteger: Optional[Integer] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueInteger_ext: Optional[Element] = Field(
        description="Placeholder element for valueInteger extensions",
        default=None,
        alias="_valueInteger",
    )
    valueInteger64: Optional[Integer64] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueInteger64_ext: Optional[Element] = Field(
        description="Placeholder element for valueInteger64 extensions",
        default=None,
        alias="_valueInteger64",
    )
    valueMarkdown: Optional[Markdown] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueMarkdown_ext: Optional[Element] = Field(
        description="Placeholder element for valueMarkdown extensions",
        default=None,
        alias="_valueMarkdown",
    )
    valueOid: Optional[Oid] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueOid_ext: Optional[Element] = Field(
        description="Placeholder element for valueOid extensions",
        default=None,
        alias="_valueOid",
    )
    valuePositiveInt: Optional[PositiveInt] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valuePositiveInt_ext: Optional[Element] = Field(
        description="Placeholder element for valuePositiveInt extensions",
        default=None,
        alias="_valuePositiveInt",
    )
    valueString: Optional[String] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueString_ext: Optional[Element] = Field(
        description="Placeholder element for valueString extensions",
        default=None,
        alias="_valueString",
    )
    valueTime: Optional[Time] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueTime_ext: Optional[Element] = Field(
        description="Placeholder element for valueTime extensions",
        default=None,
        alias="_valueTime",
    )
    valueUnsignedInt: Optional[UnsignedInt] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueUnsignedInt_ext: Optional[Element] = Field(
        description="Placeholder element for valueUnsignedInt extensions",
        default=None,
        alias="_valueUnsignedInt",
    )
    valueUri: Optional[Uri] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueUri_ext: Optional[Element] = Field(
        description="Placeholder element for valueUri extensions",
        default=None,
        alias="_valueUri",
    )
    valueUrl: Optional[Url] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueUrl_ext: Optional[Element] = Field(
        description="Placeholder element for valueUrl extensions",
        default=None,
        alias="_valueUrl",
    )
    valueUuid: Optional[Uuid] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueUuid_ext: Optional[Element] = Field(
        description="Placeholder element for valueUuid extensions",
        default=None,
        alias="_valueUuid",
    )
    valueAddress: Optional[Address] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueAge: Optional[Age] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueAnnotation: Optional[Annotation] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueAttachment: Optional[Attachment] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueCodeableConcept: Optional[CodeableConcept] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueCodeableReference: Optional[CodeableReference] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueCoding: Optional[Coding] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueContactPoint: Optional[ContactPoint] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueCount: Optional[Count] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueDistance: Optional[Distance] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueDuration: Optional[Duration] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueHumanName: Optional[HumanName] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueIdentifier: Optional[Identifier] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueMoney: Optional[Money] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valuePeriod: Optional[Period] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueRange: Optional[Range] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueRatio: Optional[Ratio] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueRatioRange: Optional[RatioRange] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueReference: Optional[Reference] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueSampledData: Optional[SampledData] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueSignature: Optional[Signature] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueTiming: Optional[Timing] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueContactDetail: Optional[ContactDetail] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueDataRequirement: Optional[DataRequirement] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueExpression: Optional[Expression] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueParameterDefinition: Optional[ParameterDefinition] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueRelatedArtifact: Optional[RelatedArtifact] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueTriggerDefinition: Optional[TriggerDefinition] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueUsageContext: Optional[UsageContext] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueAvailability: Optional[Availability] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueExtendedContactDetail: Optional[ExtendedContactDetail] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueDosage: Optional[Dosage] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueMeta: Optional[Meta] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )

    @property
    def value(self):
        return get_type_choice_value_by_base(
            self,
            base="value",
        )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return validate_element_constraint(
            self,
            elements=(
                "label",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def value_type_choice_validator(self):
        return validate_type_choice_element(
            self,
            field_types=[
                "Base64Binary",
                "Boolean",
                "Canonical",
                "Code",
                "Date",
                "DateTime",
                "Decimal",
                "Id",
                "Instant",
                "Integer",
                "Integer64",
                "Markdown",
                "Oid",
                "PositiveInt",
                "String",
                "Time",
                "UnsignedInt",
                "Uri",
                "Url",
                "Uuid",
                "Address",
                "Age",
                "Annotation",
                "Attachment",
                "CodeableConcept",
                "CodeableReference",
                "Coding",
                "ContactPoint",
                "Count",
                "Distance",
                "Duration",
                "HumanName",
                "Identifier",
                "Money",
                "Period",
                "Quantity",
                "Range",
                "Ratio",
                "RatioRange",
                "Reference",
                "SampledData",
                "Signature",
                "Timing",
                "ContactDetail",
                "DataRequirement",
                "Expression",
                "ParameterDefinition",
                "RelatedArtifact",
                "TriggerDefinition",
                "UsageContext",
                "Availability",
                "ExtendedContactDetail",
                "Dosage",
                "Meta",
            ],
            field_name_base="value",
            required=True,
            non_allowed_types=[],
        )


class ElementDefinitionConstraint(Element):
    """
    Formal constraints such as co-occurrence and other constraints that can be computationally evaluated within the context of the instance.
    """

    _type = "ElementDefinitionConstraint"

    key: Optional[Id] = Field(
        description="Target of \u0027condition\u0027 reference above",
        default=None,
    )
    key_ext: Optional[Element] = Field(
        description="Placeholder element for key extensions",
        default=None,
        alias="_key",
    )
    requirements: Optional[Markdown] = Field(
        description="Why this constraint is necessary or appropriate",
        default=None,
    )
    requirements_ext: Optional[Element] = Field(
        description="Placeholder element for requirements extensions",
        default=None,
        alias="_requirements",
    )
    severity: Optional[Code] = Field(
        description="error | warning",
        default=None,
    )
    severity_ext: Optional[Element] = Field(
        description="Placeholder element for severity extensions",
        default=None,
        alias="_severity",
    )
    suppress: Optional[Boolean] = Field(
        description="Suppress warning or hint in profile",
        default=None,
    )
    suppress_ext: Optional[Element] = Field(
        description="Placeholder element for suppress extensions",
        default=None,
        alias="_suppress",
    )
    human: Optional[String] = Field(
        description="Human description of constraint",
        default=None,
    )
    human_ext: Optional[Element] = Field(
        description="Placeholder element for human extensions",
        default=None,
        alias="_human",
    )
    expression: Optional[String] = Field(
        description="FHIRPath expression of constraint",
        default=None,
    )
    expression_ext: Optional[Element] = Field(
        description="Placeholder element for expression extensions",
        default=None,
        alias="_expression",
    )
    source: Optional[Canonical] = Field(
        description="Reference to original source of constraint",
        default=None,
    )
    source_ext: Optional[Element] = Field(
        description="Placeholder element for source extensions",
        default=None,
        alias="_source",
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return validate_element_constraint(
            self,
            elements=(
                "source",
                "expression",
                "human",
                "suppress",
                "severity",
                "requirements",
                "key",
                "extension",
                "extension",
                "extension",
                "extension",
                "extension",
                "extension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class ElementDefinitionBindingAdditional(Element):
    """
    Additional bindings that help applications implementing this element. Additional bindings do not replace the main binding but provide more information and/or context.
    """

    _type = "ElementDefinitionBindingAdditional"

    purpose: Optional[Code] = Field(
        description="maximum | minimum | required | extensible | candidate | current | preferred | ui | starter | component",
        default=None,
    )
    purpose_ext: Optional[Element] = Field(
        description="Placeholder element for purpose extensions",
        default=None,
        alias="_purpose",
    )
    valueSet: Optional[Canonical] = Field(
        description="The value set for the additional binding",
        default=None,
    )
    valueSet_ext: Optional[Element] = Field(
        description="Placeholder element for valueSet extensions",
        default=None,
        alias="_valueSet",
    )
    documentation: Optional[Markdown] = Field(
        description="Documentation of the purpose of use of the binding",
        default=None,
    )
    documentation_ext: Optional[Element] = Field(
        description="Placeholder element for documentation extensions",
        default=None,
        alias="_documentation",
    )
    shortDoco: Optional[String] = Field(
        description="Concise documentation - for summary tables",
        default=None,
    )
    shortDoco_ext: Optional[Element] = Field(
        description="Placeholder element for shortDoco extensions",
        default=None,
        alias="_shortDoco",
    )
    usage: Optional[List[UsageContext]] = Field(
        description="Qualifies the usage - jurisdiction, gender, workflow status etc.",
        default=None,
    )
    any: Optional[Boolean] = Field(
        description="Whether binding can applies to all repeats, or just one",
        default=None,
    )
    any_ext: Optional[Element] = Field(
        description="Placeholder element for any extensions",
        default=None,
        alias="_any",
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return validate_element_constraint(
            self,
            elements=(
                "any",
                "usage",
                "shortDoco",
                "documentation",
                "valueSet",
                "purpose",
                "extension",
                "extension",
                "extension",
                "extension",
                "extension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class ElementDefinitionBinding(Element):
    """
    Binds to a value set if this element is coded (code, Coding, CodeableConcept, Quantity), or the data types (string, uri).
    """

    _type = "ElementDefinitionBinding"

    strength: Optional[Code] = Field(
        description="required | extensible | preferred | example",
        default=None,
    )
    strength_ext: Optional[Element] = Field(
        description="Placeholder element for strength extensions",
        default=None,
        alias="_strength",
    )
    description: Optional[Markdown] = Field(
        description="Intended use of codes in the bound value set",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    valueSet: Optional[Canonical] = Field(
        description="Source of value set",
        default=None,
    )
    valueSet_ext: Optional[Element] = Field(
        description="Placeholder element for valueSet extensions",
        default=None,
        alias="_valueSet",
    )
    additional: Optional[List[ElementDefinitionBindingAdditional]] = Field(
        description="Additional Bindings - more rules about the binding",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return validate_element_constraint(
            self,
            elements=(
                "additional",
                "valueSet",
                "description",
                "strength",
                "extension",
                "extension",
                "extension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class ElementDefinitionMapping(Element):
    """
    Identifies a concept from an external specification that roughly corresponds to this element.
    """

    _type = "ElementDefinitionMapping"

    identity: Optional[Id] = Field(
        description="Reference to mapping declaration",
        default=None,
    )
    identity_ext: Optional[Element] = Field(
        description="Placeholder element for identity extensions",
        default=None,
        alias="_identity",
    )
    language: Optional[Code] = Field(
        description="Computable language of mapping",
        default=None,
    )
    language_ext: Optional[Element] = Field(
        description="Placeholder element for language extensions",
        default=None,
        alias="_language",
    )
    map: Optional[String] = Field(
        description="Details of the mapping",
        default=None,
    )
    map_ext: Optional[Element] = Field(
        description="Placeholder element for map extensions",
        default=None,
        alias="_map",
    )
    comment: Optional[Markdown] = Field(
        description="Comments about the mapping or its use",
        default=None,
    )
    comment_ext: Optional[Element] = Field(
        description="Placeholder element for comment extensions",
        default=None,
        alias="_comment",
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return validate_element_constraint(
            self,
            elements=(
                "comment",
                "map",
                "language",
                "identity",
                "extension",
                "extension",
                "extension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class ElementDefinition(BackboneType):
    """
    ElementDefinition Type: Captures constraints on each element within the resource, profile, or extension.
    """

    _type = "ElementDefinition"

    path: Optional[String] = Field(
        description="Path of the element in the hierarchy of elements",
        default=None,
    )
    path_ext: Optional[Element] = Field(
        description="Placeholder element for path extensions",
        default=None,
        alias="_path",
    )
    representation: Optional[List[Code]] = Field(
        description="xmlAttr | xmlText | typeAttr | cdaText | xhtml",
        default=None,
    )
    representation_ext: Optional[List[Optional[Element]]] = Field(
        description="Placeholder element for representation extensions",
        default=None,
        alias="_representation",
    )
    sliceName: Optional[String] = Field(
        description="Name for this particular element (in a set of slices)",
        default=None,
    )
    sliceName_ext: Optional[Element] = Field(
        description="Placeholder element for sliceName extensions",
        default=None,
        alias="_sliceName",
    )
    sliceIsConstraining: Optional[Boolean] = Field(
        description="If this slice definition constrains an inherited slice definition (or not)",
        default=None,
    )
    sliceIsConstraining_ext: Optional[Element] = Field(
        description="Placeholder element for sliceIsConstraining extensions",
        default=None,
        alias="_sliceIsConstraining",
    )
    label: Optional[String] = Field(
        description="Name for element to display with or prompt for element",
        default=None,
    )
    label_ext: Optional[Element] = Field(
        description="Placeholder element for label extensions",
        default=None,
        alias="_label",
    )
    code: Optional[List[Coding]] = Field(
        description="Corresponding codes in terminologies",
        default=None,
    )
    slicing: Optional[ElementDefinitionSlicing] = Field(
        description="This element is sliced - slices follow",
        default=None,
    )
    short: Optional[String] = Field(
        description="Concise definition for space-constrained presentation",
        default=None,
    )
    short_ext: Optional[Element] = Field(
        description="Placeholder element for short extensions",
        default=None,
        alias="_short",
    )
    definition: Optional[Markdown] = Field(
        description="Full formal definition as narrative text",
        default=None,
    )
    definition_ext: Optional[Element] = Field(
        description="Placeholder element for definition extensions",
        default=None,
        alias="_definition",
    )
    comment: Optional[Markdown] = Field(
        description="Comments about the use of this element",
        default=None,
    )
    comment_ext: Optional[Element] = Field(
        description="Placeholder element for comment extensions",
        default=None,
        alias="_comment",
    )
    requirements: Optional[Markdown] = Field(
        description="Why this resource has been created",
        default=None,
    )
    requirements_ext: Optional[Element] = Field(
        description="Placeholder element for requirements extensions",
        default=None,
        alias="_requirements",
    )
    alias: Optional[List[String]] = Field(
        description="Other names",
        default=None,
    )
    alias_ext: Optional[List[Optional[Element]]] = Field(
        description="Placeholder element for alias extensions",
        default=None,
        alias="_alias",
    )
    min: Optional[UnsignedInt] = Field(
        description="Minimum Cardinality",
        default=None,
    )
    min_ext: Optional[Element] = Field(
        description="Placeholder element for min extensions",
        default=None,
        alias="_min",
    )
    max: Optional[String] = Field(
        description="Maximum Cardinality (a number or *)",
        default=None,
    )
    max_ext: Optional[Element] = Field(
        description="Placeholder element for max extensions",
        default=None,
        alias="_max",
    )
    base: Optional[ElementDefinitionBase] = Field(
        description="Base definition information for tools",
        default=None,
    )
    contentReference: Optional[Uri] = Field(
        description="Reference to definition of content for the element",
        default=None,
    )
    contentReference_ext: Optional[Element] = Field(
        description="Placeholder element for contentReference extensions",
        default=None,
        alias="_contentReference",
    )
    type: Optional[List[ElementDefinitionType]] = Field(
        description="Data type and Profile for this element",
        default=None,
    )
    defaultValueBase64Binary: Optional[Base64Binary] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueBase64Binary_ext: Optional[Element] = Field(
        description="Placeholder element for defaultValueBase64Binary extensions",
        default=None,
        alias="_defaultValueBase64Binary",
    )
    defaultValueBoolean: Optional[Boolean] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueBoolean_ext: Optional[Element] = Field(
        description="Placeholder element for defaultValueBoolean extensions",
        default=None,
        alias="_defaultValueBoolean",
    )
    defaultValueCanonical: Optional[Canonical] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueCanonical_ext: Optional[Element] = Field(
        description="Placeholder element for defaultValueCanonical extensions",
        default=None,
        alias="_defaultValueCanonical",
    )
    defaultValueCode: Optional[Code] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueCode_ext: Optional[Element] = Field(
        description="Placeholder element for defaultValueCode extensions",
        default=None,
        alias="_defaultValueCode",
    )
    defaultValueDate: Optional[Date] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueDate_ext: Optional[Element] = Field(
        description="Placeholder element for defaultValueDate extensions",
        default=None,
        alias="_defaultValueDate",
    )
    defaultValueDateTime: Optional[DateTime] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueDateTime_ext: Optional[Element] = Field(
        description="Placeholder element for defaultValueDateTime extensions",
        default=None,
        alias="_defaultValueDateTime",
    )
    defaultValueDecimal: Optional[Decimal] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueDecimal_ext: Optional[Element] = Field(
        description="Placeholder element for defaultValueDecimal extensions",
        default=None,
        alias="_defaultValueDecimal",
    )
    defaultValueId: Optional[Id] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueId_ext: Optional[Element] = Field(
        description="Placeholder element for defaultValueId extensions",
        default=None,
        alias="_defaultValueId",
    )
    defaultValueInstant: Optional[Instant] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueInstant_ext: Optional[Element] = Field(
        description="Placeholder element for defaultValueInstant extensions",
        default=None,
        alias="_defaultValueInstant",
    )
    defaultValueInteger: Optional[Integer] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueInteger_ext: Optional[Element] = Field(
        description="Placeholder element for defaultValueInteger extensions",
        default=None,
        alias="_defaultValueInteger",
    )
    defaultValueInteger64: Optional[Integer64] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueInteger64_ext: Optional[Element] = Field(
        description="Placeholder element for defaultValueInteger64 extensions",
        default=None,
        alias="_defaultValueInteger64",
    )
    defaultValueMarkdown: Optional[Markdown] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueMarkdown_ext: Optional[Element] = Field(
        description="Placeholder element for defaultValueMarkdown extensions",
        default=None,
        alias="_defaultValueMarkdown",
    )
    defaultValueOid: Optional[Oid] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueOid_ext: Optional[Element] = Field(
        description="Placeholder element for defaultValueOid extensions",
        default=None,
        alias="_defaultValueOid",
    )
    defaultValuePositiveInt: Optional[PositiveInt] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValuePositiveInt_ext: Optional[Element] = Field(
        description="Placeholder element for defaultValuePositiveInt extensions",
        default=None,
        alias="_defaultValuePositiveInt",
    )
    defaultValueString: Optional[String] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueString_ext: Optional[Element] = Field(
        description="Placeholder element for defaultValueString extensions",
        default=None,
        alias="_defaultValueString",
    )
    defaultValueTime: Optional[Time] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueTime_ext: Optional[Element] = Field(
        description="Placeholder element for defaultValueTime extensions",
        default=None,
        alias="_defaultValueTime",
    )
    defaultValueUnsignedInt: Optional[UnsignedInt] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueUnsignedInt_ext: Optional[Element] = Field(
        description="Placeholder element for defaultValueUnsignedInt extensions",
        default=None,
        alias="_defaultValueUnsignedInt",
    )
    defaultValueUri: Optional[Uri] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueUri_ext: Optional[Element] = Field(
        description="Placeholder element for defaultValueUri extensions",
        default=None,
        alias="_defaultValueUri",
    )
    defaultValueUrl: Optional[Url] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueUrl_ext: Optional[Element] = Field(
        description="Placeholder element for defaultValueUrl extensions",
        default=None,
        alias="_defaultValueUrl",
    )
    defaultValueUuid: Optional[Uuid] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueUuid_ext: Optional[Element] = Field(
        description="Placeholder element for defaultValueUuid extensions",
        default=None,
        alias="_defaultValueUuid",
    )
    defaultValueAddress: Optional[Address] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueAge: Optional[Age] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueAnnotation: Optional[Annotation] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueAttachment: Optional[Attachment] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueCodeableConcept: Optional[CodeableConcept] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueCodeableReference: Optional[CodeableReference] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueCoding: Optional[Coding] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueContactPoint: Optional[ContactPoint] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueCount: Optional[Count] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueDistance: Optional[Distance] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueDuration: Optional[Duration] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueHumanName: Optional[HumanName] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueIdentifier: Optional[Identifier] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueMoney: Optional[Money] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValuePeriod: Optional[Period] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueQuantity: Optional[Quantity] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueRange: Optional[Range] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueRatio: Optional[Ratio] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueRatioRange: Optional[RatioRange] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueReference: Optional[Reference] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueSampledData: Optional[SampledData] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueSignature: Optional[Signature] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueTiming: Optional[Timing] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueContactDetail: Optional[ContactDetail] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueDataRequirement: Optional[DataRequirement] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueExpression: Optional[Expression] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueParameterDefinition: Optional[ParameterDefinition] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueRelatedArtifact: Optional[RelatedArtifact] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueTriggerDefinition: Optional[TriggerDefinition] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueUsageContext: Optional[UsageContext] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueAvailability: Optional[Availability] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueExtendedContactDetail: Optional[ExtendedContactDetail] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueDosage: Optional[Dosage] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueMeta: Optional[Meta] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    meaningWhenMissing: Optional[Markdown] = Field(
        description="Implicit meaning when this element is missing",
        default=None,
    )
    meaningWhenMissing_ext: Optional[Element] = Field(
        description="Placeholder element for meaningWhenMissing extensions",
        default=None,
        alias="_meaningWhenMissing",
    )
    orderMeaning: Optional[String] = Field(
        description="What the order of the elements means",
        default=None,
    )
    orderMeaning_ext: Optional[Element] = Field(
        description="Placeholder element for orderMeaning extensions",
        default=None,
        alias="_orderMeaning",
    )
    fixedBase64Binary: Optional[Base64Binary] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedBase64Binary_ext: Optional[Element] = Field(
        description="Placeholder element for fixedBase64Binary extensions",
        default=None,
        alias="_fixedBase64Binary",
    )
    fixedBoolean: Optional[Boolean] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedBoolean_ext: Optional[Element] = Field(
        description="Placeholder element for fixedBoolean extensions",
        default=None,
        alias="_fixedBoolean",
    )
    fixedCanonical: Optional[Canonical] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedCanonical_ext: Optional[Element] = Field(
        description="Placeholder element for fixedCanonical extensions",
        default=None,
        alias="_fixedCanonical",
    )
    fixedCode: Optional[Code] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedCode_ext: Optional[Element] = Field(
        description="Placeholder element for fixedCode extensions",
        default=None,
        alias="_fixedCode",
    )
    fixedDate: Optional[Date] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedDate_ext: Optional[Element] = Field(
        description="Placeholder element for fixedDate extensions",
        default=None,
        alias="_fixedDate",
    )
    fixedDateTime: Optional[DateTime] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedDateTime_ext: Optional[Element] = Field(
        description="Placeholder element for fixedDateTime extensions",
        default=None,
        alias="_fixedDateTime",
    )
    fixedDecimal: Optional[Decimal] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedDecimal_ext: Optional[Element] = Field(
        description="Placeholder element for fixedDecimal extensions",
        default=None,
        alias="_fixedDecimal",
    )
    fixedId: Optional[Id] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedId_ext: Optional[Element] = Field(
        description="Placeholder element for fixedId extensions",
        default=None,
        alias="_fixedId",
    )
    fixedInstant: Optional[Instant] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedInstant_ext: Optional[Element] = Field(
        description="Placeholder element for fixedInstant extensions",
        default=None,
        alias="_fixedInstant",
    )
    fixedInteger: Optional[Integer] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedInteger_ext: Optional[Element] = Field(
        description="Placeholder element for fixedInteger extensions",
        default=None,
        alias="_fixedInteger",
    )
    fixedInteger64: Optional[Integer64] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedInteger64_ext: Optional[Element] = Field(
        description="Placeholder element for fixedInteger64 extensions",
        default=None,
        alias="_fixedInteger64",
    )
    fixedMarkdown: Optional[Markdown] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedMarkdown_ext: Optional[Element] = Field(
        description="Placeholder element for fixedMarkdown extensions",
        default=None,
        alias="_fixedMarkdown",
    )
    fixedOid: Optional[Oid] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedOid_ext: Optional[Element] = Field(
        description="Placeholder element for fixedOid extensions",
        default=None,
        alias="_fixedOid",
    )
    fixedPositiveInt: Optional[PositiveInt] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedPositiveInt_ext: Optional[Element] = Field(
        description="Placeholder element for fixedPositiveInt extensions",
        default=None,
        alias="_fixedPositiveInt",
    )
    fixedString: Optional[String] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedString_ext: Optional[Element] = Field(
        description="Placeholder element for fixedString extensions",
        default=None,
        alias="_fixedString",
    )
    fixedTime: Optional[Time] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedTime_ext: Optional[Element] = Field(
        description="Placeholder element for fixedTime extensions",
        default=None,
        alias="_fixedTime",
    )
    fixedUnsignedInt: Optional[UnsignedInt] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedUnsignedInt_ext: Optional[Element] = Field(
        description="Placeholder element for fixedUnsignedInt extensions",
        default=None,
        alias="_fixedUnsignedInt",
    )
    fixedUri: Optional[Uri] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedUri_ext: Optional[Element] = Field(
        description="Placeholder element for fixedUri extensions",
        default=None,
        alias="_fixedUri",
    )
    fixedUrl: Optional[Url] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedUrl_ext: Optional[Element] = Field(
        description="Placeholder element for fixedUrl extensions",
        default=None,
        alias="_fixedUrl",
    )
    fixedUuid: Optional[Uuid] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedUuid_ext: Optional[Element] = Field(
        description="Placeholder element for fixedUuid extensions",
        default=None,
        alias="_fixedUuid",
    )
    fixedAddress: Optional[Address] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedAge: Optional[Age] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedAnnotation: Optional[Annotation] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedAttachment: Optional[Attachment] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedCodeableConcept: Optional[CodeableConcept] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedCodeableReference: Optional[CodeableReference] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedCoding: Optional[Coding] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedContactPoint: Optional[ContactPoint] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedCount: Optional[Count] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedDistance: Optional[Distance] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedDuration: Optional[Duration] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedHumanName: Optional[HumanName] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedIdentifier: Optional[Identifier] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedMoney: Optional[Money] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedPeriod: Optional[Period] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedQuantity: Optional[Quantity] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedRange: Optional[Range] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedRatio: Optional[Ratio] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedRatioRange: Optional[RatioRange] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedReference: Optional[Reference] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedSampledData: Optional[SampledData] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedSignature: Optional[Signature] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedTiming: Optional[Timing] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedContactDetail: Optional[ContactDetail] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedDataRequirement: Optional[DataRequirement] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedExpression: Optional[Expression] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedParameterDefinition: Optional[ParameterDefinition] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedRelatedArtifact: Optional[RelatedArtifact] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedTriggerDefinition: Optional[TriggerDefinition] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedUsageContext: Optional[UsageContext] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedAvailability: Optional[Availability] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedExtendedContactDetail: Optional[ExtendedContactDetail] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedDosage: Optional[Dosage] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedMeta: Optional[Meta] = Field(
        description="Value must be exactly this",
        default=None,
    )
    patternBase64Binary: Optional[Base64Binary] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternBase64Binary_ext: Optional[Element] = Field(
        description="Placeholder element for patternBase64Binary extensions",
        default=None,
        alias="_patternBase64Binary",
    )
    patternBoolean: Optional[Boolean] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternBoolean_ext: Optional[Element] = Field(
        description="Placeholder element for patternBoolean extensions",
        default=None,
        alias="_patternBoolean",
    )
    patternCanonical: Optional[Canonical] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternCanonical_ext: Optional[Element] = Field(
        description="Placeholder element for patternCanonical extensions",
        default=None,
        alias="_patternCanonical",
    )
    patternCode: Optional[Code] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternCode_ext: Optional[Element] = Field(
        description="Placeholder element for patternCode extensions",
        default=None,
        alias="_patternCode",
    )
    patternDate: Optional[Date] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternDate_ext: Optional[Element] = Field(
        description="Placeholder element for patternDate extensions",
        default=None,
        alias="_patternDate",
    )
    patternDateTime: Optional[DateTime] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternDateTime_ext: Optional[Element] = Field(
        description="Placeholder element for patternDateTime extensions",
        default=None,
        alias="_patternDateTime",
    )
    patternDecimal: Optional[Decimal] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternDecimal_ext: Optional[Element] = Field(
        description="Placeholder element for patternDecimal extensions",
        default=None,
        alias="_patternDecimal",
    )
    patternId: Optional[Id] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternId_ext: Optional[Element] = Field(
        description="Placeholder element for patternId extensions",
        default=None,
        alias="_patternId",
    )
    patternInstant: Optional[Instant] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternInstant_ext: Optional[Element] = Field(
        description="Placeholder element for patternInstant extensions",
        default=None,
        alias="_patternInstant",
    )
    patternInteger: Optional[Integer] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternInteger_ext: Optional[Element] = Field(
        description="Placeholder element for patternInteger extensions",
        default=None,
        alias="_patternInteger",
    )
    patternInteger64: Optional[Integer64] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternInteger64_ext: Optional[Element] = Field(
        description="Placeholder element for patternInteger64 extensions",
        default=None,
        alias="_patternInteger64",
    )
    patternMarkdown: Optional[Markdown] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternMarkdown_ext: Optional[Element] = Field(
        description="Placeholder element for patternMarkdown extensions",
        default=None,
        alias="_patternMarkdown",
    )
    patternOid: Optional[Oid] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternOid_ext: Optional[Element] = Field(
        description="Placeholder element for patternOid extensions",
        default=None,
        alias="_patternOid",
    )
    patternPositiveInt: Optional[PositiveInt] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternPositiveInt_ext: Optional[Element] = Field(
        description="Placeholder element for patternPositiveInt extensions",
        default=None,
        alias="_patternPositiveInt",
    )
    patternString: Optional[String] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternString_ext: Optional[Element] = Field(
        description="Placeholder element for patternString extensions",
        default=None,
        alias="_patternString",
    )
    patternTime: Optional[Time] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternTime_ext: Optional[Element] = Field(
        description="Placeholder element for patternTime extensions",
        default=None,
        alias="_patternTime",
    )
    patternUnsignedInt: Optional[UnsignedInt] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternUnsignedInt_ext: Optional[Element] = Field(
        description="Placeholder element for patternUnsignedInt extensions",
        default=None,
        alias="_patternUnsignedInt",
    )
    patternUri: Optional[Uri] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternUri_ext: Optional[Element] = Field(
        description="Placeholder element for patternUri extensions",
        default=None,
        alias="_patternUri",
    )
    patternUrl: Optional[Url] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternUrl_ext: Optional[Element] = Field(
        description="Placeholder element for patternUrl extensions",
        default=None,
        alias="_patternUrl",
    )
    patternUuid: Optional[Uuid] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternUuid_ext: Optional[Element] = Field(
        description="Placeholder element for patternUuid extensions",
        default=None,
        alias="_patternUuid",
    )
    patternAddress: Optional[Address] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternAge: Optional[Age] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternAnnotation: Optional[Annotation] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternAttachment: Optional[Attachment] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternCodeableConcept: Optional[CodeableConcept] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternCodeableReference: Optional[CodeableReference] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternCoding: Optional[Coding] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternContactPoint: Optional[ContactPoint] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternCount: Optional[Count] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternDistance: Optional[Distance] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternDuration: Optional[Duration] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternHumanName: Optional[HumanName] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternIdentifier: Optional[Identifier] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternMoney: Optional[Money] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternPeriod: Optional[Period] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternQuantity: Optional[Quantity] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternRange: Optional[Range] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternRatio: Optional[Ratio] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternRatioRange: Optional[RatioRange] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternReference: Optional[Reference] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternSampledData: Optional[SampledData] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternSignature: Optional[Signature] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternTiming: Optional[Timing] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternContactDetail: Optional[ContactDetail] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternDataRequirement: Optional[DataRequirement] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternExpression: Optional[Expression] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternParameterDefinition: Optional[ParameterDefinition] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternRelatedArtifact: Optional[RelatedArtifact] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternTriggerDefinition: Optional[TriggerDefinition] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternUsageContext: Optional[UsageContext] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternAvailability: Optional[Availability] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternExtendedContactDetail: Optional[ExtendedContactDetail] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternDosage: Optional[Dosage] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternMeta: Optional[Meta] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    example: Optional[List[ElementDefinitionExample]] = Field(
        description="Example value (as defined for type)",
        default=None,
    )
    minValueDate: Optional[Date] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValueDate_ext: Optional[Element] = Field(
        description="Placeholder element for minValueDate extensions",
        default=None,
        alias="_minValueDate",
    )
    minValueDateTime: Optional[DateTime] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValueDateTime_ext: Optional[Element] = Field(
        description="Placeholder element for minValueDateTime extensions",
        default=None,
        alias="_minValueDateTime",
    )
    minValueInstant: Optional[Instant] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValueInstant_ext: Optional[Element] = Field(
        description="Placeholder element for minValueInstant extensions",
        default=None,
        alias="_minValueInstant",
    )
    minValueTime: Optional[Time] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValueTime_ext: Optional[Element] = Field(
        description="Placeholder element for minValueTime extensions",
        default=None,
        alias="_minValueTime",
    )
    minValueDecimal: Optional[Decimal] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValueDecimal_ext: Optional[Element] = Field(
        description="Placeholder element for minValueDecimal extensions",
        default=None,
        alias="_minValueDecimal",
    )
    minValueInteger: Optional[Integer] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValueInteger_ext: Optional[Element] = Field(
        description="Placeholder element for minValueInteger extensions",
        default=None,
        alias="_minValueInteger",
    )
    minValueInteger64: Optional[Integer64] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValueInteger64_ext: Optional[Element] = Field(
        description="Placeholder element for minValueInteger64 extensions",
        default=None,
        alias="_minValueInteger64",
    )
    minValuePositiveInt: Optional[PositiveInt] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValuePositiveInt_ext: Optional[Element] = Field(
        description="Placeholder element for minValuePositiveInt extensions",
        default=None,
        alias="_minValuePositiveInt",
    )
    minValueUnsignedInt: Optional[UnsignedInt] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValueUnsignedInt_ext: Optional[Element] = Field(
        description="Placeholder element for minValueUnsignedInt extensions",
        default=None,
        alias="_minValueUnsignedInt",
    )
    minValueQuantity: Optional[Quantity] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    maxValueDate: Optional[Date] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValueDate_ext: Optional[Element] = Field(
        description="Placeholder element for maxValueDate extensions",
        default=None,
        alias="_maxValueDate",
    )
    maxValueDateTime: Optional[DateTime] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValueDateTime_ext: Optional[Element] = Field(
        description="Placeholder element for maxValueDateTime extensions",
        default=None,
        alias="_maxValueDateTime",
    )
    maxValueInstant: Optional[Instant] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValueInstant_ext: Optional[Element] = Field(
        description="Placeholder element for maxValueInstant extensions",
        default=None,
        alias="_maxValueInstant",
    )
    maxValueTime: Optional[Time] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValueTime_ext: Optional[Element] = Field(
        description="Placeholder element for maxValueTime extensions",
        default=None,
        alias="_maxValueTime",
    )
    maxValueDecimal: Optional[Decimal] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValueDecimal_ext: Optional[Element] = Field(
        description="Placeholder element for maxValueDecimal extensions",
        default=None,
        alias="_maxValueDecimal",
    )
    maxValueInteger: Optional[Integer] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValueInteger_ext: Optional[Element] = Field(
        description="Placeholder element for maxValueInteger extensions",
        default=None,
        alias="_maxValueInteger",
    )
    maxValueInteger64: Optional[Integer64] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValueInteger64_ext: Optional[Element] = Field(
        description="Placeholder element for maxValueInteger64 extensions",
        default=None,
        alias="_maxValueInteger64",
    )
    maxValuePositiveInt: Optional[PositiveInt] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValuePositiveInt_ext: Optional[Element] = Field(
        description="Placeholder element for maxValuePositiveInt extensions",
        default=None,
        alias="_maxValuePositiveInt",
    )
    maxValueUnsignedInt: Optional[UnsignedInt] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValueUnsignedInt_ext: Optional[Element] = Field(
        description="Placeholder element for maxValueUnsignedInt extensions",
        default=None,
        alias="_maxValueUnsignedInt",
    )
    maxValueQuantity: Optional[Quantity] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxLength: Optional[Integer] = Field(
        description="Max length for string type data",
        default=None,
    )
    maxLength_ext: Optional[Element] = Field(
        description="Placeholder element for maxLength extensions",
        default=None,
        alias="_maxLength",
    )
    condition: Optional[List[Id]] = Field(
        description="Reference to invariant about presence",
        default=None,
    )
    condition_ext: Optional[List[Optional[Element]]] = Field(
        description="Placeholder element for condition extensions",
        default=None,
        alias="_condition",
    )
    constraint: Optional[List[ElementDefinitionConstraint]] = Field(
        description="Condition that must evaluate to True",
        default=None,
    )
    mustHaveValue: Optional[Boolean] = Field(
        description="For primitives, that a value must be present - not replaced by an extension",
        default=None,
    )
    mustHaveValue_ext: Optional[Element] = Field(
        description="Placeholder element for mustHaveValue extensions",
        default=None,
        alias="_mustHaveValue",
    )
    valueAlternatives: Optional[List[Canonical]] = Field(
        description="Extensions that are allowed to replace a primitive value",
        default=None,
    )
    valueAlternatives_ext: Optional[List[Optional[Element]]] = Field(
        description="Placeholder element for valueAlternatives extensions",
        default=None,
        alias="_valueAlternatives",
    )
    mustSupport: Optional[Boolean] = Field(
        description="If the element must be supported (discouraged - see obligations)",
        default=None,
    )
    mustSupport_ext: Optional[Element] = Field(
        description="Placeholder element for mustSupport extensions",
        default=None,
        alias="_mustSupport",
    )
    isModifier: Optional[Boolean] = Field(
        description="If this modifies the meaning of other elements",
        default=None,
    )
    isModifier_ext: Optional[Element] = Field(
        description="Placeholder element for isModifier extensions",
        default=None,
        alias="_isModifier",
    )
    isModifierReason: Optional[String] = Field(
        description="Reason that this element is marked as a modifier",
        default=None,
    )
    isModifierReason_ext: Optional[Element] = Field(
        description="Placeholder element for isModifierReason extensions",
        default=None,
        alias="_isModifierReason",
    )
    isSummary: Optional[Boolean] = Field(
        description="Include when _summary = True?",
        default=None,
    )
    isSummary_ext: Optional[Element] = Field(
        description="Placeholder element for isSummary extensions",
        default=None,
        alias="_isSummary",
    )
    binding: Optional[ElementDefinitionBinding] = Field(
        description="ValueSet details if this is coded",
        default=None,
    )
    mapping: Optional[List[ElementDefinitionMapping]] = Field(
        description="Map element to another set of definitions",
        default=None,
    )

    @property
    def defaultValue(self):
        return get_type_choice_value_by_base(
            self,
            base="defaultValue",
        )

    @property
    def fixed(self):
        return get_type_choice_value_by_base(
            self,
            base="fixed",
        )

    @property
    def pattern(self):
        return get_type_choice_value_by_base(
            self,
            base="pattern",
        )

    @property
    def minValue(self):
        return get_type_choice_value_by_base(
            self,
            base="minValue",
        )

    @property
    def maxValue(self):
        return get_type_choice_value_by_base(
            self,
            base="maxValue",
        )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return validate_element_constraint(
            self,
            elements=(
                "mapping",
                "binding",
                "isSummary",
                "isModifierReason",
                "isModifier",
                "mustSupport",
                "valueAlternatives",
                "mustHaveValue",
                "constraint",
                "condition",
                "maxLength",
                "example",
                "orderMeaning",
                "meaningWhenMissing",
                "type",
                "contentReference",
                "base",
                "max",
                "min",
                "alias",
                "requirements",
                "comment",
                "definition",
                "short",
                "slicing",
                "code",
                "label",
                "sliceIsConstraining",
                "sliceName",
                "representation",
                "path",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_3_constraint_validator(self):
        return validate_element_constraint(
            self,
            elements=("max",),
            expression="empty() or ($this = '*') or (toInteger() >= 0)",
            human='Max SHALL be a number or "*"',
            key="eld-3",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_4_constraint_validator(self):
        return validate_element_constraint(
            self,
            elements=("type",),
            expression="aggregation.empty() or (code = 'Reference') or (code = 'canonical') or (code = 'CodeableReference')",
            human="Aggregation may only be specified if one of the allowed types for the element is a reference",
            key="eld-4",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_17_constraint_validator(self):
        return validate_element_constraint(
            self,
            elements=("type",),
            expression="(code='Reference' or code = 'canonical' or code = 'CodeableReference') or targetProfile.empty()",
            human="targetProfile is only allowed if the type is Reference or canonical",
            key="eld-17",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_21_constraint_validator(self):
        return validate_element_constraint(
            self,
            elements=("constraint",),
            expression="expression.exists()",
            human="Constraints should have an expression or else validators will not be able to enforce them",
            key="eld-21",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_eld_26_constraint_validator(self):
        return validate_element_constraint(
            self,
            elements=("constraint",),
            expression="(severity = 'error') implies suppress.empty()",
            human="Errors cannot be suppressed",
            key="eld-26",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_12_constraint_validator(self):
        return validate_element_constraint(
            self,
            elements=("binding",),
            expression="valueSet.exists() implies (valueSet.startsWith('http:') or valueSet.startsWith('https') or valueSet.startsWith('urn:') or valueSet.startsWith('#'))",
            human="ValueSet SHALL start with http:// or https:// or urn: or #",
            key="eld-12",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_23_constraint_validator(self):
        return validate_element_constraint(
            self,
            elements=("binding",),
            expression="description.exists() or valueSet.exists()",
            human="binding SHALL have either description or valueSet",
            key="eld-23",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_model_validator(self):
        return validate_model_constraint(
            self,
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def defaultValue_type_choice_validator(self):
        return validate_type_choice_element(
            self,
            field_types=[
                "Base64Binary",
                "Boolean",
                "Canonical",
                "Code",
                "Date",
                "DateTime",
                "Decimal",
                "Id",
                "Instant",
                "Integer",
                "Integer64",
                "Markdown",
                "Oid",
                "PositiveInt",
                "String",
                "Time",
                "UnsignedInt",
                "Uri",
                "Url",
                "Uuid",
                "Address",
                "Age",
                "Annotation",
                "Attachment",
                "CodeableConcept",
                "CodeableReference",
                "Coding",
                "ContactPoint",
                "Count",
                "Distance",
                "Duration",
                "HumanName",
                "Identifier",
                "Money",
                "Period",
                "Quantity",
                "Range",
                "Ratio",
                "RatioRange",
                "Reference",
                "SampledData",
                "Signature",
                "Timing",
                "ContactDetail",
                "DataRequirement",
                "Expression",
                "ParameterDefinition",
                "RelatedArtifact",
                "TriggerDefinition",
                "UsageContext",
                "Availability",
                "ExtendedContactDetail",
                "Dosage",
                "Meta",
            ],
            field_name_base="defaultValue",
            required=False,
            non_allowed_types=[],
        )

    @model_validator(mode="after")
    def fixed_type_choice_validator(self):
        return validate_type_choice_element(
            self,
            field_types=[
                "Base64Binary",
                "Boolean",
                "Canonical",
                "Code",
                "Date",
                "DateTime",
                "Decimal",
                "Id",
                "Instant",
                "Integer",
                "Integer64",
                "Markdown",
                "Oid",
                "PositiveInt",
                "String",
                "Time",
                "UnsignedInt",
                "Uri",
                "Url",
                "Uuid",
                "Address",
                "Age",
                "Annotation",
                "Attachment",
                "CodeableConcept",
                "CodeableReference",
                "Coding",
                "ContactPoint",
                "Count",
                "Distance",
                "Duration",
                "HumanName",
                "Identifier",
                "Money",
                "Period",
                "Quantity",
                "Range",
                "Ratio",
                "RatioRange",
                "Reference",
                "SampledData",
                "Signature",
                "Timing",
                "ContactDetail",
                "DataRequirement",
                "Expression",
                "ParameterDefinition",
                "RelatedArtifact",
                "TriggerDefinition",
                "UsageContext",
                "Availability",
                "ExtendedContactDetail",
                "Dosage",
                "Meta",
            ],
            field_name_base="fixed",
            required=False,
            non_allowed_types=[],
        )

    @model_validator(mode="after")
    def pattern_type_choice_validator(self):
        return validate_type_choice_element(
            self,
            field_types=[
                "Base64Binary",
                "Boolean",
                "Canonical",
                "Code",
                "Date",
                "DateTime",
                "Decimal",
                "Id",
                "Instant",
                "Integer",
                "Integer64",
                "Markdown",
                "Oid",
                "PositiveInt",
                "String",
                "Time",
                "UnsignedInt",
                "Uri",
                "Url",
                "Uuid",
                "Address",
                "Age",
                "Annotation",
                "Attachment",
                "CodeableConcept",
                "CodeableReference",
                "Coding",
                "ContactPoint",
                "Count",
                "Distance",
                "Duration",
                "HumanName",
                "Identifier",
                "Money",
                "Period",
                "Quantity",
                "Range",
                "Ratio",
                "RatioRange",
                "Reference",
                "SampledData",
                "Signature",
                "Timing",
                "ContactDetail",
                "DataRequirement",
                "Expression",
                "ParameterDefinition",
                "RelatedArtifact",
                "TriggerDefinition",
                "UsageContext",
                "Availability",
                "ExtendedContactDetail",
                "Dosage",
                "Meta",
            ],
            field_name_base="pattern",
            required=False,
            non_allowed_types=[],
        )

    @model_validator(mode="after")
    def minValue_type_choice_validator(self):
        return validate_type_choice_element(
            self,
            field_types=[
                "Date",
                "DateTime",
                "Instant",
                "Time",
                "Decimal",
                "Integer",
                "Integer64",
                "PositiveInt",
                "UnsignedInt",
                "Quantity",
            ],
            field_name_base="minValue",
            required=False,
            non_allowed_types=[],
        )

    @model_validator(mode="after")
    def maxValue_type_choice_validator(self):
        return validate_type_choice_element(
            self,
            field_types=[
                "Date",
                "DateTime",
                "Instant",
                "Time",
                "Decimal",
                "Integer",
                "Integer64",
                "PositiveInt",
                "UnsignedInt",
                "Quantity",
            ],
            field_name_base="maxValue",
            required=False,
            non_allowed_types=[],
        )

    @model_validator(mode="after")
    def FHIR_eld_2_constraint_model_validator(self):
        return validate_model_constraint(
            self,
            expression="min.empty() or max.empty() or (max = '*') or iif(max != '*', min <= max.toInteger())",
            human="Min <= Max",
            key="eld-2",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_5_constraint_model_validator(self):
        return validate_model_constraint(
            self,
            expression="contentReference.empty() or (type.empty() and defaultValue.empty() and fixed.empty() and pattern.empty() and example.empty() and minValue.empty() and maxValue.empty() and maxLength.empty() and binding.empty())",
            human="if the element definition has a contentReference, it cannot have type, defaultValue, fixed, pattern, example, minValue, maxValue, maxLength, or binding",
            key="eld-5",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_6_constraint_model_validator(self):
        return validate_model_constraint(
            self,
            expression="fixed.empty() or (type.count()  <= 1)",
            human="Fixed value may only be specified if there is one type",
            key="eld-6",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_7_constraint_model_validator(self):
        return validate_model_constraint(
            self,
            expression="pattern.empty() or (type.count() <= 1)",
            human="Pattern may only be specified if there is one type",
            key="eld-7",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_8_constraint_model_validator(self):
        return validate_model_constraint(
            self,
            expression="pattern.empty() or fixed.empty()",
            human="Pattern and fixed are mutually exclusive",
            key="eld-8",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_11_constraint_model_validator(self):
        return validate_model_constraint(
            self,
            expression="binding.empty() or type.code.empty() or type.select(code.contains(':')).exists() or type.select((code = 'code') or (code = 'Coding') or (code='CodeableConcept') or (code = 'Quantity') or (code = 'string') or (code = 'uri') or (code = 'Duration')).exists()",
            human="Binding can only be present for coded elements, string, and uri if using FHIR-defined types",
            key="eld-11",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_13_constraint_model_validator(self):
        return validate_model_constraint(
            self,
            expression="type.select(code).isDistinct()",
            human="Types must be unique by code",
            key="eld-13",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_14_constraint_model_validator(self):
        return validate_model_constraint(
            self,
            expression="constraint.select(key).isDistinct()",
            human="Constraints must be unique by key",
            key="eld-14",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_15_constraint_model_validator(self):
        return validate_model_constraint(
            self,
            expression="defaultValue.empty() or meaningWhenMissing.empty()",
            human="default value and meaningWhenMissing are mutually exclusive",
            key="eld-15",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_16_constraint_model_validator(self):
        return validate_model_constraint(
            self,
            expression="sliceName.empty() or sliceName.matches('^[a-zA-Z0-9\\/\\-_\\[\\]\\@]+$')",
            human='sliceName must be composed of proper tokens separated by "/"',
            key="eld-16",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_18_constraint_model_validator(self):
        return validate_model_constraint(
            self,
            expression="(isModifier.exists() and isModifier) implies isModifierReason.exists()",
            human="Must have a modifier reason if isModifier = True",
            key="eld-18",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_19_constraint_model_validator(self):
        return validate_model_constraint(
            self,
            expression="""path.matches('^[^\\s\\.,:;\\\'"\\/|?!@#$%&*()\\[\\]{}]{1,64}(\\.[^\\s\\.,:;\\\'"\\/|?!@#$%&*()\\[\\]{}]{1,64}(\\[x\\])?(\\:[^\\s\\.]+)?)*$')""",
            human="Element path SHALL be expressed as a set of '.'-separated components with each component restricted to a maximum of 64 characters and with some limits on the allowed choice of characters",
            key="eld-19",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_20_constraint_model_validator(self):
        return validate_model_constraint(
            self,
            expression="""path.matches('^[A-Za-z][A-Za-z0-9]{0,63}(\\.[a-z][A-Za-z0-9]{0,63}(\\[x])?)*$')""",
            human="The first component of the path should be UpperCamelCase.  Additional components (following a '.') should be lowerCamelCase.  If this syntax is not adhered to, code generation tools may be broken. Logical models may be less concerned about this implication.",
            key="eld-20",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_eld_22_constraint_model_validator(self):
        return validate_model_constraint(
            self,
            expression="sliceIsConstraining.exists() implies sliceName.exists()",
            human="sliceIsConstraining can only appear if slicename is present",
            key="eld-22",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_24_constraint_model_validator(self):
        return validate_model_constraint(
            self,
            expression="fixed.exists().not()",
            human="pattern[x] should be used rather than fixed[x]",
            key="eld-24",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_eld_25_constraint_model_validator(self):
        return validate_model_constraint(
            self,
            expression="orderMeaning.empty() implies slicing.where(rules='openAtEnd' or ordered).exists().not()",
            human="Order has no meaning (and cannot be asserted to have meaning), so enforcing rules on order is improper",
            key="eld-25",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_eld_27_constraint_model_validator(self):
        return validate_model_constraint(
            self,
            expression="mapping.select(identity).isDistinct()",
            human="Mappings SHOULD be unique by key",
            key="eld-27",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_eld_28_constraint_model_validator(self):
        return validate_model_constraint(
            self,
            expression="mustHaveValue.value implies valueAlternatives.empty()",
            human="Can't have valueAlternatives if mustHaveValue is True",
            key="eld-28",
            severity="error",
        )
