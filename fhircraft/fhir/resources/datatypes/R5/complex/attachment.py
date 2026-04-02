from typing import Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from ..primitive import *
from fhircraft.fhir.resources.datatypes.R5.complex import Element

class Attachment(Element):
    """
    Content in a format defined elsewhere
    """

    _type = "Attachment"

    contentType: Optional[Code] = Field(
        description="Mime type of the content, with charset etc.",
        default=None,
    )
    language: Optional[Code] = Field(
        description="Human language of the content (BCP-47)",
        default=None,
    )
    data: Optional[Base64Binary] = Field(
        description="Data inline, base64ed",
        default=None,
    )
    url: Optional[Url] = Field(
        description="Uri where the data can be found",
        default=None,
    )
    size: Optional[Integer64] = Field(
        description="Number of bytes of content (if url provided)",
        default=None,
    )
    hash: Optional[Base64Binary] = Field(
        description="Hash of the data (sha-1, base64ed)",
        default=None,
    )
    title: Optional[String] = Field(
        description="Label to display in place of the data",
        default=None,
    )
    creation: Optional[DateTime] = Field(
        description="Date attachment was first created",
        default=None,
    )
    height: Optional[PositiveInt] = Field(
        description="Height of the image in pixels (photo/video)",
        default=None,
    )
    width: Optional[PositiveInt] = Field(
        description="Width of the image in pixels (photo/video)",
        default=None,
    )
    frames: Optional[PositiveInt] = Field(
        description="Number of frames if \u003e 1 (photo)",
        default=None,
    )
    duration: Optional[Decimal] = Field(
        description="Length in seconds (audio / video)",
        default=None,
    )
    pages: Optional[PositiveInt] = Field(
        description="Number of printed pages",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_att_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="data.empty() or contentType.exists()",
            human="If the Attachment has data, it SHALL have a contentType",
            key="att-1",
            severity="error",
        )
