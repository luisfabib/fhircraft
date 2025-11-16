from typing import List, Optional

from pydantic import Field, field_validator, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *

from .coding import Coding
from .element import Element
from .reference import Reference


class Signature(Element):
    """
    A Signature - XML DigSig, JWS, Graphical image of signature, etc.
    """

    type: Optional[List[Coding]] = Field(
        description="Indication of the reason the entity signed the object(s)",
        default=None,
    )
    when: Optional[Instant] = Field(
        description="When the signature was created",
        default=None,
    )
    when_ext: Optional[Element] = Field(
        description="Placeholder element for when extensions",
        default=None,
        alias="_when",
    )
    who: Optional[Reference] = Field(
        description="Who signed",
        default=None,
    )
    onBehalfOf: Optional[Reference] = Field(
        description="The party represented",
        default=None,
    )
    targetFormat: Optional[Code] = Field(
        description="The technical format of the signed resources",
        default=None,
    )
    targetFormat_ext: Optional[Element] = Field(
        description="Placeholder element for targetFormat extensions",
        default=None,
        alias="_targetFormat",
    )
    sigFormat: Optional[Code] = Field(
        description="The technical format of the signature",
        default=None,
    )
    sigFormat_ext: Optional[Element] = Field(
        description="Placeholder element for sigFormat extensions",
        default=None,
        alias="_sigFormat",
    )
    data: Optional[Base64Binary] = Field(
        description="The actual signature content (XML DigSig. JWS, picture, etc.)",
        default=None,
    )
    data_ext: Optional[Element] = Field(
        description="Placeholder element for data extensions",
        default=None,
        alias="_data",
    )

    @field_validator(
        *(
            "data",
            "sigFormat",
            "targetFormat",
            "onBehalfOf",
            "who",
            "when",
            "type",
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
