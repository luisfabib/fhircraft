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
    min: Optional[Integer] = Field(
        description="Minimum Cardinality",
        default=None,
    )
    max: Optional[String] = Field(
        description="Maximum Cardinality (a number or *)",
        default=None,
    )
    documentation: Optional[String] = Field(
        description="Description of meaning/use",
        default=None,
    )
    type: Optional[Code] = Field(
        description="What type this parameter has",
        default=None,
    )
    targetProfile: Optional[ListType[Canonical]] = Field(
        description="If type is Reference | canonical, allowed targets",
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
        description="Canonical identifier for this operation definition, represented as a URI (globally unique)",
        default=None,
    )
    version: Optional[String] = Field(
        description="Business version of the operation definition",
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
        description="Name of the publisher (organization or individual)",
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
    affectsState: Optional[Boolean] = Field(
        description="Whether content is changed by the operation",
        default=None,
    )
    code: Optional[Code] = Field(
        description="Name used to invoke the operation",
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

    @model_validator(mode="after")
    def FHIR_opd_0_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.exists() implies name.matches('[A-Z]([A-Za-z0-9_]){0,254}')",
            human="Name should be usable as an identifier for the module by machine processing applications such as code generation",
            key="opd-0",
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
            expression="targetProfile.exists() implies (type = 'Reference' or type = 'canonical')",
            human="A targetProfile can only be specified for parameters of type Reference or Canonical",
            key="opd-3",
            severity="error",
        )
