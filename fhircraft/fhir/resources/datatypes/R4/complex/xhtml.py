from typing import Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators

from ..primitive import *
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
