from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from ..primitive import *
from fhircraft.fhir.resources.datatypes.R4.complex import Element, ContactPoint

class ContactDetail(Element):
    """
    Contact information
    """

    _type = "ContactDetail"

    name: Optional[String] = Field(
        description="Name of an individual to contact",
        default=None,
    )
    telecom: Optional[List[ContactPoint]] = Field(
        description="Contact details for individual or organization",
        default=None,
    )
