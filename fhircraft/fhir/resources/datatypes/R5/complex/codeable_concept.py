from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from ..primitive import *
from fhircraft.fhir.resources.datatypes.R5.complex import Coding, Element

class CodeableConcept(Element):
    """
    Concept - reference to a terminology or just  text
    """

    _type = "CodeableConcept"

    coding: Optional[List[Coding]] = Field(
        description="Code defined by a terminology system",
        default=None,
    )
    text: Optional[String] = Field(
        description="Plain text representation of the concept",
        default=None,
    )
