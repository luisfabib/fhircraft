from pydantic import Field, model_validator
from typing import Optional, List

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    Canonical,
    DateTime,
)

from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    CodeableReference,
    Annotation,
    DataRequirement,
)
from .resource import Resource
from .domain_resource import DomainResource


class GuidanceResponse(DomainResource):
    """
    A guidance response is the formal response to a guidance request, including any output parameters returned by the evaluation, as well as the description of any proposed actions to be taken.
    """

    _abstract = False
    _type = "GuidanceResponse"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/GuidanceResponse"

    requestIdentifier: Optional[Identifier] = Field(
        description="The identifier of the request associated with this response, if any",
        default=None,
    )
    identifier: Optional[List[Identifier]] = Field(
        description="Business identifier",
        default=None,
    )
    moduleUri: Optional[Uri] = Field(
        description="What guidance was requested",
        default=None,
    )
    moduleUri_ext: Optional[Element] = Field(
        description="Placeholder element for moduleUri extensions",
        default=None,
        alias="_moduleUri",
    )
    moduleCanonical: Optional[Canonical] = Field(
        description="What guidance was requested",
        default=None,
    )
    moduleCanonical_ext: Optional[Element] = Field(
        description="Placeholder element for moduleCanonical extensions",
        default=None,
        alias="_moduleCanonical",
    )
    moduleCodeableConcept: Optional[CodeableConcept] = Field(
        description="What guidance was requested",
        default=None,
    )
    status: Optional[Code] = Field(
        description="success | data-requested | data-required | in-progress | failure | entered-in-error",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    subject: Optional[Reference] = Field(
        description="Patient the request was performed for",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="Encounter during which the response was returned",
        default=None,
    )
    occurrenceDateTime: Optional[DateTime] = Field(
        description="When the guidance response was processed",
        default=None,
    )
    occurrenceDateTime_ext: Optional[Element] = Field(
        description="Placeholder element for occurrenceDateTime extensions",
        default=None,
        alias="_occurrenceDateTime",
    )
    performer: Optional[Reference] = Field(
        description="Device returning the guidance",
        default=None,
    )
    reason: Optional[List[CodeableReference]] = Field(
        description="Why guidance is needed",
        default=None,
    )
    note: Optional[List[Annotation]] = Field(
        description="Additional notes about the response",
        default=None,
    )
    evaluationMessage: Optional[Reference] = Field(
        description="Messages resulting from the evaluation of the artifact or artifacts",
        default=None,
    )
    outputParameters: Optional[Reference] = Field(
        description="The output parameters of the evaluation, if any",
        default=None,
    )
    result: Optional[List[Reference]] = Field(
        description="Proposed actions, if any",
        default=None,
    )
    dataRequirement: Optional[List[DataRequirement]] = Field(
        description="Additional required data",
        default=None,
    )

    @property
    def module(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="module",
        )

    @model_validator(mode="after")
    def module_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Uri, Canonical, CodeableConcept],
            field_name_base="module",
            required=True,
        )
