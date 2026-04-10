from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
import fhircraft.fhir.resources.datatypes.R5.primitive as fhir
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

    _type = "ExtendedContactDetail"

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
