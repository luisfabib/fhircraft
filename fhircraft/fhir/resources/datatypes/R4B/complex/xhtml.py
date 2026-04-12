from typing import Optional

from pydantic import Field

import fhircraft.fhir.resources.datatypes.R4B.primitive as fhir
from fhircraft.fhir.resources.datatypes.R4B.complex.element import Element


class Xhtml(Element):
    """
    Primitive Type xhtml
    """

    _type = "xhtml"

    value: Optional[fhir.string] = Field(
        description="Actual xhtml",
        default=None,
    )
