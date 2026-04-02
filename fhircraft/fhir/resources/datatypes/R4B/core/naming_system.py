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
    ContactDetail,
    CodeableConcept,
    UsageContext,
    BackboneElement,
    Period,
)
from .resource import Resource
from .domain_resource import DomainResource

class NamingSystemUniqueId(BackboneElement):
    """
    Indicates how the system may be identified when referenced in electronic exchange.
    """

    type: Optional[Code] = Field(
        description="oid | uuid | uri | other",
        default=None,
    )
    value: Optional[String] = Field(
        description="The unique identifier",
        default=None,
    )
    preferred: Optional[Boolean] = Field(
        description="Is this the id that should be used for this type",
        default=None,
    )
    comment: Optional[String] = Field(
        description="Notes about identifier usage",
        default=None,
    )
    period: Optional[Period] = Field(
        description="When is identifier valid?",
        default=None,
    )

class NamingSystem(DomainResource):
    """
    A curated namespace that issues unique symbols within that namespace for the identification of concepts, people, devices, etc.  Represents a "System" used within the Identifier and Coding data types.
    """

    _abstract = False
    _type = "NamingSystem"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/NamingSystem"

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
    name: Optional[String] = Field(
        description="Name for this naming system (computer friendly)",
        default=None,
    )
    status: Optional[Code] = Field(
        description="draft | active | retired | unknown",
        default=None,
    )
    kind: Optional[Code] = Field(
        description="codesystem | identifier | root",
        default=None,
    )
    date: Optional[DateTime] = Field(
        description="Date last changed",
        default=None,
    )
    publisher: Optional[String] = Field(
        description="Name of the publisher (organization or individual)",
        default=None,
    )
    contact: Optional[ListType[ContactDetail]] = Field(
        description="Contact details for the publisher",
        default=None,
    )
    responsible: Optional[String] = Field(
        description="Who maintains system namespace?",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="e.g. driver,  provider,  patient, bank etc.",
        default=None,
    )
    description: Optional[Markdown] = Field(
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
    usage: Optional[String] = Field(
        description="How/where is it used",
        default=None,
    )
    uniqueId: Optional[ListType[NamingSystemUniqueId]] = Field(
        description="Unique identifiers used for system",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_nsd_0_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.exists() implies name.matches('[A-Z]([A-Za-z0-9_]){0,254}')",
            human="Name should be usable as an identifier for the module by machine processing applications such as code generation",
            key="nsd-0",
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
