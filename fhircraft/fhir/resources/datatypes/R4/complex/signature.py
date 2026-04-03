from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators

from ..primitive import *
from .coding import Coding
from .element import Element
from .reference import Reference

class Signature(Element):
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
    sigFormat: Optional[Code] = Field(
        description="The technical format of the signature",
        default=None,
    )
    data: Optional[Base64Binary] = Field(
        description="The actual signature content (XML DigSig. JWS, picture, etc.)",
        default=None,
    )
