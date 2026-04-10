from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
import fhircraft.fhir.resources.datatypes.R4B.primitive as fhir
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
    text: Optional[fhir.string] = Field(
        description="Plain text representation of the concept",
        default=None,
    )
