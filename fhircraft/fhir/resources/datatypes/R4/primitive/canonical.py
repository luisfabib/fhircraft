from typing import Annotated
from pydantic import BeforeValidator

from fhircraft.fhir.resources.base import FHIRCanonical as FHIRCanonicalBase
from .uri import FHIRUri


class FHIRCanonical(FHIRUri, FHIRCanonicalBase):
    """A URI that refers to a resource by its canonical URL."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/canonical"
    _type = "canonical"


Canonical = Annotated[
    str | FHIRCanonical, BeforeValidator(FHIRCanonical.model_validate)
]
