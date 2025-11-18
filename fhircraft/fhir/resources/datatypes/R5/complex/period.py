from typing import List, Optional

from pydantic import Field, field_validator, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R5.complex import DataType, Element


class Period(DataType):
    """
    Time range defined by start and end date/time
    """

    start: Optional[DateTime] = Field(
        description="Starting time with inclusive boundary",
        default=None,
    )
    start_ext: Optional[Element] = Field(
        description="Placeholder element for start extensions",
        default=None,
        alias="_start",
    )
    end: Optional[DateTime] = Field(
        description="End time with inclusive boundary, if not ongoing",
        default=None,
    )
    end_ext: Optional[Element] = Field(
        description="Placeholder element for end extensions",
        default=None,
        alias="_end",
    )

    @field_validator(
        *("end", "start", "extension", "extension"), mode="after", check_fields=None
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
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_per_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="start.hasValue().not() or end.hasValue().not() or (start.lowBoundary() <= end.highBoundary())",
            human="If present, start SHALL have a lower or equal value than end",
            key="per-1",
            severity="error",
        )
