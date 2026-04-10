from typing import Annotated, Optional
from pydantic import BeforeValidator, Field

from fhircraft.fhir.resources.base import FHIRCode as FHIRCodeBase
from .string import FHIRString


class FHIRCode(FHIRString, FHIRCodeBase):
    """A string which has at least one character and no leading/trailing whitespace."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/code"
    _type = "code"

    value: Optional[str] = Field(
        default=None,
        description="The actual value",
        pattern=r"^[^\s]+(\s[^\s]+)*$",
    )


Code = Annotated[str | FHIRCode, BeforeValidator(FHIRCode.model_validate)]
