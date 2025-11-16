from typing import List, Optional

from pydantic import Field, field_validator, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *

from .backbone_element import BackboneElement
from .codeable_concept import CodeableConcept
from .identifier import Identifier
from .quantity import Quantity


class ProductShelfLife(BackboneElement):
    """
    The shelf-life and storage information for a medicinal product item or container can be described using this class
    """

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

    @field_validator(
        *(
            "specialPrecautionsForStorage",
            "period",
            "type",
            "identifier",
            "modifierExtension",
            "extension",
        ),
        mode="after",
        check_fields=None,
    )
    @classmethod
    def FHIR_ele_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @field_validator(
        *("modifierExtension", "extension"), mode="after", check_fields=None
    )
    @classmethod
    def FHIR_ext_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )
