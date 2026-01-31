from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R5.complex import Element, ContactDetail


class Contributor(Element):
    """
    Contributor information
    """

    _type = "Contributor"

    type: Optional[Code] = Field(
        description="author | editor | reviewer | endorser",
        default=None,
    )
    type_ext: Optional[Element] = Field(
        description="Placeholder element for type extensions",
        default=None,
        alias="_type",
    )
    name: Optional[String] = Field(
        description="Who contributed the content",
        default=None,
    )
    name_ext: Optional[Element] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    contact: Optional[List[ContactDetail]] = Field(
        description="Contact details of the contributor",
        default=None,
    )
