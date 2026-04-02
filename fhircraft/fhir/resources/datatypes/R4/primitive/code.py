from typing import Optional
from pydantic import Field

from .string import String


class Code(String):
    """A string which has at least one character and no leading/trailing whitespace."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/code"
    _type = "code"

    value: Optional[str] = Field(
        default=None,
        description="The actual value",
        pattern=r"^[^\s]+(\s[^\s]+)*$",
    )
