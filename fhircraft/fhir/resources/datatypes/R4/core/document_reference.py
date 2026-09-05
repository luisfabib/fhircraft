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
    Attachment,
    Coding,
    Period,
)
from .resource import Resource
from .domain_resource import DomainResource


class DocumentReferenceRelatesTo(BackboneElement):
    """
    Relationships that this document has with other document references that already exist.
    """

    code: fhir.code = Field(
        description="replaces | transforms | signs | appends",
    )
    target: Reference = Field(
        description="Target of the relationship",
    )


class DocumentReferenceContent(BackboneElement):
    """
    The document and format referenced. There may be multiple content element repetitions, each with a different format.
    """

    attachment: Attachment = Field(
        description="Where to access the document",
    )
    format: Optional[Coding] = Field(
        description="Format/content rules for the document",
        default=None,
    )


class DocumentReferenceContext(BackboneElement):
    """
    The clinical context in which the document was prepared.
    """

    encounter: Optional[ListType[Reference]] = Field(
        description="Context of the document  content",
        default=None,
    )
    event: Optional[ListType[CodeableConcept]] = Field(
        description="Main clinical acts documented",
        default=None,
    )
    period: Optional[Period] = Field(
        description="time of service that is being documented",
        default=None,
    )
    facilityType: Optional[CodeableConcept] = Field(
        description="Kind of facility where patient was seen",
        default=None,
    )
    practiceSetting: Optional[CodeableConcept] = Field(
        description="Additional details about where the content was created (e.g. clinical specialty)",
        default=None,
    )
    sourcePatientInfo: Optional[Reference] = Field(
        description="Patient demographics from source",
        default=None,
    )
    related: Optional[ListType[Reference]] = Field(
        description="Related identifiers or resources",
        default=None,
    )


class DocumentReference(DomainResource):
    """
    A reference to a document of any kind for any purpose. Provides metadata about the document so that the document can be discovered and managed. The scope of a document is any seralized object with a mime-type, so includes formal patient centric documents (CDA), cliical notes, scanned paper, and non-patient specific documents like policy text.
    """

    _abstract = False
    _type = "DocumentReference"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/DocumentReference"

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
        description="Master Version Specific Identifier",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Other identifiers for the document",
        default=None,
    )
    status: fhir.code = Field(
        description="current | superseded | entered-in-error",
    )
    docStatus: Optional[fhir.code] = Field(
        description="preliminary | final | amended | entered-in-error",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Kind of document (LOINC if possible)",
        default=None,
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description="Categorization of document",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="Who/what is the subject of the document",
        default=None,
    )
    date: Optional[fhir.instant] = Field(
        description="When this document reference was created",
        default=None,
    )
    author: Optional[ListType[Reference]] = Field(
        description="Who and/or what authored the document",
        default=None,
    )
    authenticator: Optional[Reference] = Field(
        description="Who/what authenticated the document",
        default=None,
    )
    custodian: Optional[Reference] = Field(
        description="Organization which maintains the document",
        default=None,
    )
    relatesTo: Optional[ListType[DocumentReferenceRelatesTo]] = Field(
        description="Relationships to other documents",
        default=None,
    )
    description: Optional[fhir.string] = Field(
        description="Human-readable description",
        default=None,
    )
    securityLabel: Optional[ListType[CodeableConcept]] = Field(
        description="Document security-tags",
        default=None,
    )
    content: ListType[DocumentReferenceContent] = Field(
        description="Document referenced",
        min_length=1,
    )
    context: Optional[DocumentReferenceContext] = Field(
        description="Clinical context of document",
        default=None,
    )
