import re
from datetime import date, datetime
from typing import Annotated, Optional
from pydantic import BeforeValidator, Field, field_validator, model_serializer

from fhircraft.fhir.resources.base import DateTimeBase
from fhircraft.fhir.resources.datatypes.R5.complex.primitive_type import PrimitiveType
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


class DateTime(PrimitiveType, DateTimeBase):
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
        if isinstance(v, date):
            return v.isoformat()
        if isinstance(v, str):
            if not re.match(_DATETIME_PATTERN, v):
                raise ValueError(f"Invalid DateTime: {v!r}")
            if "T" in v:
                _v = v.replace("Z", "+00:00")
                return _v
            if re.match(_FULL_DATE_PATTERN, v):
                return v
        return v

    @model_serializer
    def serialize_root_value(self):
        if self.value is None:
            return None
        return self.value.replace("+00:00", "Z")


dateTime = Annotated[
    datetime | date | str | DateTime, BeforeValidator(DateTime.model_validate)
]
