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
    Reference,
    BackboneElement,
    Period,
)
from .resource import Resource
from .domain_resource import DomainResource

class CompositionAttester(BackboneElement):
    """
    A participant who has attested to the accuracy of the composition/document.
    """

    mode: Optional[Code] = Field(
        description="personal | professional | legal | official",
        default=None,
    )
    time: Optional[DateTime] = Field(
        description="When the composition was attested",
        default=None,
    )
    party: Optional[Reference] = Field(
        description="Who attested the composition",
        default=None,
    )

class CompositionRelatesTo(BackboneElement):
    """
    Relationships that this composition has with other compositions or documents that already exist.
    """

    code: Optional[Code] = Field(
        description="replaces | transforms | signs | appends",
        default=None,
    )
    targetIdentifier: Optional[Identifier] = Field(
        description="Target of the relationship",
        default=None,
    )
    targetReference: Optional[Reference] = Field(
        description="Target of the relationship",
        default=None,
    )

    @property
    def target(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="target",
        )

    @model_validator(mode="after")
    def target_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Identifier, Reference],
            field_name_base="target",
            required=True,
        )

class CompositionEvent(BackboneElement):
    """
    The clinical service, such as a colonoscopy or an appendectomy, being documented.
    """

    code: Optional[ListType[CodeableConcept]] = Field(
        description="Code(s) that apply to the event being documented",
        default=None,
    )
    period: Optional[Period] = Field(
        description="The period covered by the documentation",
        default=None,
    )
    detail: Optional[ListType[Reference]] = Field(
        description="The event(s) being documented",
        default=None,
    )

class CompositionSection(BackboneElement):
    """
    The root of the sections that make up the composition.
    """

    title: Optional[String] = Field(
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
    mode: Optional[Code] = Field(
        description="working | snapshot | changes",
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
    identifier: Optional[Identifier] = Field(
        description="Version-independent identifier for the Composition",
        default=None,
    )
    status: Optional[Code] = Field(
        description="preliminary | final | amended | entered-in-error",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Kind of composition (LOINC if possible)",
        default=None,
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description="Categorization of Composition",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="Who and/or what the composition is about",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="Context of the Composition",
        default=None,
    )
    date: Optional[DateTime] = Field(
        description="Composition editing time",
        default=None,
    )
    author: Optional[ListType[Reference]] = Field(
        description="Who and/or what authored the composition",
        default=None,
    )
    title: Optional[String] = Field(
        description="Human Readable name/title",
        default=None,
    )
    confidentiality: Optional[Code] = Field(
        description="As defined by affinity domain",
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
    relatesTo: Optional[ListType[CompositionRelatesTo]] = Field(
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
