from typing import List, Optional

from pydantic import Field, field_validator, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R5.complex import Element


class Availability(Element):
    """
    Availability data for an {item}
    """

    availableTime: Optional[List[Element]] = Field(
        description="Times the {item} is available",
        default=None,
    )
    notAvailableTime: Optional[List[Element]] = Field(
        description="Not available during this time due to provided reason",
        default=None,
    )

    @field_validator(
        *("notAvailableTime", "availableTime", "extension"),
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

    @field_validator(*("availableTime",), mode="after", check_fields=None)
    @classmethod
    def FHIR_av_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="allDay.exists().not() or (allDay implies availableStartTime.exists().not() and availableEndTime.exists().not())",
            human="Cannot include start/end times when selecting all day availability.",
            key="av-1",
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
