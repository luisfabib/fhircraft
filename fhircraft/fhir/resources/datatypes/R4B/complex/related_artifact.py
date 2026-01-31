from typing import Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R4B.complex import Element, Attachment


class RelatedArtifact(Element):
    """
    Related artifacts for a knowledge resource
    """

    _type = "RelatedArtifact"

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
    document: Optional[Attachment] = Field(
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
