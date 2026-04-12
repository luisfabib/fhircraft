from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
import fhircraft.fhir.resources.datatypes.R5.primitive as fhir
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

    type: Optional[fhir.code] = Field(
        description="base | surcharge | deduction | discount | tax | informational",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="Codes may be used to differentiate between kinds of taxes, surcharges, discounts etc.",
        default=None,
    )
    factor: Optional[fhir.decimal] = Field(
        description="Factor used for calculating this component",
        default=None,
    )
    amount: Optional[Money] = Field(
        description="Explicit value amount to be used",
        default=None,
    )
