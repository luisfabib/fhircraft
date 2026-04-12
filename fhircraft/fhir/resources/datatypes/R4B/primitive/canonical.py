from typing import Annotated
from pydantic import BeforeValidator

from fhircraft.fhir.resources.base import CanonicalBase
from .uri import Uri


class Canonical(Uri, CanonicalBase):
    """A URI that refers to a resource by its canonical URL."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/canonical"
    _type = "canonical"


canonical = Annotated[str | Canonical, BeforeValidator(Canonical.model_validate)]
