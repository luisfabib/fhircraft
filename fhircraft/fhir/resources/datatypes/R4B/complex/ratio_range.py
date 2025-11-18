from typing import Optional

from pydantic import Field, field_validator, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R4B.complex import Element, Quantity


class RatioRange(Element):
    """
    Range of ratio values
    """

    lowNumerator: Optional[Quantity] = Field(
        description="Low Numerator limit",
        default=None,
    )
    highNumerator: Optional[Quantity] = Field(
        description="High Numerator limit",
        default=None,
    )
    denominator: Optional[Quantity] = Field(
        description="Denominator value",
        default=None,
    )

    @field_validator(
        *(
            "denominator",
            "highNumerator",
            "lowNumerator",
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
    def FHIR_inv_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="((lowNumerator.exists() or highNumerator.exists()) and denominator.exists()) or (lowNumerator.empty() and highNumerator.empty() and denominator.empty() and extension.exists())",
            human="One of lowNumerator or highNumerator and denominator SHALL be present, or all are absent. If all are absent, there SHALL be some extension present",
            key="inv-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_inv_2_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="lowNumerator.empty() or highNumerator.empty() or (lowNumerator <= highNumerator)",
            human="If present, lowNumerator SHALL have a lower value than highNumerator",
            key="inv-2",
            severity="error",
        )
