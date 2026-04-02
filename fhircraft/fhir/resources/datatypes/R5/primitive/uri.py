from typing import Optional
from pydantic import Field

from .string import String


class Uri(String):
    """A Uniform Resource Identifier Reference."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/uri"
    _type = "uri"

    value: Optional[str] = Field(
        default=None,
        description="The actual value",
        pattern=r"^\S+$",
    )
