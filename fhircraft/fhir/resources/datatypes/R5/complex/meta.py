from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from ..primitive import *
from fhircraft.fhir.resources.datatypes.R5.complex import Element, DataType, Coding

class Meta(DataType):
    """
    Metadata about a resource
    """

    _type = "Meta"

    versionId: Optional[Id] = Field(
        description="Version specific identifier",
        default=None,
    )
    lastUpdated: Optional[Instant] = Field(
        description="When the resource version last changed",
        default=None,
    )
    source: Optional[Uri] = Field(
        description="Identifies where the resource comes from",
        default=None,
    )
    profile: Optional[List[Canonical]] = Field(
        description="Profiles this resource claims to conform to",
        default=None,
    )
    security: Optional[List[Coding]] = Field(
        description="Security Labels applied to this resource",
        default=None,
    )
    tag: Optional[List[Coding]] = Field(
        description="Tags applied to this resource",
        default=None,
    )
