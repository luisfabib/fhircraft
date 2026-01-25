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

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "currency",
                "value",
                "extension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ext_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("extension",),
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )
