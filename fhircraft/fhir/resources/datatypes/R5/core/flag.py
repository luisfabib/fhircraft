from pydantic import Field, model_validator
from typing import Optional, List

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from fhircraft.fhir.resources.datatypes.primitives import String, Uri, Code

from fhircraft.fhir.resources.datatypes.R5.complex import (
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

    identifier: Optional[List[Identifier]] = Field(
        description="Business identifier",
        default=None,
    )
    status: Optional[Code] = Field(
        description="active | inactive | entered-in-error",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    category: Optional[List[CodeableConcept]] = Field(
        description="Clinical, administrative, etc",
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
