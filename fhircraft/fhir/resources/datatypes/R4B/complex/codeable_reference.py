from typing import Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from ..primitive import *
from fhircraft.fhir.resources.datatypes.R4B.complex import (
    Element,
    CodeableConcept,
    Reference,
)

class CodeableReference(Element):
    """
    Reference to a resource or a concept
    """

    _type = "CodeableReference"

    concept: Optional[CodeableConcept] = Field(
        description="Reference to a concept (by class)",
        default=None,
    )
    reference: Optional[Reference] = Field(
        description="Reference to a resource (by instance)",
        default=None,
    )
