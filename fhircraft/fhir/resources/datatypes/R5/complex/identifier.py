from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
import fhircraft.fhir.resources.datatypes.R5.primitive as fhir
from fhircraft.fhir.resources.datatypes.R5.complex import (
    DataType,
    Element,
    Period,
    Reference,
    CodeableConcept,
)

class Identifier(DataType):
    """
    An identifier intended for computation
    """

    _type = "Identifier"

    use: Optional[fhir.code] = Field(
        description="usual | official | temp | secondary | old (If known)",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Description of identifier",
        default=None,
    )
    system: Optional[fhir.uri] = Field(
        description="The namespace for the identifier value",
        default=None,
    )
    value: Optional[fhir.string] = Field(
        description="The value that is unique",
        default=None,
    )
    period: Optional[Period] = Field(
        description="time period when id is/was valid for use",
        default=None,
    )
    assigner: Optional[Reference] = Field(
        description="Organization that issued id (may be just text)",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ident_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="value.exists()",
            human="Identifier with no value has limited utility.  If communicating that an identifier value has been suppressed or missing, the value element SHOULD be present with an extension indicating the missing semantic - e.g. data-absent-reason",
            key="ident-1",
            severity="warning",
        )
