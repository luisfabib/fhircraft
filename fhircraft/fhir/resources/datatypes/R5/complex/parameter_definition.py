from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
import fhircraft.fhir.resources.datatypes.R5.primitive as fhir
from fhircraft.fhir.resources.datatypes.R5.complex import Element, DataType

class ParameterDefinition(DataType):
    """
    Definition of a parameter to a module
    """

    _type = "ParameterDefinition"

    name: Optional[fhir.code] = Field(
        description="Name used to access the parameter value",
        default=None,
    )
    use: fhir.code = Field(
        description="in | out",
    )
    min: Optional[fhir.integer] = Field(
        description="Minimum cardinality",
        default=None,
    )
    max: Optional[fhir.string] = Field(
        description="Maximum cardinality (a number of *)",
        default=None,
    )
    documentation: Optional[fhir.string] = Field(
        description="A brief description of the parameter",
        default=None,
    )
    type: fhir.code = Field(
        description="What type of value",
    )
    profile: Optional[fhir.canonical] = Field(
        description="What profile the value is expected to be",
        default=None,
    )
