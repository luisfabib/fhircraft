from typing import Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
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
    system_ext: Optional[Element] = Field(
        description="Placeholder element for system extensions",
        default=None,
        alias="_system",
    )
    version: Optional[String] = Field(
        description="Version of the system - if relevant",
        default=None,
    )
    version_ext: Optional[Element] = Field(
        description="Placeholder element for version extensions",
        default=None,
        alias="_version",
    )
    code: Optional[Code] = Field(
        description="Symbol in syntax defined by the system",
        default=None,
    )
    code_ext: Optional[Element] = Field(
        description="Placeholder element for code extensions",
        default=None,
        alias="_code",
    )
    display: Optional[String] = Field(
        description="Representation defined by the system",
        default=None,
    )
    display_ext: Optional[Element] = Field(
        description="Placeholder element for display extensions",
        default=None,
        alias="_display",
    )
    userSelected: Optional[Boolean] = Field(
        description="If this coding was chosen directly by the user",
        default=None,
    )
    userSelected_ext: Optional[Element] = Field(
        description="Placeholder element for userSelected extensions",
        default=None,
        alias="_userSelected",
    )
