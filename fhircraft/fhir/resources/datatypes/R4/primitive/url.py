from typing import Annotated
from pydantic import BeforeValidator

from fhircraft.fhir.resources.base import UrlBase
from .uri import Uri


class Url(Uri, UrlBase):
    """A Uniform Resource Locator."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/url"
    _type = "url"


url = Annotated[str | Url, BeforeValidator(Url.model_validate)]
