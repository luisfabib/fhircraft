from typing import Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *

from .element import Element


class xhtml(Element):
    """
    Primitive Type xhtml
    """

    _type = "xhtml"

    value: Optional[String] = Field(
        description="Actual xhtml",
        default=None,
    )
    value_ext: Optional[Element] = Field(
        description="Placeholder element for value extensions",
        default=None,
        alias="_value",
    )
