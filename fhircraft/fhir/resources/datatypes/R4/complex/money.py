from typing import Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators

from ..primitive import *
from .element import Element

class Money(Element):
    """
    An amount of economic utility in some recognized currency
    """

    _type = "Money"

    value: Optional[Decimal] = Field(
        description="Numerical value (with implicit precision)",
        default=None,
    )
    currency: Optional[Code] = Field(
        description="ISO 4217 Currency Code",
        default=None,
    )
