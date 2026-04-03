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
    CodeableReference,
    BackboneElement,
    Quantity,
    Ratio,
    Range,
    Period,
    Timing,
    Annotation,
)
from .resource import Resource
from .domain_resource import DomainResource

class ServiceRequestOrderDetailParameter(BackboneElement):
    """
    The parameter details for the service being requested.
    """

    code: Optional[CodeableConcept] = Field(
        description="The detail of the order being requested",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="The value for the order detail",
        default=None,
    )
    valueRatio: Optional[Ratio] = Field(
        description="The value for the order detail",
        default=None,
    )
    valueRange: Optional[Range] = Field(
        description="The value for the order detail",
        default=None,
    )
    valueBoolean: Optional[Boolean] = Field(
        description="The value for the order detail",
        default=None,
    )
    valueCodeableConcept: Optional[CodeableConcept] = Field(
        description="The value for the order detail",
        default=None,
    )
    valueString: Optional[String] = Field(
        description="The value for the order detail",
        default=None,
    )
    valuePeriod: Optional[Period] = Field(
        description="The value for the order detail",
        default=None,
    )

    @property
    def value(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="value",
        )

    @model_validator(mode="after")
    def value_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[
                Quantity,
                Ratio,
                Range,
                Boolean,
                CodeableConcept,
                String,
                Period,
            ],
            field_name_base="value",
            required=True,
        )

class ServiceRequestOrderDetail(BackboneElement):
    """
    Additional details and instructions about the how the services are to be delivered.   For example, and order for a urinary catheter may have an order detail for an external or indwelling catheter, or an order for a bandage may require additional instructions specifying how the bandage should be applied.
    """

    parameterFocus: Optional[CodeableReference] = Field(
        description="The context of the order details by reference",
        default=None,
    )
    parameter: Optional[ListType[ServiceRequestOrderDetailParameter]] = Field(
        description="The parameter details for the service being requested",
        default=None,
    )

class ServiceRequestPatientInstruction(BackboneElement):
    """
    Instructions in terms that are understood by the patient or consumer.
    """

    instructionMarkdown: Optional[Markdown] = Field(
        description="Patient or consumer-oriented instructions",
        default=None,
    )
    instructionReference: Optional[Reference] = Field(
        description="Patient or consumer-oriented instructions",
        default=None,
    )

    @property
    def instruction(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="instruction",
        )

    @model_validator(mode="after")
    def instruction_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Markdown, Reference],
            field_name_base="instruction",
            required=False,
        )

class ServiceRequest(DomainResource):
    """
    A record of a request for service such as diagnostic investigations, treatments, or operations to be performed.
    """

    _abstract = False
    _type = "ServiceRequest"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/ServiceRequest"

    identifier: Optional[ListType[Identifier]] = Field(
        description="Identifiers assigned to this order",
        default=None,
    )
    instantiatesCanonical: Optional[ListType[Canonical]] = Field(
        description="Instantiates FHIR protocol or definition",
        default=None,
    )
    instantiatesUri: Optional[ListType[Uri]] = Field(
        description="Instantiates external protocol or definition",
        default=None,
    )
    basedOn: Optional[ListType[Reference]] = Field(
        description="What request fulfills",
        default=None,
    )
    replaces: Optional[ListType[Reference]] = Field(
        description="What request replaces",
        default=None,
    )
    requisition: Optional[Identifier] = Field(
        description="Composite Request ID",
        default=None,
    )
    status: Optional[Code] = Field(
        description="draft | active | on-hold | revoked | completed | entered-in-error | unknown",
        default=None,
    )
    intent: Optional[Code] = Field(
        description="proposal | plan | directive | order +",
        default=None,
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description="Classification of service",
        default=None,
    )
    priority: Optional[Code] = Field(
        description="routine | urgent | asap | stat",
        default=None,
    )
    doNotPerform: Optional[Boolean] = Field(
        description="True if service/procedure should not be performed",
        default=None,
    )
    code: Optional[CodeableReference] = Field(
        description="What is being requested/ordered",
        default=None,
    )
    orderDetail: Optional[ListType[ServiceRequestOrderDetail]] = Field(
        description="Additional order information",
        default=None,
    )
    quantityQuantity: Optional[Quantity] = Field(
        description="Service amount",
        default=None,
    )
    quantityRatio: Optional[Ratio] = Field(
        description="Service amount",
        default=None,
    )
    quantityRange: Optional[Range] = Field(
        description="Service amount",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="Individual or Entity the service is ordered for",
        default=None,
    )
    focus: Optional[ListType[Reference]] = Field(
        description="What the service request is about, when it is not about the subject of record",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="Encounter in which the request was created",
        default=None,
    )
    occurrenceDateTime: Optional[DateTime] = Field(
        description="When service should occur",
        default=None,
    )
    occurrencePeriod: Optional[Period] = Field(
        description="When service should occur",
        default=None,
    )
    occurrenceTiming: Optional[Timing] = Field(
        description="When service should occur",
        default=None,
    )
    asNeededBoolean: Optional[Boolean] = Field(
        description="Preconditions for service",
        default=None,
    )
    asNeededCodeableConcept: Optional[CodeableConcept] = Field(
        description="Preconditions for service",
        default=None,
    )
    authoredOn: Optional[DateTime] = Field(
        description="Date request signed",
        default=None,
    )
    requester: Optional[Reference] = Field(
        description="Who/what is requesting service",
        default=None,
    )
    performerType: Optional[CodeableConcept] = Field(
        description="Performer role",
        default=None,
    )
    performer: Optional[ListType[Reference]] = Field(
        description="Requested performer",
        default=None,
    )
    location: Optional[ListType[CodeableReference]] = Field(
        description="Requested location",
        default=None,
    )
    reason: Optional[ListType[CodeableReference]] = Field(
        description="Explanation/Justification for procedure or service",
        default=None,
    )
    insurance: Optional[ListType[Reference]] = Field(
        description="Associated insurance coverage",
        default=None,
    )
    supportingInfo: Optional[ListType[CodeableReference]] = Field(
        description="Additional clinical information",
        default=None,
    )
    specimen: Optional[ListType[Reference]] = Field(
        description="Procedure Samples",
        default=None,
    )
    bodySite: Optional[ListType[CodeableConcept]] = Field(
        description="Coded location on Body",
        default=None,
    )
    bodyStructure: Optional[Reference] = Field(
        description="BodyStructure-based location on the body",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Comments",
        default=None,
    )
    patientInstruction: Optional[ListType[ServiceRequestPatientInstruction]] = Field(
        description="Patient or consumer-oriented instructions",
        default=None,
    )
    relevantHistory: Optional[ListType[Reference]] = Field(
        description="Request provenance",
        default=None,
    )

    @property
    def quantity(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="quantity",
        )

    @property
    def occurrence(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="occurrence",
        )

    @property
    def asNeeded(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="asNeeded",
        )

    @model_validator(mode="after")
    def quantity_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Quantity, Ratio, Range],
            field_name_base="quantity",
            required=False,
        )

    @model_validator(mode="after")
    def occurrence_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[DateTime, Period, Timing],
            field_name_base="occurrence",
            required=False,
        )

    @model_validator(mode="after")
    def asNeeded_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Boolean, CodeableConcept],
            field_name_base="asNeeded",
            required=False,
        )

    @model_validator(mode="after")
    def FHIR_bdystr_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="bodySite.exists() implies bodyStructure.empty()",
            human="bodyStructure SHALL only be present if bodySite is not present",
            key="bdystr-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_prr_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="orderDetail.empty() or code.exists()",
            human="orderDetail SHALL only be present if code is present",
            key="prr-1",
            severity="error",
        )
