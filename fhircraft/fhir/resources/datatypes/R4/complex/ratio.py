from typing import Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *

from .element import Element
from .quantity import Quantity


class Ratio(Element):
    """
    A ratio of two Quantity values - a numerator and a denominator
    """

    _type = "Ratio"

    numerator: Optional[Quantity] = Field(
        description="Numerator value",
        default=None,
    )
    denominator: Optional[Quantity] = Field(
        description="Denominator value",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "denominator",
                "numerator",
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

    @model_validator(mode="after")
    def FHIR_rat_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(numerator.empty() xor denominator.exists()) and (numerator.exists() or extension.exists())",
            human="Numerator and denominator SHALL both be present, or both are absent. If both are absent, there SHALL be some extension present",
            key="rat-1",
            severity="error",
        )
