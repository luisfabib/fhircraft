import re
from datetime import date, datetime
from typing import Annotated, Optional
from pydantic import BeforeValidator, Field, field_validator, model_serializer

from fhircraft.fhir.resources.base import DateBase
from fhircraft.fhir.resources.datatypes.R5.complex.primitive_type import PrimitiveType
from fhircraft.fhir.resources.datatypes import (
    YEAR_REGEX,
    MONTH_REGEX,
    DAY_REGEX,
)

_DATE_PATTERN = rf"^{YEAR_REGEX}(-{MONTH_REGEX}(-{DAY_REGEX})?)?$"
_FULL_DATE_PATTERN = rf"^{YEAR_REGEX}-{MONTH_REGEX}-{DAY_REGEX}$"


class Date(PrimitiveType, DateBase):
    """A date, or partial date."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/date"
    _type = "date"
    _kind = "primitive-type"

    value: Optional[date | str] = Field(
        default=None,
        description="The actual value",
    )

    @field_validator("value", mode="before")
    @classmethod
    def _parse(cls, v):
        if isinstance(v, datetime):
            return v.date()
        if isinstance(v, date):
            return v
        if isinstance(v, str):
            if not re.match(_DATE_PATTERN, v):
                raise ValueError(f"Invalid Date: {v!r}")
            if re.match(_FULL_DATE_PATTERN, v):
                return date.fromisoformat(v)
        return v

    @model_serializer
    def serialize_root_value(self):
        if self.value is None:
            return None
        if isinstance(self.value, date):
            return self.value.isoformat()
        return self.value


date_ = Annotated[date | str | Date, BeforeValidator(Date.model_validate)]
