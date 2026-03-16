from typing import Optional

from pydantic import Field

from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R4B.complex.element import Element


class xhtml(Element):
    """
    Primitive Type xhtml
    """

    _type = "xhtml"

    value: Optional[String] = Field(
        description="Actual xhtml",
        default=None,
    )
