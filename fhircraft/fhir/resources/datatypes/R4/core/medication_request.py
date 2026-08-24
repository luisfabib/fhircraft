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
    CodeableConcept,
    Reference,
    Annotation,
    Period,
    Dosage,
    BackboneElement,
    Quantity,
    Duration,
)
from .resource import Resource
from .domain_resource import DomainResource

class MedicationRequestDispenseRequestInitialFill(BackboneElement):
    """
    Indicates the quantity or duration for the first dispense of the medication.
    """

    quantity: Optional[Quantity] = Field(
        description="First fill quantity",
        default=None,
    )
    duration: Optional[Duration] = Field(
        description="First fill duration",
        default=None,
    )

class MedicationRequestDispenseRequest(BackboneElement):
    """
    Indicates the specific details for the dispense or medication supply part of a medication request (also known as a Medication Prescription or Medication Order).  Note that this information is not always sent with the order.  There may be in some settings (e.g. hospitals) institutional or system support for completing the dispense details in the pharmacy department.
    """

    initialFill: Optional[MedicationRequestDispenseRequestInitialFill] = Field(
        description="First fill details",
        default=None,
    )
    dispenseInterval: Optional[Duration] = Field(
        description="Minimum period of time between dispenses",
        default=None,
    )
    validityPeriod: Optional[Period] = Field(
        description="time period supply is authorized for",
        default=None,
    )
    numberOfRepeatsAllowed: Optional[fhir.unsignedInt] = Field(
        description="Number of refills authorized",
        default=None,
    )
    quantity: Optional[Quantity] = Field(
        description="Amount of medication to supply per dispense",
        default=None,
    )
    expectedSupplyDuration: Optional[Duration] = Field(
        description="Number of days supply per dispense",
        default=None,
    )
    performer: Optional[Reference] = Field(
        description="Intended dispenser",
        default=None,
    )

class MedicationRequestSubstitution(BackboneElement):
    """
    Indicates whether or not substitution can or should be part of the dispense. In some cases, substitution must happen, in other cases substitution must not happen. This block explains the prescriber's intent. If nothing is specified substitution may be done.
    """

    allowedBoolean: Optional[fhir.boolean] = Field(
        description="Whether substitution is allowed or not",
        default=None,
    )
    allowedCodeableConcept: Optional[CodeableConcept] = Field(
        description="Whether substitution is allowed or not",
        default=None,
    )
    reason: Optional[CodeableConcept] = Field(
        description="Why should (not) substitution be made",
        default=None,
    )

    @property
    def allowed(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="allowed",
        )

    @model_validator(mode="after")
    def allowed_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.Boolean, CodeableConcept],
            field_name_base="allowed",
            required=True,
        )

class MedicationRequest(DomainResource):
    """
    An order or request for both supply of the medication and the instructions for administration of the medication to a patient. The resource is called "MedicationRequest" rather than "MedicationPrescription" or "MedicationOrder" to generalize the use across inpatient and outpatient settings, including care plans, etc., and to harmonize with workflow patterns.
    """

    _abstract = False
    _type = "MedicationRequest"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/MedicationRequest"

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
        description="External ids for this request",
        default=None,
    )
    status: fhir.code = Field(
        description="active | on-hold | cancelled | completed | entered-in-error | stopped | draft | unknown",
    )
    statusReason: Optional[CodeableConcept] = Field(
        description="Reason for current status",
        default=None,
    )
    intent: fhir.code = Field(
        description="proposal | plan | order | original-order | reflex-order | filler-order | instance-order | option",
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description="Type of medication usage",
        default=None,
    )
    priority: Optional[fhir.code] = Field(
        description="routine | urgent | asap | stat",
        default=None,
    )
    doNotPerform: Optional[fhir.boolean] = Field(
        description="True if request is prohibiting action",
        default=None,
    )
    reportedBoolean: Optional[fhir.boolean] = Field(
        description="Reported rather than primary record",
        default=None,
    )
    reportedReference: Optional[Reference] = Field(
        description="Reported rather than primary record",
        default=None,
    )
    medicationCodeableConcept: Optional[CodeableConcept] = Field(
        description="Medication to be taken",
        default=None,
    )
    medicationReference: Optional[Reference] = Field(
        description="Medication to be taken",
        default=None,
    )
    subject: Reference = Field(
        description="Who or group medication request is for",
    )
    encounter: Optional[Reference] = Field(
        description="Encounter created as part of encounter/admission/stay",
        default=None,
    )
    supportingInformation: Optional[ListType[Reference]] = Field(
        description="Information to support ordering of the medication",
        default=None,
    )
    authoredOn: Optional[fhir.dateTime] = Field(
        description="When request was initially authored",
        default=None,
    )
    requester: Optional[Reference] = Field(
        description="Who/What requested the Request",
        default=None,
    )
    performer: Optional[Reference] = Field(
        description="Intended performer of administration",
        default=None,
    )
    performerType: Optional[CodeableConcept] = Field(
        description="Desired kind of performer of the medication administration",
        default=None,
    )
    recorder: Optional[Reference] = Field(
        description="Person who entered the request",
        default=None,
    )
    reasonCode: Optional[ListType[CodeableConcept]] = Field(
        description="Reason or indication for ordering or not ordering the medication",
        default=None,
    )
    reasonReference: Optional[ListType[Reference]] = Field(
        description="Condition or observation that supports why the prescription is being written",
        default=None,
    )
    instantiatesCanonical: Optional[ListType[fhir.canonical]] = Field(
        description="Instantiates FHIR protocol or definition",
        default=None,
    )
    instantiatesUri: Optional[ListType[fhir.uri]] = Field(
        description="Instantiates external protocol or definition",
        default=None,
    )
    basedOn: Optional[ListType[Reference]] = Field(
        description="What request fulfills",
        default=None,
    )
    groupIdentifier: Optional[Identifier] = Field(
        description="Composite request this is part of",
        default=None,
    )
    courseOfTherapyType: Optional[CodeableConcept] = Field(
        description="Overall pattern of medication administration",
        default=None,
    )
    insurance: Optional[ListType[Reference]] = Field(
        description="Associated insurance coverage",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Information about the prescription",
        default=None,
    )
    dosageInstruction: Optional[ListType[Dosage]] = Field(
        description="How the medication should be taken",
        default=None,
    )
    dispenseRequest: Optional[MedicationRequestDispenseRequest] = Field(
        description="Medication supply authorization",
        default=None,
    )
    substitution: Optional[MedicationRequestSubstitution] = Field(
        description="Any restrictions on medication substitution",
        default=None,
    )
    priorPrescription: Optional[Reference] = Field(
        description="An order/prescription that is being replaced",
        default=None,
    )
    detectedIssue: Optional[ListType[Reference]] = Field(
        description="Clinical Issue with action",
        default=None,
    )
    eventHistory: Optional[ListType[Reference]] = Field(
        description="A list of events of interest in the lifecycle",
        default=None,
    )

    @property
    def reported(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="reported",
        )

    @property
    def medication(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="medication",
        )

    @model_validator(mode="after")
    def reported_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.Boolean, Reference],
            field_name_base="reported",
            required=False,
        )

    @model_validator(mode="after")
    def medication_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[CodeableConcept, Reference],
            field_name_base="medication",
            required=True,
        )
