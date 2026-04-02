import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from ..primitive import *

from fhircraft.fhir.resources.datatypes.R4B.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    BackboneElement,
    Period,
    Coding,
    CodeableConcept,
    Reference,
    Duration,
)
from .resource import Resource
from .domain_resource import DomainResource

class EncounterStatusHistory(BackboneElement):
    """
    The status history permits the encounter resource to contain the status history without needing to read through the historical versions of the resource, or even have the server store them.
    """

    status: Optional[Code] = Field(
        description="planned | arrived | triaged | in-progress | onleave | finished | cancelled +",
        default=None,
    )
    period: Optional[Period] = Field(
        description="The time that the episode was in the specified status",
        default=None,
    )

class EncounterClassHistory(BackboneElement):
    """
    The class history permits the tracking of the encounters transitions without needing to go  through the resource history.  This would be used for a case where an admission starts of as an emergency encounter, then transitions into an inpatient scenario. Doing this and not restarting a new encounter ensures that any lab/diagnostic results can more easily follow the patient and not require re-processing and not get lost or cancelled during a kind of discharge from emergency to inpatient.
    """

    class_: Optional[Coding] = Field(
        description="inpatient | outpatient | ambulatory | emergency +",
        default=None,
        alias="class",
    )
    period: Optional[Period] = Field(
        description="The time that the episode was in the specified class",
        default=None,
    )

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
    individual: Optional[Reference] = Field(
        description="Persons involved in the encounter other than the patient",
        default=None,
    )

class EncounterDiagnosis(BackboneElement):
    """
    The list of diagnosis relevant to this encounter.
    """

    condition: Optional[Reference] = Field(
        description="The diagnosis or procedure relevant to the encounter",
        default=None,
    )
    use: Optional[CodeableConcept] = Field(
        description="Role that this diagnosis has within the encounter (e.g. admission, billing, discharge \u2026)",
        default=None,
    )
    rank: Optional[PositiveInt] = Field(
        description="Ranking of the diagnosis (for each role type)",
        default=None,
    )

class EncounterHospitalization(BackboneElement):
    """
    Details about the admission to a healthcare service.
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
        description="The type of hospital re-admission that has occurred (if any). If the value is absent, then this is not identified as a readmission",
        default=None,
    )
    dietPreference: Optional[ListType[CodeableConcept]] = Field(
        description="Diet preferences reported by the patient",
        default=None,
    )
    specialCourtesy: Optional[ListType[CodeableConcept]] = Field(
        description="Special courtesies (VIP, board member)",
        default=None,
    )
    specialArrangement: Optional[ListType[CodeableConcept]] = Field(
        description="Wheelchair, translator, stretcher, etc.",
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
    physicalType: Optional[CodeableConcept] = Field(
        description="The physical type of the location (usually the level in the location hierachy - bed room ward etc.)",
        default=None,
    )
    period: Optional[Period] = Field(
        description="Time period during which the patient was present at the location",
        default=None,
    )

class Encounter(DomainResource):
    """
    An interaction between a patient and healthcare provider(s) for the purpose of providing healthcare service(s) or assessing the health status of a patient.
    """

    _abstract = False
    _type = "Encounter"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Encounter"

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
        description="Identifier(s) by which this encounter is known",
        default=None,
    )
    status: Optional[Code] = Field(
        description="planned | arrived | triaged | in-progress | onleave | finished | cancelled +",
        default=None,
    )
    statusHistory: Optional[ListType[EncounterStatusHistory]] = Field(
        description="List of past encounter statuses",
        default=None,
    )
    class_: Optional[Coding] = Field(
        description="Classification of patient encounter",
        default=None,
        alias="class",
    )
    classHistory: Optional[ListType[EncounterClassHistory]] = Field(
        description="List of past encounter classes",
        default=None,
    )
    type: Optional[ListType[CodeableConcept]] = Field(
        description="Specific type of encounter",
        default=None,
    )
    serviceType: Optional[CodeableConcept] = Field(
        description="Specific type of service",
        default=None,
    )
    priority: Optional[CodeableConcept] = Field(
        description="Indicates the urgency of the encounter",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="The patient or group present at the encounter",
        default=None,
    )
    episodeOfCare: Optional[ListType[Reference]] = Field(
        description="Episode(s) of care that this encounter should be recorded against",
        default=None,
    )
    basedOn: Optional[ListType[Reference]] = Field(
        description="The ServiceRequest that initiated this encounter",
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
    period: Optional[Period] = Field(
        description="The start and end time of the encounter",
        default=None,
    )
    length: Optional[Duration] = Field(
        description="Quantity of time the encounter lasted (less time absent)",
        default=None,
    )
    reasonCode: Optional[ListType[CodeableConcept]] = Field(
        description="Coded reason the encounter takes place",
        default=None,
    )
    reasonReference: Optional[ListType[Reference]] = Field(
        description="Reason the encounter takes place (reference)",
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
    hospitalization: Optional[EncounterHospitalization] = Field(
        description="Details about the admission to a healthcare service",
        default=None,
    )
    location: Optional[ListType[EncounterLocation]] = Field(
        description="List of locations where the patient has been",
        default=None,
    )
    serviceProvider: Optional[Reference] = Field(
        description="The organization (facility) responsible for this encounter",
        default=None,
    )
    partOf: Optional[Reference] = Field(
        description="Another Encounter this encounter is part of",
        default=None,
    )
