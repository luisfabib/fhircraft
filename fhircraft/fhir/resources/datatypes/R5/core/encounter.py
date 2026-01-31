from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from fhircraft.fhir.resources.datatypes.primitives import String, Uri, Code, DateTime

from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    CodeableConcept,
    CodeableReference,
    Reference,
    BackboneElement,
    Period,
    VirtualServiceDetail,
    Duration,
)
from .resource import Resource
from .domain_resource import DomainResource


class EncounterParticipant(BackboneElement):
    """
    The list of people responsible for providing the service.
    """

    type: Optional[ListType[CodeableConcept]] = Field(
        description="Role of participant in encounter",
        default=None,
    )
    period: Optional[Period] = Field(
        description="Period of time during the encounter that the participant participated",
        default=None,
    )
    actor: Optional[Reference] = Field(
        description="The individual, device, or service participating in the encounter",
        default=None,
    )


class EncounterReason(BackboneElement):
    """
    The list of medical reasons that are expected to be addressed during the episode of care.
    """

    use: Optional[ListType[CodeableConcept]] = Field(
        description="What the reason value should be used for/as",
        default=None,
    )
    value: Optional[ListType[CodeableReference]] = Field(
        description="Reason the encounter takes place (core or reference)",
        default=None,
    )


class EncounterDiagnosis(BackboneElement):
    """
    The list of diagnosis relevant to this encounter.
    """

    condition: Optional[ListType[CodeableReference]] = Field(
        description="The diagnosis relevant to the encounter",
        default=None,
    )
    use: Optional[ListType[CodeableConcept]] = Field(
        description="Role that this diagnosis has within the encounter (e.g. admission, billing, discharge \u2026)",
        default=None,
    )


class EncounterAdmission(BackboneElement):
    """
        Details about the stay during which a healthcare service is provided.

    This does not describe the event of admitting the patient, but rather any information that is relevant from the time of admittance until the time of discharge.
    """

    preAdmissionIdentifier: Optional[Identifier] = Field(
        description="Pre-admission identifier",
        default=None,
    )
    origin: Optional[Reference] = Field(
        description="The location/organization from which the patient came before admission",
        default=None,
    )
    admitSource: Optional[CodeableConcept] = Field(
        description="From where patient was admitted (physician referral, transfer)",
        default=None,
    )
    reAdmission: Optional[CodeableConcept] = Field(
        description="Indicates that the patient is being re-admitted",
        default=None,
    )
    destination: Optional[Reference] = Field(
        description="Location/organization to which the patient is discharged",
        default=None,
    )
    dischargeDisposition: Optional[CodeableConcept] = Field(
        description="Category or kind of location after discharge",
        default=None,
    )


class EncounterLocation(BackboneElement):
    """
    List of locations where  the patient has been during this encounter.
    """

    location: Optional[Reference] = Field(
        description="Location the encounter takes place",
        default=None,
    )
    status: Optional[Code] = Field(
        description="planned | active | reserved | completed",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    form: Optional[CodeableConcept] = Field(
        description="The physical type of the location (usually the level in the location hierarchy - bed, room, ward, virtual etc.)",
        default=None,
    )
    period: Optional[Period] = Field(
        description="Time period during which the patient was present at the location",
        default=None,
    )


class Encounter(DomainResource):
    """
    An interaction between healthcare provider(s), and/or patient(s) for the purpose of providing healthcare service(s) or assessing the health status of patient(s).
    """

    _abstract = False
    _type = "Encounter"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Encounter"

    identifier: Optional[ListType[Identifier]] = Field(
        description="Identifier(s) by which this encounter is known",
        default=None,
    )
    status: Optional[Code] = Field(
        description="planned | in-progress | on-hold | discharged | completed | cancelled | discontinued | entered-in-error | unknown",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    class_: Optional[ListType[CodeableConcept]] = Field(
        description="Classification of patient encounter context - e.g. Inpatient, outpatient",
        default=None,
        alias="class",
    )
    priority: Optional[CodeableConcept] = Field(
        description="Indicates the urgency of the encounter",
        default=None,
    )
    type: Optional[ListType[CodeableConcept]] = Field(
        description="Specific type of encounter (e.g. e-mail consultation, surgical day-care, ...)",
        default=None,
    )
    serviceType: Optional[ListType[CodeableReference]] = Field(
        description="Specific type of service",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="The patient or group related to this encounter",
        default=None,
    )
    subjectStatus: Optional[CodeableConcept] = Field(
        description="The current status of the subject in relation to the Encounter",
        default=None,
    )
    episodeOfCare: Optional[ListType[Reference]] = Field(
        description="Episode(s) of care that this encounter should be recorded against",
        default=None,
    )
    basedOn: Optional[ListType[Reference]] = Field(
        description="The request that initiated this encounter",
        default=None,
    )
    careTeam: Optional[ListType[Reference]] = Field(
        description="The group(s) that are allocated to participate in this encounter",
        default=None,
    )
    partOf: Optional[Reference] = Field(
        description="Another Encounter this encounter is part of",
        default=None,
    )
    serviceProvider: Optional[Reference] = Field(
        description="The organization (facility) responsible for this encounter",
        default=None,
    )
    participant: Optional[ListType[EncounterParticipant]] = Field(
        description="List of participants involved in the encounter",
        default=None,
    )
    appointment: Optional[ListType[Reference]] = Field(
        description="The appointment that scheduled this encounter",
        default=None,
    )
    virtualService: Optional[ListType[VirtualServiceDetail]] = Field(
        description="Connection details of a virtual service (e.g. conference call)",
        default=None,
    )
    actualPeriod: Optional[Period] = Field(
        description="The actual start and end time of the encounter",
        default=None,
    )
    plannedStartDate: Optional[DateTime] = Field(
        description="The planned start date/time (or admission date) of the encounter",
        default=None,
    )
    plannedStartDate_ext: Optional[Element] = Field(
        description="Placeholder element for plannedStartDate extensions",
        default=None,
        alias="_plannedStartDate",
    )
    plannedEndDate: Optional[DateTime] = Field(
        description="The planned end date/time (or discharge date) of the encounter",
        default=None,
    )
    plannedEndDate_ext: Optional[Element] = Field(
        description="Placeholder element for plannedEndDate extensions",
        default=None,
        alias="_plannedEndDate",
    )
    length: Optional[Duration] = Field(
        description="Actual quantity of time the encounter lasted (less time absent)",
        default=None,
    )
    reason: Optional[ListType[EncounterReason]] = Field(
        description="The list of medical reasons that are expected to be addressed during the episode of care",
        default=None,
    )
    diagnosis: Optional[ListType[EncounterDiagnosis]] = Field(
        description="The list of diagnosis relevant to this encounter",
        default=None,
    )
    account: Optional[ListType[Reference]] = Field(
        description="The set of accounts that may be used for billing for this Encounter",
        default=None,
    )
    dietPreference: Optional[ListType[CodeableConcept]] = Field(
        description="Diet preferences reported by the patient",
        default=None,
    )
    specialArrangement: Optional[ListType[CodeableConcept]] = Field(
        description="Wheelchair, translator, stretcher, etc",
        default=None,
    )
    specialCourtesy: Optional[ListType[CodeableConcept]] = Field(
        description="Special courtesies (VIP, board member)",
        default=None,
    )
    admission: Optional[EncounterAdmission] = Field(
        description="Details about the admission to a healthcare service",
        default=None,
    )
    location: Optional[ListType[EncounterLocation]] = Field(
        description="List of locations where the patient has been",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_enc_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("participant",),
            expression="actor.exists() or type.exists()",
            human="A type must be provided when no explicit actor is specified",
            key="enc-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_enc_2_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("participant",),
            expression="actor.exists(resolve() is Patient or resolve() is Group) implies type.exists().not()",
            human="A type cannot be provided for a patient or group participant",
            key="enc-2",
            severity="error",
        )
