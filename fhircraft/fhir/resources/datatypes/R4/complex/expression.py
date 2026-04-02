from typing import Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from ..primitive import *

from .element import Element

class Expression(Element):
    """
    An expression that can be used to generate a value
    """

    _type = "Expression"

    description: Optional[String] = Field(
        description="Natural language description of the condition",
        default=None,
    )
    name: Optional[Id] = Field(
        description="Short name assigned to expression for reuse",
        default=None,
    )
    language: Optional[Code] = Field(
        description="text/cql | text/fhirpath | application/x-fhir-query | etc.",
        default=None,
    )
    expression: Optional[String] = Field(
        description="Expression in specified language",
        default=None,
    )
    reference: Optional[Uri] = Field(
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
