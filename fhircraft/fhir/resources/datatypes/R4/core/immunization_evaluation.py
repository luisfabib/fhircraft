import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)


import fhircraft.fhir.resources.datatypes.R4.primitive as fhir
from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
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
    status: Optional[fhir.code] = Field(
        description="completed | entered-in-error",
        default=None,
    )
    patient: Optional[Reference] = Field(
        description="Who this evaluation is for",
        default=None,
    )
    date: Optional[fhir.dateTime] = Field(
        description="Date evaluation was performed",
        default=None,
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
    description: Optional[fhir.string] = Field(
        description="Evaluation notes",
        default=None,
    )
    series: Optional[fhir.string] = Field(
        description="Name of vaccine series",
        default=None,
    )
    doseNumberPositiveInt: Optional[fhir.positiveInt] = Field(
        description="Dose number within series",
        default=None,
    )
    doseNumberString: Optional[fhir.string] = Field(
        description="Dose number within series",
        default=None,
    )
    seriesDosesPositiveInt: Optional[fhir.positiveInt] = Field(
        description="Recommended number of doses for immunity",
        default=None,
    )
    seriesDosesString: Optional[fhir.string] = Field(
        description="Recommended number of doses for immunity",
        default=None,
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
            field_types=[fhir.positiveInt, fhir.string],
            field_name_base="doseNumber",
            required=False,
        )

    @model_validator(mode="after")
    def seriesDoses_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.positiveInt, fhir.string],
            field_name_base="seriesDoses",
            required=False,
        )
