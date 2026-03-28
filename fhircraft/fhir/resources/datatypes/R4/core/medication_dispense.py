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
    Reference,
    Dosage,
    CodeableConcept,
    BackboneElement,
    Quantity,
    Annotation,
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
    actor: Optional[Reference] = Field(
        description="Individual who was performing",
        default=None,
    )


class MedicationDispenseSubstitution(BackboneElement):
    """
    Indicates whether or not substitution was made as part of the dispense.  In some cases, substitution will be expected but does not happen, in other cases substitution is not expected but does happen.  This block explains what substitution did or did not happen and why.  If nothing is specified, substitution was not done.
    """

    wasSubstituted: Optional[Boolean] = Field(
        description="Whether a substitution was or was not performed on the dispense",
        default=None,
    )
    wasSubstituted_ext: Optional[Element] = Field(
        description="Placeholder element for wasSubstituted extensions",
        default=None,
        alias="_wasSubstituted",
    )
    type: Optional[CodeableConcept] = Field(
        description="Code signifying whether a different drug was dispensed from what was prescribed",
        default=None,
    )
    reason: Optional[ListType[CodeableConcept]] = Field(
        description="Why was substitution made",
        default=None,
    )
    responsibleParty: Optional[ListType[Reference]] = Field(
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
        description="External identifier",
        default=None,
    )
    partOf: Optional[ListType[Reference]] = Field(
        description="Event that dispense is part of",
        default=None,
    )
    status: Optional[Code] = Field(
        description="preparation | in-progress | cancelled | on-hold | completed | entered-in-error | stopped | declined | unknown",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    statusReasonCodeableConcept: Optional[CodeableConcept] = Field(
        description="Why a dispense was not performed",
        default=None,
    )
    statusReasonReference: Optional[Reference] = Field(
        description="Why a dispense was not performed",
        default=None,
    )
    category: Optional[CodeableConcept] = Field(
        description="Type of medication dispense",
        default=None,
    )
    medicationCodeableConcept: Optional[CodeableConcept] = Field(
        description="What medication was supplied",
        default=None,
    )
    medicationReference: Optional[Reference] = Field(
        description="What medication was supplied",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="Who the dispense is for",
        default=None,
    )
    context: Optional[Reference] = Field(
        description="Encounter / Episode associated with event",
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
        description="Trial fill, partial fill, emergency fill, etc.",
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
    whenPrepared: Optional[DateTime] = Field(
        description="When product was packaged and reviewed",
        default=None,
    )
    whenPrepared_ext: Optional[Element] = Field(
        description="Placeholder element for whenPrepared extensions",
        default=None,
        alias="_whenPrepared",
    )
    whenHandedOver: Optional[DateTime] = Field(
        description="When product was given out",
        default=None,
    )
    whenHandedOver_ext: Optional[Element] = Field(
        description="Placeholder element for whenHandedOver extensions",
        default=None,
        alias="_whenHandedOver",
    )
    destination: Optional[Reference] = Field(
        description="Where the medication was sent",
        default=None,
    )
    receiver: Optional[ListType[Reference]] = Field(
        description="Who collected the medication",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Information about the dispense",
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
    detectedIssue: Optional[ListType[Reference]] = Field(
        description="Clinical issue with action",
        default=None,
    )
    eventHistory: Optional[ListType[Reference]] = Field(
        description="A list of relevant lifecycle events",
        default=None,
    )

    @property
    def statusReason(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="statusReason",
        )

    @property
    def medication(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="medication",
        )

    @model_validator(mode="after")
    def statusReason_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[CodeableConcept, Reference],
            field_name_base="statusReason",
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

    @model_validator(mode="after")
    def FHIR_mdd_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="whenHandedOver.empty() or whenPrepared.empty() or whenHandedOver >= whenPrepared",
            human="whenHandedOver cannot be before whenPrepared",
            key="mdd-1",
            severity="error",
        )
