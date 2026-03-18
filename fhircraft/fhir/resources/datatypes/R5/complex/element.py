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
    extension: Optional[List["Extension"]] = Field(
        description="Additional content defined by implementations",
        default=None,
    )
