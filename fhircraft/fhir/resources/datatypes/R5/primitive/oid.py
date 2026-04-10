from typing import Annotated, Optional
from pydantic import BeforeValidator, Field

from fhircraft.fhir.resources.base import FHIROid as FHIROidBase
from .uri import FHIRUri


class FHIROid(FHIRUri, FHIROidBase):
    """An OID represented as a URI."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/oid"
    _type = "oid"

    value: Optional[str] = Field(
        default=None,
        description="The actual value",
        pattern=r"^urn:oid:[0-2](\.(0|[1-9][0-9]*))+$",
    )


Oid = Annotated[str | FHIROid, BeforeValidator(FHIROid.model_validate)]
