import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    DateTime,
    Boolean,
)

from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    BackboneElement,
    Quantity,
    Attachment,
    Range,
    Ratio,
)
from .resource import Resource
from .domain_resource import DomainResource


class SubstanceSpecificationMoiety(BackboneElement):
    """
    Moiety, for structural modifications.
    """

    role: Optional[CodeableConcept] = Field(
        description="Role that the moiety is playing",
        default=None,
    )
    identifier: Optional[Identifier] = Field(
        description="Identifier by which this moiety substance is known",
        default=None,
    )
    name: Optional[String] = Field(
        description="Textual name for this moiety substance",
        default=None,
    )
    name_ext: Optional[Element] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    stereochemistry: Optional[CodeableConcept] = Field(
        description="Stereochemistry type",
        default=None,
    )
    opticalActivity: Optional[CodeableConcept] = Field(
        description="Optical activity type",
        default=None,
    )
    molecularFormula: Optional[String] = Field(
        description="Molecular formula",
        default=None,
    )
    molecularFormula_ext: Optional[Element] = Field(
        description="Placeholder element for molecularFormula extensions",
        default=None,
        alias="_molecularFormula",
    )
    amountQuantity: Optional[Quantity] = Field(
        description="Quantitative value for this moiety",
        default=None,
    )
    amountString: Optional[String] = Field(
        description="Quantitative value for this moiety",
        default=None,
    )
    amountString_ext: Optional[Element] = Field(
        description="Placeholder element for amountString extensions",
        default=None,
        alias="_amountString",
    )

    @property
    def amount(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="amount",
        )

    @model_validator(mode="after")
    def amount_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Quantity, String],
            field_name_base="amount",
            required=False,
        )


class SubstanceSpecificationProperty(BackboneElement):
    """
    General specifications for this substance, including how it is related to other substances.
    """

    category: Optional[CodeableConcept] = Field(
        description="A category for this property, e.g. Physical, Chemical, Enzymatic",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="Property type e.g. viscosity, pH, isoelectric point",
        default=None,
    )
    parameters: Optional[String] = Field(
        description="Parameters that were used in the measurement of a property (e.g. for viscosity: measured at 20C with a pH of 7.1)",
        default=None,
    )
    parameters_ext: Optional[Element] = Field(
        description="Placeholder element for parameters extensions",
        default=None,
        alias="_parameters",
    )
    definingSubstanceReference: Optional[Reference] = Field(
        description="A substance upon which a defining property depends (e.g. for solubility: in water, in alcohol)",
        default=None,
    )
    definingSubstanceCodeableConcept: Optional[CodeableConcept] = Field(
        description="A substance upon which a defining property depends (e.g. for solubility: in water, in alcohol)",
        default=None,
    )
    amountQuantity: Optional[Quantity] = Field(
        description="Quantitative value for this property",
        default=None,
    )
    amountString: Optional[String] = Field(
        description="Quantitative value for this property",
        default=None,
    )
    amountString_ext: Optional[Element] = Field(
        description="Placeholder element for amountString extensions",
        default=None,
        alias="_amountString",
    )

    @property
    def definingSubstance(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="definingSubstance",
        )

    @property
    def amount(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="amount",
        )

    @model_validator(mode="after")
    def definingSubstance_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Reference, CodeableConcept],
            field_name_base="definingSubstance",
            required=False,
        )

    @model_validator(mode="after")
    def amount_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Quantity, String],
            field_name_base="amount",
            required=False,
        )


class SubstanceSpecificationStructureIsotopeMolecularWeight(BackboneElement):
    """
    The molecular weight or weight range (for proteins, polymers or nucleic acids).
    """

    method: Optional[CodeableConcept] = Field(
        description="The method by which the molecular weight was determined",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Type of molecular weight such as exact, average (also known as. number average), weight average",
        default=None,
    )
    amount: Optional[Quantity] = Field(
        description="Used to capture quantitative values for a variety of elements. If only limits are given, the arithmetic mean would be the average. If only a single definite value for a given element is given, it would be captured in this field",
        default=None,
    )


class SubstanceSpecificationStructureIsotope(BackboneElement):
    """
    Applicable for single substances that contain a radionuclide or a non-natural isotopic ratio.
    """

    identifier: Optional[Identifier] = Field(
        description="Substance identifier for each non-natural or radioisotope",
        default=None,
    )
    name: Optional[CodeableConcept] = Field(
        description="Substance name for each non-natural or radioisotope",
        default=None,
    )
    substitution: Optional[CodeableConcept] = Field(
        description="The type of isotopic substitution present in a single substance",
        default=None,
    )
    halfLife: Optional[Quantity] = Field(
        description="Half life - for a non-natural nuclide",
        default=None,
    )
    molecularWeight: Optional[SubstanceSpecificationStructureIsotopeMolecularWeight] = (
        Field(
            description="The molecular weight or weight range (for proteins, polymers or nucleic acids)",
            default=None,
        )
    )


class SubstanceSpecificationStructureMolecularWeight(BackboneElement):
    """
    The molecular weight or weight range (for proteins, polymers or nucleic acids).
    """

    method: Optional[CodeableConcept] = Field(
        description="The method by which the molecular weight was determined",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Type of molecular weight such as exact, average (also known as. number average), weight average",
        default=None,
    )
    amount: Optional[Quantity] = Field(
        description="Used to capture quantitative values for a variety of elements. If only limits are given, the arithmetic mean would be the average. If only a single definite value for a given element is given, it would be captured in this field",
        default=None,
    )


class SubstanceSpecificationStructureRepresentation(BackboneElement):
    """
    Molecular structural representation.
    """

    type: Optional[CodeableConcept] = Field(
        description="The type of structure (e.g. Full, Partial, Representative)",
        default=None,
    )
    representation: Optional[String] = Field(
        description="The structural representation as text string in a format e.g. InChI, SMILES, MOLFILE, CDX",
        default=None,
    )
    representation_ext: Optional[Element] = Field(
        description="Placeholder element for representation extensions",
        default=None,
        alias="_representation",
    )
    attachment: Optional[Attachment] = Field(
        description="An attached file with the structural representation",
        default=None,
    )


class SubstanceSpecificationStructure(BackboneElement):
    """
    Structural information.
    """

    stereochemistry: Optional[CodeableConcept] = Field(
        description="Stereochemistry type",
        default=None,
    )
    opticalActivity: Optional[CodeableConcept] = Field(
        description="Optical activity type",
        default=None,
    )
    molecularFormula: Optional[String] = Field(
        description="Molecular formula",
        default=None,
    )
    molecularFormula_ext: Optional[Element] = Field(
        description="Placeholder element for molecularFormula extensions",
        default=None,
        alias="_molecularFormula",
    )
    molecularFormulaByMoiety: Optional[String] = Field(
        description="Specified per moiety according to the Hill system, i.e. first C, then H, then alphabetical, each moiety separated by a dot",
        default=None,
    )
    molecularFormulaByMoiety_ext: Optional[Element] = Field(
        description="Placeholder element for molecularFormulaByMoiety extensions",
        default=None,
        alias="_molecularFormulaByMoiety",
    )
    isotope: Optional[ListType[SubstanceSpecificationStructureIsotope]] = Field(
        description="Applicable for single substances that contain a radionuclide or a non-natural isotopic ratio",
        default=None,
    )
    molecularWeight: Optional[SubstanceSpecificationStructureMolecularWeight] = Field(
        description="The molecular weight or weight range (for proteins, polymers or nucleic acids)",
        default=None,
    )
    source: Optional[ListType[Reference]] = Field(
        description="Supporting literature",
        default=None,
    )
    representation: Optional[
        ListType[SubstanceSpecificationStructureRepresentation]
    ] = Field(
        description="Molecular structural representation",
        default=None,
    )


class SubstanceSpecificationCode(BackboneElement):
    """
    Codes associated with the substance.
    """

    code: Optional[CodeableConcept] = Field(
        description="The specific code",
        default=None,
    )
    status: Optional[CodeableConcept] = Field(
        description="Status of the code assignment",
        default=None,
    )
    statusDate: Optional[DateTime] = Field(
        description="The date at which the code status is changed as part of the terminology maintenance",
        default=None,
    )
    statusDate_ext: Optional[Element] = Field(
        description="Placeholder element for statusDate extensions",
        default=None,
        alias="_statusDate",
    )
    comment: Optional[String] = Field(
        description="Any comment can be provided in this field, if necessary",
        default=None,
    )
    comment_ext: Optional[Element] = Field(
        description="Placeholder element for comment extensions",
        default=None,
        alias="_comment",
    )
    source: Optional[ListType[Reference]] = Field(
        description="Supporting literature",
        default=None,
    )


class SubstanceSpecificationNameOfficial(BackboneElement):
    """
    Details of the official nature of this name.
    """

    authority: Optional[CodeableConcept] = Field(
        description="Which authority uses this official name",
        default=None,
    )
    status: Optional[CodeableConcept] = Field(
        description="The status of the official name",
        default=None,
    )
    date: Optional[DateTime] = Field(
        description="Date of official name change",
        default=None,
    )
    date_ext: Optional[Element] = Field(
        description="Placeholder element for date extensions",
        default=None,
        alias="_date",
    )


class SubstanceSpecificationName(BackboneElement):
    """
    Names applicable to this substance.
    """

    name: Optional[String] = Field(
        description="The actual name",
        default=None,
    )
    name_ext: Optional[Element] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    type: Optional[CodeableConcept] = Field(
        description="Name type",
        default=None,
    )
    status: Optional[CodeableConcept] = Field(
        description="The status of the name",
        default=None,
    )
    preferred: Optional[Boolean] = Field(
        description="If this is the preferred name for this substance",
        default=None,
    )
    preferred_ext: Optional[Element] = Field(
        description="Placeholder element for preferred extensions",
        default=None,
        alias="_preferred",
    )
    language: Optional[ListType[CodeableConcept]] = Field(
        description="Language of the name",
        default=None,
    )
    domain: Optional[ListType[CodeableConcept]] = Field(
        description="The use context of this name for example if there is a different name a drug active ingredient as opposed to a food colour additive",
        default=None,
    )
    jurisdiction: Optional[ListType[CodeableConcept]] = Field(
        description="The jurisdiction where this name applies",
        default=None,
    )
    synonym: Optional[ListType["SubstanceSpecificationName"]] = Field(
        description="A synonym of this name",
        default=None,
    )
    translation: Optional[ListType["SubstanceSpecificationName"]] = Field(
        description="A translation for this name",
        default=None,
    )
    official: Optional[ListType[SubstanceSpecificationNameOfficial]] = Field(
        description="Details of the official nature of this name",
        default=None,
    )
    source: Optional[ListType[Reference]] = Field(
        description="Supporting literature",
        default=None,
    )


class SubstanceSpecificationRelationship(BackboneElement):
    """
    A link between this substance and another, with details of the relationship.
    """

    substanceReference: Optional[Reference] = Field(
        description="A pointer to another substance, as a resource or just a representational code",
        default=None,
    )
    substanceCodeableConcept: Optional[CodeableConcept] = Field(
        description="A pointer to another substance, as a resource or just a representational code",
        default=None,
    )
    relationship: Optional[CodeableConcept] = Field(
        description='For example "salt to parent", "active moiety", "starting material"',
        default=None,
    )
    isDefining: Optional[Boolean] = Field(
        description="For example where an enzyme strongly bonds with a particular substance, this is a defining relationship for that enzyme, out of several possible substance relationships",
        default=None,
    )
    isDefining_ext: Optional[Element] = Field(
        description="Placeholder element for isDefining extensions",
        default=None,
        alias="_isDefining",
    )
    amountQuantity: Optional[Quantity] = Field(
        description="A numeric factor for the relationship, for instance to express that the salt of a substance has some percentage of the active substance in relation to some other",
        default=None,
    )
    amountRange: Optional[Range] = Field(
        description="A numeric factor for the relationship, for instance to express that the salt of a substance has some percentage of the active substance in relation to some other",
        default=None,
    )
    amountRatio: Optional[Ratio] = Field(
        description="A numeric factor for the relationship, for instance to express that the salt of a substance has some percentage of the active substance in relation to some other",
        default=None,
    )
    amountString: Optional[String] = Field(
        description="A numeric factor for the relationship, for instance to express that the salt of a substance has some percentage of the active substance in relation to some other",
        default=None,
    )
    amountString_ext: Optional[Element] = Field(
        description="Placeholder element for amountString extensions",
        default=None,
        alias="_amountString",
    )
    amountRatioLowLimit: Optional[Ratio] = Field(
        description="For use when the numeric",
        default=None,
    )
    amountType: Optional[CodeableConcept] = Field(
        description='An operator for the amount, for example "average", "approximately", "less than"',
        default=None,
    )
    source: Optional[ListType[Reference]] = Field(
        description="Supporting literature",
        default=None,
    )

    @property
    def substance(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="substance",
        )

    @property
    def amount(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="amount",
        )

    @model_validator(mode="after")
    def substance_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Reference, CodeableConcept],
            field_name_base="substance",
            required=False,
        )

    @model_validator(mode="after")
    def amount_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Quantity, Range, Ratio, String],
            field_name_base="amount",
            required=False,
        )


class SubstanceSpecification(DomainResource):
    """
    The detailed description of a substance, typically at a level beyond what is used for prescribing.
    """

    _abstract = False
    _type = "SubstanceSpecification"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/SubstanceSpecification"

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
    identifier: Optional[Identifier] = Field(
        description="Identifier by which this substance is known",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="High level categorization, e.g. polymer or nucleic acid",
        default=None,
    )
    status: Optional[CodeableConcept] = Field(
        description="Status of substance within the catalogue e.g. approved",
        default=None,
    )
    domain: Optional[CodeableConcept] = Field(
        description="If the substance applies to only human or veterinary use",
        default=None,
    )
    description: Optional[String] = Field(
        description="Textual description of the substance",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    source: Optional[ListType[Reference]] = Field(
        description="Supporting literature",
        default=None,
    )
    comment: Optional[String] = Field(
        description="Textual comment about this record of a substance",
        default=None,
    )
    comment_ext: Optional[Element] = Field(
        description="Placeholder element for comment extensions",
        default=None,
        alias="_comment",
    )
    moiety: Optional[ListType[SubstanceSpecificationMoiety]] = Field(
        description="Moiety, for structural modifications",
        default=None,
    )
    property_: Optional[ListType[SubstanceSpecificationProperty]] = Field(
        description="General specifications for this substance, including how it is related to other substances",
        default=None,
        alias="property",
    )
    referenceInformation: Optional[Reference] = Field(
        description="General information detailing this substance",
        default=None,
    )
    structure: Optional[SubstanceSpecificationStructure] = Field(
        description="Structural information",
        default=None,
    )
    code: Optional[ListType[SubstanceSpecificationCode]] = Field(
        description="Codes associated with the substance",
        default=None,
    )
    name: Optional[ListType[SubstanceSpecificationName]] = Field(
        description="Names applicable to this substance",
        default=None,
    )
    molecularWeight: Optional[
        ListType[SubstanceSpecificationStructureIsotopeMolecularWeight]
    ] = Field(
        description="The molecular weight or weight range (for proteins, polymers or nucleic acids)",
        default=None,
    )
    relationship: Optional[ListType[SubstanceSpecificationRelationship]] = Field(
        description="A link between this substance and another, with details of the relationship",
        default=None,
    )
    nucleicAcid: Optional[Reference] = Field(
        description="Data items specific to nucleic acids",
        default=None,
    )
    polymer: Optional[Reference] = Field(
        description="Data items specific to polymers",
        default=None,
    )
    protein: Optional[Reference] = Field(
        description="Data items specific to proteins",
        default=None,
    )
    sourceMaterial: Optional[Reference] = Field(
        description="Material or taxonomic/anatomical source for the substance",
        default=None,
    )
