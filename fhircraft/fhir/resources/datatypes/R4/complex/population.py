from typing import Optional

from pydantic import Field, field_validator, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *

from .backbone_element import BackboneElement
from .codeable_concept import CodeableConcept
from .range import Range


class Population(BackboneElement):
    """
    A definition of a set of people that apply to some clinically related context, for example people contraindicated for a certain medication
    """

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

    @field_validator(
        *(
            "physiologicalCondition",
            "race",
            "gender",
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
