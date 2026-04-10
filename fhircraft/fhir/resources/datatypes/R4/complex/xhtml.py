from typing import Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators

import fhircraft.fhir.resources.datatypes.R4.primitive as fhir
from .element import Element


class Xhtml(Element):
    """
    Primitive Type xhtml
    """

    _type = "xhtml"

    value: Optional[fhir.string] = Field(
        description="Actual xhtml",
        default=None,
    )
