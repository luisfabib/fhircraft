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
    BackboneElement,
)
from .resource import Resource
from .domain_resource import DomainResource


class ImmunizationRecommendationRecommendationDateCriterion(BackboneElement):
    """
    Vaccine date recommendations.  For example, earliest date to administer, latest date to administer, etc.
    """

    code: CodeableConcept = Field(
        description="Type of date",
    )
    value: fhir.dateTime = Field(
        description="Recommended date",
    )


class ImmunizationRecommendationRecommendation(BackboneElement):
    """
    Vaccine administration recommendations.
    """

    vaccineCode: Optional[ListType[CodeableConcept]] = Field(
        description="Vaccine  or vaccine group recommendation applies to",
        default=None,
    )
    targetDisease: Optional[CodeableConcept] = Field(
        description="Disease to be immunized against",
        default=None,
    )
    contraindicatedVaccineCode: Optional[ListType[CodeableConcept]] = Field(
        description="Vaccine which is contraindicated to fulfill the recommendation",
        default=None,
    )
    forecastStatus: CodeableConcept = Field(
        description="Vaccine recommendation status",
    )
    forecastReason: Optional[ListType[CodeableConcept]] = Field(
        description="Vaccine administration status reason",
        default=None,
    )
    dateCriterion: Optional[
        ListType[ImmunizationRecommendationRecommendationDateCriterion]
    ] = Field(
        description="Dates governing proposed immunization",
        default=None,
    )
    description: Optional[fhir.string] = Field(
        description="Protocol details",
        default=None,
    )
    series: Optional[fhir.string] = Field(
        description="Name of vaccination series",
        default=None,
    )
    doseNumberPositiveInt: Optional[fhir.positiveInt] = Field(
        description="Recommended dose number within series",
        default=None,
    )
    doseNumberString: Optional[fhir.string] = Field(
        description="Recommended dose number within series",
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
    supportingImmunization: Optional[ListType[Reference]] = Field(
        description="Past immunizations supporting recommendation",
        default=None,
    )
    supportingPatientInformation: Optional[ListType[Reference]] = Field(
        description="Patient observations supporting recommendation",
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
            field_types=[fhir.PositiveInt, fhir.String],
            field_name_base="doseNumber",
            required=False,
        )

    @model_validator(mode="after")
    def seriesDoses_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.PositiveInt, fhir.String],
            field_name_base="seriesDoses",
            required=False,
        )


class ImmunizationRecommendation(DomainResource):
    """
    A patient's point-in-time set of recommendations (i.e. forecasting) according to a published schedule with optional supporting justification.
    """

    _abstract = False
    _type = "ImmunizationRecommendation"
    _canonical_url = (
        "http://hl7.org/fhir/StructureDefinition/ImmunizationRecommendation"
    )

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
    patient: Reference = Field(
        description="Who this profile is for",
    )
    date: fhir.dateTime = Field(
        description="Date recommendation(s) created",
    )
    authority: Optional[Reference] = Field(
        description="Who is responsible for protocol",
        default=None,
    )
    recommendation: ListType[ImmunizationRecommendationRecommendation] = (
        Field(
            description="Vaccine administration recommendations",
         	min_length=1,
	)
    )

    @model_validator(mode="after")
    def FHIR_imr_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("recommendation",),
            expression="vaccineCode.exists() or targetDisease.exists()",
            human="One of vaccineCode or targetDisease SHALL be present",
            key="imr-1",
            severity="error",
        )
