import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)


from ..primitive import *
from fhircraft.fhir.resources.datatypes.R4B.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    ContactDetail,
    UsageContext,
    CodeableConcept,
    BackboneElement,
    Address,
    Age,
    Annotation,
    Attachment,
    Coding,
    ContactPoint,
    Count,
    Distance,
    Duration,
    HumanName,
    Money,
    Period,
    Quantity,
    Range,
    Ratio,
    Reference,
    SampledData,
    Signature,
    Timing,
    Contributor,
    DataRequirement,
    Expression,
    ParameterDefinition,
    RelatedArtifact,
    TriggerDefinition,
    Dosage,
)
from .resource import Resource
from .domain_resource import DomainResource

class StructureMapStructure(BackboneElement):
    """
    A structure definition used by this map. The structure definition may describe instances that are converted, or the instances that are produced.
    """

    url: Optional[Canonical] = Field(
        description="Canonical reference to structure definition",
        default=None,
    )
    mode: Optional[Code] = Field(
        description="source | queried | target | produced",
        default=None,
    )
    alias: Optional[String] = Field(
        description="Name for type in this map",
        default=None,
    )
    documentation: Optional[String] = Field(
        description="Documentation on use of structure",
        default=None,
    )

class StructureMapGroupInput(BackboneElement):
    """
    A name assigned to an instance of data. The instance must be provided when the mapping is invoked.
    """

    name: Optional[Id] = Field(
        description="Name for this instance of data",
        default=None,
    )
    type: Optional[String] = Field(
        description="Type for this instance of data",
        default=None,
    )
    mode: Optional[Code] = Field(
        description="source | target",
        default=None,
    )
    documentation: Optional[String] = Field(
        description="Documentation for this instance of data",
        default=None,
    )

class StructureMapGroupRuleSource(BackboneElement):
    """
    Source inputs to the mapping.
    """

    context: Optional[Id] = Field(
        description="Type or variable this rule applies to",
        default=None,
    )
    min: Optional[Integer] = Field(
        description="Specified minimum cardinality",
        default=None,
    )
    max: Optional[String] = Field(
        description="Specified maximum cardinality (number or *)",
        default=None,
    )
    type: Optional[String] = Field(
        description="Rule only applies if source has this type",
        default=None,
    )
    defaultValueBase64Binary: Optional[Base64Binary] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueBoolean: Optional[Boolean] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueCanonical: Optional[Canonical] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueCode: Optional[Code] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueDate: Optional[Date] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueDateTime: Optional[DateTime] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueDecimal: Optional[Decimal] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueId: Optional[Id] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueInstant: Optional[Instant] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueInteger: Optional[Integer] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueMarkdown: Optional[Markdown] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueOid: Optional[Oid] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValuePositiveInt: Optional[PositiveInt] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueString: Optional[String] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueTime: Optional[Time] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueUnsignedInt: Optional[UnsignedInt] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueUri: Optional[Uri] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueUrl: Optional[Url] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueUuid: Optional[Uuid] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueAddress: Optional[Address] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueAge: Optional[Age] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueAnnotation: Optional[Annotation] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueAttachment: Optional[Attachment] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueCodeableConcept: Optional[CodeableConcept] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueCoding: Optional[Coding] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueContactPoint: Optional[ContactPoint] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueCount: Optional[Count] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueDistance: Optional[Distance] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueDuration: Optional[Duration] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueHumanName: Optional[HumanName] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueIdentifier: Optional[Identifier] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueMoney: Optional[Money] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValuePeriod: Optional[Period] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueQuantity: Optional[Quantity] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueRange: Optional[Range] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueRatio: Optional[Ratio] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueReference: Optional[Reference] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueSampledData: Optional[SampledData] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueSignature: Optional[Signature] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueTiming: Optional[Timing] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueContactDetail: Optional[ContactDetail] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueContributor: Optional[Contributor] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueDataRequirement: Optional[DataRequirement] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueExpression: Optional[Expression] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueParameterDefinition: Optional[ParameterDefinition] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueRelatedArtifact: Optional[RelatedArtifact] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueTriggerDefinition: Optional[TriggerDefinition] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueUsageContext: Optional[UsageContext] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueDosage: Optional[Dosage] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueMeta: Optional[Meta] = Field(
        description="Default value if no value exists",
        default=None,
    )
    element: Optional[String] = Field(
        description="Optional field for this source",
        default=None,
    )
    listMode: Optional[Code] = Field(
        description="first | not_first | last | not_last | only_one",
        default=None,
    )
    variable: Optional[Id] = Field(
        description="Named context for field, if a field is specified",
        default=None,
    )
    condition: Optional[String] = Field(
        description="FHIRPath expression  - must be true or the rule does not apply",
        default=None,
    )
    check: Optional[String] = Field(
        description="FHIRPath expression  - must be true or the mapping engine throws an error instead of completing",
        default=None,
    )
    logMessage: Optional[String] = Field(
        description="Message to put in log if source exists (FHIRPath)",
        default=None,
    )

    @property
    def defaultValue(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="defaultValue",
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
                Address,
                Age,
                Annotation,
                Attachment,
                CodeableConcept,
                Coding,
                ContactPoint,
                Count,
                Distance,
                Duration,
                HumanName,
                Identifier,
                Money,
                Period,
                Quantity,
                Range,
                Ratio,
                Reference,
                SampledData,
                Signature,
                Timing,
                ContactDetail,
                Contributor,
                DataRequirement,
                Expression,
                ParameterDefinition,
                RelatedArtifact,
                TriggerDefinition,
                UsageContext,
                Dosage,
                Meta,
            ],
            field_name_base="defaultValue",
            required=False,
        )

class StructureMapGroupRuleTargetParameter(BackboneElement):
    """
    Parameters to the transform.
    """

    valueId: Optional[Id] = Field(
        description="Parameter value - variable or literal",
        default=None,
    )
    valueString: Optional[String] = Field(
        description="Parameter value - variable or literal",
        default=None,
    )
    valueBoolean: Optional[Boolean] = Field(
        description="Parameter value - variable or literal",
        default=None,
    )
    valueInteger: Optional[Integer] = Field(
        description="Parameter value - variable or literal",
        default=None,
    )
    valueDecimal: Optional[Decimal] = Field(
        description="Parameter value - variable or literal",
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
            field_types=[Id, String, Boolean, Integer, Decimal],
            field_name_base="value",
            required=True,
        )

class StructureMapGroupRuleTarget(BackboneElement):
    """
    Content to create because of this mapping rule.
    """

    context: Optional[Id] = Field(
        description="Type or variable this rule applies to",
        default=None,
    )
    contextType: Optional[Code] = Field(
        description="type | variable",
        default=None,
    )
    element: Optional[String] = Field(
        description="Field to create in the context",
        default=None,
    )
    variable: Optional[Id] = Field(
        description="Named context for field, if desired, and a field is specified",
        default=None,
    )
    listMode: Optional[ListType[Code]] = Field(
        description="first | share | last | collate",
        default=None,
    )
    listRuleId: Optional[Id] = Field(
        description="Internal rule reference for shared list items",
        default=None,
    )
    transform: Optional[Code] = Field(
        description="create | copy +",
        default=None,
    )
    parameter: Optional[ListType[StructureMapGroupRuleTargetParameter]] = Field(
        description="Parameters to the transform",
        default=None,
    )

class StructureMapGroupRuleDependent(BackboneElement):
    """
    Which other rules to apply in the context of this rule.
    """

    name: Optional[Id] = Field(
        description="Name of a rule or group to apply",
        default=None,
    )
    variable: Optional[ListType[String]] = Field(
        description="Variable to pass to the rule or group",
        default=None,
    )

class StructureMapGroupRule(BackboneElement):
    """
    Transform Rule from source to target.
    """

    name: Optional[Id] = Field(
        description="Name of the rule for internal references",
        default=None,
    )
    source: Optional[ListType[StructureMapGroupRuleSource]] = Field(
        description="Source inputs to the mapping",
        default=None,
    )
    target: Optional[ListType[StructureMapGroupRuleTarget]] = Field(
        description="Content to create because of this mapping rule",
        default=None,
    )
    rule: Optional[ListType["StructureMapGroupRule"]] = Field(
        description="Rules contained in this rule",
        default=None,
    )
    dependent: Optional[ListType[StructureMapGroupRuleDependent]] = Field(
        description="Which other rules to apply in the context of this rule",
        default=None,
    )
    documentation: Optional[String] = Field(
        description="Documentation for this instance of data",
        default=None,
    )

class StructureMapGroup(BackboneElement):
    """
    Organizes the mapping into manageable chunks for human review/ease of maintenance.
    """

    name: Optional[Id] = Field(
        description="Human-readable label",
        default=None,
    )
    extends: Optional[Id] = Field(
        description="Another group that this group adds rules to",
        default=None,
    )
    typeMode: Optional[Code] = Field(
        description="none | types | type-and-types",
        default=None,
    )
    documentation: Optional[String] = Field(
        description="Additional description/explanation for group",
        default=None,
    )
    input: Optional[ListType[StructureMapGroupInput]] = Field(
        description="Named instance provided when invoking the map",
        default=None,
    )
    rule: Optional[ListType[StructureMapGroupRule]] = Field(
        description="Transform Rule from source to target",
        default=None,
    )

class StructureMap(DomainResource):
    """
    A Map of relationships between 2 structures that can be used to transform data.
    """

    _abstract = False
    _type = "StructureMap"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/StructureMap"

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
        description="Canonical identifier for this structure map, represented as a URI (globally unique)",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Additional identifier for the structure map",
        default=None,
    )
    version: Optional[String] = Field(
        description="Business version of the structure map",
        default=None,
    )
    name: Optional[String] = Field(
        description="Name for this structure map (computer friendly)",
        default=None,
    )
    title: Optional[String] = Field(
        description="Name for this structure map (human friendly)",
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
        description="Natural language description of the structure map",
        default=None,
    )
    useContext: Optional[ListType[UsageContext]] = Field(
        description="The context that the content is intended to support",
        default=None,
    )
    jurisdiction: Optional[ListType[CodeableConcept]] = Field(
        description="Intended jurisdiction for structure map (if applicable)",
        default=None,
    )
    purpose: Optional[Markdown] = Field(
        description="Why this structure map is defined",
        default=None,
    )
    copyright: Optional[Markdown] = Field(
        description="Use and/or publishing restrictions",
        default=None,
    )
    structure: Optional[ListType[StructureMapStructure]] = Field(
        description="Structure Definition used by this map",
        default=None,
    )
    import_: Optional[ListType[Canonical]] = Field(
        description="Other maps used by this map (canonical URLs)",
        default=None,
        alias="import",
    )
    group: Optional[ListType[StructureMapGroup]] = Field(
        description="Named sections for reader convenience",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_smp_0_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.exists() implies name.matches('[A-Z]([A-Za-z0-9_]){0,254}')",
            human="Name should be usable as an identifier for the module by machine processing applications such as code generation",
            key="smp-0",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_smp_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("group.rule.target",),
            expression="element.exists() implies context.exists()",
            human="Can only have an element if you have a context",
            key="smp-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_smp_2_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("group.rule.target",),
            expression="context.exists() implies contextType.exists()",
            human="Must have a contextType if you have a context",
            key="smp-2",
            severity="error",
        )
