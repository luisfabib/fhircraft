from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators


from ..primitive import *
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

class StructureMapConst(BackboneElement):
    """
    Definition of a constant value used in the map rules.
    """

    name: Optional[Id] = Field(
        description="Constant name",
        default=None,
    )
    value: Optional[String] = Field(
        description="FHIRPath exression - value of the constant",
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
    defaultValue: Optional[String] = Field(
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
    valueDate: Optional[Date] = Field(
        description="Parameter value - variable or literal",
        default=None,
    )
    valueTime: Optional[Time] = Field(
        description="Parameter value - variable or literal",
        default=None,
    )
    valueDateTime: Optional[DateTime] = Field(
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
            field_types=[Id, String, Boolean, Integer, Decimal, Date, Time, DateTime],
            field_name_base="value",
            required=True,
        )

class StructureMapGroupRuleTarget(BackboneElement):
    """
    Content to create because of this mapping rule.
    """

    context: Optional[String] = Field(
        description="Variable this rule applies to",
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
        description="first | share | last | single",
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

class StructureMapGroupRuleDependentParameter(BackboneElement):
    """
    Parameter to pass to the rule or group.
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
    valueDate: Optional[Date] = Field(
        description="Parameter value - variable or literal",
        default=None,
    )
    valueTime: Optional[Time] = Field(
        description="Parameter value - variable or literal",
        default=None,
    )
    valueDateTime: Optional[DateTime] = Field(
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
            field_types=[Id, String, Boolean, Integer, Decimal, Date, Time, DateTime],
            field_name_base="value",
            required=True,
        )

class StructureMapGroupRuleDependent(BackboneElement):
    """
    Which other rules to apply in the context of this rule.
    """

    name: Optional[Id] = Field(
        description="Name of a rule or group to apply",
        default=None,
    )
    parameter: Optional[ListType[StructureMapGroupRuleDependentParameter]] = Field(
        description="Parameter to pass to the rule or group",
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
    Organizes the mapping into managable chunks for human review/ease of maintenance.
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
        description="types | type-and-types",
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
    versionAlgorithmString: Optional[String] = Field(
        description="How to compare versions",
        default=None,
    )
    versionAlgorithmCoding: Optional[Coding] = Field(
        description="How to compare versions",
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
        description="Name of the publisher/steward (organization or individual)",
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
    copyrightLabel: Optional[String] = Field(
        description="Copyright holder and year(s)",
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
    const: Optional[ListType[StructureMapConst]] = Field(
        description="Definition of the constant value used in the map rules",
        default=None,
    )
    group: Optional[ListType[StructureMapGroup]] = Field(
        description="Named sections for reader convenience",
        default=None,
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
            field_types=[String, Coding],
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
