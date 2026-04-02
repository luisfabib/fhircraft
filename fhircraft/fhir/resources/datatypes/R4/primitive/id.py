from typing import Optional
from pydantic import Field

from .string import String


class Id(String):
    """Any combination of letters, numerals, '-' and '.', with a length limit of 64 characters."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/id"
    _type = "id"

    value: Optional[str] = Field(
        default=None,
        description="The actual value",
        pattern=r"^[A-Za-z0-9\-\.]{1,64}$",
    )
