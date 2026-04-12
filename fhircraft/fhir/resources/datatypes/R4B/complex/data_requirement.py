from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
import fhircraft.fhir.resources.datatypes.R4B.primitive as fhir
from fhircraft.fhir.resources.datatypes.R4B.complex import (
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

    path: Optional[fhir.string] = Field(
        description="A code-valued attribute to filter on",
        default=None,
    )
    searchParam: Optional[fhir.string] = Field(
        description="A search parameter defined on the specified type",
        default=None,
    )
    valueSet: Optional[fhir.canonical] = Field(
        description="The valueset for the filter",
        default=None,
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

    path: Optional[fhir.string] = Field(
        description="A date-valued attribute to filter on",
        default=None,
    )
    searchParam: Optional[fhir.string] = Field(
        description="A date-valued parameter to search on",
        default=None,
    )
    valueDateTime: Optional[fhir.dateTime] = Field(
        description="The value of the filter, as a dateTime",
        default=None,
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
            field_types=["dateTime", "Period", "Duration"],
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

    path: Optional[fhir.string] = Field(
        description="The name of the attribute to perform the sort",
        default=None,
    )
    direction: Optional[fhir.code] = Field(
        description="The direction of the sort, ascending or descending",
        default=None,
    )


class DataRequirement(Element):
    """
    Describes a required data item
    """

    _type = "DataRequirement"

    type: Optional[fhir.code] = Field(
        description="The type of the required data",
        default=None,
    )
    profile: Optional[List[fhir.canonical]] = Field(
        description="The profile of the required data",
        default=None,
    )
    subjectCodeableConcept: Optional[CodeableConcept] = Field(
        description="E.g. Patient, Practitioner, RelatedPerson, Organization, Location, Device",
        default=None,
    )
    subjectReference: Optional[Reference] = Field(
        description="E.g. Patient, Practitioner, RelatedPerson, Organization, Location, Device",
        default=None,
    )
    mustSupport: Optional[List[fhir.string]] = Field(
        description="Indicates specific structure elements that are referenced by the knowledge module",
        default=None,
    )
    codeFilter: Optional[List[DataRequirementCodeFilter]] = Field(
        description="What codes are expected",
        default=None,
    )
    dateFilter: Optional[List[DataRequirementDateFilter]] = Field(
        description="What dates/date ranges are expected",
        default=None,
    )
    limit: Optional[fhir.positiveInt] = Field(
        description="Number of results",
        default=None,
    )
    sort: Optional[List[DataRequirementSort]] = Field(
        description="Order of the results",
        default=None,
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
