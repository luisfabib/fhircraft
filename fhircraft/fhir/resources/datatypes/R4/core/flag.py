import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from ..primitive import *

from fhircraft.fhir.resources.datatypes.R4.complex import (
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
    status: Optional[Code] = Field(
        description="active | inactive | entered-in-error",
        default=None,
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description="Clinical, administrative, etc.",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="Coded or textual message to display to user",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="Who/What is flag about?",
        default=None,
    )
    period: Optional[Period] = Field(
        description="Time period when flag is active",
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
