from typing import List, Optional

from pydantic import Field, field_validator, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R4B.complex import (
    DataRequirement,
    Element,
    Expression,
    Reference,
    Timing,
)


class TriggerDefinition(Element):
    """
    Defines an expected trigger for a module
    """

    type: Optional[Code] = Field(
        description="named-event | periodic | data-changed | data-added | data-modified | data-removed | data-accessed | data-access-ended",
        default=None,
    )
    type_ext: Optional[Element] = Field(
        description="Placeholder element for type extensions",
        default=None,
        alias="_type",
    )
    name: Optional[String] = Field(
        description="Name or URI that identifies the event",
        default=None,
    )
    name_ext: Optional[Element] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    timingTiming: Optional[Timing] = Field(
        description="Timing of the event",
        default=None,
    )
    timingReference: Optional[Reference] = Field(
        description="Timing of the event",
        default=None,
    )
    timingDate: Optional[Date] = Field(
        description="Timing of the event",
        default=None,
    )
    timingDateTime: Optional[DateTime] = Field(
        description="Timing of the event",
        default=None,
    )
    data: Optional[List[DataRequirement]] = Field(
        description="Triggering data of the event (multiple = \u0027and\u0027)",
        default=None,
    )
    condition: Optional[Expression] = Field(
        description="Whether the event triggers (boolean expression)",
        default=None,
    )

    @field_validator(
        *(
            "condition",
            "data",
            "name",
            "type",
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
    def timing_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=["Timing", "Reference", Date, DateTime],
            field_name_base="timing",
        )

    @model_validator(mode="after")
    def FHIR_trd_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="data.empty() or timing.empty()",
            human="Either timing, or a data requirement, but not both",
            key="trd-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_trd_2_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="condition.exists() implies data.exists()",
            human="A condition only if there is a data requirement",
            key="trd-2",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_trd_3_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(type = 'named-event' implies name.exists()) and (type = 'periodic' implies timing.exists()) and (type.startsWith('data-') implies data.exists())",
            human="A named event requires a name, a periodic event requires timing, and a data event requires data",
            key="trd-3",
            severity="error",
        )

    @property
    def timing(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="timing",
        )
