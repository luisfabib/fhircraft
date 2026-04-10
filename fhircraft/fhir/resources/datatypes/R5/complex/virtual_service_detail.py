from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
import fhircraft.fhir.resources.datatypes.R5.primitive as fhir
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
    addressUrl: Optional[fhir.url] = Field(
        description="Contact address/number",
        default=None,
    )
    addressString: Optional[fhir.string] = Field(
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
    additionalInfo: Optional[List[fhir.url]] = Field(
        description="Address to see alternative connection details",
        default=None,
    )
    maxParticipants: Optional[fhir.positiveInt] = Field(
        description="Maximum number of participants supported by the virtual service",
        default=None,
    )
    sessionKey: Optional[fhir.string] = Field(
        description="Session Key required by the virtual service",
        default=None,
    )

    @model_validator(mode="after")
    def address_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.url, fhir.string, ContactPoint, "ExtendedContactDetail"],
            field_name_base="address",
        )

    @property
    def address(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="address",
        )
