from typing import Optional

from pydantic import Field, field_validator, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R4B.complex.element import Element


class ParameterDefinition(Element):
    """
    Definition of a parameter to a module
    """

    name: Optional[Code] = Field(
        description="Name used to access the parameter value",
        default=None,
    )
    name_ext: Optional[Element] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    use: Optional[Code] = Field(
        description="in | out",
        default=None,
    )
    use_ext: Optional[Element] = Field(
        description="Placeholder element for use extensions",
        default=None,
        alias="_use",
    )
    min: Optional[Integer] = Field(
        description="Minimum cardinality",
        default=None,
    )
    min_ext: Optional[Element] = Field(
        description="Placeholder element for min extensions",
        default=None,
        alias="_min",
    )
    max: Optional[String] = Field(
        description="Maximum cardinality (a number of *)",
        default=None,
    )
    max_ext: Optional[Element] = Field(
        description="Placeholder element for max extensions",
        default=None,
        alias="_max",
    )
    documentation: Optional[String] = Field(
        description="A brief description of the parameter",
        default=None,
    )
    documentation_ext: Optional[Element] = Field(
        description="Placeholder element for documentation extensions",
        default=None,
        alias="_documentation",
    )
    type: Optional[Code] = Field(
        description="What type of value",
        default=None,
    )
    type_ext: Optional[Element] = Field(
        description="Placeholder element for type extensions",
        default=None,
        alias="_type",
    )
    profile: Optional[Canonical] = Field(
        description="What profile the value is expected to be",
        default=None,
    )
    profile_ext: Optional[Element] = Field(
        description="Placeholder element for profile extensions",
        default=None,
        alias="_profile",
    )

    @field_validator(
        *(
            "profile",
            "type",
            "documentation",
            "max",
            "min",
            "use",
            "name",
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
            expression="hasValue() or (children().count() > id.count()) or $this is Parameters",
            human="All FHIR elements must have a @value or children unless an empty Parameters resource",
            key="ele-1",
            severity="error",
        )
