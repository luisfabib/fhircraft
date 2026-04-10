from typing import Annotated, Optional
from pydantic import BeforeValidator, Field

from fhircraft.fhir.resources.base import FHIRBase64Binary as FHIRBase64BinaryBase
from fhircraft.fhir.resources.datatypes.R5.complex.primitive_type import PrimitiveType


class FHIRBase64Binary(PrimitiveType, FHIRBase64BinaryBase):
    """A stream of bytes, base64 encoded."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/base64Binary"
    _type = "base64Binary"
    _kind = "primitive-type"

    value: Optional[str] = Field(
        default=None,
        description="The actual value",
        pattern=r"^(?:[A-Za-z0-9+\/]{4})*(?:[A-Za-z0-9+\/]{2}==|[A-Za-z0-9+\/]{3}=)?$",
    )


Base64Binary = Annotated[
    str | FHIRBase64Binary, BeforeValidator(FHIRBase64Binary.model_validate)
]
