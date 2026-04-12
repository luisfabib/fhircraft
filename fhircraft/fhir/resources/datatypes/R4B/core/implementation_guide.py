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
    Reference,
)
from .resource import Resource
from .domain_resource import DomainResource


class ImplementationGuideDependsOn(BackboneElement):
    """
    Another implementation guide that this implementation depends on. Typically, an implementation guide uses value sets, profiles etc.defined in other implementation guides.
    """

    uri: Optional[fhir.canonical] = Field(
        description="Identity of the IG that this depends on",
        default=None,
    )
    packageId: Optional[fhir.id_] = Field(
        description="NPM Package name for IG this depends on",
        default=None,
    )
    version: Optional[fhir.string] = Field(
        description="Version of the IG",
        default=None,
    )


class ImplementationGuideGlobal(BackboneElement):
    """
    A set of profiles that all resources covered by this implementation guide must conform to.
    """

    type: Optional[fhir.code] = Field(
        description="Type this profile applies to",
        default=None,
    )
    profile: Optional[fhir.canonical] = Field(
        description="Profile that all resources must conform to",
        default=None,
    )


class ImplementationGuideDefinitionGrouping(BackboneElement):
    """
    A logical group of resources. Logical groups can be used when building pages.
    """

    name: Optional[fhir.string] = Field(
        description="Descriptive name for the package",
        default=None,
    )
    description: Optional[fhir.string] = Field(
        description="Human readable text describing the package",
        default=None,
    )


class ImplementationGuideDefinitionResource(BackboneElement):
    """
    A resource that is part of the implementation guide. Conformance resources (value set, structure definition, capability statements etc.) are obvious candidates for inclusion, but any kind of resource can be included as an example resource.
    """

    reference: Optional[Reference] = Field(
        description="Location of the resource",
        default=None,
    )
    fhirVersion: Optional[ListType[fhir.code]] = Field(
        description="Versions this applies to (if different to IG)",
        default=None,
    )
    name: Optional[fhir.string] = Field(
        description="Human Name for the resource",
        default=None,
    )
    description: Optional[fhir.string] = Field(
        description="Reason why included in guide",
        default=None,
    )
    exampleBoolean: Optional[fhir.boolean] = Field(
        description="Is an example/What is this an example of?",
        default=None,
    )
    exampleCanonical: Optional[fhir.canonical] = Field(
        description="Is an example/What is this an example of?",
        default=None,
    )
    groupingId: Optional[fhir.id_] = Field(
        description="Grouping this is part of",
        default=None,
    )

    @property
    def example(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="example",
        )

    @model_validator(mode="after")
    def example_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.Boolean, fhir.Canonical],
            field_name_base="example",
            required=False,
        )


class ImplementationGuideDefinitionPage(BackboneElement):
    """
    A page / section in the implementation guide. The root page is the implementation guide home page.
    """

    nameUrl: Optional[fhir.url] = Field(
        description="Where to find that page",
        default=None,
    )
    nameReference: Optional[Reference] = Field(
        description="Where to find that page",
        default=None,
    )
    title: Optional[fhir.string] = Field(
        description="Short title shown for navigational assistance",
        default=None,
    )
    generation: Optional[fhir.code] = Field(
        description="html | markdown | xml | generated",
        default=None,
    )
    page: Optional[ListType["ImplementationGuideDefinitionPage"]] = Field(
        description="Nested Pages / Sections",
        default=None,
    )

    @property
    def name(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="name",
        )

    @model_validator(mode="after")
    def name_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.Url, Reference],
            field_name_base="name",
            required=True,
        )


class ImplementationGuideDefinitionParameter(BackboneElement):
    """
    Defines how IG is built by tools.
    """

    code: Optional[fhir.code] = Field(
        description="apply | path-resource | path-pages | path-tx-cache | expansion-parameter | rule-broken-links | generate-xml | generate-json | generate-turtle | html-template",
        default=None,
    )
    value: Optional[fhir.string] = Field(
        description="Value for named type",
        default=None,
    )


class ImplementationGuideDefinitionTemplate(BackboneElement):
    """
    A template for building resources.
    """

    code: Optional[fhir.code] = Field(
        description="Type of template specified",
        default=None,
    )
    source: Optional[fhir.string] = Field(
        description="The source location for the template",
        default=None,
    )
    scope: Optional[fhir.string] = Field(
        description="The scope in which the template applies",
        default=None,
    )


class ImplementationGuideDefinition(BackboneElement):
    """
    The information needed by an IG publisher tool to publish the whole implementation guide.
    """

    grouping: Optional[ListType[ImplementationGuideDefinitionGrouping]] = Field(
        description="Grouping used to present related resources in the IG",
        default=None,
    )
    resource: Optional[ListType[ImplementationGuideDefinitionResource]] = Field(
        description="Resource in the implementation guide",
        default=None,
    )
    page: Optional[ImplementationGuideDefinitionPage] = Field(
        description="Page/Section in the Guide",
        default=None,
    )
    parameter: Optional[ListType[ImplementationGuideDefinitionParameter]] = Field(
        description="Defines how IG is built by tools",
        default=None,
    )
    template: Optional[ListType[ImplementationGuideDefinitionTemplate]] = Field(
        description="A template for building resources",
        default=None,
    )


class ImplementationGuideManifestResource(BackboneElement):
    """
    A resource that is part of the implementation guide. Conformance resources (value set, structure definition, capability statements etc.) are obvious candidates for inclusion, but any kind of resource can be included as an example resource.
    """

    reference: Optional[Reference] = Field(
        description="Location of the resource",
        default=None,
    )
    exampleBoolean: Optional[fhir.boolean] = Field(
        description="Is an example/What is this an example of?",
        default=None,
    )
    exampleCanonical: Optional[fhir.canonical] = Field(
        description="Is an example/What is this an example of?",
        default=None,
    )
    relativePath: Optional[fhir.url] = Field(
        description="Relative path for page in IG",
        default=None,
    )

    @property
    def example(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="example",
        )

    @model_validator(mode="after")
    def example_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.Boolean, fhir.Canonical],
            field_name_base="example",
            required=False,
        )


class ImplementationGuideManifestPage(BackboneElement):
    """
    Information about a page within the IG.
    """

    name: Optional[fhir.string] = Field(
        description="HTML page name",
        default=None,
    )
    title: Optional[fhir.string] = Field(
        description="Title of the page, for references",
        default=None,
    )
    anchor: Optional[ListType[fhir.string]] = Field(
        description="Anchor available on the page",
        default=None,
    )


class ImplementationGuideManifest(BackboneElement):
    """
    Information about an assembled implementation guide, created by the publication tooling.
    """

    rendering: Optional[fhir.url] = Field(
        description="Location of rendered implementation guide",
        default=None,
    )
    resource: Optional[ListType[ImplementationGuideManifestResource]] = Field(
        description="Resource in the implementation guide",
        default=None,
    )
    page: Optional[ListType[ImplementationGuideManifestPage]] = Field(
        description="HTML page within the parent IG",
        default=None,
    )
    image: Optional[ListType[fhir.string]] = Field(
        description="Image within the IG",
        default=None,
    )
    other: Optional[ListType[fhir.string]] = Field(
        description="Additional linkable file in IG",
        default=None,
    )


class ImplementationGuide(DomainResource):
    """
    A set of rules of how a particular interoperability or standards problem is solved - typically through the use of FHIR resources. This resource is used to gather all the parts of an implementation guide into a logical whole and to publish a computable definition of all the parts.
    """

    _abstract = False
    _type = "ImplementationGuide"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/ImplementationGuide"

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
        description="canonical identifier for this implementation guide, represented as a URI (globally unique)",
        default=None,
    )
    version: Optional[fhir.string] = Field(
        description="Business version of the implementation guide",
        default=None,
    )
    name: Optional[fhir.string] = Field(
        description="Name for this implementation guide (computer friendly)",
        default=None,
    )
    title: Optional[fhir.string] = Field(
        description="Name for this implementation guide (human friendly)",
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
        description="Name of the publisher (organization or individual)",
        default=None,
    )
    contact: Optional[ListType[ContactDetail]] = Field(
        description="Contact details for the publisher",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
        description="Natural language description of the implementation guide",
        default=None,
    )
    useContext: Optional[ListType[UsageContext]] = Field(
        description="The context that the content is intended to support",
        default=None,
    )
    jurisdiction: Optional[ListType[CodeableConcept]] = Field(
        description="Intended jurisdiction for implementation guide (if applicable)",
        default=None,
    )
    copyright: Optional[fhir.markdown] = Field(
        description="Use and/or publishing restrictions",
        default=None,
    )
    packageId: Optional[fhir.id_] = Field(
        description="NPM Package name for IG",
        default=None,
    )
    license: Optional[fhir.code] = Field(
        description="SPDX license code for this IG (or not-open-source)",
        default=None,
    )
    fhirVersion: Optional[ListType[fhir.code]] = Field(
        description="FHIR Version(s) this Implementation Guide targets",
        default=None,
    )
    dependsOn: Optional[ListType[ImplementationGuideDependsOn]] = Field(
        description="Another Implementation guide this depends on",
        default=None,
    )
    global_: Optional[ListType[ImplementationGuideGlobal]] = Field(
        description="Profiles that apply globally",
        default=None,
        alias="global",
    )
    definition: Optional[ImplementationGuideDefinition] = Field(
        description="Information needed to build the IG",
        default=None,
    )
    manifest: Optional[ImplementationGuideManifest] = Field(
        description="Information about an assembled IG",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ig_0_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.exists() implies name.matches('[A-Z]([A-Za-z0-9_]){0,254}')",
            human="Name should be usable as an identifier for the module by machine processing applications such as code generation",
            key="ig-0",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_ig_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("definition",),
            expression="resource.groupingId.all(%context.grouping.id contains $this)",
            human="If a resource has a groupingId, it must refer to a grouping defined in the Implementation Guide",
            key="ig-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ig_2_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="definition.resource.fhirVersion.all(%context.fhirVersion contains $this)",
            human="If a resource has a fhirVersion, it must be oe of the versions defined for the Implementation Guide",
            key="ig-2",
            severity="error",
        )
