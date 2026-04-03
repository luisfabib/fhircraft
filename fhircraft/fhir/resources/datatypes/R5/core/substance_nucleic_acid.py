from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators


from ..primitive import *
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

class SubstanceNucleicAcidSubunitLinkage(BackboneElement):
    """
    The linkages between sugar residues will also be captured.
    """

    connectivity: Optional[String] = Field(
        description="The entity that links the sugar residues together should also be captured for nearly all naturally occurring nucleic acid the linkage is a phosphate group. For many synthetic oligonucleotides phosphorothioate linkages are often seen. Linkage connectivity is assumed to be 3\u2019-5\u2019. If the linkage is either 3\u2019-3\u2019 or 5\u2019-5\u2019 this should be specified",
        default=None,
    )
    identifier: Optional[Identifier] = Field(
        description="Each linkage will be registered as a fragment and have an ID",
        default=None,
    )
    name: Optional[String] = Field(
        description="Each linkage will be registered as a fragment and have at least one name. A single name shall be assigned to each linkage",
        default=None,
    )
    residueSite: Optional[String] = Field(
        description="Residues shall be captured as described in 5.3.6.8.3",
        default=None,
    )

class SubstanceNucleicAcidSubunitSugar(BackboneElement):
    """
    5.3.6.8.1 Sugar ID (Mandatory).
    """

    identifier: Optional[Identifier] = Field(
        description="The Substance ID of the sugar or sugar-like component that make up the nucleotide",
        default=None,
    )
    name: Optional[String] = Field(
        description="The name of the sugar or sugar-like component that make up the nucleotide",
        default=None,
    )
    residueSite: Optional[String] = Field(
        description="The residues that contain a given sugar will be captured. The order of given residues will be captured in the 5\u2018-3\u2018direction consistent with the base sequences listed above",
        default=None,
    )

class SubstanceNucleicAcidSubunit(BackboneElement):
    """
    Subunits are listed in order of decreasing length; sequences of the same length will be ordered by molecular weight; subunits that have identical sequences will be repeated multiple times.
    """

    subunit: Optional[Integer] = Field(
        description="Index of linear sequences of nucleic acids in order of decreasing length. Sequences of the same length will be ordered by molecular weight. Subunits that have identical sequences will be repeated and have sequential subscripts",
        default=None,
    )
    sequence: Optional[String] = Field(
        description="Actual nucleotide sequence notation from 5\u0027 to 3\u0027 end using standard single letter codes. In addition to the base sequence, sugar and type of phosphate or non-phosphate linkage should also be captured",
        default=None,
    )
    length: Optional[Integer] = Field(
        description="The length of the sequence shall be captured",
        default=None,
    )
    sequenceAttachment: Optional[Attachment] = Field(
        description="(TBC)",
        default=None,
    )
    fivePrime: Optional[CodeableConcept] = Field(
        description="The nucleotide present at the 5\u2019 terminal shall be specified based on a controlled vocabulary. Since the sequence is represented from the 5\u0027 to the 3\u0027 end, the 5\u2019 prime nucleotide is the letter at the first position in the sequence. A separate representation would be redundant",
        default=None,
    )
    threePrime: Optional[CodeableConcept] = Field(
        description="The nucleotide present at the 3\u2019 terminal shall be specified based on a controlled vocabulary. Since the sequence is represented from the 5\u0027 to the 3\u0027 end, the 5\u2019 prime nucleotide is the letter at the last position in the sequence. A separate representation would be redundant",
        default=None,
    )
    linkage: Optional[ListType[SubstanceNucleicAcidSubunitLinkage]] = Field(
        description="The linkages between sugar residues will also be captured",
        default=None,
    )
    sugar: Optional[ListType[SubstanceNucleicAcidSubunitSugar]] = Field(
        description="5.3.6.8.1 Sugar ID (Mandatory)",
        default=None,
    )

class SubstanceNucleicAcid(DomainResource):
    """
    Nucleic acids are defined by three distinct elements: the base, sugar and linkage. Individual substance/moiety IDs will be created for each of these elements. The nucleotide sequence will be always entered in the 5’-3’ direction.
    """

    _abstract = False
    _type = "SubstanceNucleicAcid"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/SubstanceNucleicAcid"

    sequenceType: Optional[CodeableConcept] = Field(
        description="The type of the sequence shall be specified based on a controlled vocabulary",
        default=None,
    )
    numberOfSubunits: Optional[Integer] = Field(
        description="The number of linear sequences of nucleotides linked through phosphodiester bonds shall be described. Subunits would be strands of nucleic acids that are tightly associated typically through Watson-Crick base pairing. NOTE: If not specified in the reference source, the assumption is that there is 1 subunit",
        default=None,
    )
    areaOfHybridisation: Optional[String] = Field(
        description="The area of hybridisation shall be described if applicable for double stranded RNA or DNA. The number associated with the subunit followed by the number associated to the residue shall be specified in increasing order. The underscore \u201c\u201d shall be used as separator as follows: \u201cSubunitnumber Residue\u201d",
        default=None,
    )
    oligoNucleotideType: Optional[CodeableConcept] = Field(
        description="(TBC)",
        default=None,
    )
    subunit: Optional[ListType[SubstanceNucleicAcidSubunit]] = Field(
        description="Subunits are listed in order of decreasing length; sequences of the same length will be ordered by molecular weight; subunits that have identical sequences will be repeated multiple times",
        default=None,
    )
