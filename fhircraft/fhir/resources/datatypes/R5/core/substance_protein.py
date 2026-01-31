from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from fhircraft.fhir.resources.datatypes.primitives import String, Uri, Code, Integer

from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    CodeableConcept,
    BackboneElement,
    Attachment,
    Identifier,
)
from .resource import Resource
from .domain_resource import DomainResource


class SubstanceProteinSubunit(BackboneElement):
    """
    This subclause refers to the description of each subunit constituting the SubstanceProtein. A subunit is a linear sequence of amino acids linked through peptide bonds. The Subunit information shall be provided when the finished SubstanceProtein is a complex of multiple sequences; subunits are not used to delineate domains within a single sequence. Subunits are listed in order of decreasing length; sequences of the same length will be ordered by decreasing molecular weight; subunits that have identical sequences will be repeated multiple times.
    """

    subunit: Optional[Integer] = Field(
        description="Index of primary sequences of amino acids linked through peptide bonds in order of decreasing length. Sequences of the same length will be ordered by molecular weight. Subunits that have identical sequences will be repeated and have sequential subscripts",
        default=None,
    )
    subunit_ext: Optional[ListType[Optional[Element]]] = Field(
        description="Placeholder element for subunit extensions",
        default=None,
        alias="_subunit",
    )
    sequence: Optional[String] = Field(
        description="The sequence information shall be provided enumerating the amino acids from N- to C-terminal end using standard single-letter amino acid codes. Uppercase shall be used for L-amino acids and lowercase for D-amino acids. Transcribed SubstanceProteins will always be described using the translated sequence; for synthetic peptide containing amino acids that are not represented with a single letter code an X should be used within the sequence. The modified amino acids will be distinguished by their position in the sequence",
        default=None,
    )
    sequence_ext: Optional[Element] = Field(
        description="Placeholder element for sequence extensions",
        default=None,
        alias="_sequence",
    )
    length: Optional[Integer] = Field(
        description="Length of linear sequences of amino acids contained in the subunit",
        default=None,
    )
    length_ext: Optional[Element] = Field(
        description="Placeholder element for length extensions",
        default=None,
        alias="_length",
    )
    sequenceAttachment: Optional[Attachment] = Field(
        description="The sequence information shall be provided enumerating the amino acids from N- to C-terminal end using standard single-letter amino acid codes. Uppercase shall be used for L-amino acids and lowercase for D-amino acids. Transcribed SubstanceProteins will always be described using the translated sequence; for synthetic peptide containing amino acids that are not represented with a single letter code an X should be used within the sequence. The modified amino acids will be distinguished by their position in the sequence",
        default=None,
    )
    nTerminalModificationId: Optional[Identifier] = Field(
        description="Unique identifier for molecular fragment modification based on the ISO 11238 Substance ID",
        default=None,
    )
    nTerminalModification: Optional[String] = Field(
        description="The name of the fragment modified at the N-terminal of the SubstanceProtein shall be specified",
        default=None,
    )
    nTerminalModification_ext: Optional[Element] = Field(
        description="Placeholder element for nTerminalModification extensions",
        default=None,
        alias="_nTerminalModification",
    )
    cTerminalModificationId: Optional[Identifier] = Field(
        description="Unique identifier for molecular fragment modification based on the ISO 11238 Substance ID",
        default=None,
    )
    cTerminalModification: Optional[String] = Field(
        description="The modification at the C-terminal shall be specified",
        default=None,
    )
    cTerminalModification_ext: Optional[Element] = Field(
        description="Placeholder element for cTerminalModification extensions",
        default=None,
        alias="_cTerminalModification",
    )


class SubstanceProtein(DomainResource):
    """
    A SubstanceProtein is defined as a single unit of a linear amino acid sequence, or a combination of subunits that are either covalently linked or have a defined invariant stoichiometric relationship. This includes all synthetic, recombinant and purified SubstanceProteins of defined sequence, whether the use is therapeutic or prophylactic. This set of elements will be used to describe albumins, coagulation factors, cytokines, growth factors, peptide/SubstanceProtein hormones, enzymes, toxins, toxoids, recombinant vaccines, and immunomodulators.
    """

    _abstract = False
    _type = "SubstanceProtein"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/SubstanceProtein"

    sequenceType: Optional[CodeableConcept] = Field(
        description="The SubstanceProtein descriptive elements will only be used when a complete or partial amino acid sequence is available or derivable from a nucleic acid sequence",
        default=None,
    )
    numberOfSubunits: Optional[Integer] = Field(
        description="Number of linear sequences of amino acids linked through peptide bonds. The number of subunits constituting the SubstanceProtein shall be described. It is possible that the number of subunits can be variable",
        default=None,
    )
    numberOfSubunits_ext: Optional[Element] = Field(
        description="Placeholder element for numberOfSubunits extensions",
        default=None,
        alias="_numberOfSubunits",
    )
    disulfideLinkage: Optional[ListType[String]] = Field(
        description="The disulphide bond between two cysteine residues either on the same subunit or on two different subunits shall be described. The position of the disulfide bonds in the SubstanceProtein shall be listed in increasing order of subunit number and position within subunit followed by the abbreviation of the amino acids involved. The disulfide linkage positions shall actually contain the amino acid Cysteine at the respective positions",
        default=None,
    )
    disulfideLinkage_ext: Optional[ListType[Optional[Element]]] = Field(
        description="Placeholder element for disulfideLinkage extensions",
        default=None,
        alias="_disulfideLinkage",
    )
    subunit: Optional[ListType[SubstanceProteinSubunit]] = Field(
        description="This subclause refers to the description of each subunit constituting the SubstanceProtein. A subunit is a linear sequence of amino acids linked through peptide bonds. The Subunit information shall be provided when the finished SubstanceProtein is a complex of multiple sequences; subunits are not used to delineate domains within a single sequence. Subunits are listed in order of decreasing length; sequences of the same length will be ordered by decreasing molecular weight; subunits that have identical sequences will be repeated multiple times",
        default=None,
    )
