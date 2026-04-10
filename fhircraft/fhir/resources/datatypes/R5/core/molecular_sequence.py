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
    Reference,
    Attachment,
    BackboneElement,
    CodeableConcept,
    Range,
)
from .resource import Resource
from .domain_resource import DomainResource

class MolecularSequenceRelativeStartingSequence(BackboneElement):
    """
    A sequence that is used as a starting sequence to describe variants that are present in a sequence analyzed.
    """

    genomeAssembly: Optional[CodeableConcept] = Field(
        description="The genome assembly used for starting sequence, e.g. GRCh38",
        default=None,
    )
    chromosome: Optional[CodeableConcept] = Field(
        description="Chromosome Identifier",
        default=None,
    )
    sequenceCodeableConcept: Optional[CodeableConcept] = Field(
        description="The reference sequence that represents the starting sequence",
        default=None,
    )
    sequenceString: Optional[fhir.string] = Field(
        description="The reference sequence that represents the starting sequence",
        default=None,
    )
    sequenceReference: Optional[Reference] = Field(
        description="The reference sequence that represents the starting sequence",
        default=None,
    )
    windowStart: Optional[fhir.integer] = Field(
        description="Start position of the window on the starting sequence",
        default=None,
    )
    windowEnd: Optional[fhir.integer] = Field(
        description="End position of the window on the starting sequence",
        default=None,
    )
    orientation: Optional[fhir.code] = Field(
        description="sense | antisense",
        default=None,
    )
    strand: Optional[fhir.code] = Field(
        description="watson | crick",
        default=None,
    )

    @property
    def sequence(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="sequence",
        )

    @model_validator(mode="after")
    def sequence_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[CodeableConcept, fhir.String, Reference],
            field_name_base="sequence",
            required=False,
        )

class MolecularSequenceRelativeEdit(BackboneElement):
    """
    Changes in sequence from the starting sequence.
    """

    start: Optional[fhir.integer] = Field(
        description="Start position of the edit on the starting sequence",
        default=None,
    )
    end: Optional[fhir.integer] = Field(
        description="End position of the edit on the starting sequence",
        default=None,
    )
    replacementSequence: Optional[fhir.string] = Field(
        description="Allele that was observed",
        default=None,
    )
    replacedSequence: Optional[fhir.string] = Field(
        description="Allele in the starting sequence",
        default=None,
    )

class MolecularSequenceRelative(BackboneElement):
    """
    A sequence defined relative to another sequence.
    """

    coordinateSystem: Optional[CodeableConcept] = Field(
        description="Ways of identifying nucleotides or amino acids within a sequence",
        default=None,
    )
    ordinalPosition: Optional[fhir.integer] = Field(
        description="Indicates the order in which the sequence should be considered when putting multiple \u0027relative\u0027 elements together",
        default=None,
    )
    sequenceRange: Optional[Range] = Field(
        description="Indicates the nucleotide range in the composed sequence when multiple \u0027relative\u0027 elements are used together",
        default=None,
    )
    startingSequence: Optional[MolecularSequenceRelativeStartingSequence] = Field(
        description="A sequence used as starting sequence",
        default=None,
    )
    edit: Optional[ListType[MolecularSequenceRelativeEdit]] = Field(
        description="Changes in sequence from the starting sequence",
        default=None,
    )

class MolecularSequence(DomainResource):
    """
    Representation of a molecular sequence.
    """

    _abstract = False
    _type = "MolecularSequence"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/MolecularSequence"

    identifier: Optional[ListType[Identifier]] = Field(
        description="Unique ID for this particular sequence",
        default=None,
    )
    type: Optional[fhir.code] = Field(
        description="aa | dna | rna",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="Subject this sequence is associated too",
        default=None,
    )
    focus: Optional[ListType[Reference]] = Field(
        description="What the molecular sequence is about, when it is not about the subject of record",
        default=None,
    )
    specimen: Optional[Reference] = Field(
        description="Specimen used for sequencing",
        default=None,
    )
    device: Optional[Reference] = Field(
        description="The method for sequencing",
        default=None,
    )
    performer: Optional[Reference] = Field(
        description="Who should be responsible for test result",
        default=None,
    )
    literal: Optional[fhir.string] = Field(
        description="Sequence that was observed",
        default=None,
    )
    formatted: Optional[ListType[Attachment]] = Field(
        description="Embedded file or a link (URL) which contains content to represent the sequence",
        default=None,
    )
    relative: Optional[ListType[MolecularSequenceRelative]] = Field(
        description="A sequence defined relative to another sequence",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_msq_5_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("relative.startingSequence",),
            expression="chromosome.exists() = genomeAssembly.exists()",
            human="Both genomeAssembly and chromosome must be both contained if either one of them is contained",
            key="msq-5",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_msq_6_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("relative.startingSequence",),
            expression="genomeAssembly.exists() xor sequence.exists()",
            human="Have and only have one of the following elements in startingSequence: 1. genomeAssembly; 2 sequence",
            key="msq-6",
            severity="error",
        )
