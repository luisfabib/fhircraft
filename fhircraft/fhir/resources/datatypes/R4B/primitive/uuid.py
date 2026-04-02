from typing import Optional
from pydantic import Field

from .uri import Uri


class Uuid(Uri):
    """A UUID represented as a URI."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/uuid"
    _type = "uuid"

    value: Optional[str] = Field(
        default=None,
        description="The actual value",
        pattern=r"^urn:uuid:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    )
