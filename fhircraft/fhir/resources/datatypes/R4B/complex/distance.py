from pydantic import field_validator, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R4B.complex import Quantity


class Distance(Quantity):
    """
    A length - a value with a unit that is a physical distance
    """

    @model_validator(mode="after")
    def FHIR_dis_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(code.exists() or value.empty()) and (system.empty() or system = %ucum)",
            human="There SHALL be a code if there is a value and it SHALL be an expression of length.  If system is present, it SHALL be UCUM.",
            key="dis-1",
            severity="error",
        )
