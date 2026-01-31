from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R4B.complex import Element, Coding


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
    text_ext: Optional[Element] = Field(
        description="Placeholder element for text extensions",
        default=None,
        alias="_text",
    )
