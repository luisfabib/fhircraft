from typing import Annotated, Optional
from pydantic import BeforeValidator, Field

from fhircraft.fhir.resources.base import IdBase
from ._string import String


class Id(String, IdBase):
    """Any combination of letters, numerals, '-' and '.', with a length limit of 64 characters."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/id"
    _type = "id"

    value: Optional[str] = Field(
        default=None,
        description="The actual value",
        pattern=r"^[A-Za-z0-9\-\.]{1,64}$",
    )


id_ = Annotated[str | Id, BeforeValidator(Id.model_validate)]
