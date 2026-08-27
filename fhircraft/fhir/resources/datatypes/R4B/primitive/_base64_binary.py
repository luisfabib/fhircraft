from typing import Annotated, Optional
from pydantic import BeforeValidator, Field

from fhircraft.fhir.resources.base import Base64BinaryBase
from fhircraft.fhir.resources.datatypes.R4B.complex.element import Element


class Base64Binary(Element, Base64BinaryBase):
    """A stream of bytes, base64 encoded."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/base64Binary"
    _type = "base64Binary"
    _kind = "primitive-type"

    value: Optional[str] = Field(
        default=None,
        description="The actual value",
        pattern=r"^(?:[A-Za-z0-9+\/]{4})*(?:[A-Za-z0-9+\/]{2}==|[A-Za-z0-9+\/]{3}=)?$",
    )


base64Binary = Annotated[
    str | Base64Binary, BeforeValidator(Base64Binary.model_validate)
]
