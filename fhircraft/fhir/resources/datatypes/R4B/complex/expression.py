from typing import Optional

from pydantic import Field, field_validator, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R4B.complex import Element


class Expression(Element):
    """
    An expression that can be used to generate a value
    """

    description: Optional[String] = Field(
        description="Natural language description of the condition",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    name: Optional[Id] = Field(
        description="Short name assigned to expression for reuse",
        default=None,
    )
    name_ext: Optional[Element] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    language: Optional[Code] = Field(
        description="text/cql | text/fhirpath | application/x-fhir-query | text/cql-identifier | text/cql-expression | etc.",
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

    @field_validator(
        *(
            "reference",
            "expression",
            "language",
            "name",
            "description",
            "extension",
        ),
        mode="after",
        check_fields=None,
    )
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(*("extension",), mode="after", check_fields=None)
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_exp_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="expression.exists() or reference.exists()",
            human="An expression or a reference must be provided",
            key="exp-1",
            severity="error",
        )
