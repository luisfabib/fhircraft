from pydantic import model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R4B.complex.quantity import Quantity


class SimpleQuantity(Quantity):
    """
    A fixed quantity (no comparator)
    """

    @model_validator(mode="after")
    def FHIR_sqty_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="comparator.empty()",
            human="The comparator is not used on a SimpleQuantity",
            key="sqty-1",
            severity="error",
        )
