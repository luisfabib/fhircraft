from pydantic import Field, model_validator
from typing import Optional, List

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    Boolean,
    Integer,
)

from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    CodeableConcept,
    BackboneElement,
    Quantity,
    Attachment,
)
from .resource import Resource
from .domain_resource import DomainResource


class SubstancePolymerMonomerSetStartingMaterial(BackboneElement):
    """
    The starting materials - monomer(s) used in the synthesis of the polymer.
    """

    code: Optional[CodeableConcept] = Field(
        description="The type of substance for this starting material",
        default=None,
    )
    category: Optional[CodeableConcept] = Field(
        description="Substance high level category, e.g. chemical substance",
        default=None,
    )
    isDefining: Optional[Boolean] = Field(
        description="Used to specify whether the attribute described is a defining element for the unique identification of the polymer",
        default=None,
    )
    isDefining_ext: Optional[Element] = Field(
        description="Placeholder element for isDefining extensions",
        default=None,
        alias="_isDefining",
    )
    amount: Optional[Quantity] = Field(
        description="A percentage",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "amount",
                "isDefining",
                "category",
                "code",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class SubstancePolymerMonomerSet(BackboneElement):
    """
    Todo.
    """

    ratioType: Optional[CodeableConcept] = Field(
        description="Captures the type of ratio to the entire polymer, e.g. Monomer/Polymer ratio, SRU/Polymer Ratio",
        default=None,
    )
    startingMaterial: Optional[List[SubstancePolymerMonomerSetStartingMaterial]] = (
        Field(
            description="The starting materials - monomer(s) used in the synthesis of the polymer",
            default=None,
        )
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "startingMaterial",
                "ratioType",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class SubstancePolymerRepeatRepeatUnitDegreeOfPolymerisation(BackboneElement):
    """
    Applies to homopolymer and block co-polymers where the degree of polymerisation within a block can be described.
    """

    type: Optional[CodeableConcept] = Field(
        description="The type of the degree of polymerisation shall be described, e.g. SRU/Polymer Ratio",
        default=None,
    )
    average: Optional[Integer] = Field(
        description="An average amount of polymerisation",
        default=None,
    )
    average_ext: Optional[Element] = Field(
        description="Placeholder element for average extensions",
        default=None,
        alias="_average",
    )
    low: Optional[Integer] = Field(
        description="A low expected limit of the amount",
        default=None,
    )
    low_ext: Optional[Element] = Field(
        description="Placeholder element for low extensions",
        default=None,
        alias="_low",
    )
    high: Optional[Integer] = Field(
        description="A high expected limit of the amount",
        default=None,
    )
    high_ext: Optional[Element] = Field(
        description="Placeholder element for high extensions",
        default=None,
        alias="_high",
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "high",
                "low",
                "average",
                "type",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class SubstancePolymerRepeatRepeatUnitStructuralRepresentation(BackboneElement):
    """
    A graphical structure for this SRU.
    """

    type: Optional[CodeableConcept] = Field(
        description="The type of structure (e.g. Full, Partial, Representative)",
        default=None,
    )
    representation: Optional[String] = Field(
        description="The structural representation as text string in a standard format e.g. InChI, SMILES, MOLFILE, CDX, SDF, PDB, mmCIF",
        default=None,
    )
    representation_ext: Optional[Element] = Field(
        description="Placeholder element for representation extensions",
        default=None,
        alias="_representation",
    )
    format: Optional[CodeableConcept] = Field(
        description="The format of the representation e.g. InChI, SMILES, MOLFILE, CDX, SDF, PDB, mmCIF",
        default=None,
    )
    attachment: Optional[Attachment] = Field(
        description="An attached file with the structural representation",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "attachment",
                "format",
                "representation",
                "type",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class SubstancePolymerRepeatRepeatUnit(BackboneElement):
    """
    An SRU - Structural Repeat Unit.
    """

    unit: Optional[String] = Field(
        description="Structural repeat units are essential elements for defining polymers",
        default=None,
    )
    unit_ext: Optional[Element] = Field(
        description="Placeholder element for unit extensions",
        default=None,
        alias="_unit",
    )
    orientation: Optional[CodeableConcept] = Field(
        description="The orientation of the polymerisation, e.g. head-tail, head-head, random",
        default=None,
    )
    amount: Optional[Integer] = Field(
        description="Number of repeats of this unit",
        default=None,
    )
    amount_ext: Optional[Element] = Field(
        description="Placeholder element for amount extensions",
        default=None,
        alias="_amount",
    )
    degreeOfPolymerisation: Optional[
        List[SubstancePolymerRepeatRepeatUnitDegreeOfPolymerisation]
    ] = Field(
        description="Applies to homopolymer and block co-polymers where the degree of polymerisation within a block can be described",
        default=None,
    )
    structuralRepresentation: Optional[
        List[SubstancePolymerRepeatRepeatUnitStructuralRepresentation]
    ] = Field(
        description="A graphical structure for this SRU",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "structuralRepresentation",
                "degreeOfPolymerisation",
                "amount",
                "orientation",
                "unit",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class SubstancePolymerRepeat(BackboneElement):
    """
    Specifies and quantifies the repeated units and their configuration.
    """

    averageMolecularFormula: Optional[String] = Field(
        description="A representation of an (average) molecular formula from a polymer",
        default=None,
    )
    averageMolecularFormula_ext: Optional[Element] = Field(
        description="Placeholder element for averageMolecularFormula extensions",
        default=None,
        alias="_averageMolecularFormula",
    )
    repeatUnitAmountType: Optional[CodeableConcept] = Field(
        description="How the quantitative amount of Structural Repeat Units is captured (e.g. Exact, Numeric, Average)",
        default=None,
    )
    repeatUnit: Optional[List[SubstancePolymerRepeatRepeatUnit]] = Field(
        description="An SRU - Structural Repeat Unit",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "repeatUnit",
                "repeatUnitAmountType",
                "averageMolecularFormula",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class SubstancePolymer(DomainResource):
    """
    Properties of a substance specific to it being a polymer.
    """

    _abstract = False
    _type = "SubstancePolymer"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/SubstancePolymer"

    id: Optional[String] = Field(
        description="Logical id of this artifact",
        default=None,
    )
    id_ext: Optional[Element] = Field(
        description="Placeholder element for id extensions",
        default=None,
        alias="_id",
    )
    meta: Optional[Meta] = Field(
        description="Metadata about the resource.",
        default_factory=lambda: Meta(
            profile=["http://hl7.org/fhir/StructureDefinition/SubstancePolymer"]
        ),
    )
    implicitRules: Optional[Uri] = Field(
        description="A set of rules under which this content was created",
        default=None,
    )
    implicitRules_ext: Optional[Element] = Field(
        description="Placeholder element for implicitRules extensions",
        default=None,
        alias="_implicitRules",
    )
    language: Optional[Code] = Field(
        description="Language of the resource content",
        default=None,
    )
    language_ext: Optional[Element] = Field(
        description="Placeholder element for language extensions",
        default=None,
        alias="_language",
    )
    text: Optional[Narrative] = Field(
        description="Text summary of the resource, for human interpretation",
        default=None,
    )
    contained: Optional[List[Resource]] = Field(
        description="Contained, inline Resources",
        default=None,
    )
    extension: Optional[List[Extension]] = Field(
        description="Additional content defined by implementations",
        default=None,
    )
    modifierExtension: Optional[List[Extension]] = Field(
        description="Extensions that cannot be ignored",
        default=None,
    )
    identifier: Optional[Identifier] = Field(
        description="A business idenfier for this polymer, but typically this is handled by a SubstanceDefinition identifier",
        default=None,
    )
    class_: Optional[CodeableConcept] = Field(
        description="Overall type of the polymer",
        default=None,
    )
    geometry: Optional[CodeableConcept] = Field(
        description="Polymer geometry, e.g. linear, branched, cross-linked, network or dendritic",
        default=None,
    )
    copolymerConnectivity: Optional[List[CodeableConcept]] = Field(
        description="Descrtibes the copolymer sequence type (polymer connectivity)",
        default=None,
    )
    modification: Optional[String] = Field(
        description="Todo - this is intended to connect to a repeating full modification structure, also used by Protein and Nucleic Acid . String is just a placeholder",
        default=None,
    )
    modification_ext: Optional[Element] = Field(
        description="Placeholder element for modification extensions",
        default=None,
        alias="_modification",
    )
    monomerSet: Optional[List[SubstancePolymerMonomerSet]] = Field(
        description="Todo",
        default=None,
    )
    repeat: Optional[List[SubstancePolymerRepeat]] = Field(
        description="Specifies and quantifies the repeated units and their configuration",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "repeat",
                "monomerSet",
                "modification",
                "copolymerConnectivity",
                "geometry",
                "class_",
                "identifier",
                "modifierExtension",
                "extension",
                "text",
                "language",
                "implicitRules",
                "meta",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ext_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "modifierExtension",
                "extension",
            ),
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_dom_2_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="contained.contained.empty()",
            human="If the resource is contained in another resource, it SHALL NOT contain nested Resources",
            key="dom-2",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_dom_3_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="contained.where((('#'+id in (%resource.descendants().reference | %resource.descendants().ofType(canonical) | %resource.descendants().ofType(uri) | %resource.descendants().ofType(url))) or descendants().where(reference = '#').exists() or descendants().where(ofType(canonical) = '#').exists() or descendants().where(ofType(canonical) = '#').exists()).not()).trace('unmatched', id).empty()",
            human="If the resource is contained in another resource, it SHALL be referred to from elsewhere in the resource or SHALL refer to the containing resource",
            key="dom-3",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_dom_4_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="contained.meta.versionId.empty() and contained.meta.lastUpdated.empty()",
            human="If a resource is contained in another resource, it SHALL NOT have a meta.versionId or a meta.lastUpdated",
            key="dom-4",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_dom_5_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="contained.meta.security.empty()",
            human="If a resource is contained in another resource, it SHALL NOT have a security label",
            key="dom-5",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_dom_6_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="text.`div`.exists()",
            human="A resource should have narrative for robust management",
            key="dom-6",
            severity="warning",
        )
