import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    DateTime,
    PositiveInt,
)

from fhircraft.fhir.resources.datatypes.R4B.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
)
from .resource import Resource
from .domain_resource import DomainResource


class ImmunizationEvaluation(DomainResource):
    """
    Describes a comparison of an immunization event against published recommendations to determine if the administration is "valid" in relation to those  recommendations.
    """

    _abstract = False
    _type = "ImmunizationEvaluation"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/ImmunizationEvaluation"

    contained: Optional[ListType[Resource]] = Field(
        description="Contained, inline Resources",
        default=None,
    )
    extension: Optional[ListType[Extension]] = Field(
        description="Additional content defined by implementations",
        default=None,
    )
    modifierExtension: Optional[ListType[Extension]] = Field(
        description="Extensions that cannot be ignored",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Business identifier",
        default=None,
    )
    status: Optional[Code] = Field(
        description="completed | entered-in-error",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    patient: Optional[Reference] = Field(
        description="Who this evaluation is for",
        default=None,
    )
    date: Optional[DateTime] = Field(
        description="Date evaluation was performed",
        default=None,
    )
    date_ext: Optional[Element] = Field(
        description="Placeholder element for date extensions",
        default=None,
        alias="_date",
    )
    authority: Optional[Reference] = Field(
        description="Who is responsible for publishing the recommendations",
        default=None,
    )
    targetDisease: Optional[CodeableConcept] = Field(
        description="Evaluation target disease",
        default=None,
    )
    immunizationEvent: Optional[Reference] = Field(
        description="Immunization being evaluated",
        default=None,
    )
    doseStatus: Optional[CodeableConcept] = Field(
        description="Status of the dose relative to published recommendations",
        default=None,
    )
    doseStatusReason: Optional[ListType[CodeableConcept]] = Field(
        description="Reason for the dose status",
        default=None,
    )
    description: Optional[String] = Field(
        description="Evaluation notes",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    series: Optional[String] = Field(
        description="Name of vaccine series",
        default=None,
    )
    series_ext: Optional[Element] = Field(
        description="Placeholder element for series extensions",
        default=None,
        alias="_series",
    )
    doseNumberPositiveInt: Optional[PositiveInt] = Field(
        description="Dose number within series",
        default=None,
    )
    doseNumberPositiveInt_ext: Optional[Element] = Field(
        description="Placeholder element for doseNumberPositiveInt extensions",
        default=None,
        alias="_doseNumberPositiveInt",
    )
    doseNumberString: Optional[String] = Field(
        description="Dose number within series",
        default=None,
    )
    doseNumberString_ext: Optional[Element] = Field(
        description="Placeholder element for doseNumberString extensions",
        default=None,
        alias="_doseNumberString",
    )
    seriesDosesPositiveInt: Optional[PositiveInt] = Field(
        description="Recommended number of doses for immunity",
        default=None,
    )
    seriesDosesPositiveInt_ext: Optional[Element] = Field(
        description="Placeholder element for seriesDosesPositiveInt extensions",
        default=None,
        alias="_seriesDosesPositiveInt",
    )
    seriesDosesString: Optional[String] = Field(
        description="Recommended number of doses for immunity",
        default=None,
    )
    seriesDosesString_ext: Optional[Element] = Field(
        description="Placeholder element for seriesDosesString extensions",
        default=None,
        alias="_seriesDosesString",
    )

    @property
    def doseNumber(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="doseNumber",
        )

    @property
    def seriesDoses(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="seriesDoses",
        )

    @model_validator(mode="after")
    def doseNumber_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[PositiveInt, String],
            field_name_base="doseNumber",
            required=False,
        )

    @model_validator(mode="after")
    def seriesDoses_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[PositiveInt, String],
            field_name_base="seriesDoses",
            required=False,
        )
