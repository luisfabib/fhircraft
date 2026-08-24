from typing import Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
import fhircraft.fhir.resources.datatypes.R4B.primitive as fhir
from fhircraft.fhir.resources.datatypes.R4B.complex import Element, Reference

class Annotation(Element):
    """
    Text node with attribution
    """

    _type = "Annotation"

    authorReference: Optional[Reference] = Field(
        description="Individual responsible for the annotation",
        default=None,
    )
    authorString: Optional[fhir.string] = Field(
        description="Individual responsible for the annotation",
        default=None,
    )
    time: Optional[fhir.dateTime] = Field(
        description="When the annotation was made",
        default=None,
    )
    text: fhir.markdown = Field(
        description="The annotation  - text content (as markdown)",
    )

    @model_validator(mode="after")
    def author_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=["Reference", fhir.String],
            field_name_base="author",
        )

    @property
    def author(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="author",
        )
