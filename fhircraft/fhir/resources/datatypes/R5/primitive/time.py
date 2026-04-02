import re
from datetime import time
from typing import Optional
from pydantic import Field, field_validator

from fhircraft.fhir.resources.base import FHIRPrimitiveModel
from fhircraft.fhir.resources.datatypes.R5.complex import PrimitiveType
from fhircraft.fhir.resources.datatypes import (
    HOUR_REGEX,
    MINUTES_REGEX,
    SECONDS_REGEX,
    TIMEZONE_REGEX,
)

_TIME_PATTERN = (
    rf"^{HOUR_REGEX}(:{MINUTES_REGEX}(:{SECONDS_REGEX}({TIMEZONE_REGEX})?)?)?$"
)


class Time(PrimitiveType, FHIRPrimitiveModel):
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
        if isinstance(v, str) and not re.match(_TIME_PATTERN, v):
            raise ValueError(f"Invalid Time: {v!r}")
        return v
