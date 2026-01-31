from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from fhircraft.fhir.resources.datatypes.primitives import String, Uri, Code, DateTime

from fhircraft.fhir.resources.datatypes.R5.complex import (
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
