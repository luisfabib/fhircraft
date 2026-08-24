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
    Period,
    BackboneElement,
    Quantity,
    CodeableReference,
    Annotation,
)
from .resource import Resource
from .domain_resource import DomainResource

class InventoryReportInventoryListingItem(BackboneElement):
    """
    The item or items in this listing.
    """

    category: Optional[CodeableConcept] = Field(
        description="The inventory category or classification of the items being reported",
        default=None,
    )
    quantity: Quantity = Field(
        description="The quantity of the item or items being reported",
    )
    item: CodeableReference = Field(
        description="The code or reference to the item type",
    )

class InventoryReportInventoryListing(BackboneElement):
    """
    An inventory listing section (grouped by any of the attributes).
    """

    location: Optional[Reference] = Field(
        description="Location of the inventory items",
        default=None,
    )
    itemStatus: Optional[CodeableConcept] = Field(
        description="The status of the items that are being reported",
        default=None,
    )
    countingDateTime: Optional[fhir.dateTime] = Field(
        description="The date and time when the items were counted",
        default=None,
    )
    item: Optional[ListType[InventoryReportInventoryListingItem]] = Field(
        description="The item or items in this listing",
        default=None,
    )

class InventoryReport(DomainResource):
    """
    A report of inventory or stock items.
    """

    _abstract = False
    _type = "InventoryReport"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/InventoryReport"

    identifier: Optional[ListType[Identifier]] = Field(
        description="Business identifier for the report",
        default=None,
    )
    status: fhir.code = Field(
        description="draft | requested | active | entered-in-error",
    )
    countType: fhir.code = Field(
        description="snapshot | difference",
    )
    operationType: Optional[CodeableConcept] = Field(
        description="addition | subtraction",
        default=None,
    )
    operationTypeReason: Optional[CodeableConcept] = Field(
        description="The reason for this count - regular count, ad-hoc count, new arrivals, etc",
        default=None,
    )
    reportedDateTime: fhir.dateTime = Field(
        description="When the report has been submitted",
    )
    reporter: Optional[Reference] = Field(
        description="Who submits the report",
        default=None,
    )
    reportingPeriod: Optional[Period] = Field(
        description="The period the report refers to",
        default=None,
    )
    inventoryListing: Optional[ListType[InventoryReportInventoryListing]] = Field(
        description="An inventory listing section (grouped by any of the attributes)",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="A note associated with the InventoryReport",
        default=None,
    )
