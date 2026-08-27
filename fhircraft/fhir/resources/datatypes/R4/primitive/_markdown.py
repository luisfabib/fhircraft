from typing import Annotated, Optional
from pydantic import BeforeValidator, Field

from fhircraft.fhir.resources.base import MarkdownBase
from ._string import String


class Markdown(String, MarkdownBase):
    """A string that may contain Github Flavored Markdown syntax."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/markdown"
    _type = "markdown"

    value: Optional[str] = Field(
        default=None,
        description="The actual value",
        pattern=r"^\s*(\S|\s)*$",
    )


markdown = Annotated[str | Markdown, BeforeValidator(Markdown.model_validate)]
