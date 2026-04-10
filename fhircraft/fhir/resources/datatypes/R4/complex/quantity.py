from typing import Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
import fhircraft.fhir.resources.datatypes.R4.primitive as fhir
from fhircraft.fhir.resources.datatypes.R4.complex import Element


class Quantity(Element):
    """
    A measured or measurable amount
    """

    _type = "Quantity"

    value: Optional[fhir.decimal] = Field(
        description="Numerical value (with implicit precision)",
        default=None,
    )
    comparator: Optional[fhir.code] = Field(
        description="\u003c | \u003c= | \u003e= | \u003e - how to understand the value",
        default=None,
    )
    unit: Optional[fhir.string] = Field(
        description="Unit representation",
        default=None,
    )
    system: Optional[fhir.uri] = Field(
        description="System that defines coded unit form",
        default=None,
    )
    code: Optional[fhir.code] = Field(
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
