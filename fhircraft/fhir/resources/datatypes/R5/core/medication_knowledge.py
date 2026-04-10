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
    Reference,
    BackboneElement,
    Period,
    Money,
    CodeableReference,
    Dosage,
    Quantity,
    Range,
    Annotation,
    Duration,
    Ratio,
    Attachment,
)
from .resource import Resource
from .domain_resource import DomainResource


class MedicationKnowledgeRelatedMedicationKnowledge(BackboneElement):
    """
    Associated or related medications. For example, if the medication is a branded product (e.g. Crestor), this is the Therapeutic Moeity (e.g. Rosuvastatin) or if this is a generic medication (e.g. Rosuvastatin), this would link to a branded product (e.g. Crestor.
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


class MedicationKnowledgeCost(BackboneElement):
    """
    The price of the medication.
    """

    effectiveDate: Optional[ListType[Period]] = Field(
        description="The date range for which the cost is effective",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="The category of the cost information",
        default=None,
    )
    source: Optional[fhir.string] = Field(
        description="The source or owner for the price information",
        default=None,
    )
    costMoney: Optional[Money] = Field(
        description="The price or category of the cost of the medication",
        default=None,
    )
    costCodeableConcept: Optional[CodeableConcept] = Field(
        description="The price or category of the cost of the medication",
        default=None,
    )

    @property
    def cost(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="cost",
        )

    @model_validator(mode="after")
    def cost_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Money, CodeableConcept],
            field_name_base="cost",
            required=True,
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


class MedicationKnowledgeIndicationGuidelineDosingGuidelineDosage(BackboneElement):
    """
    Dosage for the medication for the specific guidelines.
    """

    type: Optional[CodeableConcept] = Field(
        description="Category of dosage for a medication",
        default=None,
    )
    dosage: Optional[ListType[Dosage]] = Field(
        description="Dosage for the medication for the specific guidelines",
        default=None,
    )


class MedicationKnowledgeIndicationGuidelineDosingGuidelinePatientCharacteristic(
    BackboneElement
):
    """
    Characteristics of the patient that are relevant to the administration guidelines (for example, height, weight, gender, etc.).
    """

    type: Optional[CodeableConcept] = Field(
        description="Categorization of specific characteristic that is relevant to the administration guideline",
        default=None,
    )
    valueCodeableConcept: Optional[CodeableConcept] = Field(
        description="The specific characteristic",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="The specific characteristic",
        default=None,
    )
    valueRange: Optional[Range] = Field(
        description="The specific characteristic",
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
            field_types=[CodeableConcept, Quantity, Range],
            field_name_base="value",
            required=False,
        )


class MedicationKnowledgeIndicationGuidelineDosingGuideline(BackboneElement):
    """
    The guidelines for the dosage of the medication for the indication.
    """

    treatmentIntent: Optional[CodeableConcept] = Field(
        description="Intention of the treatment",
        default=None,
    )
    dosage: Optional[
        ListType[MedicationKnowledgeIndicationGuidelineDosingGuidelineDosage]
    ] = Field(
        description="Dosage for the medication for the specific guidelines",
        default=None,
    )
    administrationTreatment: Optional[CodeableConcept] = Field(
        description="Type of treatment the guideline applies to",
        default=None,
    )
    patientCharacteristic: Optional[
        ListType[
            MedicationKnowledgeIndicationGuidelineDosingGuidelinePatientCharacteristic
        ]
    ] = Field(
        description="Characteristics of the patient that are relevant to the administration guidelines",
        default=None,
    )


class MedicationKnowledgeIndicationGuideline(BackboneElement):
    """
    Guidelines or protocols that are applicable for the administration of the medication based on indication.
    """

    indication: Optional[ListType[CodeableReference]] = Field(
        description="Indication for use that applies to the specific administration guideline",
        default=None,
    )
    dosingGuideline: Optional[
        ListType[MedicationKnowledgeIndicationGuidelineDosingGuideline]
    ] = Field(
        description="Guidelines for dosage of the medication",
        default=None,
    )


class MedicationKnowledgeMedicineClassification(BackboneElement):
    """
    Categorization of the medication within a formulary or classification system.
    """

    type: Optional[CodeableConcept] = Field(
        description="The type of category for the medication (for example, therapeutic classification, therapeutic sub-classification)",
        default=None,
    )
    sourceString: Optional[fhir.string] = Field(
        description="The source of the classification",
        default=None,
    )
    sourceUri: Optional[fhir.uri] = Field(
        description="The source of the classification",
        default=None,
    )
    classification: Optional[ListType[CodeableConcept]] = Field(
        description="Specific category assigned to the medication",
        default=None,
    )

    @property
    def source(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="source",
        )

    @model_validator(mode="after")
    def source_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.string, fhir.uri],
            field_name_base="source",
            required=False,
        )


class MedicationKnowledgePackagingCost(BackboneElement):
    """
    The cost of the packaged medication.
    """

    effectiveDate: Optional[ListType[Period]] = Field(
        description="The date range for which the cost is effective",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="The category of the cost information",
        default=None,
    )
    source: Optional[fhir.string] = Field(
        description="The source or owner for the price information",
        default=None,
    )
    costMoney: Optional[Money] = Field(
        description="The price or category of the cost of the medication",
        default=None,
    )
    costCodeableConcept: Optional[CodeableConcept] = Field(
        description="The price or category of the cost of the medication",
        default=None,
    )

    @property
    def cost(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="cost",
        )

    @model_validator(mode="after")
    def cost_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Money, CodeableConcept],
            field_name_base="cost",
            required=True,
        )


class MedicationKnowledgePackaging(BackboneElement):
    """
    Information that only applies to packages (not products).
    """

    cost: Optional[ListType[MedicationKnowledgePackagingCost]] = Field(
        description="Cost of the packaged medication",
        default=None,
    )
    packagedProduct: Optional[Reference] = Field(
        description="The packaged medication that is being priced",
        default=None,
    )


class MedicationKnowledgeStorageGuidelineEnvironmentalSetting(BackboneElement):
    """
    Describes a setting/value on the environment for the adequate storage of the medication and other substances.  Environment settings may involve temperature, humidity, or exposure to light.
    """

    type: Optional[CodeableConcept] = Field(
        description="Categorization of the setting",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="Value of the setting",
        default=None,
    )
    valueRange: Optional[Range] = Field(
        description="Value of the setting",
        default=None,
    )
    valueCodeableConcept: Optional[CodeableConcept] = Field(
        description="Value of the setting",
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
            field_types=[Quantity, Range, CodeableConcept],
            field_name_base="value",
            required=True,
        )


class MedicationKnowledgeStorageGuideline(BackboneElement):
    """
    Information on how the medication should be stored, for example, refrigeration temperatures and length of stability at a given temperature.
    """

    reference: Optional[fhir.uri] = Field(
        description="Reference to additional information",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Additional storage notes",
        default=None,
    )
    stabilityDuration: Optional[Duration] = Field(
        description="Duration remains stable",
        default=None,
    )
    environmentalSetting: Optional[
        ListType[MedicationKnowledgeStorageGuidelineEnvironmentalSetting]
    ] = Field(
        description="Setting or value of environment for adequate storage",
        default=None,
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
    schedule: Optional[ListType[CodeableConcept]] = Field(
        description="Specifies the schedule of a medication in jurisdiction",
        default=None,
    )
    maxDispense: Optional[MedicationKnowledgeRegulatoryMaxDispense] = Field(
        description="The maximum number of units of the medication that can be dispensed in a period",
        default=None,
    )


class MedicationKnowledgeDefinitionalIngredient(BackboneElement):
    """
    Identifies a particular constituent of interest in the product.
    """

    item: Optional[CodeableReference] = Field(
        description="Substances contained in the medication",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="A code that defines the type of ingredient, active, base, etc",
        default=None,
    )
    strengthRatio: Optional[Ratio] = Field(
        description="Quantity of ingredient present",
        default=None,
    )
    strengthCodeableConcept: Optional[CodeableConcept] = Field(
        description="Quantity of ingredient present",
        default=None,
    )
    strengthQuantity: Optional[Quantity] = Field(
        description="Quantity of ingredient present",
        default=None,
    )

    @property
    def strength(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="strength",
        )

    @model_validator(mode="after")
    def strength_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Ratio, CodeableConcept, Quantity],
            field_name_base="strength",
            required=False,
        )


class MedicationKnowledgeDefinitionalDrugCharacteristic(BackboneElement):
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
    valueAttachment: Optional[Attachment] = Field(
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
            field_types=[
                CodeableConcept,
                fhir.String,
                Quantity,
                fhir.Base64Binary,
                Attachment,
            ],
            field_name_base="value",
            required=False,
        )


class MedicationKnowledgeDefinitional(BackboneElement):
    """
    Along with the link to a Medicinal Product Definition resource, this information provides common definitional elements that are needed to understand the specific medication that is being described.
    """

    definition: Optional[ListType[Reference]] = Field(
        description="Definitional resources that provide more information about this medication",
        default=None,
    )
    doseForm: Optional[CodeableConcept] = Field(
        description="powder | tablets | capsule +",
        default=None,
    )
    intendedRoute: Optional[ListType[CodeableConcept]] = Field(
        description="The intended or approved route of administration",
        default=None,
    )
    ingredient: Optional[ListType[MedicationKnowledgeDefinitionalIngredient]] = Field(
        description="Active or inactive ingredient",
        default=None,
    )
    drugCharacteristic: Optional[
        ListType[MedicationKnowledgeDefinitionalDrugCharacteristic]
    ] = Field(
        description="Specifies descriptive properties of the medicine",
        default=None,
    )


class MedicationKnowledge(DomainResource):
    """
    Information about a medication that is used to support knowledge.
    """

    _abstract = False
    _type = "MedicationKnowledge"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/MedicationKnowledge"

    identifier: Optional[ListType[Identifier]] = Field(
        description="Business identifier for this medication",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="code that identifies this medication",
        default=None,
    )
    status: Optional[fhir.code] = Field(
        description="active | entered-in-error | inactive",
        default=None,
    )
    author: Optional[Reference] = Field(
        description="Creator or owner of the knowledge or information about the medication",
        default=None,
    )
    intendedJurisdiction: Optional[ListType[CodeableConcept]] = Field(
        description="Codes that identify the different jurisdictions for which the information of this resource was created",
        default=None,
    )
    name: Optional[ListType[fhir.string]] = Field(
        description="A name associated with the medication being described",
        default=None,
    )
    relatedMedicationKnowledge: Optional[
        ListType[MedicationKnowledgeRelatedMedicationKnowledge]
    ] = Field(
        description="Associated or related medication information",
        default=None,
    )
    associatedMedication: Optional[ListType[Reference]] = Field(
        description="The set of medication resources that are associated with this medication",
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
    preparationInstruction: Optional[fhir.markdown] = Field(
        description="The instructions for preparing the medication",
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
    indicationGuideline: Optional[ListType[MedicationKnowledgeIndicationGuideline]] = (
        Field(
            description="Guidelines or protocols for administration of the medication for an indication",
            default=None,
        )
    )
    medicineClassification: Optional[
        ListType[MedicationKnowledgeMedicineClassification]
    ] = Field(
        description="Categorization of the medication within a formulary or classification system",
        default=None,
    )
    packaging: Optional[ListType[MedicationKnowledgePackaging]] = Field(
        description="Details about packaged medications",
        default=None,
    )
    clinicalUseIssue: Optional[ListType[Reference]] = Field(
        description="Potential clinical issue with or between medication(s)",
        default=None,
    )
    storageGuideline: Optional[ListType[MedicationKnowledgeStorageGuideline]] = Field(
        description="How the medication should be stored",
        default=None,
    )
    regulatory: Optional[ListType[MedicationKnowledgeRegulatory]] = Field(
        description="Regulatory information about a medication",
        default=None,
    )
    definitional: Optional[MedicationKnowledgeDefinitional] = Field(
        description="Minimal definition information about the medication",
        default=None,
    )
