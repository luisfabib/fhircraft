from typing import List, Optional

from pydantic import Field, field_validator, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    CodeableConcept,
    Reference,
)


class DataRequirement(Element):
    """
    Describes a required data item
    """

    type: Optional[Code] = Field(
        description="The type of the required data",
        default=None,
    )
    type_ext: Optional[Element] = Field(
        description="Placeholder element for type extensions",
        default=None,
        alias="_type",
    )
    profile: Optional[List[Canonical]] = Field(
        description="The profile of the required data",
        default=None,
    )
    profile_ext: Optional[Element] = Field(
        description="Placeholder element for profile extensions",
        default=None,
        alias="_profile",
    )
    subjectCodeableConcept: Optional["CodeableConcept"] = Field(
        description="E.g. Patient, Practitioner, RelatedPerson, Organization, Location, Device",
        default=None,
    )
    subjectReference: Optional["Reference"] = Field(
        description="E.g. Patient, Practitioner, RelatedPerson, Organization, Location, Device",
        default=None,
    )
    mustSupport: Optional[List[String]] = Field(
        description="Indicates specific structure elements that are referenced by the knowledge module",
        default=None,
    )
    mustSupport_ext: Optional[Element] = Field(
        description="Placeholder element for mustSupport extensions",
        default=None,
        alias="_mustSupport",
    )
    codeFilter: Optional[List[Element]] = Field(
        description="What codes are expected",
        default=None,
    )
    dateFilter: Optional[List[Element]] = Field(
        description="What dates/date ranges are expected",
        default=None,
    )
    limit: Optional[PositiveInt] = Field(
        description="Number of results",
        default=None,
    )
    limit_ext: Optional[Element] = Field(
        description="Placeholder element for limit extensions",
        default=None,
        alias="_limit",
    )
    sort: Optional[List[Element]] = Field(
        description="Order of the results",
        default=None,
    )

    @field_validator(
        *(
            "sort",
            "limit",
            "dateFilter",
            "codeFilter",
            "mustSupport",
            "profile",
            "type",
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

    @field_validator(*("extension",), mode="after", check_fields=None)
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

    @field_validator(*("codeFilter",), mode="after", check_fields=None)
    @classmethod
    def FHIR_drq_1_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="path.exists() xor searchParam.exists()",
            human="Either a path or a searchParam must be provided, but not both",
            key="drq-1",
            severity="error",
        )

    @field_validator(*("dateFilter",), mode="after", check_fields=None)
    @classmethod
    def FHIR_drq_2_constraint_validator(cls, value):
        return fhir_validators.validate_element_constraint(
            cls,
            value,
            expression="path.exists() xor searchParam.exists()",
            human="Either a path or a searchParam must be provided, but not both",
            key="drq-2",
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
    def subject_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=["CodeableConcept", "Reference"],
            field_name_base="subject",
        )

    @property
    def subject(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="subject",
        )
