from typing import Optional
from pydantic import Field

from fhircraft.fhir.resources.base import FHIRPrimitiveModel
from fhircraft.fhir.resources.datatypes.R5.complex.primitive_type import PrimitiveType


class Base64Binary(PrimitiveType, FHIRPrimitiveModel):
    """A stream of bytes, base64 encoded."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/base64Binary"
    _type = "base64Binary"
    _kind = "primitive-type"

    value: Optional[str] = Field(
        default=None,
        description="The actual value",
        pattern=r"^(?:[A-Za-z0-9+\/]{4})*(?:[A-Za-z0-9+\/]{2}==|[A-Za-z0-9+\/]{3}=)?$",
    )
