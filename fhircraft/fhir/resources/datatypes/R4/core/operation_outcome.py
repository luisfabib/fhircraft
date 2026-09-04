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
    BackboneElement,
    CodeableConcept,
)
from .resource import Resource
from .domain_resource import DomainResource


class OperationOutcomeIssue(BackboneElement):
    """
    An error, warning, or information message that results from a system action.
    """

    severity: fhir.code = Field(
        description="fatal | error | warning | information",
    )
    code: fhir.code = Field(
        description="Error or warning code",
    )
    details: Optional[CodeableConcept] = Field(
        description="Additional details about the error",
        default=None,
    )
    diagnostics: Optional[fhir.string] = Field(
        description="Additional diagnostic information about the issue",
        default=None,
    )
    location: Optional[ListType[fhir.string]] = Field(
        description="Deprecated: Path of element(s) related to issue",
        default=None,
    )
    expression: Optional[ListType[fhir.string]] = Field(
        description="FHIRPath of element(s) related to issue",
        default=None,
    )


class OperationOutcome(DomainResource):
    """
    A collection of error, warning, or information messages that result from a system action.
    """

    _abstract = False
    _type = "OperationOutcome"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/OperationOutcome"

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
    issue: ListType[OperationOutcomeIssue] = Field(
        description="A single issue associated with the action",
     	min_length=1,
	)
