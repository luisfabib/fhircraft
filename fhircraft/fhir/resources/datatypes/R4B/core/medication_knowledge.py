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
    CodeableConcept,
    Reference,
    Quantity,
    BackboneElement,
    Ratio,
    Money,
    Dosage,
    Duration,
)
from .resource import Resource
from .domain_resource import DomainResource


class MedicationKnowledgeRelatedMedicationKnowledge(BackboneElement):
    """
    Associated or related knowledge about a medication.
    """

    type: Optional[CodeableConcept] = Field(
        description="Category of medicationKnowledge",
        default=None,
    )
    reference: Optional[ListType[Reference]] = Field(
        description="Associated documentation about the associated medication knowledge",
        default=None,
    )


class MedicationKnowledgeMonograph(BackboneElement):
    """
    Associated documentation about the medication.
    """

    type: Optional[CodeableConcept] = Field(
        description="The category of medication document",
        default=None,
    )
    source: Optional[Reference] = Field(
        description="Associated documentation about the medication",
        default=None,
    )


class MedicationKnowledgeIngredient(BackboneElement):
    """
    Identifies a particular constituent of interest in the product.
    """

    itemCodeableConcept: Optional[CodeableConcept] = Field(
        description="Medication(s) or substance(s) contained in the medication",
        default=None,
    )
    itemReference: Optional[Reference] = Field(
        description="Medication(s) or substance(s) contained in the medication",
        default=None,
    )
    isActive: Optional[fhir.boolean] = Field(
        description="Active ingredient indicator",
        default=None,
    )
    strength: Optional[Ratio] = Field(
        description="Quantity of ingredient present",
        default=None,
    )

    @property
    def item(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="item",
        )

    @model_validator(mode="after")
    def item_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[CodeableConcept, Reference],
            field_name_base="item",
            required=True,
        )


class MedicationKnowledgeCost(BackboneElement):
    """
    The price of the medication.
    """

    type: Optional[CodeableConcept] = Field(
        description="The category of the cost information",
        default=None,
    )
    source: Optional[fhir.string] = Field(
        description="The source or owner for the price information",
        default=None,
    )
    cost: Optional[Money] = Field(
        description="The price of the medication",
        default=None,
    )


class MedicationKnowledgeMonitoringProgram(BackboneElement):
    """
    The program under which the medication is reviewed.
    """

    type: Optional[CodeableConcept] = Field(
        description="Type of program under which the medication is monitored",
        default=None,
    )
    name: Optional[fhir.string] = Field(
        description="Name of the reviewing program",
        default=None,
    )


class MedicationKnowledgeAdministrationGuidelinesDosage(BackboneElement):
    """
    Dosage for the medication for the specific guidelines.
    """

    type: Optional[CodeableConcept] = Field(
        description="Type of dosage",
        default=None,
    )
    dosage: Optional[ListType[Dosage]] = Field(
        description="Dosage for the medication for the specific guidelines",
        default=None,
    )


class MedicationKnowledgeAdministrationGuidelinesPatientCharacteristics(
    BackboneElement
):
    """
    Characteristics of the patient that are relevant to the administration guidelines (for example, height, weight, gender, etc.).
    """

    characteristicCodeableConcept: Optional[CodeableConcept] = Field(
        description="Specific characteristic that is relevant to the administration guideline",
        default=None,
    )
    characteristicQuantity: Optional[Quantity] = Field(
        description="Specific characteristic that is relevant to the administration guideline",
        default=None,
    )
    value: Optional[ListType[fhir.string]] = Field(
        description="The specific characteristic",
        default=None,
    )

    @property
    def characteristic(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="characteristic",
        )

    @model_validator(mode="after")
    def characteristic_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[CodeableConcept, Quantity],
            field_name_base="characteristic",
            required=True,
        )


class MedicationKnowledgeAdministrationGuidelines(BackboneElement):
    """
    Guidelines for the administration of the medication.
    """

    dosage: Optional[ListType[MedicationKnowledgeAdministrationGuidelinesDosage]] = (
        Field(
            description="Dosage for the medication for the specific guidelines",
            default=None,
        )
    )
    indicationCodeableConcept: Optional[CodeableConcept] = Field(
        description="Indication for use that apply to the specific administration guidelines",
        default=None,
    )
    indicationReference: Optional[Reference] = Field(
        description="Indication for use that apply to the specific administration guidelines",
        default=None,
    )
    patientCharacteristics: Optional[
        ListType[MedicationKnowledgeAdministrationGuidelinesPatientCharacteristics]
    ] = Field(
        description="Characteristics of the patient that are relevant to the administration guidelines",
        default=None,
    )

    @property
    def indication(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="indication",
        )

    @model_validator(mode="after")
    def indication_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[CodeableConcept, Reference],
            field_name_base="indication",
            required=False,
        )


class MedicationKnowledgeMedicineClassification(BackboneElement):
    """
    Categorization of the medication within a formulary or classification system.
    """

    type: Optional[CodeableConcept] = Field(
        description="The type of category for the medication (for example, therapeutic classification, therapeutic sub-classification)",
        default=None,
    )
    classification: Optional[ListType[CodeableConcept]] = Field(
        description="Specific category assigned to the medication",
        default=None,
    )


class MedicationKnowledgePackaging(BackboneElement):
    """
    Information that only applies to packages (not products).
    """

    type: Optional[CodeableConcept] = Field(
        description="A code that defines the specific type of packaging that the medication can be found in",
        default=None,
    )
    quantity: Optional[Quantity] = Field(
        description="The number of product units the package would contain if fully loaded",
        default=None,
    )


class MedicationKnowledgeDrugCharacteristic(BackboneElement):
    """
    Specifies descriptive properties of the medicine, such as color, shape, imprints, etc.
    """

    type: Optional[CodeableConcept] = Field(
        description="code specifying the type of characteristic of medication",
        default=None,
    )
    valueCodeableConcept: Optional[CodeableConcept] = Field(
        description="Description of the characteristic",
        default=None,
    )
    valueString: Optional[fhir.string] = Field(
        description="Description of the characteristic",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="Description of the characteristic",
        default=None,
    )
    valueBase64Binary: Optional[fhir.base64Binary] = Field(
        description="Description of the characteristic",
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
            field_types=[CodeableConcept, fhir.string, Quantity, fhir.base64Binary],
            field_name_base="value",
            required=False,
        )


class MedicationKnowledgeRegulatorySubstitution(BackboneElement):
    """
    Specifies if changes are allowed when dispensing a medication from a regulatory perspective.
    """

    type: Optional[CodeableConcept] = Field(
        description="Specifies the type of substitution allowed",
        default=None,
    )
    allowed: Optional[fhir.boolean] = Field(
        description="Specifies if regulation allows for changes in the medication when dispensing",
        default=None,
    )


class MedicationKnowledgeRegulatorySchedule(BackboneElement):
    """
    Specifies the schedule of a medication in jurisdiction.
    """

    schedule: Optional[CodeableConcept] = Field(
        description="Specifies the specific drug schedule",
        default=None,
    )


class MedicationKnowledgeRegulatoryMaxDispense(BackboneElement):
    """
    The maximum number of units of the medication that can be dispensed in a period.
    """

    quantity: Optional[Quantity] = Field(
        description="The maximum number of units of the medication that can be dispensed",
        default=None,
    )
    period: Optional[Duration] = Field(
        description="The period that applies to the maximum number of units",
        default=None,
    )


class MedicationKnowledgeRegulatory(BackboneElement):
    """
    Regulatory information about a medication.
    """

    regulatoryAuthority: Optional[Reference] = Field(
        description="Specifies the authority of the regulation",
        default=None,
    )
    substitution: Optional[ListType[MedicationKnowledgeRegulatorySubstitution]] = Field(
        description="Specifies if changes are allowed when dispensing a medication from a regulatory perspective",
        default=None,
    )
    schedule: Optional[ListType[MedicationKnowledgeRegulatorySchedule]] = Field(
        description="Specifies the schedule of a medication in jurisdiction",
        default=None,
    )
    maxDispense: Optional[MedicationKnowledgeRegulatoryMaxDispense] = Field(
        description="The maximum number of units of the medication that can be dispensed in a period",
        default=None,
    )


class MedicationKnowledgeKinetics(BackboneElement):
    """
    The time course of drug absorption, distribution, metabolism and excretion of a medication from the body.
    """

    areaUnderCurve: Optional[ListType[Quantity]] = Field(
        description="The drug concentration measured at certain discrete points in time",
        default=None,
    )
    lethalDose50: Optional[ListType[Quantity]] = Field(
        description="The median lethal dose of a drug",
        default=None,
    )
    halfLifePeriod: Optional[Duration] = Field(
        description="time required for concentration in the body to decrease by half",
        default=None,
    )


class MedicationKnowledge(DomainResource):
    """
    Information about a medication that is used to support knowledge.
    """

    _abstract = False
    _type = "MedicationKnowledge"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/MedicationKnowledge"

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
    code: Optional[CodeableConcept] = Field(
        description="code that identifies this medication",
        default=None,
    )
    status: Optional[fhir.code] = Field(
        description="active | inactive | entered-in-error",
        default=None,
    )
    manufacturer: Optional[Reference] = Field(
        description="Manufacturer of the item",
        default=None,
    )
    doseForm: Optional[CodeableConcept] = Field(
        description="powder | tablets | capsule +",
        default=None,
    )
    amount: Optional[Quantity] = Field(
        description="Amount of drug in package",
        default=None,
    )
    synonym: Optional[ListType[fhir.string]] = Field(
        description="Additional names for a medication",
        default=None,
    )
    relatedMedicationKnowledge: Optional[
        ListType[MedicationKnowledgeRelatedMedicationKnowledge]
    ] = Field(
        description="Associated or related medication information",
        default=None,
    )
    associatedMedication: Optional[ListType[Reference]] = Field(
        description="A medication resource that is associated with this medication",
        default=None,
    )
    productType: Optional[ListType[CodeableConcept]] = Field(
        description="Category of the medication or product",
        default=None,
    )
    monograph: Optional[ListType[MedicationKnowledgeMonograph]] = Field(
        description="Associated documentation about the medication",
        default=None,
    )
    ingredient: Optional[ListType[MedicationKnowledgeIngredient]] = Field(
        description="Active or inactive ingredient",
        default=None,
    )
    preparationInstruction: Optional[fhir.markdown] = Field(
        description="The instructions for preparing the medication",
        default=None,
    )
    intendedRoute: Optional[ListType[CodeableConcept]] = Field(
        description="The intended or approved route of administration",
        default=None,
    )
    cost: Optional[ListType[MedicationKnowledgeCost]] = Field(
        description="The pricing of the medication",
        default=None,
    )
    monitoringProgram: Optional[ListType[MedicationKnowledgeMonitoringProgram]] = Field(
        description="Program under which a medication is reviewed",
        default=None,
    )
    administrationGuidelines: Optional[
        ListType[MedicationKnowledgeAdministrationGuidelines]
    ] = Field(
        description="Guidelines for administration of the medication",
        default=None,
    )
    medicineClassification: Optional[
        ListType[MedicationKnowledgeMedicineClassification]
    ] = Field(
        description="Categorization of the medication within a formulary or classification system",
        default=None,
    )
    packaging: Optional[MedicationKnowledgePackaging] = Field(
        description="Details about packaged medications",
        default=None,
    )
    drugCharacteristic: Optional[ListType[MedicationKnowledgeDrugCharacteristic]] = (
        Field(
            description="Specifies descriptive properties of the medicine",
            default=None,
        )
    )
    contraindication: Optional[ListType[Reference]] = Field(
        description="Potential clinical issue with or between medication(s)",
        default=None,
    )
    regulatory: Optional[ListType[MedicationKnowledgeRegulatory]] = Field(
        description="Regulatory information about a medication",
        default=None,
    )
    kinetics: Optional[ListType[MedicationKnowledgeKinetics]] = Field(
        description="The time course of drug absorption, distribution, metabolism and excretion of a medication from the body",
        default=None,
    )
