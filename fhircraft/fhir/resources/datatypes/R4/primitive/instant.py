import re
from datetime import datetime
from typing import Optional
from pydantic import Field, field_validator

from fhircraft.fhir.resources.base import FHIRPrimitiveModel
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

_INSTANT_PATTERN = (
    rf"^{YEAR_REGEX}-{MONTH_REGEX}-{DAY_REGEX}"
    rf"T{HOUR_REGEX}:{MINUTES_REGEX}:{SECONDS_REGEX}({TIMEZONE_REGEX})?$"
)


class Instant(Element, FHIRPrimitiveModel):
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
        if isinstance(v, str) and not re.match(_INSTANT_PATTERN, v):
            raise ValueError(f"Invalid Instant: {v!r}")
        return v
