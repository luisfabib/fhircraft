from pydantic import Field, model_validator
from typing import Optional, List

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    Canonical,
    DateTime,
)

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

    identifier: Optional[List[Identifier]] = Field(
        description="Business Identifier for item",
        default=None,
    )
    definitionUri: Optional[List[Uri]] = Field(
        description="Defining information about the code of this charge item",
        default=None,
    )
    definitionUri_ext: Optional[List[Optional[Element]]] = Field(
        description="Placeholder element for definitionUri extensions",
        default=None,
        alias="_definitionUri",
    )
    definitionCanonical: Optional[List[Canonical]] = Field(
        description="Resource defining the code of this ChargeItem",
        default=None,
    )
    definitionCanonical_ext: Optional[List[Optional[Element]]] = Field(
        description="Placeholder element for definitionCanonical extensions",
        default=None,
        alias="_definitionCanonical",
    )
    status: Optional[Code] = Field(
        description="planned | billable | not-billable | aborted | billed | entered-in-error | unknown",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    partOf: Optional[List[Reference]] = Field(
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
    occurrenceDateTime_ext: Optional[Element] = Field(
        description="Placeholder element for occurrenceDateTime extensions",
        default=None,
        alias="_occurrenceDateTime",
    )
    occurrencePeriod: Optional[Period] = Field(
        description="When the charged service was applied",
        default=None,
    )
    occurrenceTiming: Optional[Timing] = Field(
        description="When the charged service was applied",
        default=None,
    )
    performer: Optional[List[ChargeItemPerformer]] = Field(
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
    bodysite: Optional[List[CodeableConcept]] = Field(
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
    enteredDate_ext: Optional[Element] = Field(
        description="Placeholder element for enteredDate extensions",
        default=None,
        alias="_enteredDate",
    )
    reason: Optional[List[CodeableConcept]] = Field(
        description="Why was the charged  service rendered?",
        default=None,
    )
    service: Optional[List[CodeableReference]] = Field(
        description="Which rendered service is being charged?",
        default=None,
    )
    product: Optional[List[CodeableReference]] = Field(
        description="Product charged",
        default=None,
    )
    account: Optional[List[Reference]] = Field(
        description="Account to place this charge",
        default=None,
    )
    note: Optional[List[Annotation]] = Field(
        description="Comments made about the ChargeItem",
        default=None,
    )
    supportingInformation: Optional[List[Reference]] = Field(
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
