# Fhircraft modules
from pydantic import Field, model_validator
from typing import Optional

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

import fhircraft.fhir.resources.datatypes.R5.primitive as fhir
from fhircraft.fhir.resources.datatypes.R5.complex import (
    Meta,
    Reference,
    Element,
)
from .resource import Resource

class Binary(Resource):
    """
    A resource that represents the data of a single raw artifact as digital content accessible in its native format.  A Binary resource can contain any content, whether text, image, pdf, zip archive, etc.
    """

    _abstract = False
    _type = "Binary"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Binary"

    contentType: fhir.code = Field(
        description="MimeType of the binary content",
    )
    securityContext: Optional[Reference] = Field(
        description="Identifies another resource to use as proxy when enforcing access control",
        default=None,
    )
    data: Optional[fhir.base64Binary] = Field(
        description="The actual content",
        default=None,
    )
