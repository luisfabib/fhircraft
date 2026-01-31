from pydantic import model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R5.complex import Element


class DataType(Element):
    """
    Reuseable Types
    """

    _type = "DataType"
