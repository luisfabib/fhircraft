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
    Identifier,
    ContactDetail,
    UsageContext,
    CodeableConcept,
    BackboneElement,
)
from .resource import Resource
from .domain_resource import DomainResource


class ConceptMapGroupElementTargetDependsOn(BackboneElement):
    """
    A set of additional dependencies for this mapping to hold. This mapping is only applicable if the specified element can be resolved, and it has the specified value.
    """

    property_: fhir.uri = Field(
        description="Reference to property mapping depends on",
        alias="property",
    )
    system: Optional[fhir.canonical] = Field(
        description="code System (if necessary)",
        default=None,
    )
    value: fhir.string = Field(
        description="Value of the referenced element",
    )
    display: Optional[fhir.string] = Field(
        description="Display for the code (if value is a code)",
        default=None,
    )


class ConceptMapGroupElementTargetProduct(BackboneElement):
    """
    A set of additional outcomes from this mapping to other elements. To properly execute this mapping, the specified element must be mapped to some data element or source that is in context. The mapping may still be useful without a place for the additional data elements, but the equivalence cannot be relied on.
    """

    property_: Optional[fhir.uri] = Field(
        description="Reference to property mapping depends on",
        default=None,
        alias="property",
    )
    system: Optional[fhir.canonical] = Field(
        description="code System (if necessary)",
        default=None,
    )
    value: Optional[fhir.string] = Field(
        description="Value of the referenced element",
        default=None,
    )
    display: Optional[fhir.string] = Field(
        description="Display for the code (if value is a code)",
        default=None,
    )


class ConceptMapGroupElementTarget(BackboneElement):
    """
    A concept from the target value set that this concept maps to.
    """

    code: Optional[fhir.code] = Field(
        description="code that identifies the target element",
        default=None,
    )
    display: Optional[fhir.string] = Field(
        description="Display for the code",
        default=None,
    )
    equivalence: fhir.code = Field(
        description="relatedto | equivalent | equal | wider | subsumes | narrower | specializes | inexact | unmatched | disjoint",
    )
    comment: Optional[fhir.string] = Field(
        description="Description of status/issues in mapping",
        default=None,
    )
    dependsOn: Optional[ListType[ConceptMapGroupElementTargetDependsOn]] = Field(
        description="Other elements required for this mapping (from context)",
        default=None,
    )
    product: Optional[ListType[ConceptMapGroupElementTargetProduct]] = Field(
        description="Other concepts that this mapping also produces",
        default=None,
    )


class ConceptMapGroupElement(BackboneElement):
    """
    Mappings for an individual concept in the source to one or more concepts in the target.
    """

    code: Optional[fhir.code] = Field(
        description="Identifies element being mapped",
        default=None,
    )
    display: Optional[fhir.string] = Field(
        description="Display for the code",
        default=None,
    )
    target: Optional[ListType[ConceptMapGroupElementTarget]] = Field(
        description="Concept in target system for element",
        default=None,
    )


class ConceptMapGroupUnmapped(BackboneElement):
    """
    What to do when there is no mapping for the source concept. "Unmapped" does not include codes that are unmatched, and the unmapped element is ignored in a code is specified to have equivalence = unmatched.
    """

    mode: fhir.code = Field(
        description="provided | fixed | other-map",
    )
    code: Optional[fhir.code] = Field(
        description="Fixed code when mode = fixed",
        default=None,
    )
    display: Optional[fhir.string] = Field(
        description="Display for the code",
        default=None,
    )
    url: Optional[fhir.canonical] = Field(
        description="canonical reference to an additional ConceptMap to use for mapping if the source concept is unmapped",
        default=None,
    )


class ConceptMapGroup(BackboneElement):
    """
    A group of mappings that all have the same source and target system.
    """

    source: Optional[fhir.uri] = Field(
        description="Source system where concepts to be mapped are defined",
        default=None,
    )
    sourceVersion: Optional[fhir.string] = Field(
        description="Specific version of the  code system",
        default=None,
    )
    target: Optional[fhir.uri] = Field(
        description="Target system that the concepts are to be mapped to",
        default=None,
    )
    targetVersion: Optional[fhir.string] = Field(
        description="Specific version of the  code system",
        default=None,
    )
    element: ListType[ConceptMapGroupElement] = Field(
        description="Mappings for a concept from the source set",
    )
    unmapped: Optional[ConceptMapGroupUnmapped] = Field(
        description="What to do when there is no mapping for the source concept",
        default=None,
    )


class ConceptMap(DomainResource):
    """
    A statement of relationships from one set of concepts to one or more other concepts - either concepts in code systems, or data element/data element concepts, or classes in class models.
    """

    _abstract = False
    _type = "ConceptMap"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/ConceptMap"

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
        description="canonical identifier for this concept map, represented as a URI (globally unique)",
        default=None,
    )
    identifier: Optional[Identifier] = Field(
        description="Additional identifier for the concept map",
        default=None,
    )
    version: Optional[fhir.string] = Field(
        description="Business version of the concept map",
        default=None,
    )
    name: Optional[fhir.string] = Field(
        description="Name for this concept map (computer friendly)",
        default=None,
    )
    title: Optional[fhir.string] = Field(
        description="Name for this concept map (human friendly)",
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
        description="Natural language description of the concept map",
        default=None,
    )
    useContext: Optional[ListType[UsageContext]] = Field(
        description="The context that the content is intended to support",
        default=None,
    )
    jurisdiction: Optional[ListType[CodeableConcept]] = Field(
        description="Intended jurisdiction for concept map (if applicable)",
        default=None,
    )
    purpose: Optional[fhir.markdown] = Field(
        description="Why this concept map is defined",
        default=None,
    )
    copyright: Optional[fhir.markdown] = Field(
        description="Use and/or publishing restrictions",
        default=None,
    )
    sourceUri: Optional[fhir.uri] = Field(
        description="The source value set that contains the concepts that are being mapped",
        default=None,
    )
    sourceCanonical: Optional[fhir.canonical] = Field(
        description="The source value set that contains the concepts that are being mapped",
        default=None,
    )
    targetUri: Optional[fhir.uri] = Field(
        description="The target value set which provides context for the mappings",
        default=None,
    )
    targetCanonical: Optional[fhir.canonical] = Field(
        description="The target value set which provides context for the mappings",
        default=None,
    )
    group: Optional[ListType[ConceptMapGroup]] = Field(
        description="Same source and target systems",
        default=None,
    )

    @property
    def source(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="source",
        )

    @property
    def target(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="target",
        )

    @model_validator(mode="after")
    def source_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.Uri, fhir.Canonical],
            field_name_base="source",
            required=False,
        )

    @model_validator(mode="after")
    def target_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.Uri, fhir.Canonical],
            field_name_base="target",
            required=False,
        )

    @model_validator(mode="after")
    def FHIR_cmd_0_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.exists() implies name.matches('[A-Z]([A-Za-z0-9_]){0,254}')",
            human="Name should be usable as an identifier for the module by machine processing applications such as code generation",
            key="cmd-0",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_cmd_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("group.element.target",),
            expression="comment.exists() or equivalence.empty() or ((equivalence != 'narrower') and (equivalence != 'inexact'))",
            human="If the map is narrower or inexact, there SHALL be some comments",
            key="cmd-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_cmd_2_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("group.unmapped",),
            expression="(mode = 'fixed') implies code.exists()",
            human="If the mode is 'fixed', a code must be provided",
            key="cmd-2",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_cmd_3_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("group.unmapped",),
            expression="(mode = 'other-map') implies url.exists()",
            human="If the mode is 'other-map', a url must be provided",
            key="cmd-3",
            severity="error",
        )
