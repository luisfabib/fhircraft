from typing import List, Optional

from pydantic import Field, field_validator, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R5.complex import (
    BackboneType,
    Element,
    CodeableConcept,
)


class Timing(BackboneType):
    """
    A timing schedule that specifies an event that may occur multiple times
    """

    event: Optional[List[DateTime]] = Field(
        description="When the event occurs",
        default=None,
    )
    event_ext: Optional[Element] = Field(
        description="Placeholder element for event extensions",
        default=None,
        alias="_event",
    )
    repeat: Optional[Element] = Field(
        description="When the event is to occur",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="C | BID | TID | QID | AM | PM | QD | QOD | +",
        default=None,
    )

    @field_validator(
        *(
            "code",
            "repeat",
            "event",
            "modifierExtension",
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

    @field_validator(
        *("modifierExtension", "extension"), mode="after", check_fields=None
    )
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

    @field_validator(*("repeat",), mode="after", check_fields=None)
    @classmethod
    def FHIR_tim_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="duration.empty() or durationUnit.exists()",
            human="if there's a duration, there needs to be duration units",
            key="tim-1",
            severity="error",
        )

    @field_validator(*("repeat",), mode="after", check_fields=None)
    @classmethod
    def FHIR_tim_2_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="period.empty() or periodUnit.exists()",
            human="if there's a period, there needs to be period units",
            key="tim-2",
            severity="error",
        )

    @field_validator(*("repeat",), mode="after", check_fields=None)
    @classmethod
    def FHIR_tim_4_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="duration.exists() implies duration >= 0",
            human="duration SHALL be a non-negative value",
            key="tim-4",
            severity="error",
        )

    @field_validator(*("repeat",), mode="after", check_fields=None)
    @classmethod
    def FHIR_tim_5_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="period.exists() implies period >= 0",
            human="period SHALL be a non-negative value",
            key="tim-5",
            severity="error",
        )

    @field_validator(*("repeat",), mode="after", check_fields=None)
    @classmethod
    def FHIR_tim_6_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="periodMax.empty() or period.exists()",
            human="If there's a periodMax, there must be a period",
            key="tim-6",
            severity="error",
        )

    @field_validator(*("repeat",), mode="after", check_fields=None)
    @classmethod
    def FHIR_tim_7_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="durationMax.empty() or duration.exists()",
            human="If there's a durationMax, there must be a duration",
            key="tim-7",
            severity="error",
        )

    @field_validator(*("repeat",), mode="after", check_fields=None)
    @classmethod
    def FHIR_tim_8_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="countMax.empty() or count.exists()",
            human="If there's a countMax, there must be a count",
            key="tim-8",
            severity="error",
        )

    @field_validator(*("repeat",), mode="after", check_fields=None)
    @classmethod
    def FHIR_tim_9_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="offset.empty() or (when.exists() and when.select($this in ('C' | 'CM' | 'CD' | 'CV')).allFalse())",
            human="If there's an offset, there must be a when (and not C, CM, CD, CV)",
            key="tim-9",
            severity="error",
        )

    @field_validator(*("repeat",), mode="after", check_fields=None)
    @classmethod
    def FHIR_tim_10_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="timeOfDay.empty() or when.empty()",
            human="If there's a timeOfDay, there cannot be a when, or vice versa",
            key="tim-10",
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
