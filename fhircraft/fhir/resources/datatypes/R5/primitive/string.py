from typing import Any, Optional
from pydantic import Field, field_validator

from fhircraft.fhir.resources.base import FHIRPrimitiveModel
from fhircraft.fhir.resources.datatypes.R5.complex import Element


class String(Element, FHIRPrimitiveModel):
    """A sequence of Unicode characters."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/string"
    _type = "string"
    _kind = "primitive"

    value: Optional[str] = Field(
        default=None,
        description="The actual value",
    )
