from typing import List, Optional, TYPE_CHECKING

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.base import FHIRBaseModel
from ..primitive import *
from fhircraft.fhir.resources.datatypes.R4.complex import Element, Reference

class Annotation(Element):
    """
    Text node with attribution
    """

    _type = "Annotation"

    authorReference: Optional["Reference"] = Field(
        description="Individual responsible for the annotation",
        default=None,
    )
    authorString: Optional[String] = Field(
        description="Individual responsible for the annotation",
        default=None,
    )
    time: Optional[DateTime] = Field(
        description="When the annotation was made",
        default=None,
    )
    text: Optional[Markdown] = Field(
        description="The annotation  - text content (as markdown)",
        default=None,
    )

    @model_validator(mode="after")
    def author_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=["Reference", String],
            field_name_base="author",
        )

    @property
    def author(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="author",
        )
