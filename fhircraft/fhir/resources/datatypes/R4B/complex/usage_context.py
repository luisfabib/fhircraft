from typing import List, Optional

from pydantic import Field, field_validator, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R4B.complex import (
    Element,
    CodeableConcept,
    Coding,
    Quantity,
    Range,
    Reference,
)


class UsageContext(Element):
    """
    Describes the context of use for a conformance or knowledge resource
    """

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

    @field_validator(*("code", "extension"), mode="after", check_fields=None)
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
    def value_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=["CodeableConcept", "Quantity", "Range", "Reference"],
            field_name_base="value",
        )

    @property
    def value(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="value",
        )
