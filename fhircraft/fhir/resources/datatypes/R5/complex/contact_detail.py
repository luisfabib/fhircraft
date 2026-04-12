from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
import fhircraft.fhir.resources.datatypes.R5.primitive as fhir
from fhircraft.fhir.resources.datatypes.R5.complex import ContactPoint, Element

class ContactDetail(Element):
    """
    Contact information
    """

    _type = "ContactDetail"

    name: Optional[fhir.string] = Field(
        description="Name of an individual to contact",
        default=None,
    )
    telecom: Optional[List[ContactPoint]] = Field(
        description="Contact details for individual or organization",
        default=None,
    )
