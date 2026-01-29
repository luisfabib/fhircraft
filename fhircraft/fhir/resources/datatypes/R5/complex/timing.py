from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R5.complex import (
    BackboneType,
    Element,
    CodeableConcept,
    Period,
    Range,
    Duration,
)


class TimingRepeat(BackboneType):
    """
    When the event is to occur
    """

    _type = "BackboneType"

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
    count: Optional[PositiveInt] = Field(
        description="Number of times to repeat",
        default=None,
    )
    count_ext: Optional[Element] = Field(
        description="Placeholder element for count extensions",
        default=None,
        alias="_count",
    )
    countMax: Optional[PositiveInt] = Field(
        description="Maximum number of times to repeat",
        default=None,
    )
    countMax_ext: Optional[Element] = Field(
        description="Placeholder element for countMax extensions",
        default=None,
        alias="_countMax",
    )
    duration: Optional[Decimal] = Field(
        description="How long when it happens",
        default=None,
    )
    duration_ext: Optional[Element] = Field(
        description="Placeholder element for duration extensions",
        default=None,
        alias="_duration",
    )
    durationMax: Optional[Decimal] = Field(
        description="How long when it happens",
        default=None,
    )
    durationMax_ext: Optional[Element] = Field(
        description="Placeholder element for durationMax extensions",
        default=None,
        alias="_durationMax",
    )
    durationUnit: Optional[Code] = Field(
        description="s | min | h | d | wk | mo | a",
        default=None,
    )
    durationUnit_ext: Optional[Element] = Field(
        description="Placeholder element for durationUnit extensions",
        default=None,
        alias="_durationUnit",
    )
    frequency: Optional[PositiveInt] = Field(
        description="Event occurs frequency times per period",
        default=None,
    )
    frequency_ext: Optional[Element] = Field(
        description="Placeholder element for frequency extensions",
        default=None,
        alias="_frequency",
    )
    frequencyMax: Optional[PositiveInt] = Field(
        description="Event occurs up to frequencyMax times per period",
        default=None,
    )
    frequencyMax_ext: Optional[Element] = Field(
        description="Placeholder element for frequencyMax extensions",
        default=None,
        alias="_frequencyMax",
    )
    period: Optional[Decimal] = Field(
        description="Event occurs frequency times per period",
        default=None,
    )
    period_ext: Optional[Element] = Field(
        description="Placeholder element for period extensions",
        default=None,
        alias="_period",
    )
    periodMax: Optional[Decimal] = Field(
        description="Event occurs up to periodMax times per period",
        default=None,
    )
    periodMax_ext: Optional[Element] = Field(
        description="Placeholder element for periodMax extensions",
        default=None,
        alias="_periodMax",
    )
    periodUnit: Optional[Code] = Field(
        description="s | min | h | d | wk | mo | a",
        default=None,
    )
    periodUnit_ext: Optional[Element] = Field(
        description="Placeholder element for periodUnit extensions",
        default=None,
        alias="_periodUnit",
    )
    dayOfWeek: Optional[List[Code]] = Field(
        description="mon | tue | wed | thu | fri | sat | sun",
        default=None,
    )
    dayOfWeek_ext: Optional[Element] = Field(
        description="Placeholder element for dayOfWeek extensions",
        default=None,
        alias="_dayOfWeek",
    )
    timeOfDay: Optional[List[Time]] = Field(
        description="Specified time of day for action",
        default=None,
    )
    timeOfDay_ext: Optional[Element] = Field(
        description="Placeholder element for timeOfDay extensions",
        default=None,
        alias="_timeOfDay",
    )
    when: Optional[List[Code]] = Field(
        description="Code for time period of occurrence",
        default=None,
    )
    when_ext: Optional[Element] = Field(
        description="Placeholder element for when extensions",
        default=None,
        alias="_when",
    )
    offset: Optional[UnsignedInt] = Field(
        description="Minutes from event (before or after)",
        default=None,
    )
    offset_ext: Optional[Element] = Field(
        description="Placeholder element for offset extensions",
        default=None,
        alias="_offset",
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


class Timing(BackboneType):
    """
    A timing schedule that specifies an event that may occur multiple times
    """

    _type = "Timing"

    event: Optional[List[DateTime]] = Field(
        description="When the event occurs",
        default=None,
    )
    event_ext: Optional[List[Optional[Element]]] = Field(
        description="Placeholder element for event extensions",
        default=None,
        alias="_event",
    )
    repeat: Optional[TimingRepeat] = Field(
        description="When the event is to occur",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="C | BID | TID | QID | AM | PM | QD | QOD | +",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "code",
                "repeat",
                "event",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ext_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "modifierExtension",
                "extension",
            ),
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
            severity="error",
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
            expression="offset.empty() or (when.exists() and when.select($this in ('C' | 'CM' | 'CD' | 'CV')).allFalse())",
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

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )
