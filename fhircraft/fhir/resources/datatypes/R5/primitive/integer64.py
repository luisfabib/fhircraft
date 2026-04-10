import re
from typing import Annotated, Optional
from pydantic import BeforeValidator, Field, field_validator

from fhircraft.fhir.resources.datatypes import (
    MIN_SIGNED_64BIT_INT,
    MAX_SIGNED_64BIT_INT,
)
from fhircraft.fhir.resources.base import FHIRInteger64 as FHIRInteger64Base
from .integer import FHIRInteger

_INTEGER_PATTERN = r"^[0]|[-+]?[1-9][0-9]*$"


class FHIRInteger64(FHIRInteger, FHIRInteger64Base):
    """A signed 64-bit integer in the range -9,223,372,036,854,775,808..9,223,372,036,854,775,807."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/integer64"
    _type = "integer64"

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
            if not (MIN_SIGNED_64BIT_INT <= v <= MAX_SIGNED_64BIT_INT):
                raise ValueError(f"Integer {v} out of 64-bit signed range")
        return v


Integer64 = Annotated[
    int | FHIRInteger64, BeforeValidator(FHIRInteger64.model_validate)
]
