from pydantic import model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *

from .quantity import Quantity


class Duration(Quantity):
    """
    A length of time
    """

    @model_validator(mode="after")
    def FHIR_drt_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="code.exists() implies ((system = %ucum) and value.exists())",
            human="There SHALL be a code if there is a value and it SHALL be an expression of time.  If system is present, it SHALL be UCUM.",
            key="drt-1",
            severity="error",
        )
