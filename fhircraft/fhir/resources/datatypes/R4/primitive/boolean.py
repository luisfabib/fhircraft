from typing import Annotated, Optional
from pydantic import BeforeValidator, Field, field_validator

from fhircraft.fhir.resources.base import BooleanBase
from fhircraft.fhir.resources.datatypes.R4.complex.element import Element


class Boolean(Element, BooleanBase):
    """Value of 'true' or 'false'."""

    _canonical_url = "http://hl7.org/fhir/StructureDefinition/boolean"
    _type = "boolean"
    _kind = "primitive-type"

    value: Optional[bool] = Field(
        default=None,
        description="The actual value",
    )

    @field_validator("value", mode="before")
    @classmethod
    def _parse_bool(cls, v):
        if isinstance(v, str):
            if v == "true":
                return True
            if v == "false":
                return False
            raise ValueError(f"Expected 'true' or 'false', got {v!r}")
        return v


boolean = Annotated[bool | Boolean, BeforeValidator(Boolean.model_validate)]
