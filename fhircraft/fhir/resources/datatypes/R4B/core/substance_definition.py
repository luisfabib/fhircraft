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
    CodeableConcept,
    Reference,
    Annotation,
    BackboneElement,
    Quantity,
    Attachment,
    Ratio,
)
from .resource import Resource
from .domain_resource import DomainResource


class SubstanceDefinitionMoiety(BackboneElement):
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
    name: Optional[fhir.string] = Field(
        description="Textual name for this moiety substance",
        default=None,
    )
    stereochemistry: Optional[CodeableConcept] = Field(
        description="Stereochemistry type",
        default=None,
    )
    opticalActivity: Optional[CodeableConcept] = Field(
        description="Optical activity type",
        default=None,
    )
    molecularFormula: Optional[fhir.string] = Field(
        description="Molecular formula for this moiety (e.g. with the Hill system)",
        default=None,
    )
    amountQuantity: Optional[Quantity] = Field(
        description="Quantitative value for this moiety",
        default=None,
    )
    amountString: Optional[fhir.string] = Field(
        description="Quantitative value for this moiety",
        default=None,
    )
    measurementType: Optional[CodeableConcept] = Field(
        description="The measurement type of the quantitative value",
        default=None,
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
            field_types=[Quantity, fhir.String],
            field_name_base="amount",
            required=False,
        )


class SubstanceDefinitionProperty(BackboneElement):
    """
    General specifications for this substance.
    """

    type: CodeableConcept = Field(
        description="A code expressing the type of property",
    )
    valueCodeableConcept: Optional[CodeableConcept] = Field(
        description="A value for the property",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="A value for the property",
        default=None,
    )
    valueDate: Optional[fhir.date_] = Field(
        description="A value for the property",
        default=None,
    )
    valueBoolean: Optional[fhir.boolean] = Field(
        description="A value for the property",
        default=None,
    )
    valueAttachment: Optional[Attachment] = Field(
        description="A value for the property",
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
                CodeableConcept,
                Quantity,
                fhir.Date,
                fhir.Boolean,
                Attachment,
            ],
            field_name_base="value",
            required=False,
        )


class SubstanceDefinitionMolecularWeight(BackboneElement):
    """
    The molecular weight or weight range (for proteins, polymers or nucleic acids).
    """

    method: Optional[CodeableConcept] = Field(
        description="The method by which the weight was determined",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Type of molecular weight e.g. exact, average, weight average",
        default=None,
    )
    amount: Quantity = Field(
        description="Used to capture quantitative values for a variety of elements",
    )


class SubstanceDefinitionStructureMolecularWeight(BackboneElement):
    """
    The molecular weight or weight range (for proteins, polymers or nucleic acids).
    """

    method: Optional[CodeableConcept] = Field(
        description="The method by which the weight was determined",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Type of molecular weight e.g. exact, average, weight average",
        default=None,
    )
    amount: Optional[Quantity] = Field(
        description="Used to capture quantitative values for a variety of elements",
        default=None,
    )


class SubstanceDefinitionStructureRepresentation(BackboneElement):
    """
    A depiction of the structure or characterization of the substance.
    """

    type: Optional[CodeableConcept] = Field(
        description="The kind of structural representation (e.g. full, partial)",
        default=None,
    )
    representation: Optional[fhir.string] = Field(
        description="The structural representation or characterization as a text string in a standard format",
        default=None,
    )
    format: Optional[CodeableConcept] = Field(
        description="The format of the representation e.g. InChI, SMILES, MOLFILE (note: not the physical file format)",
        default=None,
    )
    document: Optional[Reference] = Field(
        description="An attachment with the structural representation e.g. a structure graphic or AnIML file",
        default=None,
    )


class SubstanceDefinitionStructure(BackboneElement):
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
    molecularFormula: Optional[fhir.string] = Field(
        description="Molecular formula (e.g. using the Hill system)",
        default=None,
    )
    molecularFormulaByMoiety: Optional[fhir.string] = Field(
        description="Specified per moiety according to the Hill system",
        default=None,
    )
    molecularWeight: Optional[SubstanceDefinitionStructureMolecularWeight] = Field(
        description="The molecular weight or weight range",
        default=None,
    )
    technique: Optional[ListType[CodeableConcept]] = Field(
        description="The method used to find the structure e.g. X-ray, NMR",
        default=None,
    )
    sourceDocument: Optional[ListType[Reference]] = Field(
        description="Source of information for the structure",
        default=None,
    )
    representation: Optional[ListType[SubstanceDefinitionStructureRepresentation]] = (
        Field(
            description="A depiction of the structure or characterization of the substance",
            default=None,
        )
    )


class SubstanceDefinitionCode(BackboneElement):
    """
    Codes associated with the substance.
    """

    code: Optional[CodeableConcept] = Field(
        description="The specific code",
        default=None,
    )
    status: Optional[CodeableConcept] = Field(
        description="Status of the code assignment, for example \u0027provisional\u0027, \u0027approved\u0027",
        default=None,
    )
    statusDate: Optional[fhir.dateTime] = Field(
        description="The date at which the code status was changed",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Any comment can be provided in this field",
        default=None,
    )
    source: Optional[ListType[Reference]] = Field(
        description="Supporting literature",
        default=None,
    )


class SubstanceDefinitionNameOfficial(BackboneElement):
    """
    Details of the official nature of this name.
    """

    authority: Optional[CodeableConcept] = Field(
        description="Which authority uses this official name",
        default=None,
    )
    status: Optional[CodeableConcept] = Field(
        description="The status of the official name, for example \u0027draft\u0027, \u0027active\u0027",
        default=None,
    )
    date: Optional[fhir.dateTime] = Field(
        description="Date of official name change",
        default=None,
    )


class SubstanceDefinitionName(BackboneElement):
    """
    Names applicable to this substance.
    """

    name: fhir.string = Field(
        description="The actual name",
    )
    type: Optional[CodeableConcept] = Field(
        description="Name type e.g. \u0027systematic\u0027,  \u0027scientific, \u0027brand\u0027",
        default=None,
    )
    status: Optional[CodeableConcept] = Field(
        description="The status of the name e.g. \u0027current\u0027, \u0027proposed\u0027",
        default=None,
    )
    preferred: Optional[fhir.boolean] = Field(
        description="If this is the preferred name for this substance",
        default=None,
    )
    language: Optional[ListType[CodeableConcept]] = Field(
        description="Human language that the name is written in",
        default=None,
    )
    domain: Optional[ListType[CodeableConcept]] = Field(
        description="The use context of this name e.g. as an active ingredient or as a food colour additive",
        default=None,
    )
    jurisdiction: Optional[ListType[CodeableConcept]] = Field(
        description="The jurisdiction where this name applies",
        default=None,
    )
    synonym: Optional[ListType["SubstanceDefinitionName"]] = Field(
        description="A synonym of this particular name, by which the substance is also known",
        default=None,
    )
    translation: Optional[ListType["SubstanceDefinitionName"]] = Field(
        description="A translation for this name into another human language",
        default=None,
    )
    official: Optional[ListType[SubstanceDefinitionNameOfficial]] = Field(
        description="Details of the official nature of this name",
        default=None,
    )
    source: Optional[ListType[Reference]] = Field(
        description="Supporting literature",
        default=None,
    )


class SubstanceDefinitionRelationship(BackboneElement):
    """
    A link between this substance and another, with details of the relationship.
    """

    substanceDefinitionReference: Optional[Reference] = Field(
        description="A pointer to another substance, as a resource or a representational code",
        default=None,
    )
    substanceDefinitionCodeableConcept: Optional[CodeableConcept] = Field(
        description="A pointer to another substance, as a resource or a representational code",
        default=None,
    )
    type: CodeableConcept = Field(
        description='For example "salt to parent", "active moiety"',
    )
    isDefining: Optional[fhir.boolean] = Field(
        description="For example where an enzyme strongly bonds with a particular substance, this is a defining relationship for that enzyme, out of several possible relationships",
        default=None,
    )
    amountQuantity: Optional[Quantity] = Field(
        description="A numeric factor for the relationship, e.g. that a substance salt has some percentage of active substance in relation to some other",
        default=None,
    )
    amountRatio: Optional[Ratio] = Field(
        description="A numeric factor for the relationship, e.g. that a substance salt has some percentage of active substance in relation to some other",
        default=None,
    )
    amountString: Optional[fhir.string] = Field(
        description="A numeric factor for the relationship, e.g. that a substance salt has some percentage of active substance in relation to some other",
        default=None,
    )
    ratioHighLimitAmount: Optional[Ratio] = Field(
        description="For use when the numeric has an uncertain range",
        default=None,
    )
    comparator: Optional[CodeableConcept] = Field(
        description='An operator for the amount, for example "average", "approximately", "less than"',
        default=None,
    )
    source: Optional[ListType[Reference]] = Field(
        description="Supporting literature",
        default=None,
    )

    @property
    def substanceDefinition(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="substanceDefinition",
        )

    @property
    def amount(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="amount",
        )

    @model_validator(mode="after")
    def substanceDefinition_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Reference, CodeableConcept],
            field_name_base="substanceDefinition",
            required=False,
        )

    @model_validator(mode="after")
    def amount_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Quantity, Ratio, fhir.String],
            field_name_base="amount",
            required=False,
        )


class SubstanceDefinitionSourceMaterial(BackboneElement):
    """
    Material or taxonomic/anatomical source for the substance.
    """

    type: Optional[CodeableConcept] = Field(
        description="Classification of the origin of the raw material. e.g. cat hair is an Animal source type",
        default=None,
    )
    genus: Optional[CodeableConcept] = Field(
        description="The genus of an organism e.g. the Latin epithet of the plant/animal scientific name",
        default=None,
    )
    species: Optional[CodeableConcept] = Field(
        description="The species of an organism e.g. the Latin epithet of the species of the plant/animal",
        default=None,
    )
    part: Optional[CodeableConcept] = Field(
        description="An anatomical origin of the source material within an organism",
        default=None,
    )
    countryOfOrigin: Optional[ListType[CodeableConcept]] = Field(
        description="The country or countries where the material is harvested",
        default=None,
    )


class SubstanceDefinition(DomainResource):
    """
    The detailed description of a substance, typically at a level beyond what is used for prescribing.
    """

    _abstract = False
    _type = "SubstanceDefinition"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/SubstanceDefinition"

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
        description="Identifier by which this substance is known",
        default=None,
    )
    version: Optional[fhir.string] = Field(
        description="A business level version identifier of the substance",
        default=None,
    )
    status: Optional[CodeableConcept] = Field(
        description="Status of substance within the catalogue e.g. active, retired",
        default=None,
    )
    classification: Optional[ListType[CodeableConcept]] = Field(
        description="A categorization, high level e.g. polymer or nucleic acid, or food, chemical, biological, or lower e.g. polymer linear or branch chain, or type of impurity",
        default=None,
    )
    domain: Optional[CodeableConcept] = Field(
        description="If the substance applies to human or veterinary use",
        default=None,
    )
    grade: Optional[ListType[CodeableConcept]] = Field(
        description="The quality standard, established benchmark, to which substance complies (e.g. USP/NF, BP)",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
        description="Textual description of the substance",
        default=None,
    )
    informationSource: Optional[ListType[Reference]] = Field(
        description="Supporting literature",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Textual comment about the substance\u0027s catalogue or registry record",
        default=None,
    )
    manufacturer: Optional[ListType[Reference]] = Field(
        description="The entity that creates, makes, produces or fabricates the substance",
        default=None,
    )
    supplier: Optional[ListType[Reference]] = Field(
        description="An entity that is the source for the substance. It may be different from the manufacturer",
        default=None,
    )
    moiety: Optional[ListType[SubstanceDefinitionMoiety]] = Field(
        description="Moiety, for structural modifications",
        default=None,
    )
    property_: Optional[ListType[SubstanceDefinitionProperty]] = Field(
        description="General specifications for this substance",
        default=None,
        alias="property",
    )
    molecularWeight: Optional[ListType[SubstanceDefinitionMolecularWeight]] = Field(
        description="The molecular weight or weight range",
        default=None,
    )
    structure: Optional[SubstanceDefinitionStructure] = Field(
        description="Structural information",
        default=None,
    )
    code: Optional[ListType[SubstanceDefinitionCode]] = Field(
        description="Codes associated with the substance",
        default=None,
    )
    name: Optional[ListType[SubstanceDefinitionName]] = Field(
        description="Names applicable to this substance",
        default=None,
    )
    relationship: Optional[ListType[SubstanceDefinitionRelationship]] = Field(
        description="A link between this substance and another",
        default=None,
    )
    sourceMaterial: Optional[SubstanceDefinitionSourceMaterial] = Field(
        description="Material or taxonomic/anatomical source",
        default=None,
    )
