from typing import Annotated, Optional
from pydantic import BeforeValidator, Field

from fhircraft.fhir.resources.base import XhtmlBase
from fhircraft.fhir.resources.datatypes.R4B.complex.element import Element


class Xhtml(Element, XhtmlBase):
    """A string of XHTML content."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/xhtml"
    _type = "xhtml"
    _kind = "primitive-type"

    value: Optional[str] = Field(
        default=None,
        description="The actual value",
    )


xhtml = Annotated[str | Xhtml, BeforeValidator(Xhtml.model_validate)]
