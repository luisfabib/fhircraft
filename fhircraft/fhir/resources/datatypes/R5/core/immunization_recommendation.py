from pydantic import Field, model_validator
from typing import Optional, List

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    DateTime,
    Markdown,
)

from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Reference,
    BackboneElement,
    CodeableConcept,
)
from .resource import Resource
from .domain_resource import DomainResource


class ImmunizationRecommendationRecommendationDateCriterion(BackboneElement):
    """
    Vaccine date recommendations.  For example, earliest date to administer, latest date to administer, etc.
    """

    code: Optional[CodeableConcept] = Field(
        description="Type of date",
        default=None,
    )
    value: Optional[DateTime] = Field(
        description="Recommended date",
        default=None,
    )
    value_ext: Optional[Element] = Field(
        description="Placeholder element for value extensions",
        default=None,
        alias="_value",
    )


class ImmunizationRecommendationRecommendation(BackboneElement):
    """
    Vaccine administration recommendations.
    """

    vaccineCode: Optional[List[CodeableConcept]] = Field(
        description="Vaccine  or vaccine group recommendation applies to",
        default=None,
    )
    targetDisease: Optional[List[CodeableConcept]] = Field(
        description="Disease to be immunized against",
        default=None,
    )
    contraindicatedVaccineCode: Optional[List[CodeableConcept]] = Field(
        description="Vaccine which is contraindicated to fulfill the recommendation",
        default=None,
    )
    forecastStatus: Optional[CodeableConcept] = Field(
        description="Vaccine recommendation status",
        default=None,
    )
    forecastReason: Optional[List[CodeableConcept]] = Field(
        description="Vaccine administration status reason",
        default=None,
    )
    dateCriterion: Optional[
        List[ImmunizationRecommendationRecommendationDateCriterion]
    ] = Field(
        description="Dates governing proposed immunization",
        default=None,
    )
    description: Optional[Markdown] = Field(
        description="Protocol details",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    series: Optional[String] = Field(
        description="Name of vaccination series",
        default=None,
    )
    series_ext: Optional[Element] = Field(
        description="Placeholder element for series extensions",
        default=None,
        alias="_series",
    )
    doseNumber: Optional[String] = Field(
        description="Recommended dose number within series",
        default=None,
    )
    doseNumber_ext: Optional[Element] = Field(
        description="Placeholder element for doseNumber extensions",
        default=None,
        alias="_doseNumber",
    )
    seriesDoses: Optional[String] = Field(
        description="Recommended number of doses for immunity",
        default=None,
    )
    seriesDoses_ext: Optional[Element] = Field(
        description="Placeholder element for seriesDoses extensions",
        default=None,
        alias="_seriesDoses",
    )
    supportingImmunization: Optional[List[Reference]] = Field(
        description="Past immunizations supporting recommendation",
        default=None,
    )
    supportingPatientInformation: Optional[List[Reference]] = Field(
        description="Patient observations supporting recommendation",
        default=None,
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

    identifier: Optional[List[Identifier]] = Field(
        description="Business identifier",
        default=None,
    )
    patient: Optional[Reference] = Field(
        description="Who this profile is for",
        default=None,
    )
    date: Optional[DateTime] = Field(
        description="Date recommendation(s) created",
        default=None,
    )
    date_ext: Optional[Element] = Field(
        description="Placeholder element for date extensions",
        default=None,
        alias="_date",
    )
    authority: Optional[Reference] = Field(
        description="Who is responsible for protocol",
        default=None,
    )
    recommendation: Optional[List[ImmunizationRecommendationRecommendation]] = Field(
        description="Vaccine administration recommendations",
        default=None,
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
