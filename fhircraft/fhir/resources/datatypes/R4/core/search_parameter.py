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
    ContactDetail,
    UsageContext,
    BackboneElement,
    CodeableConcept,
)
from .resource import Resource
from .domain_resource import DomainResource


class SearchParameterComponent(BackboneElement):
    """
    Used to define the parts of a composite search parameter.
    """

    definition: fhir.canonical = Field(
        description="Defines how the part works",
    )
    expression: fhir.string = Field(
        description="Subexpression relative to main expression",
    )


class SearchParameter(DomainResource):
    """
    A search parameter that defines a named search item that can be used to search/filter on a resource.
    """

    _abstract = False
    _type = "SearchParameter"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/SearchParameter"

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
        description="canonical identifier for this search parameter, represented as a URI (globally unique)",
    )
    version: Optional[fhir.string] = Field(
        description="Business version of the search parameter",
        default=None,
    )
    name: fhir.string = Field(
        description="Name for this search parameter (computer friendly)",
    )
    derivedFrom: Optional[fhir.canonical] = Field(
        description="Original definition for the search parameter",
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
    description: fhir.markdown = Field(
        description="Natural language description of the search parameter",
    )
    useContext: Optional[ListType[UsageContext]] = Field(
        description="The context that the content is intended to support",
        default=None,
    )
    jurisdiction: Optional[ListType[CodeableConcept]] = Field(
        description="Intended jurisdiction for search parameter (if applicable)",
        default=None,
    )
    purpose: Optional[fhir.markdown] = Field(
        description="Why this search parameter is defined",
        default=None,
    )
    code: fhir.code = Field(
        description="code used in URL",
    )
    base: ListType[fhir.code] = Field(
        description="The resource type(s) this search parameter applies to",
     	min_length=1,
	)
    type: fhir.code = Field(
        description="number | date | string | token | reference | composite | quantity | uri | special",
    )
    expression: Optional[fhir.string] = Field(
        description="FHIRPath expression that extracts the values",
        default=None,
    )
    xpath: Optional[fhir.string] = Field(
        description="XPath that extracts the values",
        default=None,
    )
    xpathUsage: Optional[fhir.code] = Field(
        description="normal | phonetic | nearby | distance | other",
        default=None,
    )
    target: Optional[ListType[fhir.code]] = Field(
        description="Types of resource (if a resource reference)",
        default=None,
    )
    multipleOr: Optional[fhir.boolean] = Field(
        description="Allow multiple values per parameter (or)",
        default=None,
    )
    multipleAnd: Optional[fhir.boolean] = Field(
        description="Allow multiple parameters (and)",
        default=None,
    )
    comparator: Optional[ListType[fhir.code]] = Field(
        description="eq | ne | gt | lt | ge | le | sa | eb | ap",
        default=None,
    )
    modifier: Optional[ListType[fhir.code]] = Field(
        description="missing | exact | contains | not | text | in | not-in | below | above | type | identifier | ofType",
        default=None,
    )
    chain: Optional[ListType[fhir.string]] = Field(
        description="Chained names supported",
        default=None,
    )
    component: Optional[ListType[SearchParameterComponent]] = Field(
        description="For Composite resources to define the parts",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_spd_0_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.matches('[A-Z]([A-Za-z0-9_]){0,254}')",
            human="Name should be usable as an identifier for the module by machine processing applications such as code generation",
            key="spd-0",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_spd_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="xpath.empty() or xpathUsage.exists()",
            human="If an xpath is present, there SHALL be an xpathUsage",
            key="spd-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_spd_2_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="chain.empty() or type = 'reference'",
            human="Search parameters can only have chain names when the search parameter type is 'reference'",
            key="spd-2",
            severity="error",
        )
