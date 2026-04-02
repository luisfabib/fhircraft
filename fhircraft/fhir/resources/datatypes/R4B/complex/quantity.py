from typing import Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from ..primitive import *
from fhircraft.fhir.resources.datatypes.R4B.complex.element import Element

class Quantity(Element):
    """
    A measured or measurable amount
    """

    _type = "Quantity"

    value: Optional[Decimal] = Field(
        description="Numerical value (with implicit precision)",
        default=None,
    )
    comparator: Optional[Code] = Field(
        description="\u003c | \u003c= | \u003e= | \u003e - how to understand the value",
        default=None,
    )
    unit: Optional[String] = Field(
        description="Unit representation",
        default=None,
    )
    system: Optional[Uri] = Field(
        description="System that defines coded unit form",
        default=None,
    )
    code: Optional[Code] = Field(
        description="Coded form of the unit",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_qty_3_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="code.empty() or system.exists()",
            human="If a code for the unit is present, the system SHALL also be present",
            key="qty-3",
            severity="error",
        )
