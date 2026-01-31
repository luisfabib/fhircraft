from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R4B.complex import Element, Coding


class Meta(Element):
    """
    Metadata about a resource
    """

    _type = "Meta"

    versionId: Optional[Id] = Field(
        description="Version specific identifier",
        default=None,
    )
    versionId_ext: Optional[Element] = Field(
        description="Placeholder element for versionId extensions",
        default=None,
        alias="_versionId",
    )
    lastUpdated: Optional[Instant] = Field(
        description="When the resource version last changed",
        default=None,
    )
    lastUpdated_ext: Optional[Element] = Field(
        description="Placeholder element for lastUpdated extensions",
        default=None,
        alias="_lastUpdated",
    )
    source: Optional[Uri] = Field(
        description="Identifies where the resource comes from",
        default=None,
    )
    source_ext: Optional[Element] = Field(
        description="Placeholder element for source extensions",
        default=None,
        alias="_source",
    )
    profile: Optional[List[Canonical]] = Field(
        description="Profiles this resource claims to conform to",
        default=None,
    )
    profile_ext: Optional[List[Optional[Element]]] = Field(
        description="Placeholder element for profile extensions",
        default=None,
        alias="_profile",
    )
    security: Optional[List[Coding]] = Field(
        description="Security Labels applied to this resource",
        default=None,
    )
    tag: Optional[List[Coding]] = Field(
        description="Tags applied to this resource",
        default=None,
    )
