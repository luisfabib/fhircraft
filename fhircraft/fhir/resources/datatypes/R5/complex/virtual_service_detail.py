from typing import List, Optional

from pydantic import Field, field_validator, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R5.complex import (
    DataType,
    Element,
    ExtendedContactDetail,
    Coding,
    ContactPoint,
)


class VirtualServiceDetail(DataType):
    """
    Virtual Service Contact Details
    """

    channelType: Optional[Coding] = Field(
        description="Channel Type",
        default=None,
    )
    addressUrl: Optional[Url] = Field(
        description="Contact address/number",
        default=None,
    )
    addressString: Optional[String] = Field(
        description="Contact address/number",
        default=None,
    )
    addressContactPoint: Optional[ContactPoint] = Field(
        description="Contact address/number",
        default=None,
    )
    addressExtendedContactDetail: Optional["ExtendedContactDetail"] = Field(
        description="Contact address/number",
        default=None,
    )
    additionalInfo: Optional[List[Url]] = Field(
        description="Address to see alternative connection details",
        default=None,
    )
    additionalInfo_ext: Optional[Element] = Field(
        description="Placeholder element for additionalInfo extensions",
        default=None,
        alias="_additionalInfo",
    )
    maxParticipants: Optional[PositiveInt] = Field(
        description="Maximum number of participants supported by the virtual service",
        default=None,
    )
    maxParticipants_ext: Optional[Element] = Field(
        description="Placeholder element for maxParticipants extensions",
        default=None,
        alias="_maxParticipants",
    )
    sessionKey: Optional[String] = Field(
        description="Session Key required by the virtual service",
        default=None,
    )
    sessionKey_ext: Optional[Element] = Field(
        description="Placeholder element for sessionKey extensions",
        default=None,
        alias="_sessionKey",
    )

    @field_validator(
        *(
            "sessionKey",
            "maxParticipants",
            "additionalInfo",
            "channelType",
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

    @model_validator(mode="after")
    def address_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Url, String, ContactPoint, "ExtendedContactDetail"],
            field_name_base="address",
        )

    @property
    def address(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="address",
        )
