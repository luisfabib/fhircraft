from typing import Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from ..primitive import *
from fhircraft.fhir.resources.datatypes.R4.complex import Element

class Coding(Element):
    """
    A reference to a code defined by a terminology system
    """

    _type = "Coding"

    system: Optional[Uri] = Field(
        description="Identity of the terminology system",
        default=None,
    )
    version: Optional[String] = Field(
        description="Version of the system - if relevant",
        default=None,
    )
    code: Optional[Code] = Field(
        description="Symbol in syntax defined by the system",
        default=None,
    )
    display: Optional[String] = Field(
        description="Representation defined by the system",
        default=None,
    )
    userSelected: Optional[Boolean] = Field(
        description="If this coding was chosen directly by the user",
        default=None,
    )
