from typing import Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from ..primitive import *

from .codeable_concept import CodeableConcept
from .element import Element
from .period import Period
from .reference import Reference

class Identifier(Element):
    """
    An identifier intended for computation
    """

    _type = "Identifier"

    use: Optional[Code] = Field(
        description="usual | official | temp | secondary | old (If known)",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Description of identifier",
        default=None,
    )
    system: Optional[Uri] = Field(
        description="The namespace for the identifier value",
        default=None,
    )
    value: Optional[String] = Field(
        description="The value that is unique",
        default=None,
    )
    period: Optional[Period] = Field(
        description="Time period when id is/was valid for use",
        default=None,
    )
    assigner: Optional[Reference] = Field(
        description="Organization that issued id (may be just text)",
        default=None,
    )
