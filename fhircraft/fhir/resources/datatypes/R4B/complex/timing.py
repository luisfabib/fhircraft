from typing import List, Optional, TYPE_CHECKING

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
import fhircraft.fhir.resources.datatypes.R4B.primitive as fhir
from fhircraft.fhir.resources.datatypes.R4B.complex import (
    BackboneElement,
    CodeableConcept,
    Element,
    Period,
    Range,
    Duration,
)


class TimingRepeat(BackboneElement):
    """
    When the event is to occur
    """

    _type = "BackboneElement"

    boundsDuration: Optional["Duration"] = Field(
        description="Length/Range of lengths, or (Start and/or end) limits",
        default=None,
    )
    boundsRange: Optional["Range"] = Field(
        description="Length/Range of lengths, or (Start and/or end) limits",
        default=None,
    )
    boundsPeriod: Optional["Period"] = Field(
        description="Length/Range of lengths, or (Start and/or end) limits",
        default=None,
    )
    count: Optional[fhir.positiveInt] = Field(
        description="Number of times to repeat",
        default=None,
    )
    countMax: Optional[fhir.positiveInt] = Field(
        description="Maximum number of times to repeat",
        default=None,
    )
    duration: Optional[fhir.decimal] = Field(
        description="How long when it happens",
        default=None,
    )
    durationMax: Optional[fhir.decimal] = Field(
        description="How long when it happens",
        default=None,
    )
    durationUnit: Optional[fhir.code] = Field(
        description="s | min | h | d | wk | mo | a",
        default=None,
    )
    frequency: Optional[fhir.positiveInt] = Field(
        description="Event occurs frequency times per period",
        default=None,
    )
    frequencyMax: Optional[fhir.positiveInt] = Field(
        description="Event occurs up to frequencyMax times per period",
        default=None,
    )
    period: Optional[fhir.decimal] = Field(
        description="Event occurs frequency times per period",
        default=None,
    )
    periodMax: Optional[fhir.decimal] = Field(
        description="Event occurs up to periodMax times per period",
        default=None,
    )
    periodUnit: Optional[fhir.code] = Field(
        description="s | min | h | d | wk | mo | a",
        default=None,
    )
    dayOfWeek: Optional[List[fhir.code]] = Field(
        description="mon | tue | wed | thu | fri | sat | sun",
        default=None,
    )
    timeOfDay: Optional[List[fhir.time_]] = Field(
        description="Specified time of day for action",
        default=None,
    )
    when: Optional[List[fhir.code]] = Field(
        description="code for time period of occurrence",
        default=None,
    )
    offset: Optional[fhir.unsignedInt] = Field(
        description="Minutes from event (before or after)",
        default=None,
    )

    @model_validator(mode="after")
    def bounds_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=["Duration", "Range", "Period"],
            field_name_base="bounds",
        )

    @property
    def bounds(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="bounds",
        )


class Timing(BackboneElement):
    """
    A timing schedule that specifies an event that may occur multiple times
    """

    _type = "Timing"

    event: Optional[List[fhir.dateTime]] = Field(
        description="When the event occurs",
        default=None,
    )
    repeat: Optional[TimingRepeat] = Field(
        description="When the event is to occur",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="BID | TID | QID | AM | PM | QD | QOD | +",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_tim_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("repeat",),
            expression="duration.empty() or durationUnit.exists()",
            human="if there's a duration, there needs to be duration units",
            key="tim-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_tim_2_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("repeat",),
            expression="period.empty() or periodUnit.exists()",
            human="if there's a period, there needs to be period units",
            key="tim-2",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_tim_4_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("repeat",),
            expression="duration.exists() implies duration >= 0",
            human="duration SHALL be a non-negative value",
            key="tim-4",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_tim_5_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("repeat",),
            expression="period.exists() implies period >= 0",
            human="period SHALL be a non-negative value",
            key="tim-5",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_tim_6_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("repeat",),
            expression="periodMax.empty() or period.exists()",
            human="If there's a periodMax, there must be a period",
            key="tim-6",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_tim_7_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("repeat",),
            expression="durationMax.empty() or duration.exists()",
            human="If there's a durationMax, there must be a duration",
            key="tim-7",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_tim_8_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("repeat",),
            expression="countMax.empty() or count.exists()",
            human="If there's a countMax, there must be a count",
            key="tim-8",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_tim_9_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("repeat",),
            expression="offset.empty() or (when.exists() and ((when in ('C' | 'CM' | 'CD' | 'CV')).not()))",
            human="If there's an offset, there must be a when (and not C, CM, CD, CV)",
            key="tim-9",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_tim_10_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("repeat",),
            expression="timeOfDay.empty() or when.empty()",
            human="If there's a timeOfDay, there cannot be a when, or vice versa",
            key="tim-10",
            severity="error",
        )
