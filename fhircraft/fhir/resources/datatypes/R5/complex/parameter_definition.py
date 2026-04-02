from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from ..primitive import *
from fhircraft.fhir.resources.datatypes.R5.complex import Element, DataType

class ParameterDefinition(DataType):
    """
    Definition of a parameter to a module
    """

    _type = "ParameterDefinition"

    name: Optional[Code] = Field(
        description="Name used to access the parameter value",
        default=None,
    )
    use: Optional[Code] = Field(
        description="in | out",
        default=None,
    )
    min: Optional[Integer] = Field(
        description="Minimum cardinality",
        default=None,
    )
    max: Optional[String] = Field(
        description="Maximum cardinality (a number of *)",
        default=None,
    )
    documentation: Optional[String] = Field(
        description="A brief description of the parameter",
        default=None,
    )
    type: Optional[Code] = Field(
        description="What type of value",
        default=None,
    )
    profile: Optional[Canonical] = Field(
        description="What profile the value is expected to be",
        default=None,
    )
