from typing import List, Optional

from pydantic import Field, field_validator, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R5.complex import (
    DataType,
    HumanName,
    Period,
    Reference,
    CodeableConcept,
    ContactPoint,
    Address,
)


class ExtendedContactDetail(DataType):
    """
    Contact information
    """

    purpose: Optional[CodeableConcept] = Field(
        description="The type of contact",
        default=None,
    )
    name: Optional[List["HumanName"]] = Field(
        description="Name of an individual to contact",
        default=None,
    )
    telecom: Optional[List[ContactPoint]] = Field(
        description="Contact details (e.g.phone/fax/url)",
        default=None,
    )
    address: Optional[Address] = Field(
        description="Address for the contact",
        default=None,
    )
    organization: Optional["Reference"] = Field(
        description="This contact detail is handled/monitored by a specific organization",
        default=None,
    )
    period: Optional["Period"] = Field(
        description="Period that this contact was valid for usage",
        default=None,
    )

    @field_validator(
        *(
            "period",
            "organization",
            "address",
            "telecom",
            "name",
            "purpose",
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

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )
