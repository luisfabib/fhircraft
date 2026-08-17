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
    Quantity,
    BackboneElement,
    Annotation,
)
from .resource import Resource
from .domain_resource import DomainResource

class ImmunizationPerformer(BackboneElement):
    """
    Indicates who performed the immunization event.
    """

    function: Optional[CodeableConcept] = Field(
        description="What type of performance was done",
        default=None,
    )
    actor: Reference = Field(
        description="Individual or organization who was performing",
    )

class ImmunizationProgramEligibility(BackboneElement):
    """
    Indicates a patient's eligibility for a funding program.
    """

    program: CodeableConcept = Field(
        description="The program that eligibility is declared for",
    )
    programStatus: CodeableConcept = Field(
        description="The patient\u0027s eligibility status for the program",
    )

class ImmunizationReaction(BackboneElement):
    """
    Categorical data indicating that an adverse event is associated in time to an immunization.
    """

    date: Optional[fhir.dateTime] = Field(
        description="When reaction started",
        default=None,
    )
    manifestation: Optional[CodeableReference] = Field(
        description="Additional information on reaction",
        default=None,
    )
    reported: Optional[fhir.boolean] = Field(
        description="Indicates self-reported reaction",
        default=None,
    )

class ImmunizationProtocolApplied(BackboneElement):
    """
    The protocol (set of recommendations) being followed by the provider who administered the dose.
    """

    series: Optional[fhir.string] = Field(
        description="Name of vaccine series",
        default=None,
    )
    authority: Optional[Reference] = Field(
        description="Who is responsible for publishing the recommendations",
        default=None,
    )
    targetDisease: Optional[ListType[CodeableConcept]] = Field(
        description="Vaccine preventatable disease being targeted",
        default=None,
    )
    doseNumber: fhir.string = Field(
        description="Dose number within series",
    )
    seriesDoses: Optional[fhir.string] = Field(
        description="Recommended number of doses for immunity",
        default=None,
    )

class Immunization(DomainResource):
    """
    Describes the event of a patient being administered a vaccine or a record of an immunization as reported by a patient, a clinician or another party.
    """

    _abstract = False
    _type = "Immunization"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Immunization"

    identifier: Optional[ListType[Identifier]] = Field(
        description="Business identifier",
        default=None,
    )
    basedOn: Optional[ListType[Reference]] = Field(
        description="Authority that the immunization event is based on",
        default=None,
    )
    status: fhir.code = Field(
        description="completed | entered-in-error | not-done",
    )
    statusReason: Optional[CodeableConcept] = Field(
        description="Reason for current status",
        default=None,
    )
    vaccineCode: CodeableConcept = Field(
        description="Vaccine administered",
    )
    administeredProduct: Optional[CodeableReference] = Field(
        description="Product that was administered",
        default=None,
    )
    manufacturer: Optional[CodeableReference] = Field(
        description="Vaccine manufacturer",
        default=None,
    )
    lotNumber: Optional[fhir.string] = Field(
        description="Vaccine lot number",
        default=None,
    )
    expirationDate: Optional[fhir.date_] = Field(
        description="Vaccine expiration date",
        default=None,
    )
    patient: Reference = Field(
        description="Who was immunized",
    )
    encounter: Optional[Reference] = Field(
        description="Encounter immunization was part of",
        default=None,
    )
    supportingInformation: Optional[ListType[Reference]] = Field(
        description="Additional information in support of the immunization",
        default=None,
    )
    occurrenceDateTime: Optional[fhir.dateTime] = Field(
        description="Vaccine administration date",
        default=None,
    )
    occurrenceString: Optional[fhir.string] = Field(
        description="Vaccine administration date",
        default=None,
    )
    primarySource: Optional[fhir.boolean] = Field(
        description="Indicates context the data was captured in",
        default=None,
    )
    informationSource: Optional[CodeableReference] = Field(
        description="Indicates the source of a  reported record",
        default=None,
    )
    location: Optional[Reference] = Field(
        description="Where immunization occurred",
        default=None,
    )
    site: Optional[CodeableConcept] = Field(
        description="Body site vaccine  was administered",
        default=None,
    )
    route: Optional[CodeableConcept] = Field(
        description="How vaccine entered body",
        default=None,
    )
    doseQuantity: Optional[Quantity] = Field(
        description="Amount of vaccine administered",
        default=None,
    )
    performer: Optional[ListType[ImmunizationPerformer]] = Field(
        description="Who performed event",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Additional immunization notes",
        default=None,
    )
    reason: Optional[ListType[CodeableReference]] = Field(
        description="Why immunization occurred",
        default=None,
    )
    isSubpotent: Optional[fhir.boolean] = Field(
        description="Dose potency",
        default=None,
    )
    subpotentReason: Optional[ListType[CodeableConcept]] = Field(
        description="Reason for being subpotent",
        default=None,
    )
    programEligibility: Optional[ListType[ImmunizationProgramEligibility]] = Field(
        description="Patient eligibility for a specific vaccination program",
        default=None,
    )
    fundingSource: Optional[CodeableConcept] = Field(
        description="Funding source for the vaccine",
        default=None,
    )
    reaction: Optional[ListType[ImmunizationReaction]] = Field(
        description="Details of a reaction that follows immunization",
        default=None,
    )
    protocolApplied: Optional[ListType[ImmunizationProtocolApplied]] = Field(
        description="Protocol followed by the provider",
        default=None,
    )

    @property
    def occurrence(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="occurrence",
        )

    @model_validator(mode="after")
    def occurrence_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.DateTime, fhir.String],
            field_name_base="occurrence",
            required=True,
        )
