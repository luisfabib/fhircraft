from pydantic import Field, model_validator
from typing import Optional

NoneType = type(None)
import fhircraft.fhir.resources.validators as fhir_validators

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    Base64Binary,
)

from fhircraft.fhir.resources.datatypes.R4B.complex import (
    Element,
    Meta,
    Reference,
)
from .resource import Resource


class Binary(Resource):
    """
    A resource that represents the data of a single raw artifact as digital content accessible in its native format.  A Binary resource can contain any content, whether text, image, pdf, zip archive, etc.
    """

    _abstract = False
    _type = "Binary"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Binary"

    contentType: Optional[Code] = Field(
        description="MimeType of the binary content",
        default=None,
    )
    contentType_ext: Optional[Element] = Field(
        description="Placeholder element for contentType extensions",
        default=None,
        alias="_contentType",
    )
    securityContext: Optional[Reference] = Field(
        description="Identifies another resource to use as proxy when enforcing access control",
        default=None,
    )
    data: Optional[Base64Binary] = Field(
        description="The actual content",
        default=None,
    )
    data_ext: Optional[Element] = Field(
        description="Placeholder element for data extensions",
        default=None,
        alias="_data",
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "data",
                "securityContext",
                "contentType",
                "language",
                "implicitRules",
                "meta",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )
