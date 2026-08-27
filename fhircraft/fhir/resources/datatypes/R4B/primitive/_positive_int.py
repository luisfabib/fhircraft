import re
from typing import Annotated, Optional
from pydantic import BeforeValidator, Field, field_validator

from fhircraft.fhir.resources.base import PositiveIntBase
from fhircraft.fhir.resources.datatypes import MAX_SIGNED_32BIT_INT
from ._integer import Integer

_POSITIVE_INT_PATTERN = r"^\+?[1-9][0-9]*$"


class PositiveInt(Integer, PositiveIntBase):
    """An integer with a value greater than 0."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/positiveInt"
    _type = "positiveInt"

    value: Optional[int] = Field(
        default=None,
        description="The actual value",
    )

    @field_validator("value", mode="before")
    @classmethod
    def _parse_int(cls, v):
        if isinstance(v, str):
            if not re.match(_POSITIVE_INT_PATTERN, v):
                raise ValueError(f"Invalid positive integer string: {v!r}")
            v = int(v)
        if isinstance(v, int) and not isinstance(v, bool):
            if not (1 <= v <= MAX_SIGNED_32BIT_INT):
                raise ValueError(
                    f"Integer {v} must be positive and within 32-bit signed range"
                )
        return v


positiveInt = Annotated[int | PositiveInt, BeforeValidator(PositiveInt.model_validate)]
