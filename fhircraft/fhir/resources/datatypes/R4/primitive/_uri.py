from typing import Annotated, Optional
from pydantic import BeforeValidator, Field

from fhircraft.fhir.resources.base import UriBase
from ._string import String


class Uri(String, UriBase):
    """A Uniform Resource Identifier Reference."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/uri"
    _type = "uri"

    value: Optional[str] = Field(
        default=None,
        description="The actual value",
        pattern=r"^\S+$",
    )


uri = Annotated[str | Uri, BeforeValidator(Uri.model_validate)]
