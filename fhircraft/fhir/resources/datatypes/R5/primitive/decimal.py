import re
from typing import Optional
from pydantic import Field, field_validator

from fhircraft.fhir.resources.base import FHIRPrimitiveModel
from fhircraft.fhir.resources.datatypes.R5.complex.primitive_type import PrimitiveType

_DECIMAL_PATTERN = r"^-?(0|[1-9][0-9]*)(\.[0-9]+)?([eE][+-]?[0-9]+)?$"


class Decimal(PrimitiveType, FHIRPrimitiveModel):
    """A rational number."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/decimal"
    _type = "decimal"
    _kind = "primitive-type"

    value: Optional[float] = Field(
        default=None,
        description="The actual value",
    )

    @field_validator("value", mode="before")
    @classmethod
    def _parse_decimal(cls, v):
        if isinstance(v, str):
            if not re.match(_DECIMAL_PATTERN, v):
                raise ValueError(f"Invalid decimal string: {v!r}")
            return float(v)
        return v
