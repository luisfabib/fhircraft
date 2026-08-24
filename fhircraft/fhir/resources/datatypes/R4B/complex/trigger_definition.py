from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
import fhircraft.fhir.resources.datatypes.R4B.primitive as fhir
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

    _type = "TriggerDefinition"

    type: fhir.code = Field(
        description="named-event | periodic | data-changed | data-added | data-modified | data-removed | data-accessed | data-access-ended",
    )
    name: Optional[fhir.string] = Field(
        description="Name or URI that identifies the event",
        default=None,
    )
    timingTiming: Optional[Timing] = Field(
        description="Timing of the event",
        default=None,
    )
    timingReference: Optional[Reference] = Field(
        description="Timing of the event",
        default=None,
    )
    timingDate: Optional[fhir.date_] = Field(
        description="Timing of the event",
        default=None,
    )
    timingDateTime: Optional[fhir.dateTime] = Field(
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

    @model_validator(mode="after")
    def FHIR_trd_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="data.empty() or timing.empty()",
            human="Either timing, or a data requirement, but not both",
            key="trd-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_trd_2_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="condition.exists() implies data.exists()",
            human="A condition only if there is a data requirement",
            key="trd-2",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_trd_3_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(type = 'named-event' implies name.exists()) and (type = 'periodic' implies timing.exists()) and (type.startsWith('data-') implies data.exists())",
            human="A named event requires a name, a periodic event requires timing, and a data event requires data",
            key="trd-3",
            severity="error",
        )

    @model_validator(mode="after")
    def timing_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=["Timing", "Reference", fhir.Date, fhir.DateTime],
            field_name_base="timing",
        )

    @property
    def timing(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="timing",
        )
