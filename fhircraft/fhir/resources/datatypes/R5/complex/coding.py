from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
import fhircraft.fhir.resources.datatypes.R5.primitive as fhir
from fhircraft.fhir.resources.datatypes.R5.complex import Element


class Coding(Element):
    """
    A reference to a code defined by a terminology system
    """

    _type = "Coding"

    system: Optional[fhir.uri] = Field(
        description="Identity of the terminology system",
        default=None,
    )
    version: Optional[fhir.string] = Field(
        description="Version of the system - if relevant",
        default=None,
    )
    code: Optional[fhir.code] = Field(
        description="Symbol in syntax defined by the system",
        default=None,
    )
    display: Optional[fhir.string] = Field(
        description="Representation defined by the system",
        default=None,
    )
    userSelected: Optional[fhir.boolean] = Field(
        description="If this coding was chosen directly by the user",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_cod_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="code.exists().not() implies display.exists().not()",
            human="A Coding SHOULD NOT have a display unless a code is also present.  Computation on Coding.display alone is generally unsafe.  Consider using CodeableConcept.text",
            key="cod-1",
            severity="warning",
        )
