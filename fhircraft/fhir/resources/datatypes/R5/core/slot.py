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
    CodeableReference,
    Reference,
)
from .resource import Resource
from .domain_resource import DomainResource


class Slot(DomainResource):
    """
    A slot of time on a schedule that may be available for booking appointments.
    """

    _abstract = False
    _type = "Slot"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Slot"

    identifier: Optional[ListType[Identifier]] = Field(
        description="External Ids for this item",
        default=None,
    )
    serviceCategory: Optional[ListType[CodeableConcept]] = Field(
        description="A broad categorization of the service that is to be performed during this appointment",
        default=None,
    )
    serviceType: Optional[ListType[CodeableReference]] = Field(
        description="The type of appointments that can be booked into this slot (ideally this would be an identifiable service - which is at a location, rather than the location itself). If provided then this overrides the value provided on the Schedule resource",
        default=None,
    )
    specialty: Optional[ListType[CodeableConcept]] = Field(
        description="The specialty of a practitioner that would be required to perform the service requested in this appointment",
        default=None,
    )
    appointmentType: Optional[ListType[CodeableConcept]] = Field(
        description="The style of appointment or patient that may be booked in the slot (not service type)",
        default=None,
    )
    schedule: Reference = Field(
        description="The schedule resource that this slot defines an interval of status information",
    )
    status: fhir.code = Field(
        description="busy | free | busy-unavailable | busy-tentative | entered-in-error",
    )
    start: fhir.instant = Field(
        description="Date/time that the slot is to begin",
    )
    end: fhir.instant = Field(
        description="Date/time that the slot is to conclude",
    )
    overbooked: Optional[fhir.boolean] = Field(
        description="This slot has already been overbooked, appointments are unlikely to be accepted for this time",
        default=None,
    )
    comment: Optional[fhir.string] = Field(
        description="Comments on the slot to describe any extended information. Such as custom constraints on the slot",
        default=None,
    )
