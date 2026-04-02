import re
from datetime import date, datetime
from typing import Optional
from pydantic import Field, field_validator

from fhircraft.fhir.resources.base import FHIRPrimitiveModel
from fhircraft.fhir.resources.datatypes.R4.complex.element import Element
from fhircraft.fhir.resources.datatypes import (
    YEAR_REGEX,
    MONTH_REGEX,
    DAY_REGEX,
)

_DATE_PATTERN = rf"^{YEAR_REGEX}(-{MONTH_REGEX}(-{DAY_REGEX})?)?$"


class Date(Element, FHIRPrimitiveModel):
    """A date, or partial date."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/date"
    _type = "date"
    _kind = "primitive-type"

    value: Optional[str] = Field(
        default=None,
        description="The actual value",
    )

    @field_validator("value", mode="before")
    @classmethod
    def _parse(cls, v):
        if isinstance(v, datetime):
            return v.date().isoformat()
        if isinstance(v, date):
            return v.isoformat()
        if isinstance(v, str) and not re.match(_DATE_PATTERN, v):
            raise ValueError(f"Invalid Date: {v!r}")
        return v
