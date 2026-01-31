from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R4B.complex import Element, ContactPoint


class ContactDetail(Element):
    """
    Contact information
    """

    _type = "ContactDetail"

    name: Optional[String] = Field(
        description="Name of an individual to contact",
        default=None,
    )
    name_ext: Optional[Element] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    telecom: Optional[List[ContactPoint]] = Field(
        description="Contact details for individual or organization",
        default=None,
    )
