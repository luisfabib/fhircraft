from typing import List, Optional

from pydantic import Field, field_validator, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *

from .attachment import Attachment
from .codeable_concept import CodeableConcept
from .element import Element
from .backbone_element import BackboneElement
from .quantity import Quantity


class ProdCharacteristic(BackboneElement):
    """
    The marketing status describes the date when a medicinal product is actually put on the market or the date as of which it is no longer available
    """

    height: Optional[Quantity] = Field(
        description="Where applicable, the height can be specified using a numerical value and its unit of measurement The unit of measurement shall be specified in accordance with ISO 11240 and the resulting terminology The symbol and the symbol identifier shall be used",
        default=None,
    )
    width: Optional[Quantity] = Field(
        description="Where applicable, the width can be specified using a numerical value and its unit of measurement The unit of measurement shall be specified in accordance with ISO 11240 and the resulting terminology The symbol and the symbol identifier shall be used",
        default=None,
    )
    depth: Optional[Quantity] = Field(
        description="Where applicable, the depth can be specified using a numerical value and its unit of measurement The unit of measurement shall be specified in accordance with ISO 11240 and the resulting terminology The symbol and the symbol identifier shall be used",
        default=None,
    )
    weight: Optional[Quantity] = Field(
        description="Where applicable, the weight can be specified using a numerical value and its unit of measurement The unit of measurement shall be specified in accordance with ISO 11240 and the resulting terminology The symbol and the symbol identifier shall be used",
        default=None,
    )
    nominalVolume: Optional[Quantity] = Field(
        description="Where applicable, the nominal volume can be specified using a numerical value and its unit of measurement The unit of measurement shall be specified in accordance with ISO 11240 and the resulting terminology The symbol and the symbol identifier shall be used",
        default=None,
    )
    externalDiameter: Optional[Quantity] = Field(
        description="Where applicable, the external diameter can be specified using a numerical value and its unit of measurement The unit of measurement shall be specified in accordance with ISO 11240 and the resulting terminology The symbol and the symbol identifier shall be used",
        default=None,
    )
    shape: Optional[String] = Field(
        description="Where applicable, the shape can be specified An appropriate controlled vocabulary shall be used The term and the term identifier shall be used",
        default=None,
    )
    shape_ext: Optional[Element] = Field(
        description="Placeholder element for shape extensions",
        default=None,
        alias="_shape",
    )
    color: Optional[List[String]] = Field(
        description="Where applicable, the color can be specified An appropriate controlled vocabulary shall be used The term and the term identifier shall be used",
        default=None,
    )
    color_ext: Optional[Element] = Field(
        description="Placeholder element for color extensions",
        default=None,
        alias="_color",
    )
    imprint: Optional[List[String]] = Field(
        description="Where applicable, the imprint can be specified as text",
        default=None,
    )
    imprint_ext: Optional[Element] = Field(
        description="Placeholder element for imprint extensions",
        default=None,
        alias="_imprint",
    )
    image: Optional[List[Attachment]] = Field(
        description="Where applicable, the image can be provided The format of the image attachment shall be specified by regional implementations",
        default=None,
    )
    scoring: Optional[CodeableConcept] = Field(
        description="Where applicable, the scoring can be specified An appropriate controlled vocabulary shall be used The term and the term identifier shall be used",
        default=None,
    )

    @field_validator(
        *(
            "scoring",
            "image",
            "imprint",
            "color",
            "shape",
            "externalDiameter",
            "nominalVolume",
            "weight",
            "depth",
            "width",
            "height",
            "modifierExtension",
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

    @field_validator(
        *("modifierExtension", "extension"), mode="after", check_fields=None
    )
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
