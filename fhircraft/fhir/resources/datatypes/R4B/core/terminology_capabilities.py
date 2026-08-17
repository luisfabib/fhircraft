import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)


import fhircraft.fhir.resources.datatypes.R4B.primitive as fhir
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


class TerminologyCapabilitiesSoftware(BackboneElement):
    """
    Software that is covered by this terminology capability statement.  It is used when the statement describes the capabilities of a particular software version, independent of an installation.
    """

    name: fhir.string = Field(
        description="A name the software is known by",
    )
    version: Optional[fhir.string] = Field(
        description="Version covered by this statement",
        default=None,
    )


class TerminologyCapabilitiesImplementation(BackboneElement):
    """
    Identifies a specific implementation instance that is described by the terminology capability statement - i.e. a particular installation, rather than the capabilities of a software program.
    """

    description: fhir.string = Field(
        description="Describes this specific instance",
    )
    url: Optional[fhir.url] = Field(
        description="Base URL for the implementation",
        default=None,
    )


class TerminologyCapabilitiesCodeSystemVersionFilter(BackboneElement):
    """
    Filter Properties supported.
    """

    code: fhir.code = Field(
        description="code of the property supported",
    )
    op: ListType[fhir.code] = Field(
        description="Operations supported for the property",
    )


class TerminologyCapabilitiesCodeSystemVersion(BackboneElement):
    """
    For the code system, a list of versions that are supported by the server.
    """

    code: Optional[fhir.string] = Field(
        description="Version identifier for this version",
        default=None,
    )
    isDefault: Optional[fhir.boolean] = Field(
        description="If this is the default version for this code system",
        default=None,
    )
    compositional: Optional[fhir.boolean] = Field(
        description="If compositional grammar is supported",
        default=None,
    )
    language: Optional[ListType[fhir.code]] = Field(
        description="Language Displays supported",
        default=None,
    )

    filter: Optional[ListType[TerminologyCapabilitiesCodeSystemVersionFilter]] = Field(
        description="Filter Properties supported",
        default=None,
    )
    property_: Optional[ListType[fhir.code]] = Field(
        description="Properties supported for $lookup",
        default=None,
        alias="property",
    )


class TerminologyCapabilitiesCodeSystem(BackboneElement):
    """
    Identifies a code system that is supported by the server. If there is a no code system URL, then this declares the general assumptions a client can make about support for any CodeSystem resource.
    """

    uri: Optional[fhir.canonical] = Field(
        description="URI for the code System",
        default=None,
    )
    version: Optional[ListType[TerminologyCapabilitiesCodeSystemVersion]] = Field(
        description="Version of code System supported",
        default=None,
    )
    subsumption: Optional[fhir.boolean] = Field(
        description="Whether subsumption is supported",
        default=None,
    )


class TerminologyCapabilitiesExpansionParameter(BackboneElement):
    """
    Supported expansion parameter.
    """

    name: fhir.code = Field(
        description="Expansion Parameter name",
    )
    documentation: Optional[fhir.string] = Field(
        description="Description of support for parameter",
        default=None,
    )


class TerminologyCapabilitiesExpansion(BackboneElement):
    """
    Information about the [ValueSet/$expand](https://www.hl7.org/fhir/R4B/valueset-operation-expand.html) operation.
    """

    hierarchical: Optional[fhir.boolean] = Field(
        description="Whether the server can return nested value sets",
        default=None,
    )
    paging: Optional[fhir.boolean] = Field(
        description="Whether the server supports paging on expansion",
        default=None,
    )
    incomplete: Optional[fhir.boolean] = Field(
        description="Allow request for incomplete expansions?",
        default=None,
    )
    parameter: Optional[ListType[TerminologyCapabilitiesExpansionParameter]] = Field(
        description="Supported expansion parameter",
        default=None,
    )
    textFilter: Optional[fhir.markdown] = Field(
        description="Documentation about text searching works",
        default=None,
    )


class TerminologyCapabilitiesValidateCode(BackboneElement):
    """
    Information about the [ValueSet/$validate-code](https://hl7.org/fhir/R4B/valueset-operation-validate-code.html) operation.
    """

    translations: fhir.boolean = Field(
        description="Whether translations are validated",
    )


class TerminologyCapabilitiesTranslation(BackboneElement):
    """
    Information about the [ConceptMap/$translate](https://hl7.org/fhir/R4B/conceptmap-operation-translate.html) operation.
    """

    needsMap: fhir.boolean = Field(
        description="Whether the client must identify the map",
    )


class TerminologyCapabilitiesClosure(BackboneElement):
    """
    Whether the $closure operation is supported.
    """

    translation: Optional[fhir.boolean] = Field(
        description="If cross-system closure is supported",
        default=None,
    )


class TerminologyCapabilities(DomainResource):
    """
    A TerminologyCapabilities resource documents a set of capabilities (behaviors) of a FHIR Terminology Server that may be used as a statement of actual server functionality or a statement of required or desired server implementation.
    """

    _abstract = False
    _type = "TerminologyCapabilities"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/TerminologyCapabilities"

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
    url: Optional[fhir.uri] = Field(
        description="canonical identifier for this terminology capabilities, represented as a URI (globally unique)",
        default=None,
    )
    version: Optional[fhir.string] = Field(
        description="Business version of the terminology capabilities",
        default=None,
    )
    name: Optional[fhir.string] = Field(
        description="Name for this terminology capabilities (computer friendly)",
        default=None,
    )
    title: Optional[fhir.string] = Field(
        description="Name for this terminology capabilities (human friendly)",
        default=None,
    )
    status: fhir.code = Field(
        description="draft | active | retired | unknown",
    )
    experimental: Optional[fhir.boolean] = Field(
        description="For testing purposes, not real usage",
        default=None,
    )
    date: fhir.dateTime = Field(
        description="Date last changed",
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
        description="Natural language description of the terminology capabilities",
        default=None,
    )
    useContext: Optional[ListType[UsageContext]] = Field(
        description="The context that the content is intended to support",
        default=None,
    )
    jurisdiction: Optional[ListType[CodeableConcept]] = Field(
        description="Intended jurisdiction for terminology capabilities (if applicable)",
        default=None,
    )
    purpose: Optional[fhir.markdown] = Field(
        description="Why this terminology capabilities is defined",
        default=None,
    )
    copyright: Optional[fhir.markdown] = Field(
        description="Use and/or publishing restrictions",
        default=None,
    )
    kind: fhir.code = Field(
        description="instance | capability | requirements",
    )
    software: Optional[TerminologyCapabilitiesSoftware] = Field(
        description="Software that is covered by this terminology capability statement",
        default=None,
    )
    implementation: Optional[TerminologyCapabilitiesImplementation] = Field(
        description="If this describes a specific instance",
        default=None,
    )
    lockedDate: Optional[fhir.boolean] = Field(
        description="Whether lockedDate is supported",
        default=None,
    )
    codeSystem: Optional[ListType[TerminologyCapabilitiesCodeSystem]] = Field(
        description="A code system supported by the server",
        default=None,
    )
    expansion: Optional[TerminologyCapabilitiesExpansion] = Field(
        description="Information about the [ValueSet/$expand](https://www.hl7.org/fhir/R4B/valueset-operation-expand.html) operation",
        default=None,
    )
    codeSearch: Optional[fhir.code] = Field(
        description="explicit | all",
        default=None,
    )
    validateCode: Optional[TerminologyCapabilitiesValidateCode] = Field(
        description="Information about the [ValueSet/$validate-code](https://hl7.org/fhir/R4B/valueset-operation-validate-code.html) operation",
        default=None,
    )
    translation: Optional[TerminologyCapabilitiesTranslation] = Field(
        description="Information about the [ConceptMap/$translate](https://hl7.org/fhir/R4B/conceptmap-operation-translate.html) operation",
        default=None,
    )
    closure: Optional[TerminologyCapabilitiesClosure] = Field(
        description="Information about the [ConceptMap/$closure](https://hl7.org/fhir/R4B/conceptmap-operation-closure.html) operation",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_tcp_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("codeSystem",),
            expression="version.count() > 1 implies version.all(code.exists())",
            human="If there is more than one version, a version code must be defined",
            key="tcp-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_tcp_0_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.exists() implies name.matches('[A-Z]([A-Za-z0-9_]){0,254}')",
            human="Name should be usable as an identifier for the module by machine processing applications such as code generation",
            key="tcp-0",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_tcp_2_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(description.count() + software.count() + implementation.count()) > 0",
            human="A Capability Statement SHALL have at least one of description, software, or implementation element.",
            key="tcp-2",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_tcp_3_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(kind != 'instance') or implementation.exists()",
            human="If kind = instance, implementation must be present and software may be present",
            key="tcp-3",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_tcp_4_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(kind != 'capability') or (implementation.exists().not() and software.exists())",
            human="If kind = capability, implementation must be absent, software must be present",
            key="tcp-4",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_tcp_5_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(kind!='requirements') or (implementation.exists().not() and software.exists().not())",
            human="If kind = requirements, implementation and software must be absent",
            key="tcp-5",
            severity="error",
        )
