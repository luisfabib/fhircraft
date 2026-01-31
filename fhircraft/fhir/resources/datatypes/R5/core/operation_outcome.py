from pydantic import Field, model_validator
from typing import Optional, List

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from fhircraft.fhir.resources.datatypes.primitives import String, Uri, Code

from fhircraft.fhir.resources.datatypes.R5.complex import (
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

    severity: Optional[Code] = Field(
        description="fatal | error | warning | information | success",
        default=None,
    )
    severity_ext: Optional[Element] = Field(
        description="Placeholder element for severity extensions",
        default=None,
        alias="_severity",
    )
    code: Optional[Code] = Field(
        description="Error or warning code",
        default=None,
    )
    code_ext: Optional[Element] = Field(
        description="Placeholder element for code extensions",
        default=None,
        alias="_code",
    )
    details: Optional[CodeableConcept] = Field(
        description="Additional details about the error",
        default=None,
    )
    diagnostics: Optional[String] = Field(
        description="Additional diagnostic information about the issue",
        default=None,
    )
    diagnostics_ext: Optional[Element] = Field(
        description="Placeholder element for diagnostics extensions",
        default=None,
        alias="_diagnostics",
    )
    location: Optional[List[String]] = Field(
        description="Deprecated: Path of element(s) related to issue",
        default=None,
    )
    location_ext: Optional[List[Optional[Element]]] = Field(
        description="Placeholder element for location extensions",
        default=None,
        alias="_location",
    )
    expression: Optional[List[String]] = Field(
        description="FHIRPath of element(s) related to issue",
        default=None,
    )
    expression_ext: Optional[List[Optional[Element]]] = Field(
        description="Placeholder element for expression extensions",
        default=None,
        alias="_expression",
    )


class OperationOutcome(DomainResource):
    """
    A collection of error, warning, or information messages that result from a system action.
    """

    _abstract = False
    _type = "OperationOutcome"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/OperationOutcome"

    issue: Optional[List[OperationOutcomeIssue]] = Field(
        description="A single issue associated with the action",
        default=None,
    )
