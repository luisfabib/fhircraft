from typing import Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
import fhircraft.fhir.resources.datatypes.R4B.primitive as fhir
from fhircraft.fhir.resources.datatypes.R4B.complex.element import Element

class Money(Element):
    """
    An amount of economic utility in some recognized currency
    """

    _type = "Money"

    value: Optional[fhir.decimal] = Field(
        description="Numerical value (with implicit precision)",
        default=None,
    )
    currency: Optional[fhir.code] = Field(
        description="ISO 4217 Currency code",
        default=None,
    )
