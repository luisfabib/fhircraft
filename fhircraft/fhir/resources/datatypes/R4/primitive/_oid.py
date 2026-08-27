from typing import Annotated, Optional
from pydantic import BeforeValidator, Field

from fhircraft.fhir.resources.base import OidBase
from ._uri import Uri


class Oid(Uri, OidBase):
    """An OID represented as a URI."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/oid"
    _type = "oid"

    value: Optional[str] = Field(
        default=None,
        description="The actual value",
        pattern=r"^urn:oid:[0-2](\.(0|[1-9][0-9]*))+$",
    )


oid = Annotated[str | Oid, BeforeValidator(Oid.model_validate)]
