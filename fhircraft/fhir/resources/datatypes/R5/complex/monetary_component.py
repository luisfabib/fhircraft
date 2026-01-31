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
