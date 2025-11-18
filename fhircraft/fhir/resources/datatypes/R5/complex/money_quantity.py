from pydantic import model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R5.complex import Quantity


class MoneyQuantity(Quantity):
    """
    An amount of money.
    """

    @model_validator(mode="after")
    def FHIR_mtqy_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(code.exists() or value.empty()) and (system.empty() or system = 'urn:iso:std:iso:4217')",
            human='There SHALL be a code if there is a value and it SHALL be an expression of currency.  If system is present, it SHALL be ISO 4217 (system = "urn:iso:std:iso:4217" - currency).',
            key="mtqy-1",
            severity="error",
        )
