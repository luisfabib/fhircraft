from typing import Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R5.complex import Element, Reference


class Annotation(Element):
    """
    Text node with attribution
    """

    _type = "Annotation"

    authorReference: Optional[Reference] = Field(
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
    time_ext: Optional[Element] = Field(
        description="Placeholder element for time extensions",
        default=None,
        alias="_time",
    )
    text: Optional[Markdown] = Field(
        description="The annotation  - text content (as markdown)",
        default=None,
    )
    text_ext: Optional[Element] = Field(
        description="Placeholder element for text extensions",
        default=None,
        alias="_text",
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "text",
                "time",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ext_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("extension",),
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
            severity="error",
        )

    @model_validator(mode="after")
    def author_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Reference, String],
            field_name_base="author",
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

    @property
    def author(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="author",
        )
