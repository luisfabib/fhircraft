from pydantic import Field, model_validator
from typing import Optional, List

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from fhircraft.fhir.resources.datatypes.primitives import String, Uri, Code, DateTime

from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    BackboneElement,
    Quantity,
    Annotation,
)
from .resource import Resource
from .domain_resource import DomainResource


class BiologicallyDerivedProductDispensePerformer(BackboneElement):
    """
    Indicates who or what performed an action.
    """

    function: Optional[CodeableConcept] = Field(
        description="Identifies the function of the performer during the dispense",
        default=None,
    )
    actor: Optional[Reference] = Field(
        description="Who performed the action",
        default=None,
    )


class BiologicallyDerivedProductDispense(DomainResource):
    """
    A record of dispensation of a biologically derived product.
    """

    _abstract = False
    _type = "BiologicallyDerivedProductDispense"
    _canonical_url = (
        "http://hl7.org/fhir/StructureDefinition/BiologicallyDerivedProductDispense"
    )

    identifier: Optional[List[Identifier]] = Field(
        description="Business identifier for this dispense",
        default=None,
    )
    basedOn: Optional[List[Reference]] = Field(
        description="The order or request that this dispense is fulfilling",
        default=None,
    )
    partOf: Optional[List[Reference]] = Field(
        description="Short description",
        default=None,
    )
    status: Optional[Code] = Field(
        description="preparation | in-progress | allocated | issued | unfulfilled | returned | entered-in-error | unknown",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    originRelationshipType: Optional[CodeableConcept] = Field(
        description="Relationship between the donor and intended recipient",
        default=None,
    )
    product: Optional[Reference] = Field(
        description="The BiologicallyDerivedProduct that is dispensed",
        default=None,
    )
    patient: Optional[Reference] = Field(
        description="The intended recipient of the dispensed product",
        default=None,
    )
    matchStatus: Optional[CodeableConcept] = Field(
        description="Indicates the type of matching associated with the dispense",
        default=None,
    )
    performer: Optional[List[BiologicallyDerivedProductDispensePerformer]] = Field(
        description="Indicates who or what performed an action",
        default=None,
    )
    location: Optional[Reference] = Field(
        description="Where the dispense occurred",
        default=None,
    )
    quantity: Optional[Quantity] = Field(
        description="Amount dispensed",
        default=None,
    )
    preparedDate: Optional[DateTime] = Field(
        description="When product was selected/matched",
        default=None,
    )
    preparedDate_ext: Optional[Element] = Field(
        description="Placeholder element for preparedDate extensions",
        default=None,
        alias="_preparedDate",
    )
    whenHandedOver: Optional[DateTime] = Field(
        description="When the product was dispatched",
        default=None,
    )
    whenHandedOver_ext: Optional[Element] = Field(
        description="Placeholder element for whenHandedOver extensions",
        default=None,
        alias="_whenHandedOver",
    )
    destination: Optional[Reference] = Field(
        description="Where the product was dispatched to",
        default=None,
    )
    note: Optional[List[Annotation]] = Field(
        description="Additional notes",
        default=None,
    )
    usageInstruction: Optional[String] = Field(
        description="Specific instructions for use",
        default=None,
    )
    usageInstruction_ext: Optional[Element] = Field(
        description="Placeholder element for usageInstruction extensions",
        default=None,
        alias="_usageInstruction",
    )
