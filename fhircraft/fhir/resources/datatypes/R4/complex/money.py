from typing import Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *

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
    value_ext: Optional[Element] = Field(
        description="Placeholder element for value extensions",
        default=None,
        alias="_value",
    )
    currency: Optional[Code] = Field(
        description="ISO 4217 Currency Code",
        default=None,
    )
    currency_ext: Optional[Element] = Field(
        description="Placeholder element for currency extensions",
        default=None,
        alias="_currency",
    )
