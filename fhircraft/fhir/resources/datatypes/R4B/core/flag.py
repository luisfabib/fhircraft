import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)


import fhircraft.fhir.resources.datatypes.R4B.primitive as fhir
from fhircraft.fhir.resources.datatypes.R4B.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    Period,
)
from .resource import Resource
from .domain_resource import DomainResource


class Flag(DomainResource):
    """
    Prospective warnings of potential issues when providing care to the patient.
    """

    _abstract = False
    _type = "Flag"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Flag"

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
    status: fhir.code = Field(
        description="active | inactive | entered-in-error",
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description="Clinical, administrative, etc.",
        default=None,
    )
    code: CodeableConcept = Field(
        description="Coded or textual message to display to user",
    )
    subject: Reference = Field(
        description="Who/What is flag about?",
    )
    period: Optional[Period] = Field(
        description="time period when flag is active",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="Alert relevant during encounter",
        default=None,
    )
    author: Optional[Reference] = Field(
        description="Flag creator",
        default=None,
    )
