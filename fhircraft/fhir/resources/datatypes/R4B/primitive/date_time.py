import re
from datetime import datetime
from typing import Optional
from pydantic import Field, field_validator

from fhircraft.fhir.resources.base import FHIRPrimitiveModel
from fhircraft.fhir.resources.datatypes.R4B.complex import Element
from fhircraft.fhir.resources.datatypes import (
    YEAR_REGEX,
    MONTH_REGEX,
    DAY_REGEX,
    HOUR_REGEX,
    MINUTES_REGEX,
    SECONDS_REGEX,
    TIMEZONE_REGEX,
)

_DATETIME_PATTERN = (
    rf"^{YEAR_REGEX}(-{MONTH_REGEX}(-{DAY_REGEX})?)?"
    rf"(T{HOUR_REGEX}(:{MINUTES_REGEX}(:{SECONDS_REGEX}({TIMEZONE_REGEX})?)?)?)?$"
)


class DateTime(Element, FHIRPrimitiveModel):
    """A date, date-time or partial date."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/dateTime"
    _type = "dateTime"
    _kind = "primitive-type"

    value: Optional[str] = Field(
        default=None,
        description="The actual value",
    )

    @field_validator("value", mode="before")
    @classmethod
    def _parse(cls, v):
        if isinstance(v, datetime):
            return v.isoformat()
        if isinstance(v, str) and not re.match(_DATETIME_PATTERN, v):
            raise ValueError(f"Invalid DateTime: {v!r}")
        return v
