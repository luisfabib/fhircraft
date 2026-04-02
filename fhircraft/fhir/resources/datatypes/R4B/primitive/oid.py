from typing import Optional
from pydantic import Field

from .uri import Uri


class Oid(Uri):
    """An OID represented as a URI."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/oid"
    _type = "oid"

    value: Optional[str] = Field(
        default=None,
        description="The actual value",
        pattern=r"^urn:oid:[0-2](\.(0|[1-9][0-9]*))+$",
    )
