from typing import Optional
from pydantic import Field

from .string import String


class Markdown(String):
    """A string that may contain Github Flavored Markdown syntax."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/markdown"
    _type = "markdown"

    value: Optional[str] = Field(
        default=None,
        description="The actual value",
        pattern=r"^\s*(\S|\s)*$",
    )
