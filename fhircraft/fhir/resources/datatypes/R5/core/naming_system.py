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
    Coding,
    ContactDetail,
    CodeableConcept,
    UsageContext,
    Period,
    RelatedArtifact,
    BackboneElement,
)
from .resource import Resource
from .domain_resource import DomainResource


class NamingSystemUniqueId(BackboneElement):
    """
    Indicates how the system may be identified when referenced in electronic exchange.
    """

    type: fhir.code = Field(
        description="oid | uuid | uri | iri-stem | v2csmnemonic | other",
    )
    value: fhir.string = Field(
        description="The unique identifier",
    )
    preferred: Optional[fhir.boolean] = Field(
        description="Is this the id that should be used for this type",
        default=None,
    )
    comment: Optional[fhir.string] = Field(
        description="Notes about identifier usage",
        default=None,
    )
    period: Optional[Period] = Field(
        description="When is identifier valid?",
        default=None,
    )
    authoritative: Optional[fhir.boolean] = Field(
        description="Whether the identifier is authoritative",
        default=None,
    )


class NamingSystem(DomainResource):
    """
    A curated namespace that issues unique symbols within that namespace for the identification of concepts, people, devices, etc.  Represents a "System" used within the Identifier and Coding data types.
    """

    _abstract = False
    _type = "NamingSystem"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/NamingSystem"

    url: Optional[fhir.uri] = Field(
        description="canonical identifier for this naming system, represented as a URI (globally unique)",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Additional identifier for the naming system (business identifier)",
        default=None,
    )
    version: Optional[fhir.string] = Field(
        description="Business version of the naming system",
        default=None,
    )
    versionAlgorithmString: Optional[fhir.string] = Field(
        description="How to compare versions",
        default=None,
    )
    versionAlgorithmCoding: Optional[Coding] = Field(
        description="How to compare versions",
        default=None,
    )
    name: fhir.string = Field(
        description="Name for this naming system (computer friendly)",
    )
    title: Optional[fhir.string] = Field(
        description="Title for this naming system (human friendly)",
        default=None,
    )
    status: fhir.code = Field(
        description="draft | active | retired | unknown",
    )
    kind: fhir.code = Field(
        description="codesystem | identifier | root",
    )
    experimental: Optional[fhir.boolean] = Field(
        description="For testing purposes, not real usage",
        default=None,
    )
    date: fhir.dateTime = Field(
        description="Date last changed",
    )
    publisher: Optional[fhir.string] = Field(
        description="Name of the publisher/steward (organization or individual)",
        default=None,
    )
    contact: Optional[ListType[ContactDetail]] = Field(
        description="Contact details for the publisher",
        default=None,
    )
    responsible: Optional[fhir.string] = Field(
        description="Who maintains system namespace?",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="e.g. driver,  provider,  patient, bank etc",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
        description="Natural language description of the naming system",
        default=None,
    )
    useContext: Optional[ListType[UsageContext]] = Field(
        description="The context that the content is intended to support",
        default=None,
    )
    jurisdiction: Optional[ListType[CodeableConcept]] = Field(
        description="Intended jurisdiction for naming system (if applicable)",
        default=None,
    )
    purpose: Optional[fhir.markdown] = Field(
        description="Why this naming system is defined",
        default=None,
    )
    copyright: Optional[fhir.markdown] = Field(
        description="Use and/or publishing restrictions",
        default=None,
    )
    copyrightLabel: Optional[fhir.string] = Field(
        description="Copyright holder and year(s)",
        default=None,
    )
    approvalDate: Optional[fhir.date_] = Field(
        description="When the NamingSystem was approved by publisher",
        default=None,
    )
    lastReviewDate: Optional[fhir.date_] = Field(
        description="When the NamingSystem was last reviewed by the publisher",
        default=None,
    )
    effectivePeriod: Optional[Period] = Field(
        description="When the NamingSystem is expected to be used",
        default=None,
    )
    topic: Optional[ListType[CodeableConcept]] = Field(
        description="E.g. Education, Treatment, Assessment, etc",
        default=None,
    )
    author: Optional[ListType[ContactDetail]] = Field(
        description="Who authored the CodeSystem",
        default=None,
    )
    editor: Optional[ListType[ContactDetail]] = Field(
        description="Who edited the NamingSystem",
        default=None,
    )
    reviewer: Optional[ListType[ContactDetail]] = Field(
        description="Who reviewed the NamingSystem",
        default=None,
    )
    endorser: Optional[ListType[ContactDetail]] = Field(
        description="Who endorsed the NamingSystem",
        default=None,
    )
    relatedArtifact: Optional[ListType[RelatedArtifact]] = Field(
        description="Additional documentation, citations, etc",
        default=None,
    )
    usage: Optional[fhir.string] = Field(
        description="How/where is it used",
        default=None,
    )
    uniqueId: ListType[NamingSystemUniqueId] = Field(
        description="Unique identifiers used for system",
    )

    @property
    def versionAlgorithm(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="versionAlgorithm",
        )

    @model_validator(mode="after")
    def versionAlgorithm_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.String, Coding],
            field_name_base="versionAlgorithm",
            required=False,
        )

    @model_validator(mode="after")
    def FHIR_cnl_0_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.exists() implies name.matches('^[A-Z]([A-Za-z0-9_]){1,254}$')",
            human="Name should be usable as an identifier for the module by machine processing applications such as code generation",
            key="cnl-0",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_cnl_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("url",),
            expression="exists() implies matches('^[^|# ]+$')",
            human="URL should not contain | or # - these characters make processing canonical references problematic",
            key="cnl-1",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_nsd_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="kind != 'root' or uniqueId.all(type != 'uuid')",
            human="Root systems cannot have uuid identifiers",
            key="nsd-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_nsd_2_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="uniqueId.where(preferred = true).select(type).isDistinct()",
            human="Can't have more than one preferred identifier for a type",
            key="nsd-2",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_nsd_3_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="uniqueId.where(authoritative = 'true').select(type.toString() & period.start.toString() & period.end.toString()).isDistinct()",
            human="Can't have more than one authoritative identifier for a type/period combination (only one authoritative identifier allowed at any given point of time)",
            key="nsd-3",
            severity="error",
        )
