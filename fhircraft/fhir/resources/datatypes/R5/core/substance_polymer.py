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
    isDefining: Optional[fhir.boolean] = Field(
        description="Used to specify whether the attribute described is a defining element for the unique identification of the polymer",
        default=None,
    )
    amount: Optional[Quantity] = Field(
        description="A percentage",
        default=None,
    )


class SubstancePolymerMonomerSet(BackboneElement):
    """
    Todo.
    """

    ratioType: Optional[CodeableConcept] = Field(
        description="Captures the type of ratio to the entire polymer, e.g. Monomer/Polymer ratio, SRU/Polymer Ratio",
        default=None,
    )
    startingMaterial: Optional[ListType[SubstancePolymerMonomerSetStartingMaterial]] = (
        Field(
            description="The starting materials - monomer(s) used in the synthesis of the polymer",
            default=None,
        )
    )


class SubstancePolymerRepeatRepeatUnitDegreeOfPolymerisation(BackboneElement):
    """
    Applies to homopolymer and block co-polymers where the degree of polymerisation within a block can be described.
    """

    type: Optional[CodeableConcept] = Field(
        description="The type of the degree of polymerisation shall be described, e.g. SRU/Polymer Ratio",
        default=None,
    )
    average: Optional[fhir.integer] = Field(
        description="An average amount of polymerisation",
        default=None,
    )
    low: Optional[fhir.integer] = Field(
        description="A low expected limit of the amount",
        default=None,
    )
    high: Optional[fhir.integer] = Field(
        description="A high expected limit of the amount",
        default=None,
    )


class SubstancePolymerRepeatRepeatUnitStructuralRepresentation(BackboneElement):
    """
    A graphical structure for this SRU.
    """

    type: Optional[CodeableConcept] = Field(
        description="The type of structure (e.g. Full, Partial, Representative)",
        default=None,
    )
    representation: Optional[fhir.string] = Field(
        description="The structural representation as text string in a standard format e.g. InChI, SMILES, MOLFILE, CDX, SDF, PDB, mmCIF",
        default=None,
    )
    format: Optional[CodeableConcept] = Field(
        description="The format of the representation e.g. InChI, SMILES, MOLFILE, CDX, SDF, PDB, mmCIF",
        default=None,
    )
    attachment: Optional[Attachment] = Field(
        description="An attached file with the structural representation",
        default=None,
    )


class SubstancePolymerRepeatRepeatUnit(BackboneElement):
    """
    An SRU - Structural Repeat Unit.
    """

    unit: Optional[fhir.string] = Field(
        description="Structural repeat units are essential elements for defining polymers",
        default=None,
    )
    orientation: Optional[CodeableConcept] = Field(
        description="The orientation of the polymerisation, e.g. head-tail, head-head, random",
        default=None,
    )
    amount: Optional[fhir.integer] = Field(
        description="Number of repeats of this unit",
        default=None,
    )
    degreeOfPolymerisation: Optional[
        ListType[SubstancePolymerRepeatRepeatUnitDegreeOfPolymerisation]
    ] = Field(
        description="Applies to homopolymer and block co-polymers where the degree of polymerisation within a block can be described",
        default=None,
    )
    structuralRepresentation: Optional[
        ListType[SubstancePolymerRepeatRepeatUnitStructuralRepresentation]
    ] = Field(
        description="A graphical structure for this SRU",
        default=None,
    )


class SubstancePolymerRepeat(BackboneElement):
    """
    Specifies and quantifies the repeated units and their configuration.
    """

    averageMolecularFormula: Optional[fhir.string] = Field(
        description="A representation of an (average) molecular formula from a polymer",
        default=None,
    )
    repeatUnitAmountType: Optional[CodeableConcept] = Field(
        description="How the quantitative amount of Structural Repeat Units is captured (e.g. Exact, Numeric, Average)",
        default=None,
    )
    repeatUnit: Optional[ListType[SubstancePolymerRepeatRepeatUnit]] = Field(
        description="An SRU - Structural Repeat Unit",
        default=None,
    )


class SubstancePolymer(DomainResource):
    """
    Properties of a substance specific to it being a polymer.
    """

    _abstract = False
    _type = "SubstancePolymer"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/SubstancePolymer"

    identifier: Optional[Identifier] = Field(
        description="A business idenfier for this polymer, but typically this is handled by a SubstanceDefinition identifier",
        default=None,
    )
    class_: Optional[CodeableConcept] = Field(
        description="Overall type of the polymer",
        default=None,
        alias="class",
    )
    geometry: Optional[CodeableConcept] = Field(
        description="Polymer geometry, e.g. linear, branched, cross-linked, network or dendritic",
        default=None,
    )
    copolymerConnectivity: Optional[ListType[CodeableConcept]] = Field(
        description="Descrtibes the copolymer sequence type (polymer connectivity)",
        default=None,
    )
    modification: Optional[fhir.string] = Field(
        description="Todo - this is intended to connect to a repeating full modification structure, also used by Protein and Nucleic Acid . string is just a placeholder",
        default=None,
    )
    monomerSet: Optional[ListType[SubstancePolymerMonomerSet]] = Field(
        description="Todo",
        default=None,
    )
    repeat: Optional[ListType[SubstancePolymerRepeat]] = Field(
        description="Specifies and quantifies the repeated units and their configuration",
        default=None,
    )
