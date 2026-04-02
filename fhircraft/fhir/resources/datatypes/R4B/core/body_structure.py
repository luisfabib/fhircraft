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
    Attachment,
    Reference,
)
from .resource import Resource
from .domain_resource import DomainResource

class BodyStructure(DomainResource):
    """
    Record details about an anatomical structure.  This resource may be used when a coded concept does not provide the necessary detail needed for the use case.
    """

    _abstract = False
    _type = "BodyStructure"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/BodyStructure"

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
        description="Bodystructure identifier",
        default=None,
    )
    active: Optional[Boolean] = Field(
        description="Whether this record is in active use",
        default=None,
    )
    morphology: Optional[CodeableConcept] = Field(
        description="Kind of Structure",
        default=None,
    )
    location: Optional[CodeableConcept] = Field(
        description="Body site",
        default=None,
    )
    locationQualifier: Optional[ListType[CodeableConcept]] = Field(
        description="Body site modifier",
        default=None,
    )
    description: Optional[String] = Field(
        description="Text description",
        default=None,
    )
    image: Optional[ListType[Attachment]] = Field(
        description="Attached images",
        default=None,
    )
    patient: Optional[Reference] = Field(
        description="Who this is about",
        default=None,
    )
