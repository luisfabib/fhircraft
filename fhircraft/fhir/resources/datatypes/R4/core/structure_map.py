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
    Dosage,
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
)
from .resource import Resource
from .domain_resource import DomainResource


class StructureMapStructure(BackboneElement):
    """
    A structure definition used by this map. The structure definition may describe instances that are converted, or the instances that are produced.
    """

    url: fhir.canonical = Field(
        description="canonical reference to structure definition",
    )
    mode: fhir.code = Field(
        description="source | queried | target | produced",
    )
    alias: Optional[fhir.string] = Field(
        description="Name for type in this map",
        default=None,
    )
    documentation: Optional[fhir.string] = Field(
        description="Documentation on use of structure",
        default=None,
    )


class StructureMapGroupInput(BackboneElement):
    """
    A name assigned to an instance of data. The instance must be provided when the mapping is invoked.
    """

    name: fhir.id_ = Field(
        description="Name for this instance of data",
    )
    type: Optional[fhir.string] = Field(
        description="Type for this instance of data",
        default=None,
    )
    mode: fhir.code = Field(
        description="source | target",
    )
    documentation: Optional[fhir.string] = Field(
        description="Documentation for this instance of data",
        default=None,
    )


class StructureMapGroupRuleSource(BackboneElement):
    """
    Source inputs to the mapping.
    """

    context: fhir.id_ = Field(
        description="Type or variable this rule applies to",
    )
    min: Optional[fhir.integer] = Field(
        description="Specified minimum cardinality",
        default=None,
    )
    max: Optional[fhir.string] = Field(
        description="Specified maximum cardinality (number or *)",
        default=None,
    )
    type: Optional[fhir.string] = Field(
        description="Rule only applies if source has this type",
        default=None,
    )
    defaultValueBase64Binary: Optional[fhir.base64Binary] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueBoolean: Optional[fhir.boolean] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueCanonical: Optional[fhir.canonical] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueCode: Optional[fhir.code] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueDate: Optional[fhir.date_] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueDateTime: Optional[fhir.dateTime] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueDecimal: Optional[fhir.decimal] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueId: Optional[fhir.id_] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueInstant: Optional[fhir.instant] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueInteger: Optional[fhir.integer] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueMarkdown: Optional[fhir.markdown] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueOid: Optional[fhir.oid] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValuePositiveInt: Optional[fhir.positiveInt] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueString: Optional[fhir.string] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueTime: Optional[fhir.time_] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueUnsignedInt: Optional[fhir.unsignedInt] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueUri: Optional[fhir.uri] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueUrl: Optional[fhir.url] = Field(
        description="Default value if no value exists",
        default=None,
    )
    defaultValueUuid: Optional[fhir.uuid] = Field(
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
    element: Optional[fhir.string] = Field(
        description="Optional field for this source",
        default=None,
    )
    listMode: Optional[fhir.code] = Field(
        description="first | not_first | last | not_last | only_one",
        default=None,
    )
    variable: Optional[fhir.id_] = Field(
        description="Named context for field, if a field is specified",
        default=None,
    )
    condition: Optional[fhir.string] = Field(
        description="FHIRPath expression  - must be true or the rule does not apply",
        default=None,
    )
    check: Optional[fhir.string] = Field(
        description="FHIRPath expression  - must be true or the mapping engine throws an error instead of completing",
        default=None,
    )
    logMessage: Optional[fhir.string] = Field(
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

    valueId: Optional[fhir.id_] = Field(
        description="Parameter value - variable or literal",
        default=None,
    )
    valueString: Optional[fhir.string] = Field(
        description="Parameter value - variable or literal",
        default=None,
    )
    valueBoolean: Optional[fhir.boolean] = Field(
        description="Parameter value - variable or literal",
        default=None,
    )
    valueInteger: Optional[fhir.integer] = Field(
        description="Parameter value - variable or literal",
        default=None,
    )
    valueDecimal: Optional[fhir.decimal] = Field(
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
            field_types=[
                fhir.Id,
                fhir.String,
                fhir.Boolean,
                fhir.Integer,
                fhir.Decimal,
            ],
            field_name_base="value",
            required=True,
        )


class StructureMapGroupRuleTarget(BackboneElement):
    """
    Content to create because of this mapping rule.
    """

    context: Optional[fhir.id_] = Field(
        description="Type or variable this rule applies to",
        default=None,
    )
    contextType: Optional[fhir.code] = Field(
        description="type | variable",
        default=None,
    )
    element: Optional[fhir.string] = Field(
        description="Field to create in the context",
        default=None,
    )
    variable: Optional[fhir.id_] = Field(
        description="Named context for field, if desired, and a field is specified",
        default=None,
    )
    listMode: Optional[ListType[fhir.code]] = Field(
        description="first | share | last | collate",
        default=None,
    )
    listRuleId: Optional[fhir.id_] = Field(
        description="Internal rule reference for shared list items",
        default=None,
    )
    transform: Optional[fhir.code] = Field(
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

    name: fhir.id_ = Field(
        description="Name of a rule or group to apply",
    )
    variable: ListType[fhir.string] = Field(
        description="Variable to pass to the rule or group",
    )


class StructureMapGroupRule(BackboneElement):
    """
    Transform Rule from source to target.
    """

    name: fhir.id_ = Field(
        description="Name of the rule for internal references",
    )
    source: ListType[StructureMapGroupRuleSource] = Field(
        description="Source inputs to the mapping",
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
    documentation: Optional[fhir.string] = Field(
        description="Documentation for this instance of data",
        default=None,
    )


class StructureMapGroup(BackboneElement):
    """
    Organizes the mapping into manageable chunks for human review/ease of maintenance.
    """

    name: fhir.id_ = Field(
        description="Human-readable label",
    )
    extends: Optional[fhir.id_] = Field(
        description="Another group that this group adds rules to",
        default=None,
    )
    typeMode: fhir.code = Field(
        description="none | types | type-and-types",
    )
    documentation: Optional[fhir.string] = Field(
        description="Additional description/explanation for group",
        default=None,
    )
    input: ListType[StructureMapGroupInput] = Field(
        description="Named instance provided when invoking the map",
    )
    rule: ListType[StructureMapGroupRule] = Field(
        description="Transform Rule from source to target",
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
    url: fhir.uri = Field(
        description="canonical identifier for this structure map, represented as a URI (globally unique)",
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Additional identifier for the structure map",
        default=None,
    )
    version: Optional[fhir.string] = Field(
        description="Business version of the structure map",
        default=None,
    )
    name: fhir.string = Field(
        description="Name for this structure map (computer friendly)",
    )
    title: Optional[fhir.string] = Field(
        description="Name for this structure map (human friendly)",
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
    purpose: Optional[fhir.markdown] = Field(
        description="Why this structure map is defined",
        default=None,
    )
    copyright: Optional[fhir.markdown] = Field(
        description="Use and/or publishing restrictions",
        default=None,
    )
    structure: Optional[ListType[StructureMapStructure]] = Field(
        description="Structure Definition used by this map",
        default=None,
    )
    import_: Optional[ListType[fhir.canonical]] = Field(
        description="Other maps used by this map (canonical URLs)",
        default=None,
        alias="import",
    )
    group: ListType[StructureMapGroup] = Field(
        description="Named sections for reader convenience",
    )

    @model_validator(mode="after")
    def FHIR_smp_0_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.matches('[A-Z]([A-Za-z0-9_]){0,254}')",
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
