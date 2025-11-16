from typing import List, Optional

from pydantic import Field, field_validator, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *

from fhircraft.fhir.resources.datatypes.R4.complex import (
    Address,
    Age,
    Annotation,
    Attachment,
    CodeableConcept,
    Coding,
    ContactDetail,
    ContactPoint,
    Contributor,
    Count,
    DataRequirement,
    Distance,
    Dosage,
    Duration,
    Element,
    BackboneElement,
    Expression,
    HumanName,
    Identifier,
    Meta,
    Money,
    ParameterDefinition,
    Period,
    Quantity,
    Range,
    Ratio,
    Reference,
    RelatedArtifact,
    SampledData,
    Signature,
    Timing,
    TriggerDefinition,
    UsageContext,
)


class ElementDefinition(BackboneElement):
    """
    Definition of an element in a resource or extension
    """

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
    representation_ext: Optional[Element] = Field(
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
    code: Optional[List["Coding"]] = Field(
        description="Corresponding codes in terminologies",
        default=None,
    )
    slicing: Optional[Element] = Field(
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
    alias_ext: Optional[Element] = Field(
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
    base: Optional[Element] = Field(
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
    type: Optional[List[Element]] = Field(
        description="Data type and Profile for this element",
        default=None,
    )
    defaultValueBase64Binary: Optional[Base64Binary] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueBoolean: Optional[Boolean] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueCanonical: Optional[Canonical] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueCode: Optional[Code] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueDate: Optional[Date] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueDateTime: Optional[DateTime] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueDecimal: Optional[Decimal] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueId: Optional[Id] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueInstant: Optional[Instant] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueInteger: Optional[Integer] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueMarkdown: Optional[Markdown] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueOid: Optional[Oid] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValuePositiveInt: Optional[PositiveInt] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueString: Optional[String] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueTime: Optional[Time] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueUnsignedInt: Optional[UnsignedInt] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueUri: Optional[Uri] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueUrl: Optional[Url] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueUuid: Optional[Uuid] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueAddress: Optional["Address"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueAge: Optional["Age"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueAnnotation: Optional["Annotation"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueAttachment: Optional["Attachment"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueCodeableConcept: Optional["CodeableConcept"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueCoding: Optional["Coding"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueContactPoint: Optional["ContactPoint"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueCount: Optional["Count"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueDistance: Optional["Distance"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueDuration: Optional["Duration"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueHumanName: Optional["HumanName"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueIdentifier: Optional["Identifier"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueMoney: Optional["Money"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValuePeriod: Optional["Period"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueQuantity: Optional["Quantity"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueRange: Optional["Range"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueRatio: Optional["Ratio"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueReference: Optional["Reference"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueSampledData: Optional["SampledData"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueSignature: Optional["Signature"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueTiming: Optional["Timing"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueContactDetail: Optional["ContactDetail"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueContributor: Optional["Contributor"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueDataRequirement: Optional["DataRequirement"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueExpression: Optional["Expression"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueParameterDefinition: Optional["ParameterDefinition"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueRelatedArtifact: Optional["RelatedArtifact"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueTriggerDefinition: Optional["TriggerDefinition"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueUsageContext: Optional["UsageContext"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueDosage: Optional["Dosage"] = Field(
        description="Specified value if missing from instance",
        default=None,
    )
    defaultValueMeta: Optional["Meta"] = Field(
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
    fixedBoolean: Optional[Boolean] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedCanonical: Optional[Canonical] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedCode: Optional[Code] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedDate: Optional[Date] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedDateTime: Optional[DateTime] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedDecimal: Optional[Decimal] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedId: Optional[Id] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedInstant: Optional[Instant] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedInteger: Optional[Integer] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedMarkdown: Optional[Markdown] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedOid: Optional[Oid] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedPositiveInt: Optional[PositiveInt] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedString: Optional[String] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedTime: Optional[Time] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedUnsignedInt: Optional[UnsignedInt] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedUri: Optional[Uri] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedUrl: Optional[Url] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedUuid: Optional[Uuid] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedAddress: Optional["Address"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedAge: Optional["Age"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedAnnotation: Optional["Annotation"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedAttachment: Optional["Attachment"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedCodeableConcept: Optional["CodeableConcept"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedCoding: Optional["Coding"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedContactPoint: Optional["ContactPoint"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedCount: Optional["Count"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedDistance: Optional["Distance"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedDuration: Optional["Duration"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedHumanName: Optional["HumanName"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedIdentifier: Optional["Identifier"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedMoney: Optional["Money"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedPeriod: Optional["Period"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedQuantity: Optional["Quantity"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedRange: Optional["Range"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedRatio: Optional["Ratio"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedReference: Optional["Reference"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedSampledData: Optional["SampledData"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedSignature: Optional["Signature"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedTiming: Optional["Timing"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedContactDetail: Optional["ContactDetail"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedContributor: Optional["Contributor"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedDataRequirement: Optional["DataRequirement"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedExpression: Optional["Expression"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedParameterDefinition: Optional["ParameterDefinition"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedRelatedArtifact: Optional["RelatedArtifact"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedTriggerDefinition: Optional["TriggerDefinition"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedUsageContext: Optional["UsageContext"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedDosage: Optional["Dosage"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    fixedMeta: Optional["Meta"] = Field(
        description="Value must be exactly this",
        default=None,
    )
    patternBase64Binary: Optional[Base64Binary] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternBoolean: Optional[Boolean] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternCanonical: Optional[Canonical] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternCode: Optional[Code] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternDate: Optional[Date] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternDateTime: Optional[DateTime] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternDecimal: Optional[Decimal] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternId: Optional[Id] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternInstant: Optional[Instant] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternInteger: Optional[Integer] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternMarkdown: Optional[Markdown] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternOid: Optional[Oid] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternPositiveInt: Optional[PositiveInt] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternString: Optional[String] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternTime: Optional[Time] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternUnsignedInt: Optional[UnsignedInt] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternUri: Optional[Uri] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternUrl: Optional[Url] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternUuid: Optional[Uuid] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternAddress: Optional["Address"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternAge: Optional["Age"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternAnnotation: Optional["Annotation"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternAttachment: Optional["Attachment"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternCodeableConcept: Optional["CodeableConcept"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternCoding: Optional["Coding"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternContactPoint: Optional["ContactPoint"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternCount: Optional["Count"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternDistance: Optional["Distance"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternDuration: Optional["Duration"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternHumanName: Optional["HumanName"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternIdentifier: Optional["Identifier"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternMoney: Optional["Money"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternPeriod: Optional["Period"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternQuantity: Optional["Quantity"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternRange: Optional["Range"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternRatio: Optional["Ratio"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternReference: Optional["Reference"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternSampledData: Optional["SampledData"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternSignature: Optional["Signature"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternTiming: Optional["Timing"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternContactDetail: Optional["ContactDetail"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternContributor: Optional["Contributor"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternDataRequirement: Optional["DataRequirement"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternExpression: Optional["Expression"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternParameterDefinition: Optional["ParameterDefinition"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternRelatedArtifact: Optional["RelatedArtifact"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternTriggerDefinition: Optional["TriggerDefinition"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternUsageContext: Optional["UsageContext"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternDosage: Optional["Dosage"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    patternMeta: Optional["Meta"] = Field(
        description="Value must have at least these property values",
        default=None,
    )
    example: Optional[List[Element]] = Field(
        description="Example value (as defined for type)",
        default=None,
    )
    minValueDate: Optional[Date] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValueDateTime: Optional[DateTime] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValueInstant: Optional[Instant] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValueTime: Optional[Time] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValueDecimal: Optional[Decimal] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValueInteger: Optional[Integer] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValuePositiveInt: Optional[PositiveInt] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValueUnsignedInt: Optional[UnsignedInt] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    minValueQuantity: Optional["Quantity"] = Field(
        description="Minimum Allowed Value (for some types)",
        default=None,
    )
    maxValueDate: Optional[Date] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValueDateTime: Optional[DateTime] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValueInstant: Optional[Instant] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValueTime: Optional[Time] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValueDecimal: Optional[Decimal] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValueInteger: Optional[Integer] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValuePositiveInt: Optional[PositiveInt] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValueUnsignedInt: Optional[UnsignedInt] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxValueQuantity: Optional["Quantity"] = Field(
        description="Maximum Allowed Value (for some types)",
        default=None,
    )
    maxLength: Optional[Integer] = Field(
        description="Max length for strings",
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
    condition_ext: Optional[Element] = Field(
        description="Placeholder element for condition extensions",
        default=None,
        alias="_condition",
    )
    constraint: Optional[List[Element]] = Field(
        description="Condition that must evaluate to true",
        default=None,
    )
    mustSupport: Optional[Boolean] = Field(
        description="If the element must be supported",
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
        description="Include when _summary = true?",
        default=None,
    )
    isSummary_ext: Optional[Element] = Field(
        description="Placeholder element for isSummary extensions",
        default=None,
        alias="_isSummary",
    )
    binding: Optional[Element] = Field(
        description="ValueSet details if this is coded",
        default=None,
    )
    mapping: Optional[List[Element]] = Field(
        description="Map element to another set of definitions",
        default=None,
    )

    @field_validator(
        *(
            "mapping",
            "binding",
            "isSummary",
            "isModifierReason",
            "isModifier",
            "mustSupport",
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
        mode="after",
        check_fields=None,
    )
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(
        *("modifierExtension", "extension"), mode="after", check_fields=None
    )
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
            severity="error",
        )

    @field_validator(*("slicing",), mode="after", check_fields=None)
    @classmethod
    def FHIR_eld_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="discriminator.exists() or description.exists()",
            human="If there are no discriminators, there must be a definition",
            key="eld-1",
            severity="error",
        )

    @field_validator(*("max",), mode="after", check_fields=None)
    @classmethod
    def FHIR_eld_3_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="empty() or ($this = '*') or (toInteger() >= 0)",
            human='Max SHALL be a number or "*"',
            key="eld-3",
            severity="error",
        )

    @field_validator(*("type",), mode="after", check_fields=None)
    @classmethod
    def FHIR_eld_4_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="aggregation.empty() or (code = 'Reference') or (code = 'canonical')",
            human="Aggregation may only be specified if one of the allowed types for the element is a reference",
            key="eld-4",
            severity="error",
        )

    @field_validator(*("type",), mode="after", check_fields=None)
    @classmethod
    def FHIR_eld_17_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="(code='Reference' or code = 'canonical') or targetProfile.empty()",
            human="targetProfile is only allowed if the type is Reference or canonical",
            key="eld-17",
            severity="error",
        )

    @field_validator(*("constraint",), mode="after", check_fields=None)
    @classmethod
    def FHIR_eld_21_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="expression.exists()",
            human="Constraints should have an expression or else validators will not be able to enforce them",
            key="eld-21",
            severity="warning",
        )

    @field_validator(*("binding",), mode="after", check_fields=None)
    @classmethod
    def FHIR_eld_12_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="valueSet.exists() implies (valueSet.startsWith('http:') or valueSet.startsWith('https') or valueSet.startsWith('urn:'))",
            human="ValueSet SHALL start with http:// or https:// or urn:",
            key="eld-12",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def defaultValue_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[
                Base64Binary,
                Boolean,
                Canonical,
                Code,
                Date,
                DateTime,
                Decimal,
                Id,
                Instant,
                Integer,
                Markdown,
                Oid,
                PositiveInt,
                String,
                Time,
                UnsignedInt,
                Uri,
                Url,
                Uuid,
                "Address",
                "Age",
                "Annotation",
                "Attachment",
                "CodeableConcept",
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
                "Meta",
            ],
            field_name_base="defaultValue",
        )

    @model_validator(mode="after")
    def fixed_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[
                Base64Binary,
                Boolean,
                Canonical,
                Code,
                Date,
                DateTime,
                Decimal,
                Id,
                Instant,
                Integer,
                Markdown,
                Oid,
                PositiveInt,
                String,
                Time,
                UnsignedInt,
                Uri,
                Url,
                Uuid,
                "Address",
                "Age",
                "Annotation",
                "Attachment",
                "CodeableConcept",
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
                "Meta",
            ],
            field_name_base="fixed",
        )

    @model_validator(mode="after")
    def pattern_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[
                Base64Binary,
                Boolean,
                Canonical,
                Code,
                Date,
                DateTime,
                Decimal,
                Id,
                Instant,
                Integer,
                Markdown,
                Oid,
                PositiveInt,
                String,
                Time,
                UnsignedInt,
                Uri,
                Url,
                Uuid,
                "Address",
                "Age",
                "Annotation",
                "Attachment",
                "CodeableConcept",
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
                "Meta",
            ],
            field_name_base="pattern",
        )

    @model_validator(mode="after")
    def minValue_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[
                Date,
                DateTime,
                Instant,
                Time,
                Decimal,
                Integer,
                PositiveInt,
                UnsignedInt,
                "Quantity",
            ],
            field_name_base="minValue",
        )

    @model_validator(mode="after")
    def maxValue_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[
                Date,
                DateTime,
                Instant,
                Time,
                Decimal,
                Integer,
                PositiveInt,
                UnsignedInt,
                "Quantity",
            ],
            field_name_base="maxValue",
        )

    @model_validator(mode="after")
    def FHIR_eld_2_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="min.empty() or max.empty() or (max = '*') or iif(max != '*', min <= max.toInteger())",
            human="Min <= Max",
            key="eld-2",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_5_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="contentReference.empty() or (type.empty() and defaultValue.empty() and fixed.empty() and pattern.empty() and example.empty() and minValue.empty() and maxValue.empty() and maxLength.empty() and binding.empty())",
            human="if the element definition has a contentReference, it cannot have type, defaultValue, fixed, pattern, example, minValue, maxValue, maxLength, or binding",
            key="eld-5",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_6_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="fixed.empty() or (type.count()  <= 1)",
            human="Fixed value may only be specified if there is one type",
            key="eld-6",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_7_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="pattern.empty() or (type.count() <= 1)",
            human="Pattern may only be specified if there is one type",
            key="eld-7",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_8_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="pattern.empty() or fixed.empty()",
            human="Pattern and fixed are mutually exclusive",
            key="eld-8",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_11_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="binding.empty() or type.code.empty() or type.select((code = 'code') or (code = 'Coding') or (code='CodeableConcept') or (code = 'Quantity') or (code = 'string') or (code = 'uri')).exists()",
            human="Binding can only be present for coded elements, string, and uri",
            key="eld-11",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_13_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="type.select(code).isDistinct()",
            human="Types must be unique by code",
            key="eld-13",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_14_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="constraint.select(key).isDistinct()",
            human="Constraints must be unique by key",
            key="eld-14",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_15_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="defaultValue.empty() or meaningWhenMissing.empty()",
            human="default value and meaningWhenMissing are mutually exclusive",
            key="eld-15",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_16_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="sliceName.empty() or sliceName.matches('^[a-zA-Z0-9\\/\\-_\\[\\]\\@]+$')",
            human='sliceName must be composed of proper tokens separated by "/"',
            key="eld-16",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_18_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(isModifier.exists() and isModifier) implies isModifierReason.exists()",
            human="Must have a modifier reason if isModifier = true",
            key="eld-18",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_19_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="path.matches('[^\\s\\.,:;\\'\"\\/|?!@#$%&*()\\[\\]{}]{1,64}(\\.[^\\s\\.,:;\\'\"\\/|?!@#$%&*()\\[\\]{}]{1,64}(\\[x\\])?(\\:[^\\s\\.]+)?)*')",
            human="Element names cannot include some special characters",
            key="eld-19",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_eld_20_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="path.matches('[A-Za-z][A-Za-z0-9]*(\\.[a-z][A-Za-z0-9]*(\\[x])?)*')",
            human="Element names should be simple alphanumerics with a max of 64 characters, or code generation tools may be broken",
            key="eld-20",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_eld_22_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="sliceIsConstraining.exists() implies sliceName.exists()",
            human="sliceIsConstraining can only appear if slicename is present",
            key="eld-22",
            severity="error",
        )

    @property
    def defaultValue(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="defaultValue",
        )

    @property
    def fixed(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="fixed",
        )

    @property
    def pattern(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="pattern",
        )

    @property
    def minValue(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="minValue",
        )

    @property
    def maxValue(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="maxValue",
        )
