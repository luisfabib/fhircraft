from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R5.complex import (
    DataType,
    Element,
    Coding,
    Reference,
)


class Signature(DataType):
    """
    A Signature - XML DigSig, JWS, Graphical image of signature, etc.
    """

    _type = "Signature"

    type: Optional[List[Coding]] = Field(
        description="Indication of the reason the entity signed the object(s)",
        default=None,
    )
    when: Optional[Instant] = Field(
        description="When the signature was created",
        default=None,
    )
    when_ext: Optional[Element] = Field(
        description="Placeholder element for when extensions",
        default=None,
        alias="_when",
    )
    who: Optional[Reference] = Field(
        description="Who signed",
        default=None,
    )
    onBehalfOf: Optional[Reference] = Field(
        description="The party represented",
        default=None,
    )
    targetFormat: Optional[Code] = Field(
        description="The technical format of the signed resources",
        default=None,
    )
    targetFormat_ext: Optional[Element] = Field(
        description="Placeholder element for targetFormat extensions",
        default=None,
        alias="_targetFormat",
    )
    sigFormat: Optional[Code] = Field(
        description="The technical format of the signature",
        default=None,
    )
    sigFormat_ext: Optional[Element] = Field(
        description="Placeholder element for sigFormat extensions",
        default=None,
        alias="_sigFormat",
    )
    data: Optional[Base64Binary] = Field(
        description="The actual signature content (XML DigSig. JWS, picture, etc.)",
        default=None,
    )
    data_ext: Optional[Element] = Field(
        description="Placeholder element for data extensions",
        default=None,
        alias="_data",
    )
