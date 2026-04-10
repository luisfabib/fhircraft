from typing import Annotated, Optional
from pydantic import BeforeValidator, Field

from fhircraft.fhir.resources.base import FHIRUri as FHIRUriBase
from .string import FHIRString


class FHIRUri(FHIRString, FHIRUriBase):
    """A Uniform Resource Identifier Reference."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/uri"
    _type = "uri"

    value: Optional[str] = Field(
        default=None,
        description="The actual value",
        pattern=r"^\S+$",
    )


Uri = Annotated[str | FHIRUri, BeforeValidator(FHIRUri.model_validate)]
