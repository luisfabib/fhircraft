from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R5.complex import DataType, Element


class Quantity(DataType):
    """
    A measured or measurable amount
    """

    _type = "Quantity"

    value: Optional[Decimal] = Field(
        description="Numerical value (with implicit precision)",
        default=None,
    )
    value_ext: Optional[Element] = Field(
        description="Placeholder element for value extensions",
        default=None,
        alias="_value",
    )
    comparator: Optional[Code] = Field(
        description="\u003c | \u003c= | \u003e= | \u003e | ad - how to understand the value",
        default=None,
    )
    comparator_ext: Optional[Element] = Field(
        description="Placeholder element for comparator extensions",
        default=None,
        alias="_comparator",
    )
    unit: Optional[String] = Field(
        description="Unit representation",
        default=None,
    )
    unit_ext: Optional[Element] = Field(
        description="Placeholder element for unit extensions",
        default=None,
        alias="_unit",
    )
    system: Optional[Uri] = Field(
        description="System that defines coded unit form",
        default=None,
    )
    system_ext: Optional[Element] = Field(
        description="Placeholder element for system extensions",
        default=None,
        alias="_system",
    )
    code: Optional[Code] = Field(
        description="Coded form of the unit",
        default=None,
    )
    code_ext: Optional[Element] = Field(
        description="Placeholder element for code extensions",
        default=None,
        alias="_code",
    )

    @model_validator(mode="after")
    def FHIR_qty_3_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="code.empty() or system.exists()",
            human="If a code for the unit is present, the system SHALL also be present",
            key="qty-3",
            severity="error",
        )
