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
    CodeableConcept,
    CodeableReference,
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
    dispenser: Optional[Reference] = Field(
        description="Intended performer of dispense",
        default=None,
    )
    dispenserInstruction: Optional[ListType[Annotation]] = Field(
        description="Additional information for the dispenser",
        default=None,
    )
    doseAdministrationAid: Optional[CodeableConcept] = Field(
        description="Type of adherence packaging to use for the dispense",
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

    identifier: Optional[ListType[Identifier]] = Field(
        description="External ids for this request",
        default=None,
    )
    basedOn: Optional[ListType[Reference]] = Field(
        description="A plan or request that is fulfilled in whole or in part by this medication request",
        default=None,
    )
    priorPrescription: Optional[Reference] = Field(
        description="Reference to an order/prescription that is being replaced by this MedicationRequest",
        default=None,
    )
    groupIdentifier: Optional[Identifier] = Field(
        description="Composite request this is part of",
        default=None,
    )
    status: fhir.code = Field(
        description="active | on-hold | ended | stopped | completed | cancelled | entered-in-error | draft | unknown",
    )
    statusReason: Optional[CodeableConcept] = Field(
        description="Reason for current status",
        default=None,
    )
    statusChanged: Optional[fhir.dateTime] = Field(
        description="When the status was changed",
        default=None,
    )
    intent: fhir.code = Field(
        description="proposal | plan | order | original-order | reflex-order | filler-order | instance-order | option",
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description="Grouping or category of medication request",
        default=None,
    )
    priority: Optional[fhir.code] = Field(
        description="routine | urgent | asap | stat",
        default=None,
    )
    doNotPerform: Optional[fhir.boolean] = Field(
        description="True if patient is to stop taking or not to start taking the medication",
        default=None,
    )
    medication: CodeableReference = Field(
        description="Medication to be taken",
    )
    subject: Reference = Field(
        description="Individual or group for whom the medication has been requested",
    )
    informationSource: Optional[ListType[Reference]] = Field(
        description="The person or organization who provided the information about this request, if the source is someone other than the requestor",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="Encounter created as part of encounter/admission/stay",
        default=None,
    )
    supportingInformation: Optional[ListType[Reference]] = Field(
        description="Information to support fulfilling of the medication",
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
    reported: Optional[fhir.boolean] = Field(
        description="Reported rather than primary record",
        default=None,
    )
    performerType: Optional[CodeableConcept] = Field(
        description="Desired kind of performer of the medication administration",
        default=None,
    )
    performer: Optional[ListType[Reference]] = Field(
        description="Intended performer of administration",
        default=None,
    )
    device: Optional[ListType[CodeableReference]] = Field(
        description="Intended type of device for the administration",
        default=None,
    )
    recorder: Optional[Reference] = Field(
        description="Person who entered the request",
        default=None,
    )
    reason: Optional[ListType[CodeableReference]] = Field(
        description="Reason or indication for ordering or not ordering the medication",
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
    renderedDosageInstruction: Optional[fhir.markdown] = Field(
        description="Full representation of the dosage instructions",
        default=None,
    )
    effectiveDosePeriod: Optional[Period] = Field(
        description="Period over which the medication is to be taken",
        default=None,
    )
    dosageInstruction: Optional[ListType[Dosage]] = Field(
        description="Specific instructions for how the medication should be taken",
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
    eventHistory: Optional[ListType[Reference]] = Field(
        description="A list of events of interest in the lifecycle",
        default=None,
    )
