from typing import List, Optional, TYPE_CHECKING

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.base import FHIRBaseModel

if TYPE_CHECKING:
    from fhircraft.fhir.resources.datatypes.R4B.complex import Extension


class Element(FHIRBaseModel):
    """
    Base for all elements
    """

    _type = "Element"
    _kind = "complex-type"
    _fhir_release = "R4B"

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
        return fhir_validators.validate_model_constraint(
            self,
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )
