import re
from datetime import date, datetime
from typing import Annotated, Optional
from pydantic import BeforeValidator, Field, field_validator, model_serializer

from fhircraft.fhir.resources.base import DateTimeBase
from fhircraft.fhir.resources.datatypes.R4.complex.element import Element
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
_FULL_DATE_PATTERN = rf"^{YEAR_REGEX}-{MONTH_REGEX}-{DAY_REGEX}$"
_FULL_DATETIME_PATTERN = (
    rf"^{YEAR_REGEX}-{MONTH_REGEX}-{DAY_REGEX}"
    rf"T{HOUR_REGEX}:{MINUTES_REGEX}:{SECONDS_REGEX}({TIMEZONE_REGEX})?$"
)


class DateTime(Element, DateTimeBase):
    """A date, date-time or partial date."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/dateTime"
    _type = "dateTime"
    _kind = "primitive-type"

    value: Optional[datetime | date | str] = Field(
        default=None,
        description="The actual value",
    )

    @field_validator("value", mode="before")
    @classmethod
    def _parse(cls, v):
        if isinstance(v, datetime):
            return v
        if isinstance(v, date):
            return v
        if isinstance(v, str):
            if not re.match(_DATETIME_PATTERN, v):
                raise ValueError(f"Invalid DateTime: {v!r}")
            if "T" in v:
                _v = v.replace("Z", "+00:00")
                return datetime.fromisoformat(_v)
            if re.match(_FULL_DATE_PATTERN, v):
                return date.fromisoformat(v)
        return v

    @model_serializer
    def serialize_root_value(self):
        if self.value is None:
            return None
        if isinstance(self.value, datetime):
            s = self.value.isoformat()
            if "." in s:
                s = s.rstrip("0").rstrip(".")
            return s
        if isinstance(self.value, date):
            return self.value.isoformat()
        return self.value


dateTime = Annotated[
    datetime | date | str | DateTime, BeforeValidator(DateTime.model_validate)
]
