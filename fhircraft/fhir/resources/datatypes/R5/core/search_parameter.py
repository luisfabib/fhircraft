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


class SearchParameterComponent(BackboneElement):
    """
    Used to define the parts of a composite search parameter.
    """

    definition: Optional[fhir.canonical] = Field(
        description="Defines how the part works",
        default=None,
    )
    expression: Optional[fhir.string] = Field(
        description="Subexpression relative to main expression",
        default=None,
    )


class SearchParameter(DomainResource):
    """
    A search parameter that defines a named search item that can be used to search/filter on a resource.
    """

    _abstract = False
    _type = "SearchParameter"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/SearchParameter"

    url: Optional[fhir.uri] = Field(
        description="canonical identifier for this search parameter, represented as a URI (globally unique)",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Additional identifier for the search parameter (business identifier)",
        default=None,
    )
    version: Optional[fhir.string] = Field(
        description="Business version of the search parameter",
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
    name: Optional[fhir.string] = Field(
        description="Name for this search parameter (computer friendly)",
        default=None,
    )
    title: Optional[fhir.string] = Field(
        description="Name for this search parameter (human friendly)",
        default=None,
    )
    derivedFrom: Optional[fhir.canonical] = Field(
        description="Original definition for the search parameter",
        default=None,
    )
    status: Optional[fhir.code] = Field(
        description="draft | active | retired | unknown",
        default=None,
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
        description="Natural language description of the search parameter",
        default=None,
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
    copyright: Optional[fhir.markdown] = Field(
        description="Use and/or publishing restrictions",
        default=None,
    )
    copyrightLabel: Optional[fhir.string] = Field(
        description="Copyright holder and year(s)",
        default=None,
    )
    code: Optional[fhir.code] = Field(
        description="Recommended name for parameter in search url",
        default=None,
    )
    base: Optional[ListType[fhir.code]] = Field(
        description="The resource type(s) this search parameter applies to",
        default=None,
    )
    type: Optional[fhir.code] = Field(
        description="number | date | string | token | reference | composite | quantity | uri | special",
        default=None,
    )
    expression: Optional[fhir.string] = Field(
        description="FHIRPath expression that extracts the values",
        default=None,
    )
    processingMode: Optional[fhir.code] = Field(
        description="normal | phonetic | other",
        default=None,
    )
    constraint: Optional[fhir.string] = Field(
        description="FHIRPath expression that constraints the usage of this SearchParamete",
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
        description="missing | exact | contains | not | text | in | not-in | below | above | type | identifier | of-type | code-text | text-advanced | iterate",
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
            field_types=[fhir.string, Coding],
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
    def FHIR_spd_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="expression.empty() or processingMode.exists()",
            human="If an expression is present, there SHALL be a processingMode",
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

    @model_validator(mode="after")
    def FHIR_spd_3_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="comparator.empty() or (type in ('number' | 'date' | 'quantity' | 'special'))",
            human="Search parameters comparator can only be used on type 'number', 'date', 'quantity' or 'special'.",
            key="spd-3",
            severity="error",
        )
