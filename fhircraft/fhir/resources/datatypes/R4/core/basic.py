import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import String, Uri, Code, Date

from fhircraft.fhir.resources.datatypes.R4.complex import (
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
        description="Business identifier",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="Kind of Resource",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="Identifies the focus of this resource",
        default=None,
    )
    created: Optional[Date] = Field(
        description="When created",
        default=None,
    )
    created_ext: Optional[Element] = Field(
        description="Placeholder element for created extensions",
        default=None,
        alias="_created",
    )
    author: Optional[Reference] = Field(
        description="Who created",
        default=None,
    )
