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
    ElementDefinition,
)
from .resource import Resource
from .domain_resource import DomainResource


class StructureDefinitionMapping(BackboneElement):
    """
    An external specification that the content is mapped to.
    """

    identity: Optional[fhir.id_] = Field(
        description="Internal id when this mapping is used",
        default=None,
    )
    uri: Optional[fhir.uri] = Field(
        description="Identifies what this mapping refers to",
        default=None,
    )
    name: Optional[fhir.string] = Field(
        description="Names what this mapping refers to",
        default=None,
    )
    comment: Optional[fhir.string] = Field(
        description="Versions, Issues, Scope limitations etc",
        default=None,
    )


class StructureDefinitionContext(BackboneElement):
    """
    Identifies the types of resource or data type elements to which the extension can be applied. For more guidance on using the 'context' element, see the [defining extensions page](https://hl7.org/fhir/R5/defining-extensions.html#context).
    """

    type: Optional[fhir.code] = Field(
        description="fhirpath | element | extension",
        default=None,
    )
    expression: Optional[fhir.string] = Field(
        description="Where the extension can be used in instances",
        default=None,
    )


class StructureDefinitionSnapshot(BackboneElement):
    """
    A snapshot view is expressed in a standalone form that can be used and interpreted without considering the base StructureDefinition.
    """

    element: Optional[ListType[ElementDefinition]] = Field(
        description="Definition of elements in the resource (if no StructureDefinition)",
        default=None,
        min_length=1,
    )


class StructureDefinitionDifferential(BackboneElement):
    """
    A differential view is expressed relative to the base StructureDefinition - a statement of differences that it applies.
    """

    element: Optional[ListType[ElementDefinition]] = Field(
        description="Definition of elements in the resource (if no StructureDefinition)",
        default=None,
    )


class StructureDefinition(DomainResource):
    """
    A definition of a FHIR structure. This resource is used to describe the underlying resources, data types defined in FHIR, and also for describing extensions and constraints on resources and data types.
    """

    _abstract = False
    _type = "StructureDefinition"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/StructureDefinition"

    url: Optional[fhir.uri] = Field(
        description="canonical identifier for this structure definition, represented as a URI (globally unique)",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Additional identifier for the structure definition",
        default=None,
    )
    version: Optional[fhir.string] = Field(
        description="Business version of the structure definition",
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
        description="Name for this structure definition (computer friendly)",
        default=None,
    )
    title: Optional[fhir.string] = Field(
        description="Name for this structure definition (human friendly)",
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
        description="Natural language description of the structure definition",
        default=None,
    )
    useContext: Optional[ListType[UsageContext]] = Field(
        description="The context that the content is intended to support",
        default=None,
    )
    jurisdiction: Optional[ListType[CodeableConcept]] = Field(
        description="Intended jurisdiction for structure definition (if applicable)",
        default=None,
    )
    purpose: Optional[fhir.markdown] = Field(
        description="Why this structure definition is defined",
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
    keyword: Optional[ListType[Coding]] = Field(
        description="Assist with indexing and finding",
        default=None,
    )
    fhirVersion: Optional[fhir.code] = Field(
        description="FHIR Version this StructureDefinition targets",
        default=None,
    )
    mapping: Optional[ListType[StructureDefinitionMapping]] = Field(
        description="External specification that the content is mapped to",
        default=None,
    )
    kind: Optional[fhir.code] = Field(
        description="primitive-type | complex-type | resource | logical",
        default=None,
    )
    abstract: Optional[fhir.boolean] = Field(
        description="Whether the structure is abstract",
        default=None,
    )
    context: Optional[ListType[StructureDefinitionContext]] = Field(
        description="If an extension, where it can be used in instances",
        default=None,
    )
    contextInvariant: Optional[ListType[fhir.string]] = Field(
        description="FHIRPath invariants - when the extension can be used",
        default=None,
    )
    type: Optional[fhir.uri] = Field(
        description="Type defined or constrained by this structure",
        default=None,
    )
    baseDefinition: Optional[fhir.canonical] = Field(
        description="Definition that this type is constrained/specialized from",
        default=None,
    )
    derivation: Optional[fhir.code] = Field(
        description="specialization | constraint - How relates to base definition",
        default=None,
    )
    snapshot: Optional[StructureDefinitionSnapshot] = Field(
        description="Snapshot view of the structure",
        default=None,
    )
    differential: Optional[StructureDefinitionDifferential] = Field(
        description="Differential view of the structure",
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
            field_types=[fhir.String, Coding],
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
    def FHIR_sdf_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="derivation = 'constraint' or snapshot.element.select(path).isDistinct()",
            human="Element paths must be unique unless the structure is a constraint",
            key="sdf-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_sdf_2_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("mapping",),
            expression="name.exists() or uri.exists()",
            human="Must have at least a name or a uri (or both)",
            key="sdf-2",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_sdf_3_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("snapshot",),
            expression="%resource.kind = 'logical' or element.all(definition.exists() and min.exists() and max.exists())",
            human="Each element definition in a snapshot must have a formal definition and cardinalities, unless model is a logical model",
            key="sdf-3",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_sdf_4_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="abstract = true or baseDefinition.exists()",
            human="If the structure is not abstract, then there SHALL be a baseDefinition",
            key="sdf-4",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_sdf_5_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="type != 'Extension' or derivation = 'specialization' or (context.exists())",
            human="If the structure defines an extension then the structure must have context information",
            key="sdf-5",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_sdf_6_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="snapshot.exists() or differential.exists()",
            human="A structure must have either a differential, or a snapshot (or both)",
            key="sdf-6",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_sdf_8_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("snapshot",),
            expression="(%resource.kind = 'logical' or element.first().path = %resource.type) and element.tail().all(path.startsWith(%resource.snapshot.element.first().path&'.'))",
            human="All snapshot elements must start with the StructureDefinition's specified type for non-logical models, or with the same type name for logical models",
            key="sdf-8",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_sdf_8a_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("differential",),
            expression="(%resource.kind = 'logical' or element.first().path.startsWith(%resource.type)) and (element.tail().empty() or  element.tail().all(path.startsWith(%resource.differential.element.first().path.replaceMatches('\\..*','')&'.')))",
            human="In any differential, all the elements must start with the StructureDefinition's specified type for non-logical models, or with the same type name for logical models",
            key="sdf-8a",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_sdf_8b_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("snapshot",),
            expression="element.all(base.exists())",
            human="All snapshot elements must have a base definition",
            key="sdf-8b",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_sdf_9_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="children().element.where(path.contains('.').not()).label.empty() and children().element.where(path.contains('.').not()).code.empty() and children().element.where(path.contains('.').not()).requirements.empty()",
            human='In any snapshot or differential, no label, code or requirements on an element without a "." in the path (e.g. the first element)',
            key="sdf-9",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_sdf_10_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("snapshot.element",),
            expression="binding.empty() or binding.valueSet.exists() or binding.description.exists()",
            human="provide either a binding reference or a description (or both)",
            key="sdf-10",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_sdf_11_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="kind != 'logical' implies snapshot.empty() or snapshot.element.first().path = type",
            human="If there's a type, its content must match the path name in the first element of a snapshot",
            key="sdf-11",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_sdf_14_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="snapshot.element.all(id.exists()) and differential.element.all(id.exists())",
            human="All element definitions must have an id",
            key="sdf-14",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_sdf_15_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="kind!='logical'  implies snapshot.element.first().type.empty()",
            human="The first element in a snapshot has no type unless model is a logical model.",
            key="sdf-15",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_sdf_15a_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(kind!='logical'  and differential.element.first().path.contains('.').not()) implies differential.element.first().type.empty()",
            human='If the first element in a differential has no "." in the path and it\'s not a logical model, it has no type',
            key="sdf-15a",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_sdf_16_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="snapshot.element.all(id.exists()) and snapshot.element.id.trace('ids').isDistinct()",
            human="All element definitions must have unique ids (snapshot)",
            key="sdf-16",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_sdf_17_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="differential.element.all(id.exists()) and differential.element.id.trace('ids').isDistinct()",
            human="All element definitions must have unique ids (diff)",
            key="sdf-17",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_sdf_18_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="contextInvariant.exists() implies type = 'Extension'",
            human="Context Invariants can only be used for extensions",
            key="sdf-18",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_sdf_19_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="url.startsWith('http://hl7.org/fhir/StructureDefinition') implies (differential | snapshot).element.type.code.all(matches('^[a-zA-Z0-9]+$') or matches('^http:\\/\\/hl7\\.org\\/fhirpath\\/System\\.[A-Z][A-Za-z]+$'))",
            human="FHIR Specification models only use FHIR defined types",
            key="sdf-19",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_sdf_20_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("differential",),
            expression="element.where(path.contains('.').not()).slicing.empty()",
            human="No slicing on the root element",
            key="sdf-20",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_sdf_21_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="differential.element.defaultValue.exists() implies (derivation = 'specialization')",
            human="Default values can only be specified on specializations",
            key="sdf-21",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_sdf_22_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="url.startsWith('http://hl7.org/fhir/StructureDefinition') implies (snapshot.element.defaultValue.empty() and differential.element.defaultValue.empty())",
            human="FHIR Specification models never have default values",
            key="sdf-22",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_sdf_23_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(snapshot | differential).element.all(path.contains('.').not() implies sliceName.empty())",
            human="No slice name on root",
            key="sdf-23",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_sdf_24_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("snapshot",),
            expression="element.where(type.where(code='Reference').exists() and path.endsWith('.reference') and type.targetProfile.exists() and (path.substring(0,$this.path.length()-10) in %context.element.where(type.where(code='CodeableReference').exists()).path)).exists().not()",
            human="For CodeableReference elements, target profiles must be listed on the CodeableReference, not the CodeableReference.reference",
            key="sdf-24",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_sdf_25_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("snapshot",),
            expression="element.where(type.where(code='CodeableConcept').exists() and path.endsWith('.concept') and binding.exists() and (path.substring(0,$this.path.length()-8) in %context.element.where(type.where(code='CodeableReference').exists()).path)).exists().not()",
            human="For CodeableReference elements, bindings must be listed on the CodeableReference, not the CodeableReference.concept",
            key="sdf-25",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_sdf_26_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("snapshot",),
            expression="$this.where(element[0].mustSupport='true').exists().not()",
            human="The root element of a profile should not have mustSupport = true",
            key="sdf-26",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_sdf_27_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="baseDefinition.exists() implies derivation.exists()",
            human="If there's a base definition, there must be a derivation ",
            key="sdf-27",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_sdf_28_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("snapshot.element",),
            expression="slicing.exists().not() or (slicing.discriminator.exists() or slicing.description.exists())",
            human="If there are no discriminators, there must be a definition",
            key="sdf-28",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_sdf_29_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="((kind in 'resource' | 'complex-type') and (derivation = 'specialization')) implies differential.element.where((min != 0 and min != 1) or (max != '1' and max != '*')).empty()",
            human="Elements in Resources must have a min cardinality or 0 or 1 and a max cardinality of 1 or *",
            key="sdf-29",
            severity="warning",
        )
