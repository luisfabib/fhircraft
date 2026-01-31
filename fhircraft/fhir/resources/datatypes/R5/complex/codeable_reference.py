from typing import TYPE_CHECKING, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    CodeableConcept,
)

if TYPE_CHECKING:
    from fhircraft.fhir.resources.datatypes.R5.complex import (
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
    reference: Optional["Reference"] = Field(
        description="Reference to a resource (by instance)",
        default=None,
    )
