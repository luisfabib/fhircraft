import re
from typing import Annotated, Optional
from pydantic import BeforeValidator, Field, field_validator

from fhircraft.fhir.resources.base import IntegerBase
from fhircraft.fhir.resources.datatypes.R5.complex.primitive_type import PrimitiveType
from fhircraft.fhir.resources.datatypes import (
    MIN_SIGNED_32BIT_INT,
    MAX_SIGNED_32BIT_INT,
)

_INTEGER_PATTERN = r"^[0]|[-+]?[1-9][0-9]*$"


class Integer(PrimitiveType, IntegerBase):
    """A signed integer in the range -2,147,483,648..2,147,483,647."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/integer"
    _type = "integer"
    _kind = "primitive-type"

    value: Optional[int] = Field(
        default=None,
        description="The actual value",
    )

    @field_validator("value", mode="before")
    @classmethod
    def _parse_int(cls, v):
        if isinstance(v, str):
            if not re.match(_INTEGER_PATTERN, v):
                raise ValueError(f"Invalid integer string: {v!r}")
            v = int(v)
        if isinstance(v, int) and not isinstance(v, bool):
            if not (MIN_SIGNED_32BIT_INT <= v <= MAX_SIGNED_32BIT_INT):
                raise ValueError(f"Integer {v} out of 32-bit signed range")
        return v


integer = Annotated[int | Integer, BeforeValidator(Integer.model_validate)]
