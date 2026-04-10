from typing import Annotated
from pydantic import BeforeValidator

from fhircraft.fhir.resources.base import FHIRUrl as FHIRUrlBase
from .uri import FHIRUri


class FHIRUrl(FHIRUri, FHIRUrlBase):
    """A Uniform Resource Locator."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/url"
    _type = "url"


Url = Annotated[str | FHIRUrl, BeforeValidator(FHIRUrl.model_validate)]
