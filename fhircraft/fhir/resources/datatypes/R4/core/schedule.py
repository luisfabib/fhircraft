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
    Period,
    Reference,
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
    serviceType: Optional[ListType[CodeableConcept]] = Field(
        description="Specific service",
        default=None,
    )
    specialty: Optional[ListType[CodeableConcept]] = Field(
        description="Type of specialty needed",
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
    comment: Optional[fhir.string] = Field(
        description="Comments on availability",
        default=None,
    )
