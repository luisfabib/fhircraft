from pydantic import model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R5.complex.quantity import Quantity


class Age(Quantity):
    """
    A duration of time during which an organism (or a process) has existed
    """

    @model_validator(mode="after")
    def FHIR_age_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(code.exists() or value.empty()) and (system.empty() or system = %ucum) and (value.empty() or value.hasValue().not() or value > 0)",
            human="There SHALL be a code if there is a value and it SHALL be an expression of time.  If system is present, it SHALL be UCUM.  If value is present, it SHALL be positive.",
            key="age-1",
            severity="error",
        )
