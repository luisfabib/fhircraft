from typing import Optional

from pydantic import Field, field_validator, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *

from .codeable_concept import CodeableConcept
from .element import Element
from .backbone_element import BackboneElement
from .period import Period


class MarketingStatus(BackboneElement):
    """
    The marketing status describes the date when a medicinal product is actually put on the market or the date as of which it is no longer available
    """

    country: Optional[CodeableConcept] = Field(
        description="The country in which the marketing authorisation has been granted shall be specified It should be specified using the ISO 3166 \u2011 1 alpha-2 code elements",
        default=None,
    )
    jurisdiction: Optional[CodeableConcept] = Field(
        description="Where a Medicines Regulatory Agency has granted a marketing authorisation for which specific provisions within a jurisdiction apply, the jurisdiction can be specified using an appropriate controlled terminology The controlled term and the controlled term identifier shall be specified",
        default=None,
    )
    status: Optional[CodeableConcept] = Field(
        description="This attribute provides information on the status of the marketing of the medicinal product See ISO/TS 20443 for more information and examples",
        default=None,
    )
    dateRange: Optional[Period] = Field(
        description="The date when the Medicinal Product is placed on the market by the Marketing Authorisation Holder (or where applicable, the manufacturer/distributor) in a country and/or jurisdiction shall be provided A complete date consisting of day, month and year shall be specified using the ISO 8601 date format NOTE \u201cPlaced on the market\u201d refers to the release of the Medicinal Product into the distribution chain",
        default=None,
    )
    restoreDate: Optional[DateTime] = Field(
        description="The date when the Medicinal Product is placed on the market by the Marketing Authorisation Holder (or where applicable, the manufacturer/distributor) in a country and/or jurisdiction shall be provided A complete date consisting of day, month and year shall be specified using the ISO 8601 date format NOTE \u201cPlaced on the market\u201d refers to the release of the Medicinal Product into the distribution chain",
        default=None,
    )
    restoreDate_ext: Optional[Element] = Field(
        description="Placeholder element for restoreDate extensions",
        default=None,
        alias="_restoreDate",
    )

    @field_validator(
        *(
            "restoreDate",
            "dateRange",
            "status",
            "jurisdiction",
            "country",
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
