from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R5.complex import (
    BackboneType,
    Duration,
    CodeableConcept,
)


class ProductShelfLife(BackboneType):
    """
    The shelf-life and storage information for a medicinal product item or container can be described using this class
    """

    _type = "ProductShelfLife"

    type: Optional[CodeableConcept] = Field(
        description="This describes the shelf life, taking into account various scenarios such as shelf life of the packaged Medicinal Product itself, shelf life after transformation where necessary and shelf life after the first opening of a bottle, etc. The shelf life type shall be specified using an appropriate controlled vocabulary The controlled term and the controlled term identifier shall be specified",
        default=None,
    )
    periodDuration: Optional[Duration] = Field(
        description="The shelf life time period can be specified using a numerical value for the period of time and its unit of time measurement The unit of measurement shall be specified in accordance with ISO 11240 and the resulting terminology The symbol and the symbol identifier shall be used",
        default=None,
    )
    periodString: Optional[String] = Field(
        description="The shelf life time period can be specified using a numerical value for the period of time and its unit of time measurement The unit of measurement shall be specified in accordance with ISO 11240 and the resulting terminology The symbol and the symbol identifier shall be used",
        default=None,
    )
    specialPrecautionsForStorage: Optional[List[CodeableConcept]] = Field(
        description="Special precautions for storage, if any, can be specified using an appropriate controlled vocabulary The controlled term and the controlled term identifier shall be specified",
        default=None,
    )

    @model_validator(mode="after")
    def period_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Duration, String],
            field_name_base="period",
        )

    @property
    def period(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="period",
        )
