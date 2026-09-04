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
    UsageContext,
    Annotation,
    BackboneElement,
    RelatedArtifact,
    Period,
    CodeableReference,
)
from .resource import Resource
from .domain_resource import DomainResource


class CompositionAttester(BackboneElement):
    """
    A participant who has attested to the accuracy of the composition/document.
    """

    mode: CodeableConcept = Field(
        description="personal | professional | legal | official",
    )
    time: Optional[fhir.dateTime] = Field(
        description="When the composition was attested",
        default=None,
    )
    party: Optional[Reference] = Field(
        description="Who attested the composition",
        default=None,
    )


class CompositionEvent(BackboneElement):
    """
    The clinical service, such as a colonoscopy or an appendectomy, being documented.
    """

    period: Optional[Period] = Field(
        description="The period covered by the documentation",
        default=None,
    )
    detail: Optional[ListType[CodeableReference]] = Field(
        description="The event(s) being documented, as code(s), reference(s), or both",
        default=None,
    )


class CompositionSection(BackboneElement):
    """
    The root of the sections that make up the composition.
    """

    title: Optional[fhir.string] = Field(
        description="Label for section (e.g. for ToC)",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="Classification of section (recommended)",
        default=None,
    )
    author: Optional[ListType[Reference]] = Field(
        description="Who and/or what authored the section",
        default=None,
    )
    focus: Optional[Reference] = Field(
        description="Who/what the section is about, when it is not about the subject of composition",
        default=None,
    )
    text: Optional[Narrative] = Field(
        description="Text summary of the section, for human interpretation",
        default=None,
    )
    orderedBy: Optional[CodeableConcept] = Field(
        description="Order of section entries",
        default=None,
    )
    entry: Optional[ListType[Reference]] = Field(
        description="A reference to data that supports this section",
        default=None,
    )
    emptyReason: Optional[CodeableConcept] = Field(
        description="Why the section is empty",
        default=None,
    )
    section: Optional[ListType["CompositionSection"]] = Field(
        description="Nested Section",
        default=None,
    )


class Composition(DomainResource):
    """
    A set of healthcare-related information that is assembled together into a single logical package that provides a single coherent statement of meaning, establishes its own context and that has clinical attestation with regard to who is making the statement. A Composition defines the structure and narrative content necessary for a document. However, a Composition alone does not constitute a document. Rather, the Composition must be the first entry in a Bundle where Bundle.type=document, and any other resources referenced from Composition must be included as subsequent entries in the Bundle (for example Patient, Practitioner, Encounter, etc.).
    """

    _abstract = False
    _type = "Composition"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Composition"

    url: Optional[fhir.uri] = Field(
        description="canonical identifier for this Composition, represented as a URI (globally unique)",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Version-independent identifier for the Composition",
        default=None,
    )
    version: Optional[fhir.string] = Field(
        description="An explicitly assigned identifer of a variation of the content in the Composition",
        default=None,
    )
    status: fhir.code = Field(
        description="registered | partial | preliminary | final | amended | corrected | appended | cancelled | entered-in-error | deprecated | unknown",
    )
    type: CodeableConcept = Field(
        description="Kind of composition (LOINC if possible)",
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description="Categorization of Composition",
        default=None,
    )
    subject: Optional[ListType[Reference]] = Field(
        description="Who and/or what the composition is about",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="Context of the Composition",
        default=None,
    )
    date: fhir.dateTime = Field(
        description="Composition editing time",
    )
    useContext: Optional[ListType[UsageContext]] = Field(
        description="The context that the content is intended to support",
        default=None,
    )
    author: ListType[Reference] = Field(
        description="Who and/or what authored the composition",
     	min_length=1,
	)
    name: Optional[fhir.string] = Field(
        description="Name for this Composition (computer friendly)",
        default=None,
    )
    title: fhir.string = Field(
        description="Human Readable name/title",
    )
    note: Optional[ListType[Annotation]] = Field(
        description="For any additional notes",
        default=None,
    )
    attester: Optional[ListType[CompositionAttester]] = Field(
        description="Attests to accuracy of composition",
        default=None,
    )
    custodian: Optional[Reference] = Field(
        description="Organization which maintains the composition",
        default=None,
    )
    relatesTo: Optional[ListType[RelatedArtifact]] = Field(
        description="Relationships to other compositions/documents",
        default=None,
    )
    event: Optional[ListType[CompositionEvent]] = Field(
        description="The clinical service(s) being documented",
        default=None,
    )
    section: Optional[ListType[CompositionSection]] = Field(
        description="Composition is broken into sections",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_cmp_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("section",),
            expression="text.exists() or entry.exists() or section.exists()",
            human="A section must contain at least one of text, entries, or sub-sections",
            key="cmp-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_cmp_2_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("section",),
            expression="emptyReason.empty() or entry.empty()",
            human="A section can only have an emptyReason if it is empty",
            key="cmp-2",
            severity="error",
        )
