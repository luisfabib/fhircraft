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
    Quantity,
    BackboneElement,
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
    actor: Optional[Reference] = Field(
        description="Individual or organization who was performing",
        default=None,
    )

class ImmunizationEducation(BackboneElement):
    """
    Educational material presented to the patient (or guardian) at the time of vaccine administration.
    """

    documentType: Optional[fhir.string] = Field(
        description="Educational material document identifier",
        default=None,
    )
    reference: Optional[fhir.uri] = Field(
        description="Educational material reference pointer",
        default=None,
    )
    publicationDate: Optional[fhir.dateTime] = Field(
        description="Educational material publication date",
        default=None,
    )
    presentationDate: Optional[fhir.dateTime] = Field(
        description="Educational material presentation date",
        default=None,
    )

class ImmunizationReaction(BackboneElement):
    """
    Categorical data indicating that an adverse event is associated in time to an immunization.
    """

    date: Optional[fhir.dateTime] = Field(
        description="When reaction started",
        default=None,
    )
    detail: Optional[Reference] = Field(
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
        description="Vaccine preventatable disease being targetted",
        default=None,
    )
    doseNumberPositiveInt: Optional[fhir.positiveInt] = Field(
        description="Dose number within series",
        default=None,
    )
    doseNumberString: Optional[fhir.string] = Field(
        description="Dose number within series",
        default=None,
    )
    seriesDosesPositiveInt: Optional[fhir.positiveInt] = Field(
        description="Recommended number of doses for immunity",
        default=None,
    )
    seriesDosesString: Optional[fhir.string] = Field(
        description="Recommended number of doses for immunity",
        default=None,
    )

    @property
    def doseNumber(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="doseNumber",
        )

    @property
    def seriesDoses(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="seriesDoses",
        )

    @model_validator(mode="after")
    def doseNumber_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.positiveInt, fhir.string],
            field_name_base="doseNumber",
            required=True,
        )

    @model_validator(mode="after")
    def seriesDoses_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.positiveInt, fhir.string],
            field_name_base="seriesDoses",
            required=False,
        )

class Immunization(DomainResource):
    """
    Describes the event of a patient being administered a vaccine or a record of an immunization as reported by a patient, a clinician or another party.
    """

    _abstract = False
    _type = "Immunization"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Immunization"

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
        description="Business identifier",
        default=None,
    )
    status: Optional[fhir.code] = Field(
        description="completed | entered-in-error | not-done",
        default=None,
    )
    statusReason: Optional[CodeableConcept] = Field(
        description="Reason not done",
        default=None,
    )
    vaccineCode: Optional[CodeableConcept] = Field(
        description="Vaccine product administered",
        default=None,
    )
    patient: Optional[Reference] = Field(
        description="Who was immunized",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="Encounter immunization was part of",
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
    recorded: Optional[fhir.dateTime] = Field(
        description="When the immunization was first captured in the subject\u0027s record",
        default=None,
    )
    primarySource: Optional[fhir.boolean] = Field(
        description="Indicates context the data was recorded in",
        default=None,
    )
    reportOrigin: Optional[CodeableConcept] = Field(
        description="Indicates the source of a secondarily reported record",
        default=None,
    )
    location: Optional[Reference] = Field(
        description="Where immunization occurred",
        default=None,
    )
    manufacturer: Optional[Reference] = Field(
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
    reasonCode: Optional[ListType[CodeableConcept]] = Field(
        description="Why immunization occurred",
        default=None,
    )
    reasonReference: Optional[ListType[Reference]] = Field(
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
    education: Optional[ListType[ImmunizationEducation]] = Field(
        description="Educational material presented to patient",
        default=None,
    )
    programEligibility: Optional[ListType[CodeableConcept]] = Field(
        description="Patient eligibility for a vaccination program",
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
    def FHIR_imm_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("education",),
            expression="documentType.exists() or reference.exists()",
            human="One of documentType or reference SHALL be present",
            key="imm-1",
            severity="error",
        )

    @model_validator(mode="after")
    def occurrence_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.dateTime, fhir.string],
            field_name_base="occurrence",
            required=True,
        )
