from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.datatypes.R4B.primitive as fhir
from fhircraft.fhir.resources.validators import (
    get_type_choice_value_by_base,
    validate_element_constraint,
    validate_model_constraint,
    validate_type_choice_element,
)
from fhircraft.fhir.resources.datatypes.R4B.complex import (
    BackboneElement,
    Address,
    Age,
    Annotation,
    CodeableConcept,
    CodeableReference,
    Coding,
    Attachment,
    ContactPoint,
    ContactDetail,
    Count,
    Contributor,
    DataRequirement,
    Distance,
    Duration,
    Dosage,
    Duration,
    Element,
    Expression,
    HumanName,
    Identifier,
    Money,
    ParameterDefinition,
    Period,
    Quantity,
    Range,
    Ratio,
    RatioRange,
    Reference,
    RelatedArtifact,
    SampledData,
    Signature,
    Timing,
    TriggerDefinition,
    UsageContext,
)


class ElementDefinitionSlicingDiscriminator(Element):
    """
    Designates which child elements are used to discriminate between the slices when processing an instance. If one or more discriminators are provided, the value of the child elements in the instance data SHALL completely distinguish which slice the element in the resource matches based on the allowed values for those elements in each of the slices.
    """

    _type = "ElementDefinitionSlicingDiscriminator"

    type: fhir.code = Field(
        description="value | exists | pattern | type | profile",
    )
    path: fhir.string = Field(
        description="Path to element value",
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
    description: Optional[fhir.string] = Field(
        description="Text description of how slicing works (or not)",
        default=None,
    )
    ordered: Optional[fhir.boolean] = Field(
        description="If elements must be in same order as slices",
        default=None,
    )
    rules: fhir.code = Field(
        description="closed | open | openAtEnd",
    )


class ElementDefinitionBase(Element):
    """
    Information about the base definition of the element, provided to make it unnecessary for tools to trace the deviation of the element through the derived and related profiles. When the element definition is not the original definition of an element - i.g. either in a constraint on another type, or for elements from a super type in a snap shot - then the information in provided in the element definition may be different to the base definition. On the original definition of the element, it will be same.
    """

    _type = "ElementDefinitionBase"

    path: fhir.string = Field(
        description="Path that identifies the base element",
    )
    min: fhir.unsignedInt = Field(
        description="Min cardinality of the base element",
    )
    max: fhir.string = Field(
        description="Max cardinality of the base element",
    )


class ElementDefinitionType(Element):
    """
    The data type or resource that the value of this element is permitted to be.
    """

    _type = "ElementDefinitionType"

    code: fhir.uri = Field(
        description="Data type or Resource (reference to definition)",
    )
    profile: Optional[List[fhir.canonical]] = Field(
        description="Profiles (StructureDefinition or IG) - one must apply",
        default=None,
    )
    targetProfile: Optional[List[fhir.canonical]] = Field(
        description="Profile (StructureDefinition or IG) on the Reference/canonical target - one must apply",
        default=None,
    )
    aggregation: Optional[List[fhir.code]] = Field(
        description="contained | referenced | bundled - how aggregated",
        default=None,
    )
    versioning: Optional[fhir.code] = Field(
        description="either | independent | specific",
        default=None,
    )


class ElementDefinitionExample(Element):
    """
    A sample value for this element demonstrating the type of information that would typically be found in the element.
    """

    _type = "ElementDefinitionExample"

    label: fhir.string = Field(
        description="Describes the purpose of this example",
    )
    valueBase64Binary: Optional[fhir.base64Binary] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueBoolean: Optional[fhir.boolean] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueCanonical: Optional[fhir.canonical] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueCode: Optional[fhir.code] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueDate: Optional[fhir.date_] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueDateTime: Optional[fhir.dateTime] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueDecimal: Optional[fhir.decimal] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueId: Optional[fhir.id_] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueInstant: Optional[fhir.instant] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueInteger: Optional[fhir.integer] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueMarkdown: Optional[fhir.markdown] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueOid: Optional[fhir.oid] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valuePositiveInt: Optional[fhir.positiveInt] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueString: Optional[fhir.string] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueTime: Optional[fhir.time_] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueUnsignedInt: Optional[fhir.unsignedInt] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueUri: Optional[fhir.uri] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueUrl: Optional[fhir.url] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
    )
    valueUuid: Optional[fhir.uuid] = Field(
        description="Value of Example (one of allowed types)",
        default=None,
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
    valueContributor: Optional[Contributor] = Field(
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
    valueDosage: Optional[Dosage] = Field(
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
    def value_type_choice_validator(self):
        return validate_type_choice_element(
            self,
            field_types=[
                fhir.Base64Binary,
                fhir.Boolean,
                fhir.Canonical,
                fhir.Code,
                fhir.Date,
                fhir.DateTime,
                fhir.Decimal,
                fhir.Id,
                fhir.Instant,
                fhir.Integer,
                fhir.Markdown,
                fhir.Oid,
                fhir.PositiveInt,
                fhir.String,
                fhir.Time,
                fhir.UnsignedInt,
                fhir.Uri,
                fhir.Url,
                fhir.Uuid,
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
                "Contributor",
                "DataRequirement",
                "Expression",
                "ParameterDefinition",
                "RelatedArtifact",
                "TriggerDefinition",
                "UsageContext",
                "Dosage",
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

    key: fhir.id_ = Field(
        description="Target of \u0027condition\u0027 reference above",
    )
    requirements: Optional[fhir.string] = Field(
        description="Why this constraint is necessary or appropriate",
        default=None,
    )
    severity: fhir.code = Field(
        description="error | warning",
    )
    human: fhir.string = Field(
        description="Human description of constraint",
    )
    expression: Optional[fhir.string] = Field(
        description="FHIRPath expression of constraint",
        default=None,
    )
    xpath: Optional[fhir.string] = Field(
        description="XPath expression of constraint",
        default=None,
    )
    source: Optional[fhir.canonical] = Field(
        description="Reference to original source of constraint",
        default=None,
    )


class ElementDefinitionBinding(Element):
    """
    Binds to a value set if this element is coded (code, Coding, CodeableConcept, Quantity), or the data types (string, uri).
    """

    _type = "ElementDefinitionBinding"

    strength: fhir.code = Field(
        description="required | extensible | preferred | example",
    )
    description: Optional[fhir.string] = Field(
        description="Human explanation of the value set",
        default=None,
    )
    valueSet: Optional[fhir.canonical] = Field(
        description="Source of value set",
        default=None,
    )


class ElementDefinitionMapping(Element):
    """
    Identifies a concept from an external specification that roughly corresponds to this element.
    """

    _type = "ElementDefinitionMapping"

    identity: fhir.id_ = Field(
        description="Reference to mapping declaration",
    )
    language: Optional[fhir.code] = Field(
        description="Computable language of mapping",
        default=None,
    )
    map: fhir.string = Field(
        description="Details of the mapping",
    )
    comment: Optional[fhir.string] = Field(
        description="Comments about the mapping or its use",
        default=None,
    )


class ElementDefinition(BackboneElement):
    """
    Base StructureDefinition for ElementDefinition Type: Captures constraints on each element within the resource, profile, or extension.
    """

    _type = "ElementDefinition"

    path: fhir.string = Field(
        description="Path of the element in the hierarchy of elements",
    )
    representation: Optional[List[fhir.code]] = Field(
        description="xmlAttr | xmlText | typeAttr | cdaText | xhtml",
        default=None,
    )
    sliceName: Optional[fhir.string] = Field(
        description="Name for this particular element (in a set of slices)",
        default=None,
    )
    sliceIsConstraining: Optional[fhir.boolean] = Field(
        description="If this slice definition constrains an inherited slice definition (or not)",
        default=None,
    )
    label: Optional[fhir.string] = Field(
        description="Name for element to display with or prompt for element",
        default=None,
    )
    code: Optional[List[Coding]] = Field(
        description="Corresponding codes in terminologies",
        default=None,
    )
    slicing: Optional[ElementDefinitionSlicing] = Field(
        description="This element is sliced - slices follow",
        default=None,
    )
    short: Optional[fhir.string] = Field(
        description="Concise definition for space-constrained presentation",
        default=None,
    )
    definition: Optional[fhir.markdown] = Field(
        description="Full formal definition as narrative text",
        default=None,
    )
    comment: Optional[fhir.markdown] = Field(
        description="Comments about the use of this element",
        default=None,
    )
    requirements: Optional[fhir.markdown] = Field(
        description="Why this resource has been created",
        default=None,
    )
    alias: Optional[List[fhir.string]] = Field(
        description="Other names",
        default=None,
    )
    min: Optional[fhir.unsignedInt] = Field(
        description="Minimum Cardinality",
        default=None,
    )
    max: Optional[fhir.string] = Field(
        description="Maximum Cardinality (a number or *)",
        default=None,
    )
    base: Optional[ElementDefinitionBase] = Field(
        description="Base definition information for tools",
        default=None,
    )
    contentReference: Optional[fhir.uri] = Field(
        description="Reference to definition of content for the element",
        default=None,
    )
    type: Optional[List[ElementDefinitionType]] = Field(
        description="Data type and Profile for this element",
        default=None,
    )
    defaultValueBase64Binary: Optional[fhir.base64Binary] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueBoolean: Optional[fhir.boolean] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueCanonical: Optional[fhir.canonical] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueCode: Optional[fhir.code] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueDate: Optional[fhir.date_] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueDateTime: Optional[fhir.dateTime] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueDecimal: Optional[fhir.decimal] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueId: Optional[fhir.id_] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueInstant: Optional[fhir.instant] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueInteger: Optional[fhir.integer] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueMarkdown: Optional[fhir.markdown] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueOid: Optional[fhir.oid] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValuePositiveInt: Optional[fhir.positiveInt] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueString: Optional[fhir.string] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueTime: Optional[fhir.time_] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueUnsignedInt: Optional[fhir.unsignedInt] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueUri: Optional[fhir.uri] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueUrl: Optional[fhir.url] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueUuid: Optional[fhir.uuid] = Field(
        description="Specified value if missing from instance",
        default=None,
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
    defaultValueContributor: Optional[Contributor] = Field(
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
    defaultValueDosage: Optional[Dosage] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    meaningWhenMissing: Optional[fhir.markdown] = Field(
        description="Implicit meaning when this element is missing",
        default=None,
    )
    orderMeaning: Optional[fhir.string] = Field(
        description="What the order of the elements means",
        default=None,
    )
    fixedBase64Binary: Optional[fhir.base64Binary] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedBoolean: Optional[fhir.boolean] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedCanonical: Optional[fhir.canonical] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedCode: Optional[fhir.code] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedDate: Optional[fhir.date_] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedDateTime: Optional[fhir.dateTime] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedDecimal: Optional[fhir.decimal] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedId: Optional[fhir.id_] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedInstant: Optional[fhir.instant] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedInteger: Optional[fhir.integer] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedMarkdown: Optional[fhir.markdown] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedOid: Optional[fhir.oid] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedPositiveInt: Optional[fhir.positiveInt] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedString: Optional[fhir.string] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedTime: Optional[fhir.time_] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedUnsignedInt: Optional[fhir.unsignedInt] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedUri: Optional[fhir.uri] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedUrl: Optional[fhir.url] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedUuid: Optional[fhir.uuid] = Field(
        description="Value must be exactly this",
        default=None,
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
    fixedContributor: Optional[Contributor] = Field(
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
    fixedDosage: Optional[Dosage] = Field(
        description="Value must be exactly this",
        default=None,
    )
    patternBase64Binary: Optional[fhir.base64Binary] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternBoolean: Optional[fhir.boolean] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternCanonical: Optional[fhir.canonical] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternCode: Optional[fhir.code] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternDate: Optional[fhir.date_] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternDateTime: Optional[fhir.dateTime] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternDecimal: Optional[fhir.decimal] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternId: Optional[fhir.id_] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternInstant: Optional[fhir.instant] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternInteger: Optional[fhir.integer] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternMarkdown: Optional[fhir.markdown] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternOid: Optional[fhir.oid] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternPositiveInt: Optional[fhir.positiveInt] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternString: Optional[fhir.string] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternTime: Optional[fhir.time_] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternUnsignedInt: Optional[fhir.unsignedInt] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternUri: Optional[fhir.uri] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternUrl: Optional[fhir.url] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternUuid: Optional[fhir.uuid] = Field(
        description="Value must have at least these property values",
        default=None,
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
    patternContributor: Optional[Contributor] = Field(
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
    patternDosage: Optional[Dosage] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    example: Optional[List[ElementDefinitionExample]] = Field(
        description="Example value (as defined for type)",
        default=None,
    )
    minValueDate: Optional[fhir.date_] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValueDateTime: Optional[fhir.dateTime] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValueInstant: Optional[fhir.instant] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValueTime: Optional[fhir.time_] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValueDecimal: Optional[fhir.decimal] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValueInteger: Optional[fhir.integer] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValuePositiveInt: Optional[fhir.positiveInt] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValueUnsignedInt: Optional[fhir.unsignedInt] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValueQuantity: Optional[Quantity] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    maxValueDate: Optional[fhir.date_] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValueDateTime: Optional[fhir.dateTime] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValueInstant: Optional[fhir.instant] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValueTime: Optional[fhir.time_] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValueDecimal: Optional[fhir.decimal] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValueInteger: Optional[fhir.integer] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValuePositiveInt: Optional[fhir.positiveInt] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValueUnsignedInt: Optional[fhir.unsignedInt] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValueQuantity: Optional[Quantity] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxLength: Optional[fhir.integer] = Field(
        description="Max length for strings",
        default=None,
    )
    condition: Optional[List[fhir.id_]] = Field(
        description="Reference to invariant about presence",
        default=None,
    )
    constraint: Optional[List[ElementDefinitionConstraint]] = Field(
        description="Condition that must evaluate to True",
        default=None,
    )
    mustSupport: Optional[fhir.boolean] = Field(
        description="If the element must be supported",
        default=None,
    )
    isModifier: Optional[fhir.boolean] = Field(
        description="If this modifies the meaning of other elements",
        default=None,
    )
    isModifierReason: Optional[fhir.string] = Field(
        description="Reason that this element is marked as a modifier",
        default=None,
    )
    isSummary: Optional[fhir.boolean] = Field(
        description="Include when _summary = True?",
        default=None,
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
    def FHIR_eld_1_constraint_validator(self):
        return validate_element_constraint(
            self,
            elements=("slicing",),
            expression="discriminator.exists() or description.exists()",
            human="If there are no discriminators, there must be a definition",
            key="eld-1",
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
            expression="aggregation.empty() or (code = 'Reference') or (code = 'canonical')",
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
    def FHIR_eld_12_constraint_validator(self):
        return validate_element_constraint(
            self,
            elements=("binding",),
            expression="valueSet.exists() implies (valueSet.startsWith('http:') or valueSet.startsWith('https') or valueSet.startsWith('urn:') or valueSet.startsWith('#'))",
            human="ValueSet SHALL start with http:// or https:// or urn:",
            key="eld-12",
            severity="error",
        )

    @model_validator(mode="after")
    def defaultValue_type_choice_validator(self):
        return validate_type_choice_element(
            self,
            field_types=[
                fhir.Base64Binary,
                fhir.Boolean,
                fhir.Canonical,
                fhir.Code,
                fhir.Date,
                fhir.DateTime,
                fhir.Decimal,
                fhir.Id,
                fhir.Instant,
                fhir.Integer,
                fhir.Markdown,
                fhir.Oid,
                fhir.PositiveInt,
                fhir.String,
                fhir.Time,
                fhir.UnsignedInt,
                fhir.Uri,
                fhir.Url,
                fhir.Uuid,
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
                "Contributor",
                "DataRequirement",
                "Expression",
                "ParameterDefinition",
                "RelatedArtifact",
                "TriggerDefinition",
                "UsageContext",
                "Dosage",
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
                fhir.Base64Binary,
                fhir.Boolean,
                fhir.Canonical,
                fhir.Code,
                fhir.Date,
                fhir.DateTime,
                fhir.Decimal,
                fhir.Id,
                fhir.Instant,
                fhir.Integer,
                fhir.Markdown,
                fhir.Oid,
                fhir.PositiveInt,
                fhir.String,
                fhir.Time,
                fhir.UnsignedInt,
                fhir.Uri,
                fhir.Url,
                fhir.Uuid,
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
                "Contributor",
                "DataRequirement",
                "Expression",
                "ParameterDefinition",
                "RelatedArtifact",
                "TriggerDefinition",
                "UsageContext",
                "Dosage",
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
                fhir.Base64Binary,
                fhir.Boolean,
                fhir.Canonical,
                fhir.Code,
                fhir.Date,
                fhir.DateTime,
                fhir.Decimal,
                fhir.Id,
                fhir.Instant,
                fhir.Integer,
                fhir.Markdown,
                fhir.Oid,
                fhir.PositiveInt,
                fhir.String,
                fhir.Time,
                fhir.UnsignedInt,
                fhir.Uri,
                fhir.Url,
                fhir.Uuid,
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
                "Contributor",
                "DataRequirement",
                "Expression",
                "ParameterDefinition",
                "RelatedArtifact",
                "TriggerDefinition",
                "UsageContext",
                "Dosage",
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
                "date",
                "dateTime",
                "instant",
                "time",
                "decimal",
                "integer",
                "positiveInt",
                "unsignedInt",
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
                "date",
                "dateTime",
                "instant",
                "time",
                "decimal",
                "integer",
                "positiveInt",
                "unsignedInt",
                "Quantity",
            ],
            field_name_base="maxValue",
            required=False,
            non_allowed_types=[],
        )

    @model_validator(mode="after")
    def FHIR_eld_2_constraint_validator(self):
        return validate_model_constraint(
            self,
            expression="min.empty() or max.empty() or (max = '*') or iif(max != '*', min <= max.toInteger())",
            human="Min <= Max",
            key="eld-2",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_5_constraint_validator(self):
        return validate_model_constraint(
            self,
            expression="contentReference.empty() or (type.empty() and defaultValue.empty() and fixed.empty() and pattern.empty() and example.empty() and minValue.empty() and maxValue.empty() and maxLength.empty() and binding.empty())",
            human="if the element definition has a contentReference, it cannot have type, defaultValue, fixed, pattern, example, minValue, maxValue, maxLength, or binding",
            key="eld-5",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_6_constraint_validator(self):
        return validate_model_constraint(
            self,
            expression="fixed.empty() or (type.count()  <= 1)",
            human="Fixed value may only be specified if there is one type",
            key="eld-6",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_7_constraint_validator(self):
        return validate_model_constraint(
            self,
            expression="pattern.empty() or (type.count() <= 1)",
            human="Pattern may only be specified if there is one type",
            key="eld-7",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_8_constraint_validator(self):
        return validate_model_constraint(
            self,
            expression="pattern.empty() or fixed.empty()",
            human="Pattern and fixed are mutually exclusive",
            key="eld-8",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_11_constraint_validator(self):
        return validate_model_constraint(
            self,
            expression="binding.empty() or type.code.empty() or type.select((code = 'code') or (code = 'Coding') or (code='CodeableConcept') or (code = 'Quantity') or (code = 'string') or (code = 'uri') or (code = 'Duration')).exists()",
            human="Binding can only be present for coded elements, string, and uri",
            key="eld-11",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_13_constraint_validator(self):
        return validate_model_constraint(
            self,
            expression="type.select(code).isDistinct()",
            human="Types must be unique by code",
            key="eld-13",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_14_constraint_validator(self):
        return validate_model_constraint(
            self,
            expression="constraint.select(key).isDistinct()",
            human="Constraints must be unique by key",
            key="eld-14",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_15_constraint_validator(self):
        return validate_model_constraint(
            self,
            expression="defaultValue.empty() or meaningWhenMissing.empty()",
            human="default value and meaningWhenMissing are mutually exclusive",
            key="eld-15",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_16_constraint_validator(self):
        return validate_model_constraint(
            self,
            expression="sliceName.empty() or sliceName.matches('^[a-zA-Z0-9\\/\\-_\\[\\]\\@]+$')",
            human='sliceName must be composed of proper tokens separated by"/"',
            key="eld-16",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_18_constraint_validator(self):
        return validate_model_constraint(
            self,
            expression="(isModifier.exists() and isModifier) implies isModifierReason.exists()",
            human="Must have a modifier reason if isModifier = True",
            key="eld-18",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_19_constraint_validator(self):
        return validate_model_constraint(
            self,
            expression="""path.matches('^[^\\s\\.,:;\\\'"\\/|?!@#$%&*()\\[\\]{}]{1,64}(\\.[^\\s\\.,:;\\\'"\\/|?!@#$%&*()\\[\\]{}]{1,64}(\\[x\\])?(\\:[^\\s\\.]+)?)*$')""",
            human="Element path SHALL be expressed as a set of '.'-separated components with each component restricted to a maximum of 64 characters and with some limits on the allowed choice of characters",
            key="eld-19",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_20_constraint_validator(self):
        return validate_model_constraint(
            self,
            expression="""path.matches('^[A-Za-z][A-Za-z0-9]*(\\.[a-z][A-Za-z0-9]*(\\[x])?)*$')""",
            human="The first component of the path should be UpperCamelCase.  Additional components (following a '.') should be lowerCamelCase.  If this syntax is not adhered to, code generation tools may be broken. Logical models may be less concerned about this implication.",
            key="eld-20",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_eld_22_constraint_validator(self):
        return validate_model_constraint(
            self,
            expression="sliceIsConstraining.exists() implies sliceName.exists()",
            human="sliceIsConstraining can only appear if slicename is present",
            key="eld-22",
            severity="error",
        )
