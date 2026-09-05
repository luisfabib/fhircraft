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
    Period,
)
from .resource import Resource
from .domain_resource import DomainResource


class Schedule(DomainResource):
    """
    A container for slots of time that may be available for booking appointments.
    """

    _abstract = False
    _type = "Schedule"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Schedule"

    identifier: Optional[ListType[Identifier]] = Field(
        description="External Ids for this item",
        default=None,
    )
    active: Optional[fhir.boolean] = Field(
        description="Whether this schedule is in active use",
        default=None,
    )
    serviceCategory: Optional[ListType[CodeableConcept]] = Field(
        description="High-level category",
        default=None,
    )
    serviceType: Optional[ListType[CodeableReference]] = Field(
        description="Specific service",
        default=None,
    )
    specialty: Optional[ListType[CodeableConcept]] = Field(
        description="Type of specialty needed",
        default=None,
    )
    name: Optional[fhir.string] = Field(
        description="Human-readable label",
        default=None,
    )
    actor: ListType[Reference] = Field(
        description="Resource(s) that availability information is being provided for",
        min_length=1,
    )
    planningHorizon: Optional[Period] = Field(
        description="Period of time covered by schedule",
        default=None,
    )
    comment: Optional[fhir.markdown] = Field(
        description="Comments on availability",
        default=None,
    )
