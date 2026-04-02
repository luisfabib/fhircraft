from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from ..primitive import *
from fhircraft.fhir.resources.datatypes.R4B.complex import Element, ContactDetail

class Contributor(Element):
    """
    Contributor information
    """

    _type = "Contributor"

    type: Optional[Code] = Field(
        description="author | editor | reviewer | endorser",
        default=None,
    )
    name: Optional[String] = Field(
        description="Who contributed the content",
        default=None,
    )
    contact: Optional[List[ContactDetail]] = Field(
        description="Contact details of the contributor",
        default=None,
    )
