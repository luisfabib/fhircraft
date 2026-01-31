from typing import List, Optional

from pydantic import Field, model_validator

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

    _type = "VirtualServiceDetail"

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
    additionalInfo_ext: Optional[List[Optional[Element]]] = Field(
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
