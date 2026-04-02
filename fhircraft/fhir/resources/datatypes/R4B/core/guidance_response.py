import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from ..primitive import *

from fhircraft.fhir.resources.datatypes.R4B.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
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
    requestIdentifier: Optional[Identifier] = Field(
        description="The identifier of the request associated with this response, if any",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Business identifier",
        default=None,
    )
    moduleUri: Optional[Uri] = Field(
        description="What guidance was requested",
        default=None,
    )
    moduleCanonical: Optional[Canonical] = Field(
        description="What guidance was requested",
        default=None,
    )
    moduleCodeableConcept: Optional[CodeableConcept] = Field(
        description="What guidance was requested",
        default=None,
    )
    status: Optional[Code] = Field(
        description="success | data-requested | data-required | in-progress | failure | entered-in-error",
        default=None,
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
    performer: Optional[Reference] = Field(
        description="Device returning the guidance",
        default=None,
    )
    reasonCode: Optional[ListType[CodeableConcept]] = Field(
        description="Why guidance is needed",
        default=None,
    )
    reasonReference: Optional[ListType[Reference]] = Field(
        description="Why guidance is needed",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Additional notes about the response",
        default=None,
    )
    evaluationMessage: Optional[ListType[Reference]] = Field(
        description="Messages resulting from the evaluation of the artifact or artifacts",
        default=None,
    )
    outputParameters: Optional[Reference] = Field(
        description="The output parameters of the evaluation, if any",
        default=None,
    )
    result: Optional[Reference] = Field(
        description="Proposed actions, if any",
        default=None,
    )
    dataRequirement: Optional[ListType[DataRequirement]] = Field(
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
