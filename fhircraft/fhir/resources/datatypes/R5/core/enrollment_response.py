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


class EnrollmentResponse(DomainResource):
    """
    This resource provides enrollment and plan details from the processing of an EnrollmentRequest resource.
    """

    _abstract = False
    _type = "EnrollmentResponse"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/EnrollmentResponse"

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
    request: Optional[Reference] = Field(
        description="Claim reference",
        default=None,
    )
    outcome: Optional[Code] = Field(
        description="queued | complete | error | partial",
        default=None,
    )
    outcome_ext: Optional[Element] = Field(
        description="Placeholder element for outcome extensions",
        default=None,
        alias="_outcome",
    )
    disposition: Optional[String] = Field(
        description="Disposition Message",
        default=None,
    )
    disposition_ext: Optional[Element] = Field(
        description="Placeholder element for disposition extensions",
        default=None,
        alias="_disposition",
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
    organization: Optional[Reference] = Field(
        description="Insurer",
        default=None,
    )
    requestProvider: Optional[Reference] = Field(
        description="Responsible practitioner",
        default=None,
    )
