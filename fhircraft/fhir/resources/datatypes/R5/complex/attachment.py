from typing import Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
import fhircraft.fhir.resources.datatypes.R5.primitive as fhir
from fhircraft.fhir.resources.datatypes.R5.complex import Element


class Attachment(Element):
    """
    Content in a format defined elsewhere
    """

    _type = "Attachment"

    contentType: Optional[fhir.code] = Field(
        description="Mime type of the content, with charset etc.",
        default=None,
    )
    language: Optional[fhir.code] = Field(
        description="Human language of the content (BCP-47)",
        default=None,
    )
    data: Optional[fhir.base64Binary] = Field(
        description="Data inline, base64ed",
        default=None,
    )
    url: Optional[fhir.url] = Field(
        description="uri where the data can be found",
        default=None,
    )
    size: Optional[fhir.integer64] = Field(
        description="Number of bytes of content (if url provided)",
        default=None,
    )
    hash: Optional[fhir.base64Binary] = Field(
        description="Hash of the data (sha-1, base64ed)",
        default=None,
    )
    title: Optional[fhir.string] = Field(
        description="Label to display in place of the data",
        default=None,
    )
    creation: Optional[fhir.dateTime] = Field(
        description="Date attachment was first created",
        default=None,
    )
    height: Optional[fhir.positiveInt] = Field(
        description="Height of the image in pixels (photo/video)",
        default=None,
    )
    width: Optional[fhir.positiveInt] = Field(
        description="Width of the image in pixels (photo/video)",
        default=None,
    )
    frames: Optional[fhir.positiveInt] = Field(
        description="Number of frames if \u003e 1 (photo)",
        default=None,
    )
    duration: Optional[fhir.decimal] = Field(
        description="Length in seconds (audio / video)",
        default=None,
    )
    pages: Optional[fhir.positiveInt] = Field(
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
