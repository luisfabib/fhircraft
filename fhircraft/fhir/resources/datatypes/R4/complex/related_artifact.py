from typing import Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators

from ..primitive import *
from .attachment import Attachment
from .element import Element

class RelatedArtifact(Element):
    """
    Related artifacts for a knowledge resource
    """

    _type = "RelatedArtifact"

    type: Optional[Code] = Field(
        description="documentation | justification | citation | predecessor | successor | derived-from | depends-on | composed-of",
        default=None,
    )
    label: Optional[String] = Field(
        description="Short label",
        default=None,
    )
    display: Optional[String] = Field(
        description="Brief description of the related artifact",
        default=None,
    )
    citation: Optional[Markdown] = Field(
        description="Bibliographic citation for the artifact",
        default=None,
    )
    url: Optional[Url] = Field(
        description="Where the artifact can be accessed",
        default=None,
    )
    document: Optional["Attachment"] = Field(
        description="What document is being referenced",
        default=None,
    )
    resource: Optional[Canonical] = Field(
        description="What resource is being referenced",
        default=None,
    )
