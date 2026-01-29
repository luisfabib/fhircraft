from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    CodeableConcept,
    Reference,
    BackboneElement,
    Coding,
    Period,
    Duration,
)


class DataRequirementCodeFilter(BackboneElement):
    """
    What codes are expected
    """

    _type = "BackboneElement"

    path: Optional[String] = Field(
        description="A code-valued attribute to filter on",
        default=None,
    )
    path_ext: Optional[Element] = Field(
        description="Placeholder element for path extensions",
        default=None,
        alias="_path",
    )
    searchParam: Optional[String] = Field(
        description="A search parameter defined on the specified type",
        default=None,
    )
    searchParam_ext: Optional[Element] = Field(
        description="Placeholder element for searchParam extensions",
        default=None,
        alias="_searchParam",
    )
    valueSet: Optional[Canonical] = Field(
        description="The valueset for the filter",
        default=None,
    )
    valueSet_ext: Optional[Element] = Field(
        description="Placeholder element for valueSet extensions",
        default=None,
        alias="_valueSet",
    )
    code: Optional[List[Coding]] = Field(
        description="What code is expected",
        default=None,
    )


class DataRequirementDateFilter(BackboneElement):
    """
    What dates/date ranges are expected
    """

    _type = "BackboneElement"

    path: Optional[String] = Field(
        description="A date-valued attribute to filter on",
        default=None,
    )
    path_ext: Optional[Element] = Field(
        description="Placeholder element for path extensions",
        default=None,
        alias="_path",
    )
    searchParam: Optional[String] = Field(
        description="A date-valued parameter to search on",
        default=None,
    )
    searchParam_ext: Optional[Element] = Field(
        description="Placeholder element for searchParam extensions",
        default=None,
        alias="_searchParam",
    )
    valueDateTime: Optional[DateTime] = Field(
        description="The value of the filter, as a dateTime",
        default=None,
    )
    valueDateTime_ext: Optional[Element] = Field(
        description="Placeholder element for valueDateTime extensions",
        default=None,
        alias="_valueDateTime",
    )
    valuePeriod: Optional[Period] = Field(
        description="The value of the filter, as a period",
        default=None,
    )
    valueDuration: Optional[Duration] = Field(
        description="The value of the filter, as a duration",
        default=None,
    )

    @model_validator(mode="after")
    def value_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=["DateTime", "Period", "Duration"],
            field_name_base="value",
        )

    @property
    def value(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="value",
        )


class DataRequirementSort(BackboneElement):
    """
    Order of the results
    """

    _type = "BackboneElement"

    path: Optional[String] = Field(
        description="The name of the attribute to perform the sort",
        default=None,
    )
    path_ext: Optional[Element] = Field(
        description="Placeholder element for path extensions",
        default=None,
        alias="_path",
    )
    direction: Optional[Code] = Field(
        description="The direction of the sort, ascending or descending",
        default=None,
    )
    direction_ext: Optional[Element] = Field(
        description="Placeholder element for direction extensions",
        default=None,
        alias="_direction",
    )


class DataRequirement(Element):
    """
    Describes a required data item
    """

    _type = "DataRequirement"

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
    profile_ext: Optional[List[Optional[Element]]] = Field(
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
    mustSupport_ext: Optional[List[Optional[Element]]] = Field(
        description="Placeholder element for mustSupport extensions",
        default=None,
        alias="_mustSupport",
    )
    codeFilter: Optional[List[DataRequirementCodeFilter]] = Field(
        description="What codes are expected",
        default=None,
    )
    dateFilter: Optional[List[DataRequirementDateFilter]] = Field(
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
    sort: Optional[List[DataRequirementSort]] = Field(
        description="Order of the results",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "sort",
                "limit",
                "dateFilter",
                "codeFilter",
                "mustSupport",
                "profile",
                "type",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ext_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("extension",),
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_drq_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("codeFilter",),
            expression="path.exists() xor searchParam.exists()",
            human="Either a path or a searchParam must be provided, but not both",
            key="drq-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_drq_2_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("dateFilter",),
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
