from typing import Optional, List

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
import fhircraft.fhir.resources.datatypes.R4B.primitive as fhir
from fhircraft.fhir.resources.datatypes.R4B.complex import Coding, Element, Reference

class Signature(Element):
    """
    A Signature - XML DigSig, JWS, Graphical image of signature, etc.
    """

    _type = "Signature"

    type: List[Coding] = Field(
        description="Indication of the reason the entity signed the object(s)",
     	min_length=1,
	)
    when: fhir.instant = Field(
        description="When the signature was created",
    )
    who: Reference = Field(
        description="Who signed",
    )
    onBehalfOf: Optional[Reference] = Field(
        description="The party represented",
        default=None,
    )
    targetFormat: Optional[fhir.code] = Field(
        description="The technical format of the signed resources",
        default=None,
    )
    sigFormat: Optional[fhir.code] = Field(
        description="The technical format of the signature",
        default=None,
    )
    data: Optional[fhir.base64Binary] = Field(
        description="The actual signature content (XML DigSig. JWS, picture, etc.)",
        default=None,
    )
