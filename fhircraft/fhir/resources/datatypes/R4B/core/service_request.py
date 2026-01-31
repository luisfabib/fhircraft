import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    Canonical,
    Boolean,
    DateTime,
)

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
    instantiatesCanonical: Optional[ListType[Canonical]] = Field(
        description="Instantiates FHIR protocol or definition",
        default=None,
    )
    instantiatesCanonical_ext: Optional[Element] = Field(
        description="Placeholder element for instantiatesCanonical extensions",
        default=None,
        alias="_instantiatesCanonical",
    )
    instantiatesUri: Optional[ListType[Uri]] = Field(
        description="Instantiates external protocol or definition",
        default=None,
    )
    instantiatesUri_ext: Optional[Element] = Field(
        description="Placeholder element for instantiatesUri extensions",
        default=None,
        alias="_instantiatesUri",
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
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    intent: Optional[Code] = Field(
        description="proposal | plan | directive | order | original-order | reflex-order | filler-order | instance-order | option",
        default=None,
    )
    intent_ext: Optional[Element] = Field(
        description="Placeholder element for intent extensions",
        default=None,
        alias="_intent",
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description="Classification of service",
        default=None,
    )
    priority: Optional[Code] = Field(
        description="routine | urgent | asap | stat",
        default=None,
    )
    priority_ext: Optional[Element] = Field(
        description="Placeholder element for priority extensions",
        default=None,
        alias="_priority",
    )
    doNotPerform: Optional[Boolean] = Field(
        description="True if service/procedure should not be performed",
        default=None,
    )
    doNotPerform_ext: Optional[Element] = Field(
        description="Placeholder element for doNotPerform extensions",
        default=None,
        alias="_doNotPerform",
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
    occurrenceDateTime: Optional[DateTime] = Field(
        description="When service should occur",
        default=None,
    )
    occurrenceDateTime_ext: Optional[Element] = Field(
        description="Placeholder element for occurrenceDateTime extensions",
        default=None,
        alias="_occurrenceDateTime",
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
    asNeededBoolean_ext: Optional[Element] = Field(
        description="Placeholder element for asNeededBoolean extensions",
        default=None,
        alias="_asNeededBoolean",
    )
    asNeededCodeableConcept: Optional[CodeableConcept] = Field(
        description="Preconditions for service",
        default=None,
    )
    authoredOn: Optional[DateTime] = Field(
        description="Date request signed",
        default=None,
    )
    authoredOn_ext: Optional[Element] = Field(
        description="Placeholder element for authoredOn extensions",
        default=None,
        alias="_authoredOn",
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
    patientInstruction: Optional[String] = Field(
        description="Patient or consumer-oriented instructions",
        default=None,
    )
    patientInstruction_ext: Optional[Element] = Field(
        description="Placeholder element for patientInstruction extensions",
        default=None,
        alias="_patientInstruction",
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
    def FHIR_prr_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="orderDetail.empty() or code.exists()",
            human="orderDetail SHALL only be present if code is present",
            key="prr-1",
            severity="error",
        )
