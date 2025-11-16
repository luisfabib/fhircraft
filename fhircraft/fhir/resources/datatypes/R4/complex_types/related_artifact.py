from typing import Optional

from pydantic import Field, field_validator, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *

from .attachment import Attachment
from .element import Element


class RelatedArtifact(Element):
    """
    Related artifacts for a knowledge resource
    """

    type: Optional[Code] = Field(
        description="documentation | justification | citation | predecessor | successor | derived-from | depends-on | composed-of",
        default=None,
    )
    type_ext: Optional[Element] = Field(
        description="Placeholder element for type extensions",
        default=None,
        alias="_type",
    )
    label: Optional[String] = Field(
        description="Short label",
        default=None,
    )
    label_ext: Optional[Element] = Field(
        description="Placeholder element for label extensions",
        default=None,
        alias="_label",
    )
    display: Optional[String] = Field(
        description="Brief description of the related artifact",
        default=None,
    )
    display_ext: Optional[Element] = Field(
        description="Placeholder element for display extensions",
        default=None,
        alias="_display",
    )
    citation: Optional[Markdown] = Field(
        description="Bibliographic citation for the artifact",
        default=None,
    )
    citation_ext: Optional[Element] = Field(
        description="Placeholder element for citation extensions",
        default=None,
        alias="_citation",
    )
    url: Optional[Url] = Field(
        description="Where the artifact can be accessed",
        default=None,
    )
    url_ext: Optional[Element] = Field(
        description="Placeholder element for url extensions",
        default=None,
        alias="_url",
    )
    document: Optional["Attachment"] = Field(
        description="What document is being referenced",
        default=None,
    )
    resource: Optional[Canonical] = Field(
        description="What resource is being referenced",
        default=None,
    )
    resource_ext: Optional[Element] = Field(
        description="Placeholder element for resource extensions",
        default=None,
        alias="_resource",
    )

    @field_validator(
        *(
            "resource",
            "document",
            "url",
            "citation",
            "display",
            "label",
            "type",
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
    def FHIR_ele_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )
