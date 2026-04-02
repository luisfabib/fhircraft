from pydantic import model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from ..primitive import *
from fhircraft.fhir.resources.datatypes.R5.complex import Quantity

class SimpleQuantity(Quantity):
    """
    A fixed quantity (no comparator)
    """

    _type = "Quantity"

    @model_validator(mode="after")
    def FHIR_sqty_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="comparator.empty()",
            human="The comparator is not used on a SimpleQuantity",
            key="sqty-1",
            severity="error",
        )
