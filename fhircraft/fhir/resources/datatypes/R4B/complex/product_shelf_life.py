from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
import fhircraft.fhir.resources.datatypes.R4B.primitive as fhir
from fhircraft.fhir.resources.datatypes.R4B.complex import (
    BackboneElement,
    CodeableConcept,
    Identifier,
    Quantity,
)

class ProductShelfLife(BackboneElement):
    """
    The shelf-life and storage information for a medicinal product item or container can be described using this class
    """

    _type = "ProductShelfLife"

    identifier: Optional[Identifier] = Field(
        description="Unique identifier for the packaged Medicinal Product",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="This describes the shelf life, taking into account various scenarios such as shelf life of the packaged Medicinal Product itself, shelf life after transformation where necessary and shelf life after the first opening of a bottle, etc. The shelf life type shall be specified using an appropriate controlled vocabulary The controlled term and the controlled term identifier shall be specified",
        default=None,
    )
    period: Optional[Quantity] = Field(
        description="The shelf life time period can be specified using a numerical value for the period of time and its unit of time measurement The unit of measurement shall be specified in accordance with ISO 11240 and the resulting terminology The symbol and the symbol identifier shall be used",
        default=None,
    )
    specialPrecautionsForStorage: Optional[List[CodeableConcept]] = Field(
        description="Special precautions for storage, if any, can be specified using an appropriate controlled vocabulary The controlled term and the controlled term identifier shall be specified",
        default=None,
    )
