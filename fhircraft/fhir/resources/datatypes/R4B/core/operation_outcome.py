import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import String, Uri, Code

from fhircraft.fhir.resources.datatypes.R4B.complex import (
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
        description="fatal | error | warning | information",
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
    location: Optional[ListType[String]] = Field(
        description="Deprecated: Path of element(s) related to issue",
        default=None,
    )
    location_ext: Optional[Element] = Field(
        description="Placeholder element for location extensions",
        default=None,
        alias="_location",
    )
    expression: Optional[ListType[String]] = Field(
        description="FHIRPath of element(s) related to issue",
        default=None,
    )
    expression_ext: Optional[Element] = Field(
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
    issue: Optional[ListType[OperationOutcomeIssue]] = Field(
        description="A single issue associated with the action",
        default=None,
    )
