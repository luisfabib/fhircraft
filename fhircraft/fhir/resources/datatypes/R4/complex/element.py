from typing import List, Optional, TYPE_CHECKING

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.base import FHIRBaseModel

if TYPE_CHECKING:
    from fhircraft.fhir.resources.datatypes.R4 import Extension


class Element(FHIRBaseModel):
    """
    Base for all elements
    """

    _fhir_release = "R4"
    _type = "Element"
    _kind = "complex-type"

    id: Optional[str] = Field(
        description="Unique id for inter-element referencing",
        default=None,
    )
    extension: Optional[List["Extension"]] = Field(
        description="Additional content defined by implementations",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(list(self.__class__.model_fields.keys())),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )
