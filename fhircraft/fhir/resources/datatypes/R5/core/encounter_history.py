from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators


from ..primitive import *
from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Reference,
    Identifier,
    CodeableConcept,
    CodeableReference,
    Period,
    Duration,
    BackboneElement,
)
from .resource import Resource
from .domain_resource import DomainResource

class EncounterHistoryLocation(BackboneElement):
    """
    The location of the patient at this point in the encounter, the multiple cardinality permits de-normalizing the levels of the location hierarchy, such as site/ward/room/bed.
    """

    location: Optional[Reference] = Field(
        description="Location the encounter takes place",
        default=None,
    )
    form: Optional[CodeableConcept] = Field(
        description="The physical type of the location (usually the level in the location hierarchy - bed, room, ward, virtual etc.)",
        default=None,
    )

class EncounterHistory(DomainResource):
    """
    A record of significant events/milestones key data throughout the history of an Encounter
    """

    _abstract = False
    _type = "EncounterHistory"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/EncounterHistory"

    encounter: Optional[Reference] = Field(
        description="The Encounter associated with this set of historic values",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Identifier(s) by which this encounter is known",
        default=None,
    )
    status: Optional[Code] = Field(
        description="planned | in-progress | on-hold | discharged | completed | cancelled | discontinued | entered-in-error | unknown",
        default=None,
    )
    class_: Optional[CodeableConcept] = Field(
        description="Classification of patient encounter",
        default=None,
        alias="class",
    )
    type: Optional[ListType[CodeableConcept]] = Field(
        description="Specific type of encounter",
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
    actualPeriod: Optional[Period] = Field(
        description="The actual start and end time associated with this set of values associated with the encounter",
        default=None,
    )
    plannedStartDate: Optional[DateTime] = Field(
        description="The planned start date/time (or admission date) of the encounter",
        default=None,
    )
    plannedEndDate: Optional[DateTime] = Field(
        description="The planned end date/time (or discharge date) of the encounter",
        default=None,
    )
    length: Optional[Duration] = Field(
        description="Actual quantity of time the encounter lasted (less time absent)",
        default=None,
    )
    location: Optional[ListType[EncounterHistoryLocation]] = Field(
        description="Location of the patient at this point in the encounter",
        default=None,
    )
