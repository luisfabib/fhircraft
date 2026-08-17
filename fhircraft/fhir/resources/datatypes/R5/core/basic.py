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
    CodeableConcept,
    Reference,
)
from .resource import Resource
from .domain_resource import DomainResource


class Basic(DomainResource):
    """
    Basic is used for handling concepts not yet defined in FHIR, narrative-only resources that don't map to an existing resource, and custom resources not appropriate for inclusion in the FHIR specification.
    """

    _abstract = False
    _type = "Basic"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Basic"

    identifier: Optional[ListType[Identifier]] = Field(
        description="Business identifier",
        default=None,
    )
    code: CodeableConcept = Field(
        description="Kind of Resource",
    )
    subject: Optional[Reference] = Field(
        description="Identifies the focus of this resource",
        default=None,
    )
    created: Optional[fhir.dateTime] = Field(
        description="When created",
        default=None,
    )
    author: Optional[Reference] = Field(
        description="Who created",
        default=None,
    )
