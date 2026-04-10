from typing import Annotated, Any, Optional
from pydantic import BeforeValidator, Field

from fhircraft.fhir.resources.base import StringBase
from fhircraft.fhir.resources.datatypes.R5.complex.primitive_type import PrimitiveType


class String(PrimitiveType, StringBase):
    """A sequence of Unicode characters."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/string"
    _type = "string"
    _kind = "primitive-type"

    value: Optional[str] = Field(
        default=None,
        description="The actual string value.",
    )


string = Annotated[str | String, BeforeValidator(String.model_validate)]
