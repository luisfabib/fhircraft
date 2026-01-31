# Fhircraft modules
import fhircraft.fhir.resources.validators as fhir_validators

# Pydantic modules
from pydantic import Field, model_validator, BaseModel
from pydantic.fields import FieldInfo

# Standard modules
from typing import Optional, Literal, Union
from enum import Enum

NoneType = type(None)

# Dynamic modules

from fhircraft.fhir.resources.base import FHIRBaseModel

from typing import Optional, Literal

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    Base64Binary,
)

from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Reference,
)
from .resource import Resource


class Binary(Resource):
    """
    A resource that represents the data of a single raw artifact as digital content accessible in its native format.  A Binary resource can contain any content, whether text, image, pdf, zip archive, etc.
    """

    _abstract = False
    _type = "Binary"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Binary"

    contentType: Optional[Code] = Field(
        description="MimeType of the binary content",
        default=None,
    )
    contentType_ext: Optional[Element] = Field(
        description="Placeholder element for contentType extensions",
        default=None,
        alias="_contentType",
    )
    securityContext: Optional[Reference] = Field(
        description="Identifies another resource to use as proxy when enforcing access control",
        default=None,
    )
    data: Optional[Base64Binary] = Field(
        description="The actual content",
        default=None,
    )
    data_ext: Optional[Element] = Field(
        description="Placeholder element for data extensions",
        default=None,
        alias="_data",
    )
