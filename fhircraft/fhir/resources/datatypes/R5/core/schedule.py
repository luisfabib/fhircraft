from pydantic import Field, model_validator
from typing import Optional, List

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    Boolean,
    Markdown,
)

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

    identifier: Optional[List[Identifier]] = Field(
        description="External Ids for this item",
        default=None,
    )
    active: Optional[Boolean] = Field(
        description="Whether this schedule is in active use",
        default=None,
    )
    active_ext: Optional[Element] = Field(
        description="Placeholder element for active extensions",
        default=None,
        alias="_active",
    )
    serviceCategory: Optional[List[CodeableConcept]] = Field(
        description="High-level category",
        default=None,
    )
    serviceType: Optional[List[CodeableReference]] = Field(
        description="Specific service",
        default=None,
    )
    specialty: Optional[List[CodeableConcept]] = Field(
        description="Type of specialty needed",
        default=None,
    )
    name: Optional[String] = Field(
        description="Human-readable label",
        default=None,
    )
    name_ext: Optional[Element] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    actor: Optional[List[Reference]] = Field(
        description="Resource(s) that availability information is being provided for",
        default=None,
    )
    planningHorizon: Optional[Period] = Field(
        description="Period of time covered by schedule",
        default=None,
    )
    comment: Optional[Markdown] = Field(
        description="Comments on availability",
        default=None,
    )
    comment_ext: Optional[Element] = Field(
        description="Placeholder element for comment extensions",
        default=None,
        alias="_comment",
    )
