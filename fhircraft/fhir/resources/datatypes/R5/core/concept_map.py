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
    Period,
    RelatedArtifact,
    BackboneElement,
    Quantity,
)
from .resource import Resource
from .domain_resource import DomainResource


class ConceptMapProperty(BackboneElement):
    """
    A property defines a slot through which additional information can be provided about a map from source -> target.
    """

    code: fhir.code = Field(
        description="Identifies the property on the mappings, and when referred to in the $translate operation",
    )
    uri: Optional[fhir.uri] = Field(
        description="Formal identifier for the property",
        default=None,
    )
    description: Optional[fhir.string] = Field(
        description="Why the property is defined, and/or what it conveys",
        default=None,
    )
    type: fhir.code = Field(
        description="Coding | string | integer | boolean | dateTime | decimal | code",
    )
    system: Optional[fhir.canonical] = Field(
        description="The CodeSystem from which code values come",
        default=None,
    )


class ConceptMapAdditionalAttribute(BackboneElement):
    """
    An additionalAttribute defines an additional data element found in the source or target data model where the data will come from or be mapped to. Some mappings are based on data in addition to the source data element, where codes in multiple fields are combined to a single field (or vice versa).
    """

    code: fhir.code = Field(
        description="Identifies this additional attribute through this resource",
    )
    uri: Optional[fhir.uri] = Field(
        description="Formal identifier for the data element referred to in this attribte",
        default=None,
    )
    description: Optional[fhir.string] = Field(
        description="Why the additional attribute is defined, and/or what the data element it refers to is",
        default=None,
    )
    type: fhir.code = Field(
        description="code | Coding | string | boolean | Quantity",
    )


class ConceptMapGroupElementTargetProperty(BackboneElement):
    """
    A property value for this source -> target mapping.
    """

    code: fhir.code = Field(
        description="Reference to ConceptMap.property.code",
    )
    valueCoding: Optional[Coding] = Field(
        description="Value of the property for this concept",
        default=None,
    )
    valueString: Optional[fhir.string] = Field(
        description="Value of the property for this concept",
        default=None,
    )
    valueInteger: Optional[fhir.integer] = Field(
        description="Value of the property for this concept",
        default=None,
    )
    valueBoolean: Optional[fhir.boolean] = Field(
        description="Value of the property for this concept",
        default=None,
    )
    valueDateTime: Optional[fhir.dateTime] = Field(
        description="Value of the property for this concept",
        default=None,
    )
    valueDecimal: Optional[fhir.decimal] = Field(
        description="Value of the property for this concept",
        default=None,
    )
    valueCode: Optional[fhir.code] = Field(
        description="Value of the property for this concept",
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
                Coding,
                fhir.String,
                fhir.Integer,
                fhir.Boolean,
                fhir.DateTime,
                fhir.Decimal,
                fhir.Code,
            ],
            field_name_base="value",
            required=True,
        )


class ConceptMapGroupElementTargetDependsOn(BackboneElement):
    """
    A set of additional dependencies for this mapping to hold. This mapping is only applicable if the specified data attribute can be resolved, and it has the specified value.
    """

    attribute: fhir.code = Field(
        description="A reference to a mapping attribute defined in ConceptMap.additionalAttribute",
    )
    valueCode: Optional[fhir.code] = Field(
        description="Value of the referenced data element",
        default=None,
    )
    valueCoding: Optional[Coding] = Field(
        description="Value of the referenced data element",
        default=None,
    )
    valueString: Optional[fhir.string] = Field(
        description="Value of the referenced data element",
        default=None,
    )
    valueBoolean: Optional[fhir.boolean] = Field(
        description="Value of the referenced data element",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="Value of the referenced data element",
        default=None,
    )
    valueSet: Optional[fhir.canonical] = Field(
        description="The mapping depends on a data element with a value from this value set",
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
            field_types=[fhir.Code, Coding, fhir.String, fhir.Boolean, Quantity],
            field_name_base="value",
            required=False,
        )


class ConceptMapGroupElementTargetProduct(BackboneElement):
    """
    Product is the output of a ConceptMap that provides additional values that go in other attributes / data elemnts of the target data.
    """

    attribute: Optional[fhir.code] = Field(
        description="A reference to a mapping attribute defined in ConceptMap.additionalAttribute",
        default=None,
    )
    valueCode: Optional[fhir.code] = Field(
        description="Value of the referenced data element",
        default=None,
    )
    valueCoding: Optional[Coding] = Field(
        description="Value of the referenced data element",
        default=None,
    )
    valueString: Optional[fhir.string] = Field(
        description="Value of the referenced data element",
        default=None,
    )
    valueBoolean: Optional[fhir.boolean] = Field(
        description="Value of the referenced data element",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="Value of the referenced data element",
        default=None,
    )
    valueSet: Optional[fhir.canonical] = Field(
        description="The mapping depends on a data element with a value from this value set",
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
            field_types=[fhir.Code, Coding, fhir.String, fhir.Boolean, Quantity],
            field_name_base="value",
            required=False,
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
    valueSet: Optional[fhir.canonical] = Field(
        description="Identifies the set of target concepts",
        default=None,
    )
    relationship: fhir.code = Field(
        description="related-to | equivalent | source-is-narrower-than-target | source-is-broader-than-target | not-related-to",
    )
    comment: Optional[fhir.string] = Field(
        description="Description of status/issues in mapping",
        default=None,
    )
    property_: Optional[ListType[ConceptMapGroupElementTargetProperty]] = Field(
        description="Property value for the source -\u003e target mapping",
        default=None,
        alias="property",
    )
    dependsOn: Optional[ListType[ConceptMapGroupElementTargetDependsOn]] = Field(
        description="Other properties required for this mapping",
        default=None,
    )
    product: Optional[ListType[ConceptMapGroupElementTargetProduct]] = Field(
        description="Other data elements that this mapping also produces",
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
    valueSet: Optional[fhir.canonical] = Field(
        description="Identifies the set of concepts being mapped",
        default=None,
    )
    noMap: Optional[fhir.boolean] = Field(
        description="No mapping to a target concept for this source concept",
        default=None,
    )
    target: Optional[ListType[ConceptMapGroupElementTarget]] = Field(
        description="Concept in target system for element",
        default=None,
    )


class ConceptMapGroupUnmapped(BackboneElement):
    """
    What to do when there is no mapping to a target concept from the source concept and ConceptMap.group.element.noMap is not true. This provides the "default" to be applied when there is no target concept mapping specified or the expansion of ConceptMap.group.element.target.valueSet is empty.
    """

    mode: fhir.code = Field(
        description="use-source-code | fixed | other-map",
    )
    code: Optional[fhir.code] = Field(
        description="Fixed code when mode = fixed",
        default=None,
    )
    display: Optional[fhir.string] = Field(
        description="Display for the code",
        default=None,
    )
    valueSet: Optional[fhir.canonical] = Field(
        description="Fixed code set when mode = fixed",
        default=None,
    )
    relationship: Optional[fhir.code] = Field(
        description="related-to | equivalent | source-is-narrower-than-target | source-is-broader-than-target | not-related-to",
        default=None,
    )
    otherMap: Optional[fhir.canonical] = Field(
        description="canonical reference to an additional ConceptMap to use for mapping if the source concept is unmapped",
        default=None,
    )


class ConceptMapGroup(BackboneElement):
    """
    A group of mappings that all have the same source and target system.
    """

    source: Optional[fhir.canonical] = Field(
        description="Source system where concepts to be mapped are defined",
        default=None,
    )
    target: Optional[fhir.canonical] = Field(
        description="Target system that the concepts are to be mapped to",
        default=None,
    )
    element: ListType[ConceptMapGroupElement] = Field(
        description="Mappings for a concept from the source set",
     	min_length=1,
	)
    unmapped: Optional[ConceptMapGroupUnmapped] = Field(
        description="What to do when there is no mapping target for the source concept and ConceptMap.group.element.noMap is not true",
        default=None,
    )


class ConceptMap(DomainResource):
    """
    A statement of relationships from one set of concepts to one or more other concepts - either concepts in code systems, or data element/data element concepts, or classes in class models.
    """

    _abstract = False
    _type = "ConceptMap"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/ConceptMap"

    url: Optional[fhir.uri] = Field(
        description="canonical identifier for this concept map, represented as a URI (globally unique)",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Additional identifier for the concept map",
        default=None,
    )
    version: Optional[fhir.string] = Field(
        description="Business version of the concept map",
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
        description="Name of the publisher/steward (organization or individual)",
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
    copyrightLabel: Optional[fhir.string] = Field(
        description="Copyright holder and year(s)",
        default=None,
    )
    approvalDate: Optional[fhir.date_] = Field(
        description="When the ConceptMap was approved by publisher",
        default=None,
    )
    lastReviewDate: Optional[fhir.date_] = Field(
        description="When the ConceptMap was last reviewed by the publisher",
        default=None,
    )
    effectivePeriod: Optional[Period] = Field(
        description="When the ConceptMap is expected to be used",
        default=None,
    )
    topic: Optional[ListType[CodeableConcept]] = Field(
        description="E.g. Education, Treatment, Assessment, etc",
        default=None,
    )
    author: Optional[ListType[ContactDetail]] = Field(
        description="Who authored the ConceptMap",
        default=None,
    )
    editor: Optional[ListType[ContactDetail]] = Field(
        description="Who edited the ConceptMap",
        default=None,
    )
    reviewer: Optional[ListType[ContactDetail]] = Field(
        description="Who reviewed the ConceptMap",
        default=None,
    )
    endorser: Optional[ListType[ContactDetail]] = Field(
        description="Who endorsed the ConceptMap",
        default=None,
    )
    relatedArtifact: Optional[ListType[RelatedArtifact]] = Field(
        description="Additional documentation, citations, etc",
        default=None,
    )
    property_: Optional[ListType[ConceptMapProperty]] = Field(
        description="Additional properties of the mapping",
        default=None,
        alias="property",
    )
    additionalAttribute: Optional[ListType[ConceptMapAdditionalAttribute]] = Field(
        description="Definition of an additional attribute to act as a data source or target",
        default=None,
    )
    sourceScopeUri: Optional[fhir.uri] = Field(
        description="The source value set that contains the concepts that are being mapped",
        default=None,
    )
    sourceScopeCanonical: Optional[fhir.canonical] = Field(
        description="The source value set that contains the concepts that are being mapped",
        default=None,
    )
    targetScopeUri: Optional[fhir.uri] = Field(
        description="The target value set which provides context for the mappings",
        default=None,
    )
    targetScopeCanonical: Optional[fhir.canonical] = Field(
        description="The target value set which provides context for the mappings",
        default=None,
    )
    group: Optional[ListType[ConceptMapGroup]] = Field(
        description="Same source and target systems",
        default=None,
    )

    @property
    def versionAlgorithm(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="versionAlgorithm",
        )

    @property
    def sourceScope(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="sourceScope",
        )

    @property
    def targetScope(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="targetScope",
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
    def sourceScope_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.Uri, fhir.Canonical],
            field_name_base="sourceScope",
            required=False,
        )

    @model_validator(mode="after")
    def targetScope_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.Uri, fhir.Canonical],
            field_name_base="targetScope",
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
    def FHIR_cmd_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("group.element.target",),
            expression="comment.exists() or (%resource.status = 'draft') or relationship.empty() or ((relationship != 'source-is-broader-than-target') and (relationship != 'not-related-to'))",
            human="If the map is source-is-broader-than-target or not-related-to, there SHALL be some comments, unless the status is 'draft'",
            key="cmd-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_cmd_2_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("unmapped",),
            expression="(mode = 'fixed') implies ((code.exists() and valueSet.empty()) or (code.empty() and valueSet.exists()))",
            human="If the mode is 'fixed', either a code or valueSet must be provided, but not both.",
            key="cmd-2",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_cmd_3_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("group.unmapped",),
            expression="(mode = 'other-map') implies otherMap.exists()",
            human="If the mode is 'other-map', a url for the other map must be provided",
            key="cmd-3",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_cmd_4_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("element",),
            expression="(noMap.exists() and noMap=true) implies target.empty()",
            human="If noMap is present, target SHALL NOT be present",
            key="cmd-4",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_cmd_5_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("element",),
            expression="(code.exists() and valueSet.empty()) or (code.empty() and valueSet.exists())",
            human="Either code or valueSet SHALL be present but not both.",
            key="cmd-5",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_cmd_6_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("group.element.target.dependsOn",),
            expression="(value.exists() and valueSet.empty()) or (value.empty() and valueSet.exists())",
            human="One of value[x] or valueSet must exist, but not both.",
            key="cmd-6",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_cmd_7_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("group.element.target",),
            expression="(code.exists() and valueSet.empty()) or (code.empty() and valueSet.exists())",
            human="Either code or valueSet SHALL be present but not both.",
            key="cmd-7",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_cmd_8_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("group.unmapped",),
            expression="(mode != 'fixed') implies (code.empty() and display.empty() and valueSet.empty())",
            human="If the mode is not 'fixed', code, display and valueSet are not allowed",
            key="cmd-8",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_cmd_9_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("group.unmapped",),
            expression="(mode != 'other-map') implies relationship.exists()",
            human="If the mode is not 'other-map', relationship must be provided",
            key="cmd-9",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_cmd_10_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("group.unmapped",),
            expression="(mode != 'other-map') implies otherMap.empty()",
            human="If the mode is not 'other-map', otherMap is not allowed",
            key="cmd-10",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_cmd_11_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("property_",),
            expression="type = 'code' implies system.exists()",
            human="If the property type is code, a system SHALL be specified",
            key="cmd-11",
            severity="error",
        )
