from typing import Optional
from pydantic import Field

from fhircraft.fhir.resources.base import FHIRPrimitiveModel
from fhircraft.fhir.resources.datatypes.R4.complex import Element


class Xhtml(Element, FHIRPrimitiveModel):
    """A string of XHTML content."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/xhtml"
    _type = "xhtml"
    _kind = "primitive-type"

    value: Optional[str] = Field(
        default=None,
        description="The actual value",
    )
