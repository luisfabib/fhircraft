from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators


from ..primitive import *
from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    CodeableReference,
    Period,
    BackboneElement,
    Attachment,
    Coding,
)
from .resource import Resource
from .domain_resource import DomainResource

class DocumentReferenceAttester(BackboneElement):
    """
    A participant who has authenticated the accuracy of the document.
    """

    mode: Optional[CodeableConcept] = Field(
        description="personal | professional | legal | official",
        default=None,
    )
    time: Optional[DateTime] = Field(
        description="When the document was attested",
        default=None,
    )
    party: Optional[Reference] = Field(
        description="Who attested the document",
        default=None,
    )

class DocumentReferenceRelatesTo(BackboneElement):
    """
    Relationships that this document has with other document references that already exist.
    """

    code: Optional[CodeableConcept] = Field(
        description="The relationship type with another document",
        default=None,
    )
    target: Optional[Reference] = Field(
        description="Target of the relationship",
        default=None,
    )

class DocumentReferenceContentProfile(BackboneElement):
    """
    An identifier of the document constraints, encoding, structure, and template that the document conforms to beyond the base format indicated in the mimeType.
    """

    valueCoding: Optional[Coding] = Field(
        description="Code|uri|canonical",
        default=None,
    )
    valueUri: Optional[Uri] = Field(
        description="Code|uri|canonical",
        default=None,
    )
    valueCanonical: Optional[Canonical] = Field(
        description="Code|uri|canonical",
        default=None,
    )

    @property
    def value(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="value",
        )

    @model_validator(mode="after")
    def value_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Coding, Uri, Canonical],
            field_name_base="value",
            required=True,
        )

class DocumentReferenceContent(BackboneElement):
    """
    The document and format referenced.  If there are multiple content element repetitions, these must all represent the same document in different format, or attachment metadata.
    """

    attachment: Optional[Attachment] = Field(
        description="Where to access the document",
        default=None,
    )
    profile: Optional[ListType[DocumentReferenceContentProfile]] = Field(
        description="Content profile rules for the document",
        default=None,
    )

class DocumentReference(DomainResource):
    """
    A reference to a document of any kind for any purpose. While the term “document” implies a more narrow focus, for this resource this “document” encompasses *any* serialized object with a mime-type, it includes formal patient-centric documents (CDA), clinical notes, scanned paper, non-patient specific documents like policy text, as well as a photo, video, or audio recording acquired or used in healthcare.  The DocumentReference resource provides metadata about the document so that the document can be discovered and managed.  The actual content may be inline base64 encoded data or provided by direct reference.
    """

    _abstract = False
    _type = "DocumentReference"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/DocumentReference"

    identifier: Optional[ListType[Identifier]] = Field(
        description="Business identifiers for the document",
        default=None,
    )
    version: Optional[String] = Field(
        description="An explicitly assigned identifer of a variation of the content in the DocumentReference",
        default=None,
    )
    basedOn: Optional[ListType[Reference]] = Field(
        description="Procedure that caused this media to be created",
        default=None,
    )
    status: Optional[Code] = Field(
        description="current | superseded | entered-in-error",
        default=None,
    )
    docStatus: Optional[Code] = Field(
        description="registered | partial | preliminary | final | amended | corrected | appended | cancelled | entered-in-error | deprecated | unknown",
        default=None,
    )
    modality: Optional[ListType[CodeableConcept]] = Field(
        description="Imaging modality used",
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
    context: Optional[ListType[Reference]] = Field(
        description="Context of the document content",
        default=None,
    )
    event: Optional[ListType[CodeableReference]] = Field(
        description="Main clinical acts documented",
        default=None,
    )
    bodySite: Optional[ListType[CodeableReference]] = Field(
        description="Body part included",
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
    period: Optional[Period] = Field(
        description="Time of service that is being documented",
        default=None,
    )
    date: Optional[Instant] = Field(
        description="When this document reference was created",
        default=None,
    )
    author: Optional[ListType[Reference]] = Field(
        description="Who and/or what authored the document",
        default=None,
    )
    attester: Optional[ListType[DocumentReferenceAttester]] = Field(
        description="Attests to accuracy of the document",
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
    description: Optional[Markdown] = Field(
        description="Human-readable description",
        default=None,
    )
    securityLabel: Optional[ListType[CodeableConcept]] = Field(
        description="Document security-tags",
        default=None,
    )
    content: Optional[ListType[DocumentReferenceContent]] = Field(
        description="Document referenced",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_docRef_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="facilityType.empty() or context.where(resolve() is Encounter).empty()",
            human="facilityType SHALL only be present if context is not an encounter",
            key="docRef-1",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_docRef_2_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="practiceSetting.empty() or context.where(resolve() is Encounter).empty()",
            human="practiceSetting SHALL only be present if context is not present",
            key="docRef-2",
            severity="warning",
        )
