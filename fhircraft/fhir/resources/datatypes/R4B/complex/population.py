from typing import Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from ..primitive import *
from fhircraft.fhir.resources.datatypes.R4B.complex import (
    BackboneElement,
    CodeableConcept,
    Range,
)

class Population(BackboneElement):
    """
    A definition of a set of people that apply to some clinically related context, for example people contraindicated for a certain medication
    """

    _type = "Population"

    ageRange: Optional[Range] = Field(
        description="The age of the specific population",
        default=None,
    )
    ageCodeableConcept: Optional[CodeableConcept] = Field(
        description="The age of the specific population",
        default=None,
    )
    gender: Optional[CodeableConcept] = Field(
        description="The gender of the specific population",
        default=None,
    )
    race: Optional[CodeableConcept] = Field(
        description="Race of the specific population",
        default=None,
    )
    physiologicalCondition: Optional[CodeableConcept] = Field(
        description="The existing physiological conditions of the specific population to which this applies",
        default=None,
    )

    @model_validator(mode="after")
    def age_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=["Range", "CodeableConcept"],
            field_name_base="age",
        )

    @property
    def age(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="age",
        )
