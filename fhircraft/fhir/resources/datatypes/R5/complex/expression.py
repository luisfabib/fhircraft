from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
import fhircraft.fhir.resources.datatypes.R5.primitive as fhir
from fhircraft.fhir.resources.datatypes.R5.complex import DataType, Element

class Expression(DataType):
    """
    An expression that can be used to generate a value
    """

    _type = "Expression"

    description: Optional[fhir.string] = Field(
        description="Natural language description of the condition",
        default=None,
    )
    name: Optional[fhir.code] = Field(
        description="Short name assigned to expression for reuse",
        default=None,
    )
    language: Optional[fhir.code] = Field(
        description="text/cql | text/fhirpath | application/x-fhir-query | etc.",
        default=None,
    )
    expression: Optional[fhir.string] = Field(
        description="Expression in specified language",
        default=None,
    )
    reference: Optional[fhir.uri] = Field(
        description="Where the expression is found",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_exp_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="expression.exists() or reference.exists()",
            human="An expression or a reference must be provided",
            key="exp-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_exp_2_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.hasValue() implies name.matches('[A-Za-z][A-Za-z0-9\\_]{0,63}')",
            human="The name must be a valid variable name in most computer languages",
            key="exp-2",
            severity="error",
        )
