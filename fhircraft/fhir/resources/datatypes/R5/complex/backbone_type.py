from typing import List, Optional, TYPE_CHECKING

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *

from fhircraft.fhir.resources.datatypes.R5.complex import Element

if TYPE_CHECKING:
    from fhircraft.fhir.resources.datatypes.R5.complex import Extension


class BackboneType(Element):
    """
    Base for datatypes that can carry modifier extensions
    """

    _type = "BackboneType"

    modifierExtension: Optional[List["Extension"]] = Field(
        description="Extensions that cannot be ignored even if unrecognized",
        default=None,
    )
