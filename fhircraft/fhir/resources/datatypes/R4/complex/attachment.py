from typing import List, Optional, TYPE_CHECKING

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
import fhircraft.fhir.resources.datatypes.R4.primitive as fhir
from fhircraft.fhir.resources.datatypes.R4.complex import Element


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
    size: Optional[fhir.unsignedInt] = Field(
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

    @model_validator(mode="after")
    def FHIR_att_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="data.empty() or contentType.exists()",
            human="If the Attachment has data, it SHALL have a contentType",
            key="att-1",
            severity="error",
        )
