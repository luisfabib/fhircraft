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
    BackboneElement,
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


class StructureMapConst(BackboneElement):
    """
    Definition of a constant value used in the map rules.
    """

    name: Optional[fhir.id_] = Field(
        description="Constant name",
        default=None,
    )
    value: Optional[fhir.string] = Field(
        description="FHIRPath exression - value of the constant",
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
    defaultValue: Optional[fhir.string] = Field(
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
    valueDate: Optional[fhir.date_] = Field(
        description="Parameter value - variable or literal",
        default=None,
    )
    valueTime: Optional[fhir.time_] = Field(
        description="Parameter value - variable or literal",
        default=None,
    )
    valueDateTime: Optional[fhir.dateTime] = Field(
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
                fhir.Date,
                fhir.Time,
                fhir.DateTime,
            ],
            field_name_base="value",
            required=True,
        )


class StructureMapGroupRuleTarget(BackboneElement):
    """
    Content to create because of this mapping rule.
    """

    context: Optional[fhir.string] = Field(
        description="Variable this rule applies to",
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
        description="first | share | last | single",
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


class StructureMapGroupRuleDependentParameter(BackboneElement):
    """
    Parameter to pass to the rule or group.
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
    valueDate: Optional[fhir.date_] = Field(
        description="Parameter value - variable or literal",
        default=None,
    )
    valueTime: Optional[fhir.time_] = Field(
        description="Parameter value - variable or literal",
        default=None,
    )
    valueDateTime: Optional[fhir.dateTime] = Field(
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
                fhir.Date,
                fhir.Time,
                fhir.DateTime,
            ],
            field_name_base="value",
            required=True,
        )


class StructureMapGroupRuleDependent(BackboneElement):
    """
    Which other rules to apply in the context of this rule.
    """

    name: fhir.id_ = Field(
        description="Name of a rule or group to apply",
    )
    parameter: ListType[StructureMapGroupRuleDependentParameter] = Field(
        description="Parameter to pass to the rule or group",
        min_length=1,
    )


class StructureMapGroupRule(BackboneElement):
    """
    Transform Rule from source to target.
    """

    name: Optional[fhir.id_] = Field(
        description="Name of the rule for internal references",
        default=None,
    )
    source: ListType[StructureMapGroupRuleSource] = Field(
        description="Source inputs to the mapping",
        min_length=1,
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
    Organizes the mapping into managable chunks for human review/ease of maintenance.
    """

    name: fhir.id_ = Field(
        description="Human-readable label",
    )
    extends: Optional[fhir.id_] = Field(
        description="Another group that this group adds rules to",
        default=None,
    )
    typeMode: Optional[fhir.code] = Field(
        description="types | type-and-types",
        default=None,
    )
    documentation: Optional[fhir.string] = Field(
        description="Additional description/explanation for group",
        default=None,
    )
    input: ListType[StructureMapGroupInput] = Field(
        description="Named instance provided when invoking the map",
        min_length=1,
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
    versionAlgorithmString: Optional[fhir.string] = Field(
        description="How to compare versions",
        default=None,
    )
    versionAlgorithmCoding: Optional[Coding] = Field(
        description="How to compare versions",
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
        description="Name of the publisher/steward (organization or individual)",
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
    copyrightLabel: Optional[fhir.string] = Field(
        description="Copyright holder and year(s)",
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
    const: Optional[ListType[StructureMapConst]] = Field(
        description="Definition of the constant value used in the map rules",
        default=None,
    )
    group: ListType[StructureMapGroup] = Field(
        description="Named sections for reader convenience",
        min_length=1,
    )

    @property
    def versionAlgorithm(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="versionAlgorithm",
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
    def FHIR_smp_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("group.rule.target",),
            expression="element.exists() implies context.exists()",
            human="Can only have an element if you have a context",
            key="smp-1",
            severity="error",
        )
