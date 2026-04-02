from typing import Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from ..primitive import *
from fhircraft.fhir.resources.datatypes.R5.complex import Base, Element, Meta

class Resource(Base):
    """
    Base Resource
    """

    _abstract = True
    _type = "Resource"
    _kind = "resource"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Resource"

    id: Optional[Id] = Field(
        description="Logical id of this artifact",
        default=None,
    )
    meta: Optional[Meta] = Field(
        description="Metadata about the resource",
        default=None,
    )
    implicitRules: Optional[Uri] = Field(
        description="A set of rules under which this content was created",
        default=None,
    )
    language: Optional[Code] = Field(
        description="Language of the resource content",
        default=None,
    )
