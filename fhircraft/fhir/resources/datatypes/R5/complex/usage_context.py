from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
import fhircraft.fhir.resources.datatypes.R5.primitive as fhir
from fhircraft.fhir.resources.datatypes.R5.complex import (
    DataType,
    Coding,
    CodeableConcept,
    Quantity,
    Range,
    Reference,
)


class UsageContext(DataType):
    """
    Describes the context of use for a conformance or knowledge resource
    """

    _type = "UsageContext"

    code: Optional[Coding] = Field(
        description="Type of context being specified",
        default=None,
    )
    valueCodeableConcept: Optional[CodeableConcept] = Field(
        description="Value that defines the context",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="Value that defines the context",
        default=None,
    )
    valueRange: Optional[Range] = Field(
        description="Value that defines the context",
        default=None,
    )
    valueReference: Optional[Reference] = Field(
        description="Value that defines the context",
        default=None,
    )

    @model_validator(mode="after")
    def value_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[CodeableConcept, Quantity, Range, Reference],
            field_name_base="value",
        )

    @property
    def value(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="value",
        )
