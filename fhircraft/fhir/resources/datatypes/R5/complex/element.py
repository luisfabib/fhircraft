from typing import List, Optional, TYPE_CHECKING

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *

from fhircraft.fhir.resources.datatypes.R5.complex import Base

if TYPE_CHECKING:
    from fhircraft.fhir.resources.datatypes.R5.complex import Extension


class Element(Base):
    """
    Base for all elements
    """

    _abstract = False
    _kind = "complex-type"
    _type = "Element"

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

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("extension",),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ext_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("extension",),
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
