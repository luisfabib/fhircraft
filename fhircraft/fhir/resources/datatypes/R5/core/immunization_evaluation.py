from pydantic import Field, model_validator
from typing import Optional, List as ListType

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
        description="The vaccine preventable disease schedule being evaluated",
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
        description="Reason why the doese is considered valid, invalid or some other status",
        default=None,
    )
    description: Optional[Markdown] = Field(
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
    doseNumber: Optional[String] = Field(
        description="Dose number within series",
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
