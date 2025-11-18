from typing import Optional

from pydantic import Field, field_validator, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R5.complex import Element


class Attachment(Element):
    """
    Content in a format defined elsewhere
    """

    contentType: Optional[Code] = Field(
        description="Mime type of the content, with charset etc.",
        default=None,
    )
    contentType_ext: Optional[Element] = Field(
        description="Placeholder element for contentType extensions",
        default=None,
        alias="_contentType",
    )
    language: Optional[Code] = Field(
        description="Human language of the content (BCP-47)",
        default=None,
    )
    language_ext: Optional[Element] = Field(
        description="Placeholder element for language extensions",
        default=None,
        alias="_language",
    )
    data: Optional[Base64Binary] = Field(
        description="Data inline, base64ed",
        default=None,
    )
    data_ext: Optional[Element] = Field(
        description="Placeholder element for data extensions",
        default=None,
        alias="_data",
    )
    url: Optional[Url] = Field(
        description="Uri where the data can be found",
        default=None,
    )
    url_ext: Optional[Element] = Field(
        description="Placeholder element for url extensions",
        default=None,
        alias="_url",
    )
    size: Optional[Integer64] = Field(
        description="Number of bytes of content (if url provided)",
        default=None,
    )
    size_ext: Optional[Element] = Field(
        description="Placeholder element for size extensions",
        default=None,
        alias="_size",
    )
    hash: Optional[Base64Binary] = Field(
        description="Hash of the data (sha-1, base64ed)",
        default=None,
    )
    hash_ext: Optional[Element] = Field(
        description="Placeholder element for hash extensions",
        default=None,
        alias="_hash",
    )
    title: Optional[String] = Field(
        description="Label to display in place of the data",
        default=None,
    )
    title_ext: Optional[Element] = Field(
        description="Placeholder element for title extensions",
        default=None,
        alias="_title",
    )
    creation: Optional[DateTime] = Field(
        description="Date attachment was first created",
        default=None,
    )
    creation_ext: Optional[Element] = Field(
        description="Placeholder element for creation extensions",
        default=None,
        alias="_creation",
    )
    height: Optional[PositiveInt] = Field(
        description="Height of the image in pixels (photo/video)",
        default=None,
    )
    height_ext: Optional[Element] = Field(
        description="Placeholder element for height extensions",
        default=None,
        alias="_height",
    )
    width: Optional[PositiveInt] = Field(
        description="Width of the image in pixels (photo/video)",
        default=None,
    )
    width_ext: Optional[Element] = Field(
        description="Placeholder element for width extensions",
        default=None,
        alias="_width",
    )
    frames: Optional[PositiveInt] = Field(
        description="Number of frames if \u003e 1 (photo)",
        default=None,
    )
    frames_ext: Optional[Element] = Field(
        description="Placeholder element for frames extensions",
        default=None,
        alias="_frames",
    )
    duration: Optional[Decimal] = Field(
        description="Length in seconds (audio / video)",
        default=None,
    )
    duration_ext: Optional[Element] = Field(
        description="Placeholder element for duration extensions",
        default=None,
        alias="_duration",
    )
    pages: Optional[PositiveInt] = Field(
        description="Number of printed pages",
        default=None,
    )
    pages_ext: Optional[Element] = Field(
        description="Placeholder element for pages extensions",
        default=None,
        alias="_pages",
    )

    @field_validator(
        *(
            "pages",
            "duration",
            "frames",
            "width",
            "height",
            "creation",
            "title",
            "hash",
            "size",
            "url",
            "data",
            "language",
            "contentType",
            "extension",
        ),
        mode="after",
        check_fields=None,
    )
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*("extension",), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_att_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="data.empty() or contentType.exists()",
            human="If the Attachment has data, it SHALL have a contentType",
            key="att-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )
