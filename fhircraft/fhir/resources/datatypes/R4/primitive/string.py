from typing import Annotated, Any, Optional
from pydantic import BeforeValidator, Field, field_validator

from fhircraft.fhir.resources.base import StringBase
from fhircraft.fhir.resources.datatypes.R4.complex.element import Element


class String(Element, StringBase):
    """A sequence of Unicode characters."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/string"
    _type = "string"
    _kind = "primitive-type"

    value: Optional[str] = Field(
        default=None,
        description="The actual string value.",
    )


string = Annotated[str | String, BeforeValidator(String.model_validate)]
