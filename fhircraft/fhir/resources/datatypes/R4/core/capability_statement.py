import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)


from ..primitive import *
from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    ContactDetail,
    UsageContext,
    CodeableConcept,
    BackboneElement,
    Reference,
    Coding,
)
from .resource import Resource
from .domain_resource import DomainResource

class CapabilityStatementSoftware(BackboneElement):
    """
    Software that is covered by this capability statement.  It is used when the capability statement describes the capabilities of a particular software version, independent of an installation.
    """

    name: Optional[String] = Field(
        description="A name the software is known by",
        default=None,
    )
    version: Optional[String] = Field(
        description="Version covered by this statement",
        default=None,
    )
    releaseDate: Optional[DateTime] = Field(
        description="Date this version was released",
        default=None,
    )

class CapabilityStatementImplementation(BackboneElement):
    """
    Identifies a specific implementation instance that is described by the capability statement - i.e. a particular installation, rather than the capabilities of a software program.
    """

    description: Optional[String] = Field(
        description="Describes this specific instance",
        default=None,
    )
    url: Optional[Url] = Field(
        description="Base URL for the installation",
        default=None,
    )
    custodian: Optional[Reference] = Field(
        description="Organization that manages the data",
        default=None,
    )

class CapabilityStatementRestSecurity(BackboneElement):
    """
    Information about security implementation from an interface perspective - what a client needs to know.
    """

    cors: Optional[Boolean] = Field(
        description="Adds CORS Headers (http://enable-cors.org/)",
        default=None,
    )
    service: Optional[ListType[CodeableConcept]] = Field(
        description="OAuth | SMART-on-FHIR | NTLM | Basic | Kerberos | Certificates",
        default=None,
    )
    description: Optional[Markdown] = Field(
        description="General description of how security works",
        default=None,
    )

class CapabilityStatementRestResourceInteraction(BackboneElement):
    """
    Identifies a restful operation supported by the solution.
    """

    code: Optional[Code] = Field(
        description="read | vread | update | patch | delete | history-instance | history-type | create | search-type",
        default=None,
    )
    documentation: Optional[Markdown] = Field(
        description="Anything special about operation behavior",
        default=None,
    )

class CapabilityStatementRestResourceSearchParam(BackboneElement):
    """
    Search parameters for implementations to support and/or make use of - either references to ones defined in the specification, or additional ones defined for/by the implementation.
    """

    name: Optional[String] = Field(
        description="Name of search parameter",
        default=None,
    )
    definition: Optional[Canonical] = Field(
        description="Source of definition for parameter",
        default=None,
    )
    type: Optional[Code] = Field(
        description="number | date | string | token | reference | composite | quantity | uri | special",
        default=None,
    )
    documentation: Optional[Markdown] = Field(
        description="Server-specific usage",
        default=None,
    )

class CapabilityStatementRestResourceOperation(BackboneElement):
    """
    Definition of an operation or a named query together with its parameters and their meaning and type. Consult the definition of the operation for details about how to invoke the operation, and the parameters.
    """

    name: Optional[String] = Field(
        description="Name by which the operation/query is invoked",
        default=None,
    )
    definition: Optional[Canonical] = Field(
        description="The defined operation/query",
        default=None,
    )
    documentation: Optional[Markdown] = Field(
        description="Specific details about operation behavior",
        default=None,
    )

class CapabilityStatementRestResource(BackboneElement):
    """
    A specification of the restful capabilities of the solution for a specific resource type.
    """

    type: Optional[Code] = Field(
        description="A resource type that is supported",
        default=None,
    )
    profile: Optional[Canonical] = Field(
        description="Base System profile for all uses of resource",
        default=None,
    )
    supportedProfile: Optional[ListType[Canonical]] = Field(
        description="Profiles for use cases supported",
        default=None,
    )
    documentation: Optional[Markdown] = Field(
        description="Additional information about the use of the resource type",
        default=None,
    )
    interaction: Optional[ListType[CapabilityStatementRestResourceInteraction]] = Field(
        description="What operations are supported?",
        default=None,
    )
    versioning: Optional[Code] = Field(
        description="no-version | versioned | versioned-update",
        default=None,
    )
    readHistory: Optional[Boolean] = Field(
        description="Whether vRead can return past versions",
        default=None,
    )
    updateCreate: Optional[Boolean] = Field(
        description="If update can commit to a new identity",
        default=None,
    )
    conditionalCreate: Optional[Boolean] = Field(
        description="If allows/uses conditional create",
        default=None,
    )
    conditionalRead: Optional[Code] = Field(
        description="not-supported | modified-since | not-match | full-support",
        default=None,
    )
    conditionalUpdate: Optional[Boolean] = Field(
        description="If allows/uses conditional update",
        default=None,
    )
    conditionalDelete: Optional[Code] = Field(
        description="not-supported | single | multiple - how conditional delete is supported",
        default=None,
    )
    referencePolicy: Optional[ListType[Code]] = Field(
        description="literal | logical | resolves | enforced | local",
        default=None,
    )
    searchInclude: Optional[ListType[String]] = Field(
        description="_include values supported by the server",
        default=None,
    )
    searchRevInclude: Optional[ListType[String]] = Field(
        description="_revinclude values supported by the server",
        default=None,
    )
    searchParam: Optional[ListType[CapabilityStatementRestResourceSearchParam]] = Field(
        description="Search parameters supported by implementation",
        default=None,
    )
    operation: Optional[ListType[CapabilityStatementRestResourceOperation]] = Field(
        description="Definition of a resource operation",
        default=None,
    )

class CapabilityStatementRestInteraction(BackboneElement):
    """
    A specification of restful operations supported by the system.
    """

    code: Optional[Code] = Field(
        description="transaction | batch | search-system | history-system",
        default=None,
    )
    documentation: Optional[Markdown] = Field(
        description="Anything special about operation behavior",
        default=None,
    )

class CapabilityStatementRestSearchParam(BackboneElement):
    """
    Search parameters that are supported for searching all resources for implementations to support and/or make use of - either references to ones defined in the specification, or additional ones defined for/by the implementation.
    """

    name: Optional[String] = Field(
        description="Name of search parameter",
        default=None,
    )
    definition: Optional[Canonical] = Field(
        description="Source of definition for parameter",
        default=None,
    )
    type: Optional[Code] = Field(
        description="number | date | string | token | reference | composite | quantity | uri | special",
        default=None,
    )
    documentation: Optional[Markdown] = Field(
        description="Server-specific usage",
        default=None,
    )

class CapabilityStatementRestOperation(BackboneElement):
    """
    Definition of an operation or a named query together with its parameters and their meaning and type.
    """

    name: Optional[String] = Field(
        description="Name by which the operation/query is invoked",
        default=None,
    )
    definition: Optional[Canonical] = Field(
        description="The defined operation/query",
        default=None,
    )
    documentation: Optional[Markdown] = Field(
        description="Specific details about operation behavior",
        default=None,
    )

class CapabilityStatementRest(BackboneElement):
    """
    A definition of the restful capabilities of the solution, if any.
    """

    mode: Optional[Code] = Field(
        description="client | server",
        default=None,
    )
    documentation: Optional[Markdown] = Field(
        description="General description of implementation",
        default=None,
    )
    security: Optional[CapabilityStatementRestSecurity] = Field(
        description="Information about security of implementation",
        default=None,
    )
    resource: Optional[ListType[CapabilityStatementRestResource]] = Field(
        description="Resource served on the REST interface",
        default=None,
    )
    interaction: Optional[ListType[CapabilityStatementRestInteraction]] = Field(
        description="What operations are supported?",
        default=None,
    )
    searchParam: Optional[ListType[CapabilityStatementRestSearchParam]] = Field(
        description="Search parameters for searching all resources",
        default=None,
    )
    operation: Optional[ListType[CapabilityStatementRestOperation]] = Field(
        description="Definition of a system level operation",
        default=None,
    )
    compartment: Optional[ListType[Canonical]] = Field(
        description="Compartments served/used by system",
        default=None,
    )

class CapabilityStatementMessagingEndpoint(BackboneElement):
    """
    An endpoint (network accessible address) to which messages and/or replies are to be sent.
    """

    protocol: Optional[Coding] = Field(
        description="http | ftp | mllp +",
        default=None,
    )
    address: Optional[Url] = Field(
        description="Network address or identifier of the end-point",
        default=None,
    )

class CapabilityStatementMessagingSupportedMessage(BackboneElement):
    """
    References to message definitions for messages this system can send or receive.
    """

    mode: Optional[Code] = Field(
        description="sender | receiver",
        default=None,
    )
    definition: Optional[Canonical] = Field(
        description="Message supported by this system",
        default=None,
    )

class CapabilityStatementMessaging(BackboneElement):
    """
    A description of the messaging capabilities of the solution.
    """

    endpoint: Optional[ListType[CapabilityStatementMessagingEndpoint]] = Field(
        description="Where messages should be sent",
        default=None,
    )
    reliableCache: Optional[UnsignedInt] = Field(
        description="Reliable Message Cache Length (min)",
        default=None,
    )
    documentation: Optional[Markdown] = Field(
        description="Messaging interface behavior details",
        default=None,
    )
    supportedMessage: Optional[
        ListType[CapabilityStatementMessagingSupportedMessage]
    ] = Field(
        description="Messages supported by this system",
        default=None,
    )

class CapabilityStatementDocument(BackboneElement):
    """
    A document definition.
    """

    mode: Optional[Code] = Field(
        description="producer | consumer",
        default=None,
    )
    documentation: Optional[Markdown] = Field(
        description="Description of document support",
        default=None,
    )
    profile: Optional[Canonical] = Field(
        description="Constraint on the resources used in the document",
        default=None,
    )

class CapabilityStatement(DomainResource):
    """
    A Capability Statement documents a set of capabilities (behaviors) of a FHIR Server for a particular version of FHIR that may be used as a statement of actual server functionality or a statement of required or desired server implementation.
    """

    _abstract = False
    _type = "CapabilityStatement"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/CapabilityStatement"

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
        description="Canonical identifier for this capability statement, represented as a URI (globally unique)",
        default=None,
    )
    version: Optional[String] = Field(
        description="Business version of the capability statement",
        default=None,
    )
    name: Optional[String] = Field(
        description="Name for this capability statement (computer friendly)",
        default=None,
    )
    title: Optional[String] = Field(
        description="Name for this capability statement (human friendly)",
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
        description="Natural language description of the capability statement",
        default=None,
    )
    useContext: Optional[ListType[UsageContext]] = Field(
        description="The context that the content is intended to support",
        default=None,
    )
    jurisdiction: Optional[ListType[CodeableConcept]] = Field(
        description="Intended jurisdiction for capability statement (if applicable)",
        default=None,
    )
    purpose: Optional[Markdown] = Field(
        description="Why this capability statement is defined",
        default=None,
    )
    copyright: Optional[Markdown] = Field(
        description="Use and/or publishing restrictions",
        default=None,
    )
    kind: Optional[Code] = Field(
        description="instance | capability | requirements",
        default=None,
    )
    instantiates: Optional[ListType[Canonical]] = Field(
        description="Canonical URL of another capability statement this implements",
        default=None,
    )
    imports: Optional[ListType[Canonical]] = Field(
        description="Canonical URL of another capability statement this adds to",
        default=None,
    )
    software: Optional[CapabilityStatementSoftware] = Field(
        description="Software that is covered by this capability statement",
        default=None,
    )
    implementation: Optional[CapabilityStatementImplementation] = Field(
        description="If this describes a specific instance",
        default=None,
    )
    fhirVersion: Optional[Code] = Field(
        description="FHIR Version the system supports",
        default=None,
    )
    format: Optional[ListType[Code]] = Field(
        description="formats supported (xml | json | ttl | mime type)",
        default=None,
    )
    patchFormat: Optional[ListType[Code]] = Field(
        description="Patch formats supported",
        default=None,
    )
    implementationGuide: Optional[ListType[Canonical]] = Field(
        description="Implementation guides supported",
        default=None,
    )
    rest: Optional[ListType[CapabilityStatementRest]] = Field(
        description="If the endpoint is a RESTful one",
        default=None,
    )
    messaging: Optional[ListType[CapabilityStatementMessaging]] = Field(
        description="If messaging is supported",
        default=None,
    )
    document: Optional[ListType[CapabilityStatementDocument]] = Field(
        description="Document definition",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_cpb_9_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("rest",),
            expression="resource.select(type).isDistinct()",
            human="A given resource can only be described once per RESTful mode.",
            key="cpb-9",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_cpb_0_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.matches('[A-Z]([A-Za-z0-9_]){0,254}')",
            human="Name should be usable as an identifier for the module by machine processing applications such as code generation",
            key="cpb-0",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_cpb_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="rest.exists() or messaging.exists() or document.exists()",
            human="A Capability Statement SHALL have at least one of REST, messaging or document element.",
            key="cpb-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_cpb_2_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(description.count() + software.count() + implementation.count()) > 0",
            human="A Capability Statement SHALL have at least one of description, software, or implementation element.",
            key="cpb-2",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_cpb_3_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="messaging.endpoint.empty() or kind = 'instance'",
            human="Messaging end-point is required (and is only permitted) when a statement is for an implementation.",
            key="cpb-3",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_cpb_7_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="document.select(profile&mode).isDistinct()",
            human="The set of documents must be unique by the combination of profile and mode.",
            key="cpb-7",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_cpb_12_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("rest.resource",),
            expression="searchParam.select(name).isDistinct()",
            human="Search parameter names must be unique in the context of a resource.",
            key="cpb-12",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_cpb_14_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(kind != 'instance') or implementation.exists()",
            human="If kind = instance, implementation must be present and software may be present",
            key="cpb-14",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_cpb_15_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(kind != 'capability') or (implementation.exists().not() and software.exists())",
            human="If kind = capability, implementation must be absent, software must be present",
            key="cpb-15",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_cpb_16_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(kind!='requirements') or (implementation.exists().not() and software.exists().not())",
            human="If kind = requirements, implementation and software must be absent",
            key="cpb-16",
            severity="error",
        )
