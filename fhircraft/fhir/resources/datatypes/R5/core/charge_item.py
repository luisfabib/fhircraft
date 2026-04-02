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
    Period,
    Timing,
    BackboneElement,
    Quantity,
    MonetaryComponent,
    CodeableReference,
    Annotation,
)
from .resource import Resource
from .domain_resource import DomainResource

class ChargeItemPerformer(BackboneElement):
    """
    Indicates who or what performed or participated in the charged service.
    """

    function: Optional[CodeableConcept] = Field(
        description="What type of performance was done",
        default=None,
    )
    actor: Optional[Reference] = Field(
        description="Individual who was performing",
        default=None,
    )

class ChargeItem(DomainResource):
    """
    The resource ChargeItem describes the provision of healthcare provider products for a certain patient, therefore referring not only to the product, but containing in addition details of the provision, like date, time, amounts and participating organizations and persons. Main Usage of the ChargeItem is to enable the billing process and internal cost allocation.
    """

    _abstract = False
    _type = "ChargeItem"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/ChargeItem"

    identifier: Optional[ListType[Identifier]] = Field(
        description="Business Identifier for item",
        default=None,
    )
    definitionUri: Optional[ListType[Uri]] = Field(
        description="Defining information about the code of this charge item",
        default=None,
    )
    definitionCanonical: Optional[ListType[Canonical]] = Field(
        description="Resource defining the code of this ChargeItem",
        default=None,
    )
    status: Optional[Code] = Field(
        description="planned | billable | not-billable | aborted | billed | entered-in-error | unknown",
        default=None,
    )
    partOf: Optional[ListType[Reference]] = Field(
        description="Part of referenced ChargeItem",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="A code that identifies the charge, like a billing code",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="Individual service was done for/to",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="Encounter associated with this ChargeItem",
        default=None,
    )
    occurrenceDateTime: Optional[DateTime] = Field(
        description="When the charged service was applied",
        default=None,
    )
    occurrencePeriod: Optional[Period] = Field(
        description="When the charged service was applied",
        default=None,
    )
    occurrenceTiming: Optional[Timing] = Field(
        description="When the charged service was applied",
        default=None,
    )
    performer: Optional[ListType[ChargeItemPerformer]] = Field(
        description="Who performed charged service",
        default=None,
    )
    performingOrganization: Optional[Reference] = Field(
        description="Organization providing the charged service",
        default=None,
    )
    requestingOrganization: Optional[Reference] = Field(
        description="Organization requesting the charged service",
        default=None,
    )
    costCenter: Optional[Reference] = Field(
        description="Organization that has ownership of the (potential, future) revenue",
        default=None,
    )
    quantity: Optional[Quantity] = Field(
        description="Quantity of which the charge item has been serviced",
        default=None,
    )
    bodysite: Optional[ListType[CodeableConcept]] = Field(
        description="Anatomical location, if relevant",
        default=None,
    )
    unitPriceComponent: Optional[MonetaryComponent] = Field(
        description="Unit price overriding the associated rules",
        default=None,
    )
    totalPriceComponent: Optional[MonetaryComponent] = Field(
        description="Total price overriding the associated rules",
        default=None,
    )
    overrideReason: Optional[CodeableConcept] = Field(
        description="Reason for overriding the list price/factor",
        default=None,
    )
    enterer: Optional[Reference] = Field(
        description="Individual who was entering",
        default=None,
    )
    enteredDate: Optional[DateTime] = Field(
        description="Date the charge item was entered",
        default=None,
    )
    reason: Optional[ListType[CodeableConcept]] = Field(
        description="Why was the charged  service rendered?",
        default=None,
    )
    service: Optional[ListType[CodeableReference]] = Field(
        description="Which rendered service is being charged?",
        default=None,
    )
    product: Optional[ListType[CodeableReference]] = Field(
        description="Product charged",
        default=None,
    )
    account: Optional[ListType[Reference]] = Field(
        description="Account to place this charge",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Comments made about the ChargeItem",
        default=None,
    )
    supportingInformation: Optional[ListType[Reference]] = Field(
        description="Further information supporting this charge",
        default=None,
    )

    @property
    def occurrence(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="occurrence",
        )

    @model_validator(mode="after")
    def occurrence_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[DateTime, Period, Timing],
            field_name_base="occurrence",
            required=False,
        )
