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
    Identifier,
    CodeableConcept,
    Reference,
    BackboneElement,
)
from .resource import Resource
from .domain_resource import DomainResource

class DocumentManifestRelated(BackboneElement):
    """
    Related identifiers or resources associated with the DocumentManifest.
    """

    identifier: Optional[Identifier] = Field(
        description="Identifiers of things that are related",
        default=None,
    )
    ref: Optional[Reference] = Field(
        description="Related Resource",
        default=None,
    )

class DocumentManifest(DomainResource):
    """
    A collection of documents compiled for a purpose together with metadata that applies to the collection.
    """

    _abstract = False
    _type = "DocumentManifest"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/DocumentManifest"

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
    masterIdentifier: Optional[Identifier] = Field(
        description="Unique Identifier for the set of documents",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Other identifiers for the manifest",
        default=None,
    )
    status: fhir.code = Field(
        description="current | superseded | entered-in-error",
    )
    type: Optional[CodeableConcept] = Field(
        description="Kind of document set",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="The subject of the set of documents",
        default=None,
    )
    created: Optional[fhir.dateTime] = Field(
        description="When this document manifest created",
        default=None,
    )
    author: Optional[ListType[Reference]] = Field(
        description="Who and/or what authored the DocumentManifest",
        default=None,
    )
    recipient: Optional[ListType[Reference]] = Field(
        description="Intended to get notified about this set of documents",
        default=None,
    )
    source: Optional[fhir.uri] = Field(
        description="The source system/application/software",
        default=None,
    )
    description: Optional[fhir.string] = Field(
        description="Human-readable description (title)",
        default=None,
    )
    content: ListType[Reference] = Field(
        description="Items in manifest",
     	min_length=1,
	)
    related: Optional[ListType[DocumentManifestRelated]] = Field(
        description="Related things",
        default=None,
    )
