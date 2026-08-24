import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)


import fhircraft.fhir.resources.datatypes.R4.primitive as fhir
from fhircraft.fhir.resources.datatypes.R4.complex import (
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
    Annotation,
    Money,
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
    actor: Reference = Field(
        description="Individual who was performing",
    )


class ChargeItem(DomainResource):
    """
    The resource ChargeItem describes the provision of healthcare provider products for a certain patient, therefore referring not only to the product, but containing in addition details of the provision, like date, time, amounts and participating organizations and persons. Main Usage of the ChargeItem is to enable the billing process and internal cost allocation.
    """

    _abstract = False
    _type = "ChargeItem"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/ChargeItem"

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
        description="Business Identifier for item",
        default=None,
    )
    definitionUri: Optional[ListType[fhir.uri]] = Field(
        description="Defining information about the code of this charge item",
        default=None,
    )
    definitionCanonical: Optional[ListType[fhir.canonical]] = Field(
        description="Resource defining the code of this ChargeItem",
        default=None,
    )
    status: fhir.code = Field(
        description="planned | billable | not-billable | aborted | billed | entered-in-error | unknown",
    )
    partOf: Optional[ListType[Reference]] = Field(
        description="Part of referenced ChargeItem",
        default=None,
    )
    code: CodeableConcept = Field(
        description="A code that identifies the charge, like a billing code",
    )
    subject: Reference = Field(
        description="Individual service was done for/to",
    )
    context: Optional[Reference] = Field(
        description="Encounter / Episode associated with event",
        default=None,
    )
    occurrenceDateTime: Optional[fhir.dateTime] = Field(
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
    factorOverride: Optional[fhir.decimal] = Field(
        description="Factor overriding the associated rules",
        default=None,
    )
    priceOverride: Optional[Money] = Field(
        description="Price overriding the associated rules",
        default=None,
    )
    overrideReason: Optional[fhir.string] = Field(
        description="Reason for overriding the list price/factor",
        default=None,
    )
    enterer: Optional[Reference] = Field(
        description="Individual who was entering",
        default=None,
    )
    enteredDate: Optional[fhir.dateTime] = Field(
        description="Date the charge item was entered",
        default=None,
    )
    reason: Optional[ListType[CodeableConcept]] = Field(
        description="Why was the charged  service rendered?",
        default=None,
    )
    service: Optional[ListType[Reference]] = Field(
        description="Which rendered service is being charged?",
        default=None,
    )
    productReference: Optional[Reference] = Field(
        description="Product charged",
        default=None,
    )
    productCodeableConcept: Optional[CodeableConcept] = Field(
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

    @property
    def product(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="product",
        )

    @model_validator(mode="after")
    def occurrence_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.DateTime, Period, Timing],
            field_name_base="occurrence",
            required=False,
        )

    @model_validator(mode="after")
    def product_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Reference, CodeableConcept],
            field_name_base="product",
            required=False,
        )
