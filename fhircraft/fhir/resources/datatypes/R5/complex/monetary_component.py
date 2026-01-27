from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R5.complex import (
    DataType,
    Element,
    Money,
    CodeableConcept,
)


class MonetaryComponent(DataType):
    """
    Availability data for an {item}
    """

    _type = "MonetaryComponent"

    type: Optional[Code] = Field(
        description="base | surcharge | deduction | discount | tax | informational",
        default=None,
    )
    type_ext: Optional[Element] = Field(
        description="Placeholder element for type extensions",
        default=None,
        alias="_type",
    )
    code: Optional[CodeableConcept] = Field(
        description="Codes may be used to differentiate between kinds of taxes, surcharges, discounts etc.",
        default=None,
    )
    factor: Optional[Decimal] = Field(
        description="Factor used for calculating this component",
        default=None,
    )
    factor_ext: Optional[Element] = Field(
        description="Placeholder element for factor extensions",
        default=None,
        alias="_factor",
    )
    amount: Optional[Money] = Field(
        description="Explicit value amount to be used",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "amount",
                "factor",
                "code",
                "type",
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
