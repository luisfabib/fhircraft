from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators


import fhircraft.fhir.resources.datatypes.R5.primitive as fhir
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
    targetDisease: Optional[ListType[CodeableConcept]] = Field(
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
    description: Optional[fhir.markdown] = Field(
        description="Protocol details",
        default=None,
    )
    series: Optional[fhir.string] = Field(
        description="Name of vaccination series",
        default=None,
    )
    doseNumber: Optional[fhir.string] = Field(
        description="Recommended dose number within series",
        default=None,
    )
    seriesDoses: Optional[fhir.string] = Field(
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


class ImmunizationRecommendation(DomainResource):
    """
    A patient's point-in-time set of recommendations (i.e. forecasting) according to a published schedule with optional supporting justification.
    """

    _abstract = False
    _type = "ImmunizationRecommendation"
    _canonical_url = (
        "http://hl7.org/fhir/StructureDefinition/ImmunizationRecommendation"
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
