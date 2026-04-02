import re
from typing import Optional
from pydantic import Field, field_validator

from fhircraft.fhir.resources.datatypes import (
    MIN_UNSIGNED_32BIT_INT,
    MAX_UNSIGNED_32BIT_INT,
)
from .integer import Integer

_UNSIGNED_INT_PATTERN = r"^[0]|([1-9][0-9]*)$"


class UnsignedInt(Integer):
    """An integer with a value in the range 0..2,147,483,647."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/unsignedInt"
    _type = "unsignedInt"

    value: Optional[int] = Field(
        default=None,
        description="The actual value",
    )

    @field_validator("value", mode="before")
    @classmethod
    def _parse_int(cls, v):
        if isinstance(v, str):
            if not re.match(_UNSIGNED_INT_PATTERN, v):
                raise ValueError(f"Invalid unsigned integer string: {v!r}")
            v = int(v)
        if isinstance(v, int) and not isinstance(v, bool):
            if not (MIN_UNSIGNED_32BIT_INT <= v <= MAX_UNSIGNED_32BIT_INT):
                raise ValueError(f"Integer {v} out of unsigned 32-bit range")
        return v
