import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import String, Uri, Code, DateTime

from fhircraft.fhir.resources.datatypes.R4B.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Reference,
)
from .resource import Resource
from .domain_resource import DomainResource


class EnrollmentRequest(DomainResource):
    """
    This resource provides the insurance enrollment details to the insurer regarding a specified coverage.
    """

    _abstract = False
    _type = "EnrollmentRequest"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/EnrollmentRequest"

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
        description="Business Identifier",
        default=None,
    )
    status: Optional[Code] = Field(
        description="active | cancelled | draft | entered-in-error",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    created: Optional[DateTime] = Field(
        description="Creation date",
        default=None,
    )
    created_ext: Optional[Element] = Field(
        description="Placeholder element for created extensions",
        default=None,
        alias="_created",
    )
    insurer: Optional[Reference] = Field(
        description="Target",
        default=None,
    )
    provider: Optional[Reference] = Field(
        description="Responsible practitioner",
        default=None,
    )
    candidate: Optional[Reference] = Field(
        description="The subject to be enrolled",
        default=None,
    )
    coverage: Optional[Reference] = Field(
        description="Insurance information",
        default=None,
    )
