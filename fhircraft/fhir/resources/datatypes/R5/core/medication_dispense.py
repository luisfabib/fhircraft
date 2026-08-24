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
    CodeableReference,
    CodeableConcept,
    BackboneElement,
    Quantity,
    Annotation,
    Dosage,
)
from .resource import Resource
from .domain_resource import DomainResource

class MedicationDispensePerformer(BackboneElement):
    """
    Indicates who or what performed the event.
    """

    function: Optional[CodeableConcept] = Field(
        description="Who performed the dispense and what they did",
        default=None,
    )
    actor: Reference = Field(
        description="Individual who was performing",
    )

class MedicationDispenseSubstitution(BackboneElement):
    """
    Indicates whether or not substitution was made as part of the dispense.  In some cases, substitution will be expected but does not happen, in other cases substitution is not expected but does happen.  This block explains what substitution did or did not happen and why.  If nothing is specified, substitution was not done.
    """

    wasSubstituted: fhir.boolean = Field(
        description="Whether a substitution was or was not performed on the dispense",
    )
    type: Optional[CodeableConcept] = Field(
        description="code signifying whether a different drug was dispensed from what was prescribed",
        default=None,
    )
    reason: Optional[ListType[CodeableConcept]] = Field(
        description="Why was substitution made",
        default=None,
    )
    responsibleParty: Optional[Reference] = Field(
        description="Who is responsible for the substitution",
        default=None,
    )

class MedicationDispense(DomainResource):
    """
    Indicates that a medication product is to be or has been dispensed for a named person/patient.  This includes a description of the medication product (supply) provided and the instructions for administering the medication.  The medication dispense is the result of a pharmacy system responding to a medication order.
    """

    _abstract = False
    _type = "MedicationDispense"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/MedicationDispense"

    identifier: Optional[ListType[Identifier]] = Field(
        description="External identifier",
        default=None,
    )
    basedOn: Optional[ListType[Reference]] = Field(
        description="Plan that is fulfilled by this dispense",
        default=None,
    )
    partOf: Optional[ListType[Reference]] = Field(
        description="Event that dispense is part of",
        default=None,
    )
    status: fhir.code = Field(
        description="preparation | in-progress | cancelled | on-hold | completed | entered-in-error | stopped | declined | unknown",
    )
    notPerformedReason: Optional[CodeableReference] = Field(
        description="Why a dispense was not performed",
        default=None,
    )
    statusChanged: Optional[fhir.dateTime] = Field(
        description="When the status changed",
        default=None,
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description="Type of medication dispense",
        default=None,
    )
    medication: CodeableReference = Field(
        description="What medication was supplied",
    )
    subject: Reference = Field(
        description="Who the dispense is for",
    )
    encounter: Optional[Reference] = Field(
        description="Encounter associated with event",
        default=None,
    )
    supportingInformation: Optional[ListType[Reference]] = Field(
        description="Information that supports the dispensing of the medication",
        default=None,
    )
    performer: Optional[ListType[MedicationDispensePerformer]] = Field(
        description="Who performed event",
        default=None,
    )
    location: Optional[Reference] = Field(
        description="Where the dispense occurred",
        default=None,
    )
    authorizingPrescription: Optional[ListType[Reference]] = Field(
        description="Medication order that authorizes the dispense",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Trial fill, partial fill, emergency fill, etc",
        default=None,
    )
    quantity: Optional[Quantity] = Field(
        description="Amount dispensed",
        default=None,
    )
    daysSupply: Optional[Quantity] = Field(
        description="Amount of medication expressed as a timing amount",
        default=None,
    )
    recorded: Optional[fhir.dateTime] = Field(
        description="When the recording of the dispense started",
        default=None,
    )
    whenPrepared: Optional[fhir.dateTime] = Field(
        description="When product was packaged and reviewed",
        default=None,
    )
    whenHandedOver: Optional[fhir.dateTime] = Field(
        description="When product was given out",
        default=None,
    )
    destination: Optional[Reference] = Field(
        description="Where the medication was/will be sent",
        default=None,
    )
    receiver: Optional[ListType[Reference]] = Field(
        description="Who collected the medication or where the medication was delivered",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Information about the dispense",
        default=None,
    )
    renderedDosageInstruction: Optional[fhir.markdown] = Field(
        description="Full representation of the dosage instructions",
        default=None,
    )
    dosageInstruction: Optional[ListType[Dosage]] = Field(
        description="How the medication is to be used by the patient or administered by the caregiver",
        default=None,
    )
    substitution: Optional[MedicationDispenseSubstitution] = Field(
        description="Whether a substitution was performed on the dispense",
        default=None,
    )
    eventHistory: Optional[ListType[Reference]] = Field(
        description="A list of relevant lifecycle events",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_mdd_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="whenHandedOver.empty() or whenPrepared.empty() or whenHandedOver >= whenPrepared",
            human="whenHandedOver cannot be before whenPrepared",
            key="mdd-1",
            severity="error",
        )
