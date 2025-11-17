from typing import List, Optional

from pydantic import Field, field_validator, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *
from fhircraft.fhir.resources.datatypes.R5.complex import Element, DataType, Coding


class Meta(DataType):
    """
    Metadata about a resource
    """

    versionId: Optional[Id] = Field(
        description="Version specific identifier",
        default=None,
    )
    versionId_ext: Optional[Element] = Field(
        description="Placeholder element for versionId extensions",
        default=None,
        alias="_versionId",
    )
    lastUpdated: Optional[Instant] = Field(
        description="When the resource version last changed",
        default=None,
    )
    lastUpdated_ext: Optional[Element] = Field(
        description="Placeholder element for lastUpdated extensions",
        default=None,
        alias="_lastUpdated",
    )
    source: Optional[Uri] = Field(
        description="Identifies where the resource comes from",
        default=None,
    )
    source_ext: Optional[Element] = Field(
        description="Placeholder element for source extensions",
        default=None,
        alias="_source",
    )
    profile: Optional[List[Canonical]] = Field(
        description="Profiles this resource claims to conform to",
        default=None,
    )
    profile_ext: Optional[Element] = Field(
        description="Placeholder element for profile extensions",
        default=None,
        alias="_profile",
    )
    security: Optional[List[Coding]] = Field(
        description="Security Labels applied to this resource",
        default=None,
    )
    tag: Optional[List[Coding]] = Field(
        description="Tags applied to this resource",
        default=None,
    )

    @field_validator(
        *(
            "tag",
            "security",
            "profile",
            "source",
            "lastUpdated",
            "versionId",
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
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )
