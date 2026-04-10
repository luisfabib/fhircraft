import re
from datetime import time
from typing import Annotated, Optional
from pydantic import BeforeValidator, Field, field_validator, model_serializer

from fhircraft.fhir.resources.base import TimeBase
from fhircraft.fhir.resources.datatypes.R4B.complex.element import Element
from fhircraft.fhir.resources.datatypes import (
    HOUR_REGEX,
    MINUTES_REGEX,
    SECONDS_REGEX,
    TIMEZONE_REGEX,
)

_TIME_PATTERN = (
    rf"^{HOUR_REGEX}(:{MINUTES_REGEX}(:{SECONDS_REGEX}({TIMEZONE_REGEX})?)?)?$"
)


class Time(Element, TimeBase):
    """A time during the day."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/time"
    _type = "time"
    _kind = "primitive-type"

    value: Optional[time] = Field(
        default=None,
        description="The actual value",
    )

    @field_validator("value", mode="before")
    @classmethod
    def _parse(cls, v):
        if isinstance(v, time):
            return v
        if isinstance(v, str):
            if not re.match(_TIME_PATTERN, v):
                raise ValueError(f"Invalid Time: {v!r}")
            return time.fromisoformat(v)
        return v

    @model_serializer
    def serialize_root_value(self):
        if self.value is None:
            return None
        return self.value.isoformat()


time_ = Annotated[time | Time, BeforeValidator(Time.model_validate)]
