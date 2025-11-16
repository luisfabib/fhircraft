from typing import List, Optional, TYPE_CHECKING

from pydantic import Field, field_validator, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.base import FHIRBaseModel
from fhircraft.fhir.resources.datatypes.primitives import *

if TYPE_CHECKING:
    from fhircraft.fhir.resources.datatypes.R4B.complex import Extension


class Element(FHIRBaseModel):
    """
    Base for all elements
    """

    id: Optional[String] = Field(
        description="Unique id for inter-element referencing",
        default=None,
    )
    id_ext: Optional["Element"] = Field(
        description="Placeholder element for id extensions",
        default=None,
        alias="_id",
    )
    extension: Optional[List["Extension"]] = Field(
        description="Additional content defined by implementations",
        default=None,
    )

    @field_validator(*("extension",), mode="after", check_fields=None)
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
