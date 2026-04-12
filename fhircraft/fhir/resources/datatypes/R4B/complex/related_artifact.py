from typing import Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
import fhircraft.fhir.resources.datatypes.R4B.primitive as fhir
from fhircraft.fhir.resources.datatypes.R4B.complex import Element, Attachment


class RelatedArtifact(Element):
    """
    Related artifacts for a knowledge resource
    """

    _type = "RelatedArtifact"

    type: Optional[fhir.code] = Field(
        description="documentation | justification | citation | predecessor | successor | derived-from | depends-on | composed-of",
        default=None,
    )
    label: Optional[fhir.string] = Field(
        description="Short label",
        default=None,
    )
    display: Optional[fhir.string] = Field(
        description="Brief description of the related artifact",
        default=None,
    )
    citation: Optional[fhir.markdown] = Field(
        description="Bibliographic citation for the artifact",
        default=None,
    )
    url: Optional[fhir.url] = Field(
        description="Where the artifact can be accessed",
        default=None,
    )
    document: Optional[Attachment] = Field(
        description="What document is being referenced",
        default=None,
    )
    resource: Optional[fhir.canonical] = Field(
        description="What resource is being referenced",
        default=None,
    )
