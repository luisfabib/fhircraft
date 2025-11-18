from pydantic import model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R4B.complex.quantity import Quantity


class Count(Quantity):
    """
    A measured or measurable amount
    """

    @model_validator(mode="after")
    def FHIR_cnt_3_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(code.exists() or value.empty()) and (system.empty() or system = %ucum) and (code.empty() or code = '1') and (value.empty() or value.hasValue().not() or value.toString().contains('.').not())",
            human='There SHALL be a code with a value of "1" if there is a value. If system is present, it SHALL be UCUM.  If present, the value SHALL be a whole number.',
            key="cnt-3",
            severity="error",
        )
