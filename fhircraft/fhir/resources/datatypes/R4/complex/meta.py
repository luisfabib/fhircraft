from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators

import fhircraft.fhir.resources.datatypes.R4.primitive as fhir
from .coding import Coding
from .element import Element

class Meta(Element):
    """
    Metadata about a resource
    """

    _type = "Meta"

    versionId: Optional[fhir.id_] = Field(
        description="Version specific identifier",
        default=None,
    )
    lastUpdated: Optional[fhir.instant] = Field(
        description="When the resource version last changed",
        default=None,
    )
    source: Optional[fhir.uri] = Field(
        description="Identifies where the resource comes from",
        default=None,
    )
    profile: Optional[List[fhir.canonical]] = Field(
        description="Profiles this resource claims to conform to",
        default=None,
    )
    security: Optional[List["Coding"]] = Field(
        description="Security Labels applied to this resource",
        default=None,
    )
    tag: Optional[List["Coding"]] = Field(
        description="Tags applied to this resource",
        default=None,
    )
