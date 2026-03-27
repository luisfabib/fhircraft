from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R5.complex import DataType, Element


class Expression(DataType):
    """
    An expression that can be used to generate a value
    """

    _type = "Expression"

    description: Optional[String] = Field(
        description="Natural language description of the condition",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    name: Optional[Code] = Field(
        description="Short name assigned to expression for reuse",
        default=None,
    )
    name_ext: Optional[Element] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    language: Optional[Code] = Field(
        description="text/cql | text/fhirpath | application/x-fhir-query | etc.",
        default=None,
    )
    language_ext: Optional[Element] = Field(
        description="Placeholder element for language extensions",
        default=None,
        alias="_language",
    )
    expression: Optional[String] = Field(
        description="Expression in specified language",
        default=None,
    )
    expression_ext: Optional[Element] = Field(
        description="Placeholder element for expression extensions",
        default=None,
        alias="_expression",
    )
    reference: Optional[Uri] = Field(
        description="Where the expression is found",
        default=None,
    )
    reference_ext: Optional[Element] = Field(
        description="Placeholder element for reference extensions",
        default=None,
        alias="_reference",
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
