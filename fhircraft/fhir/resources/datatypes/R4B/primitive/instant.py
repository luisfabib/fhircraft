import re
from datetime import datetime
from typing import Annotated, Optional
from pydantic import BeforeValidator, Field, field_validator, model_serializer

from fhircraft.fhir.resources.base import InstantBase
from fhircraft.fhir.resources.datatypes.R4B.complex.element import Element
from fhircraft.fhir.resources.datatypes import (
    YEAR_REGEX,
    MONTH_REGEX,
    DAY_REGEX,
    HOUR_REGEX,
    MINUTES_REGEX,
    SECONDS_REGEX,
    TIMEZONE_REGEX,
)

_INSTANT_PATTERN = (
    rf"^{YEAR_REGEX}-{MONTH_REGEX}-{DAY_REGEX}"
    rf"T{HOUR_REGEX}:{MINUTES_REGEX}:{SECONDS_REGEX}({TIMEZONE_REGEX})?$"
)


class Instant(Element, InstantBase):
    """An instant in time in the format YYYY-MM-DDThh:mm:ss.sss+zz:zz."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/instant"
    _type = "instant"
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
        if isinstance(v, str):
            if not re.match(_INSTANT_PATTERN, v):
                raise ValueError(f"Invalid Instant: {v!r}")
            return v
        return v

    @model_serializer
    def serialize_root_value(self):
        if self.value is None:
            return None
        return self.value


instant = Annotated[datetime | Instant, BeforeValidator(Instant.model_validate)]
