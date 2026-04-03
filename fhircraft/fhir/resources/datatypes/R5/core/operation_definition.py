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

class OperationDefinitionParameterBinding(BackboneElement):
    """
    Binds to a value set if this parameter is coded (code, Coding, CodeableConcept).
    """

    strength: Optional[Code] = Field(
        description="required | extensible | preferred | example",
        default=None,
    )
    valueSet: Optional[Canonical] = Field(
        description="Source of value set",
        default=None,
    )

class OperationDefinitionParameterReferencedFrom(BackboneElement):
    """
    Identifies other resource parameters within the operation invocation that are expected to resolve to this resource.
    """

    source: Optional[String] = Field(
        description="Referencing parameter",
        default=None,
    )
    sourceId: Optional[String] = Field(
        description="Element id of reference",
        default=None,
    )

class OperationDefinitionParameter(BackboneElement):
    """
    The parameters for the operation/query.
    """

    name: Optional[Code] = Field(
        description="Name in Parameters.parameter.name or in URL",
        default=None,
    )
    use: Optional[Code] = Field(
        description="in | out",
        default=None,
    )
    scope: Optional[ListType[Code]] = Field(
        description="instance | type | system",
        default=None,
    )
    min: Optional[Integer] = Field(
        description="Minimum Cardinality",
        default=None,
    )
    max: Optional[String] = Field(
        description="Maximum Cardinality (a number or *)",
        default=None,
    )
    documentation: Optional[Markdown] = Field(
        description="Description of meaning/use",
        default=None,
    )
    type: Optional[Code] = Field(
        description="What type this parameter has",
        default=None,
    )
    allowedType: Optional[ListType[Code]] = Field(
        description="Allowed sub-type this parameter can have (if type is abstract)",
        default=None,
    )
    targetProfile: Optional[ListType[Canonical]] = Field(
        description="If type is Reference | canonical, allowed targets. If type is \u0027Resource\u0027, then this constrains the allowed resource types",
        default=None,
    )
    searchType: Optional[Code] = Field(
        description="number | date | string | token | reference | composite | quantity | uri | special",
        default=None,
    )
    binding: Optional[OperationDefinitionParameterBinding] = Field(
        description="ValueSet details if this is coded",
        default=None,
    )
    referencedFrom: Optional[ListType[OperationDefinitionParameterReferencedFrom]] = (
        Field(
            description="References to this parameter",
            default=None,
        )
    )
    part: Optional[ListType["OperationDefinitionParameter"]] = Field(
        description="Parts of a nested Parameter",
        default=None,
    )

class OperationDefinitionOverload(BackboneElement):
    """
    Defines an appropriate combination of parameters to use when invoking this operation, to help code generators when generating overloaded parameter sets for this operation.
    """

    parameterName: Optional[ListType[String]] = Field(
        description="Name of parameter to include in overload",
        default=None,
    )
    comment: Optional[String] = Field(
        description="Comments to go on overload",
        default=None,
    )

class OperationDefinition(DomainResource):
    """
    A formal computable definition of an operation (on the RESTful interface) or a named query (using the search interaction).
    """

    _abstract = False
    _type = "OperationDefinition"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/OperationDefinition"

    url: Optional[Uri] = Field(
        description="Canonical identifier for this operation definition, represented as an absolute URI (globally unique)",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Additional identifier for the implementation guide (business identifier)",
        default=None,
    )
    version: Optional[String] = Field(
        description="Business version of the operation definition",
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
        description="Name for this operation definition (computer friendly)",
        default=None,
    )
    title: Optional[String] = Field(
        description="Name for this operation definition (human friendly)",
        default=None,
    )
    status: Optional[Code] = Field(
        description="draft | active | retired | unknown",
        default=None,
    )
    kind: Optional[Code] = Field(
        description="operation | query",
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
        description="Natural language description of the operation definition",
        default=None,
    )
    useContext: Optional[ListType[UsageContext]] = Field(
        description="The context that the content is intended to support",
        default=None,
    )
    jurisdiction: Optional[ListType[CodeableConcept]] = Field(
        description="Intended jurisdiction for operation definition (if applicable)",
        default=None,
    )
    purpose: Optional[Markdown] = Field(
        description="Why this operation definition is defined",
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
    affectsState: Optional[Boolean] = Field(
        description="Whether content is changed by the operation",
        default=None,
    )
    code: Optional[Code] = Field(
        description="Recommended name for operation in search url",
        default=None,
    )
    comment: Optional[Markdown] = Field(
        description="Additional information about use",
        default=None,
    )
    base: Optional[Canonical] = Field(
        description="Marks this as a profile of the base",
        default=None,
    )
    resource: Optional[ListType[Code]] = Field(
        description="Types this operation applies to",
        default=None,
    )
    system: Optional[Boolean] = Field(
        description="Invoke at the system level?",
        default=None,
    )
    type: Optional[Boolean] = Field(
        description="Invoke at the type level?",
        default=None,
    )
    instance: Optional[Boolean] = Field(
        description="Invoke on an instance?",
        default=None,
    )
    inputProfile: Optional[Canonical] = Field(
        description="Validation information for in parameters",
        default=None,
    )
    outputProfile: Optional[Canonical] = Field(
        description="Validation information for out parameters",
        default=None,
    )
    parameter: Optional[ListType[OperationDefinitionParameter]] = Field(
        description="Parameters for the operation/query",
        default=None,
    )
    overload: Optional[ListType[OperationDefinitionOverload]] = Field(
        description="Define overloaded variants for when  generating code",
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
    def FHIR_opd_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("parameter",),
            expression="type.exists() or part.exists()",
            human="Either a type must be provided, or parts",
            key="opd-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_opd_2_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("parameter",),
            expression="searchType.exists() implies type = 'string'",
            human="A search type can only be specified for parameters of type string",
            key="opd-2",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_opd_3_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("parameter",),
            expression="targetProfile.exists() implies (type = 'Reference' or type = 'canonical' or type.memberOf('http://hl7.org/fhir/ValueSet/resource-types'))",
            human="A targetProfile can only be specified for parameters of type Reference, Canonical, or a Resource",
            key="opd-3",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_opd_4_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("parameter",),
            expression="(use = 'out') implies searchType.empty()",
            human="SearchParamType can only be specified on in parameters",
            key="opd-4",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_opd_5_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(kind = 'query') implies (instance = false)",
            human="A query operation cannot be defined at the instance level",
            key="opd-5",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_opd_6_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(kind = 'query') implies (parameter.all((use = 'in' and searchType.exists()) or (use != 'in')))",
            human="A query operation requires input parameters to have a search type",
            key="opd-6",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_opd_7_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(kind = 'query') implies ((parameter.where(use = 'out').count() = 1) and (parameter.where(use = 'out').all(name = 'result' and type = 'Bundle')))",
            human="Named queries always have a single output parameter named 'result' of type Bundle",
            key="opd-7",
            severity="error",
        )
