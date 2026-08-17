import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)


import fhircraft.fhir.resources.datatypes.R4.primitive as fhir
from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Reference,
    Quantity,
    CodeableConcept,
    BackboneElement,
)
from .resource import Resource
from .domain_resource import DomainResource


class MolecularSequenceReferenceSeq(BackboneElement):
    """
    A sequence that is used as a reference to describe variants that are present in a sequence analyzed.
    """

    chromosome: Optional[CodeableConcept] = Field(
        description="Chromosome containing genetic finding",
        default=None,
    )
    genomeBuild: Optional[fhir.string] = Field(
        description="The Genome Build used for reference, following GRCh build versions e.g. \u0027GRCh 37\u0027",
        default=None,
    )
    orientation: Optional[fhir.code] = Field(
        description="sense | antisense",
        default=None,
    )
    referenceSeqId: Optional[CodeableConcept] = Field(
        description="Reference identifier",
        default=None,
    )
    referenceSeqPointer: Optional[Reference] = Field(
        description="A pointer to another MolecularSequence entity as reference sequence",
        default=None,
    )
    referenceSeqString: Optional[fhir.string] = Field(
        description="A string to represent reference sequence",
        default=None,
    )
    strand: Optional[fhir.code] = Field(
        description="watson | crick",
        default=None,
    )
    windowStart: Optional[fhir.integer] = Field(
        description="Start position of the window on the  reference sequence",
        default=None,
    )
    windowEnd: Optional[fhir.integer] = Field(
        description="End position of the window on the reference sequence",
        default=None,
    )


class MolecularSequenceVariant(BackboneElement):
    """
    The definition of variant here originates from Sequence ontology ([variant_of](http://www.sequenceontology.org/browser/current_svn/term/variant_of)). This element can represent amino acid or nucleic sequence change(including insertion,deletion,SNP,etc.)  It can represent some complex mutation or segment variation with the assist of CIGAR string.
    """

    start: Optional[fhir.integer] = Field(
        description="Start position of the variant on the  reference sequence",
        default=None,
    )
    end: Optional[fhir.integer] = Field(
        description="End position of the variant on the reference sequence",
        default=None,
    )
    observedAllele: Optional[fhir.string] = Field(
        description="Allele that was observed",
        default=None,
    )
    referenceAllele: Optional[fhir.string] = Field(
        description="Allele in the reference sequence",
        default=None,
    )
    cigar: Optional[fhir.string] = Field(
        description="Extended CIGAR string for aligning the sequence with reference bases",
        default=None,
    )
    variantPointer: Optional[Reference] = Field(
        description="Pointer to observed variant information",
        default=None,
    )


class MolecularSequenceQualityRoc(BackboneElement):
    """
    Receiver Operator Characteristic (ROC) Curve  to give sensitivity/specificity tradeoff.
    """

    score: Optional[ListType[fhir.integer]] = Field(
        description="Genotype quality score",
        default=None,
    )
    numTP: Optional[ListType[fhir.integer]] = Field(
        description="Roc score true positive numbers",
        default=None,
    )
    numFP: Optional[ListType[fhir.integer]] = Field(
        description="Roc score false positive numbers",
        default=None,
    )
    numFN: Optional[ListType[fhir.integer]] = Field(
        description="Roc score false negative numbers",
        default=None,
    )
    precision: Optional[ListType[fhir.decimal]] = Field(
        description="Precision of the GQ score",
        default=None,
    )
    sensitivity: Optional[ListType[fhir.decimal]] = Field(
        description="Sensitivity of the GQ score",
        default=None,
    )
    fMeasure: Optional[ListType[fhir.decimal]] = Field(
        description="FScore of the GQ score",
        default=None,
    )


class MolecularSequenceQuality(BackboneElement):
    """
    An experimental feature attribute that defines the quality of the feature in a quantitative way, such as a phred quality score ([SO:0001686](http://www.sequenceontology.org/browser/current_svn/term/SO:0001686)).
    """

    type: fhir.code = Field(
        description="indel | snp | unknown",
    )
    standardSequence: Optional[CodeableConcept] = Field(
        description="Standard sequence for comparison",
        default=None,
    )
    start: Optional[fhir.integer] = Field(
        description="Start position of the sequence",
        default=None,
    )
    end: Optional[fhir.integer] = Field(
        description="End position of the sequence",
        default=None,
    )
    score: Optional[Quantity] = Field(
        description="Quality score for the comparison",
        default=None,
    )
    method: Optional[CodeableConcept] = Field(
        description="Method to get quality",
        default=None,
    )
    truthTP: Optional[fhir.decimal] = Field(
        description="True positives from the perspective of the truth data",
        default=None,
    )
    queryTP: Optional[fhir.decimal] = Field(
        description="True positives from the perspective of the query data",
        default=None,
    )
    truthFN: Optional[fhir.decimal] = Field(
        description="False negatives",
        default=None,
    )
    queryFP: Optional[fhir.decimal] = Field(
        description="False positives",
        default=None,
    )
    gtFP: Optional[fhir.decimal] = Field(
        description="False positives where the non-REF alleles in the Truth and Query Call Sets match",
        default=None,
    )
    precision: Optional[fhir.decimal] = Field(
        description="Precision of comparison",
        default=None,
    )
    recall: Optional[fhir.decimal] = Field(
        description="Recall of comparison",
        default=None,
    )
    fScore: Optional[fhir.decimal] = Field(
        description="F-score",
        default=None,
    )
    roc: Optional[MolecularSequenceQualityRoc] = Field(
        description="Receiver Operator Characteristic (ROC) Curve",
        default=None,
    )


class MolecularSequenceRepository(BackboneElement):
    """
    Configurations of the external repository. The repository shall store target's observedSeq or records related with target's observedSeq.
    """

    type: fhir.code = Field(
        description="directlink | openapi | login | oauth | other",
    )
    url: Optional[fhir.uri] = Field(
        description="URI of the repository",
        default=None,
    )
    name: Optional[fhir.string] = Field(
        description="Repository\u0027s name",
        default=None,
    )
    datasetId: Optional[fhir.string] = Field(
        description="id_ of the dataset that used to call for dataset in repository",
        default=None,
    )
    variantsetId: Optional[fhir.string] = Field(
        description="id_ of the variantset that used to call for variantset in repository",
        default=None,
    )
    readsetId: Optional[fhir.string] = Field(
        description="id_ of the read",
        default=None,
    )


class MolecularSequenceStructureVariantOuter(BackboneElement):
    """
    Structural variant outer.
    """

    start: Optional[fhir.integer] = Field(
        description="Structural variant outer start",
        default=None,
    )
    end: Optional[fhir.integer] = Field(
        description="Structural variant outer end",
        default=None,
    )


class MolecularSequenceStructureVariantInner(BackboneElement):
    """
    Structural variant inner.
    """

    start: Optional[fhir.integer] = Field(
        description="Structural variant inner start",
        default=None,
    )
    end: Optional[fhir.integer] = Field(
        description="Structural variant inner end",
        default=None,
    )


class MolecularSequenceStructureVariant(BackboneElement):
    """
    Information about chromosome structure variation.
    """

    variantType: Optional[CodeableConcept] = Field(
        description="Structural variant change type",
        default=None,
    )
    exact: Optional[fhir.boolean] = Field(
        description="Does the structural variant have base pair resolution breakpoints?",
        default=None,
    )
    length: Optional[fhir.integer] = Field(
        description="Structural variant length",
        default=None,
    )
    outer: Optional[MolecularSequenceStructureVariantOuter] = Field(
        description="Structural variant outer",
        default=None,
    )
    inner: Optional[MolecularSequenceStructureVariantInner] = Field(
        description="Structural variant inner",
        default=None,
    )


class MolecularSequence(DomainResource):
    """
    Raw data describing a biological sequence.
    """

    _abstract = False
    _type = "MolecularSequence"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/MolecularSequence"

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
    identifier: Optional[ListType[Identifier]] = Field(
        description="Unique ID for this particular sequence. This is a FHIR-defined id",
        default=None,
    )
    type: Optional[fhir.code] = Field(
        description="aa | dna | rna",
        default=None,
    )
    coordinateSystem: fhir.integer = Field(
        description="Base number of coordinate system (0 for 0-based numbering or coordinates, inclusive start, exclusive end, 1 for 1-based numbering, inclusive start, inclusive end)",
    )
    patient: Optional[Reference] = Field(
        description="Who and/or what this is about",
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
    quantity: Optional[Quantity] = Field(
        description="The number of copies of the sequence of interest.  (RNASeq)",
        default=None,
    )
    referenceSeq: Optional[MolecularSequenceReferenceSeq] = Field(
        description="A sequence used as reference",
        default=None,
    )
    variant: Optional[ListType[MolecularSequenceVariant]] = Field(
        description="Variant in sequence",
        default=None,
    )
    observedSeq: Optional[fhir.string] = Field(
        description="Sequence that was observed",
        default=None,
    )
    quality: Optional[ListType[MolecularSequenceQuality]] = Field(
        description="An set of value as quality of sequence",
        default=None,
    )
    readCoverage: Optional[fhir.integer] = Field(
        description="Average number of reads representing a given nucleotide in the reconstructed sequence",
        default=None,
    )
    repository: Optional[ListType[MolecularSequenceRepository]] = Field(
        description="External repository which contains detailed report related with observedSeq in this resource",
        default=None,
    )
    pointer: Optional[ListType[Reference]] = Field(
        description="Pointer to next atomic sequence",
        default=None,
    )
    structureVariant: Optional[ListType[MolecularSequenceStructureVariant]] = Field(
        description="Structural variant",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_msq_3_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="coordinateSystem = 1 or coordinateSystem = 0",
            human="Only 0 and 1 are valid for coordinateSystem",
            key="msq-3",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_msq_5_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("referenceSeq",),
            expression="(chromosome.empty() and genomeBuild.empty()) or (chromosome.exists() and genomeBuild.exists())",
            human="GenomeBuild and chromosome must be both contained if either one of them is contained",
            key="msq-5",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_msq_6_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("referenceSeq",),
            expression="(genomeBuild.count()+referenceSeqId.count()+ referenceSeqPointer.count()+ referenceSeqString.count()) = 1",
            human="Have and only have one of the following elements in referenceSeq : 1. genomeBuild ; 2 referenceSeqId; 3. referenceSeqPointer;  4. referenceSeqString;",
            key="msq-6",
            severity="error",
        )
