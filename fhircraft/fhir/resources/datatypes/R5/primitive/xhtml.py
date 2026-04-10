from typing import Annotated, Optional
from pydantic import BeforeValidator, Field

from fhircraft.fhir.resources.base import FHIRXhtml as FHIRXhtmlBase
from fhircraft.fhir.resources.datatypes.R5.complex.primitive_type import PrimitiveType


class FHIRXhtml(PrimitiveType, FHIRXhtmlBase):
    """A string of XHTML content."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/xhtml"
    _type = "xhtml"
    _kind = "primitive-type"

    value: Optional[str] = Field(
        default=None,
        description="The actual value",
    )


Xhtml = Annotated[str | FHIRXhtml, BeforeValidator(FHIRXhtml.model_validate)]
