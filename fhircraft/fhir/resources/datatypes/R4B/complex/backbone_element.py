from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R4B.complex import Element, Extension


class BackboneElement(Element):
    """
    Base for elements defined inside a resource
    """

    _type = "BackboneElement"

    _fhir_release = "R4B"

    modifierExtension: Optional[List[Extension]] = Field(
        description="Extensions that cannot be ignored even if unrecognized",
        default=None,
    )
