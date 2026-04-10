from typing import Annotated, Optional
from pydantic import BeforeValidator, Field

from fhircraft.fhir.resources.base import FHIRUuid as FHIRUuidBase
from .uri import FHIRUri


class FHIRUuid(FHIRUri, FHIRUuidBase):
    """A UUID represented as a URI."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/uuid"
    _type = "uuid"

    value: Optional[str] = Field(
        default=None,
        description="The actual value",
        pattern=r"^urn:uuid:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    )


Uuid = Annotated[str | FHIRUuid, BeforeValidator(FHIRUuid.model_validate)]
