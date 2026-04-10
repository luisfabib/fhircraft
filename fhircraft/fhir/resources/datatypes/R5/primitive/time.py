import re
from datetime import time
from typing import Annotated, Optional
from pydantic import BeforeValidator, Field, field_validator, model_serializer

from fhircraft.fhir.resources.base import TimeBase
from fhircraft.fhir.resources.datatypes.R5.complex.primitive_type import PrimitiveType
from fhircraft.fhir.resources.datatypes import (
    HOUR_REGEX,
    MINUTES_REGEX,
    SECONDS_REGEX,
    TIMEZONE_REGEX,
)

_TIME_PATTERN = (
    rf"^{HOUR_REGEX}(:{MINUTES_REGEX}(:{SECONDS_REGEX}({TIMEZONE_REGEX})?)?)?$"
)


class Time(PrimitiveType, TimeBase):
    """A time during the day."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/time"
    _type = "time"
    _kind = "primitive-type"

    value: Optional[str] = Field(
        default=None,
        description="The actual value",
    )

    @field_validator("value", mode="before")
    @classmethod
    def _parse(cls, v):
        if isinstance(v, time):
            return v.isoformat()
        if isinstance(v, str):
            if not re.match(_TIME_PATTERN, v):
                raise ValueError(f"Invalid Time: {v!r}")
        return v

    @model_serializer
    def serialize_root_value(self):
        if self.value is None:
            return None
        return self.value.replace("+00:00", "Z")


time_ = Annotated[time | Time, BeforeValidator(Time.model_validate)]
