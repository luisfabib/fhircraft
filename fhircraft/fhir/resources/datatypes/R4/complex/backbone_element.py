from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators

from ..primitive import *
from .element import Element
from .extension import Extension

class BackboneElement(Element):
    """
    Base for elements defined inside a resource
    """

    _fhir_release = "R4"
    _type = "BackboneElement"

    modifierExtension: Optional[List[Extension]] = Field(
        description="Extensions that cannot be ignored even if unrecognized",
        default=None,
    )
