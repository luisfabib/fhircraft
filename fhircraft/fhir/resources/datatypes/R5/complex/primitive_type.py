from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R5.complex.data_type import DataType


class PrimitiveType(DataType):
    """
    Parent type for DataTypes with a simple value
    """

    _type = "PrimitiveType"
