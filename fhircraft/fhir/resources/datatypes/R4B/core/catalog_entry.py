import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)


import fhircraft.fhir.resources.datatypes.R4B.primitive as fhir
from fhircraft.fhir.resources.datatypes.R4B.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    Period,
    BackboneElement,
)
from .resource import Resource
from .domain_resource import DomainResource

class CatalogEntryRelatedEntry(BackboneElement):
    """
    Used for example, to point to a substance, or to a device used to administer a medication.
    """

    relationtype: Optional[fhir.code] = Field(
        description="triggers | is-replaced-by",
        default=None,
    )
    item: Optional[Reference] = Field(
        description="The reference to the related item",
        default=None,
    )

class CatalogEntry(DomainResource):
    """
    Catalog entries are wrappers that contextualize items included in a catalog.
    """

    _abstract = False
    _type = "CatalogEntry"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/CatalogEntry"

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
        description="Unique identifier of the catalog item",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="The type of item - medication, device, service, protocol or other",
        default=None,
    )
    orderable: Optional[fhir.boolean] = Field(
        description="Whether the entry represents an orderable item",
        default=None,
    )
    referencedItem: Optional[Reference] = Field(
        description="The item that is being defined",
        default=None,
    )
    additionalIdentifier: Optional[ListType[Identifier]] = Field(
        description="Any additional identifier(s) for the catalog item, in the same granularity or concept",
        default=None,
    )
    classification: Optional[ListType[CodeableConcept]] = Field(
        description="Classification (category or class) of the item entry",
        default=None,
    )
    status: Optional[fhir.code] = Field(
        description="draft | active | retired | unknown",
        default=None,
    )
    validityPeriod: Optional[Period] = Field(
        description="The time period in which this catalog entry is expected to be active",
        default=None,
    )
    validTo: Optional[fhir.dateTime] = Field(
        description="The date until which this catalog entry is expected to be active",
        default=None,
    )
    lastUpdated: Optional[fhir.dateTime] = Field(
        description="When was this catalog last updated",
        default=None,
    )
    additionalCharacteristic: Optional[ListType[CodeableConcept]] = Field(
        description="Additional characteristics of the catalog entry",
        default=None,
    )
    additionalClassification: Optional[ListType[CodeableConcept]] = Field(
        description="Additional classification of the catalog entry",
        default=None,
    )
    relatedEntry: Optional[ListType[CatalogEntryRelatedEntry]] = Field(
        description="An item that this catalog entry is related to",
        default=None,
    )
