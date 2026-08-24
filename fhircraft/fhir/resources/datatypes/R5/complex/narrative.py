from typing import List, Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
import fhircraft.fhir.resources.datatypes.R5.primitive as fhir
from fhircraft.fhir.resources.datatypes.R5.complex import DataType, Element

class Narrative(DataType):
    """
    Human-readable summary of the resource (essential clinical and business information)
    """

    _type = "Narrative"

    status: fhir.code = Field(
        description="generated | extensions | additional | empty",
    )
    div: str = Field(
        description="Limited xhtml content",
    )

    @model_validator(mode="after")
    def FHIR_txt_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("div",),
            expression="htmlChecks()",
            human="The narrative SHALL contain only the basic html formatting elements and attributes described in chapters 7-11 (except section 4 of chapter 9) and 15 of the HTML 4.0 standard, <a> elements (either name or href), images and internally contained style attributes",
            key="txt-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_txt_2_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("div",),
            expression="htmlChecks()",
            human="The narrative SHALL have some non-whitespace content",
            key="txt-2",
            severity="error",
        )
