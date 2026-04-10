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
    Reference,
    CodeableConcept,
    Quantity,
    Ratio,
    Range,
    Period,
    Timing,
    Annotation,
)
from .resource import Resource
from .domain_resource import DomainResource


class ServiceRequest(DomainResource):
    """
    A record of a request for service such as diagnostic investigations, treatments, or operations to be performed.
    """

    _abstract = False
    _type = "ServiceRequest"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/ServiceRequest"

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
        description="Identifiers assigned to this order",
        default=None,
    )
    instantiatesCanonical: Optional[ListType[fhir.canonical]] = Field(
        description="Instantiates FHIR protocol or definition",
        default=None,
    )
    instantiatesUri: Optional[ListType[fhir.uri]] = Field(
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
    status: Optional[fhir.code] = Field(
        description="draft | active | on-hold | revoked | completed | entered-in-error | unknown",
        default=None,
    )
    intent: Optional[fhir.code] = Field(
        description="proposal | plan | directive | order | original-order | reflex-order | filler-order | instance-order | option",
        default=None,
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description="Classification of service",
        default=None,
    )
    priority: Optional[fhir.code] = Field(
        description="routine | urgent | asap | stat",
        default=None,
    )
    doNotPerform: Optional[fhir.boolean] = Field(
        description="True if service/procedure should not be performed",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="What is being requested/ordered",
        default=None,
    )
    orderDetail: Optional[ListType[CodeableConcept]] = Field(
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
    encounter: Optional[Reference] = Field(
        description="Encounter in which the request was created",
        default=None,
    )
    occurrenceDateTime: Optional[fhir.dateTime] = Field(
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
    asNeededBoolean: Optional[fhir.boolean] = Field(
        description="Preconditions for service",
        default=None,
    )
    asNeededCodeableConcept: Optional[CodeableConcept] = Field(
        description="Preconditions for service",
        default=None,
    )
    authoredOn: Optional[fhir.dateTime] = Field(
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
    locationCode: Optional[ListType[CodeableConcept]] = Field(
        description="Requested location",
        default=None,
    )
    locationReference: Optional[ListType[Reference]] = Field(
        description="Requested location",
        default=None,
    )
    reasonCode: Optional[ListType[CodeableConcept]] = Field(
        description="Explanation/Justification for procedure or service",
        default=None,
    )
    reasonReference: Optional[ListType[Reference]] = Field(
        description="Explanation/Justification for service or service",
        default=None,
    )
    insurance: Optional[ListType[Reference]] = Field(
        description="Associated insurance coverage",
        default=None,
    )
    supportingInfo: Optional[ListType[Reference]] = Field(
        description="Additional clinical information",
        default=None,
    )
    specimen: Optional[ListType[Reference]] = Field(
        description="Procedure Samples",
        default=None,
    )
    bodySite: Optional[ListType[CodeableConcept]] = Field(
        description="Location on Body",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Comments",
        default=None,
    )
    patientInstruction: Optional[fhir.string] = Field(
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
            field_types=[fhir.dateTime, Period, Timing],
            field_name_base="occurrence",
            required=False,
        )

    @model_validator(mode="after")
    def asNeeded_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.boolean, CodeableConcept],
            field_name_base="asNeeded",
            required=False,
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
