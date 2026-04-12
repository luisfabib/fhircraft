from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
import fhircraft.fhir.resources.datatypes.R5.primitive as fhir
from fhircraft.fhir.resources.datatypes.R5.complex import Element


class Xhtml(Element):
    """
    Primitive Type xhtml
    """

    _type = "xhtml"

    value: Optional[fhir.string] = Field(
        description="Actual xhtml",
        default=None,
    )
