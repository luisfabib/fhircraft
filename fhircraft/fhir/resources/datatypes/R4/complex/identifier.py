from typing import Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators

import fhircraft.fhir.resources.datatypes.R4.primitive as fhir
from .codeable_concept import CodeableConcept
from .element import Element
from .period import Period
from .reference import Reference

class Identifier(Element):
    """
    An identifier intended for computation
    """

    _type = "Identifier"

    use: Optional[fhir.code] = Field(
        description="usual | official | temp | secondary | old (If known)",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Description of identifier",
        default=None,
    )
    system: Optional[fhir.uri] = Field(
        description="The namespace for the identifier value",
        default=None,
    )
    value: Optional[fhir.string] = Field(
        description="The value that is unique",
        default=None,
    )
    period: Optional[Period] = Field(
        description="time period when id is/was valid for use",
        default=None,
    )
    assigner: Optional[Reference] = Field(
        description="Organization that issued id (may be just text)",
        default=None,
    )
