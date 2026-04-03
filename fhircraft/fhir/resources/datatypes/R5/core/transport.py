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
    Annotation,
    BackboneElement,
    Period,
    Address,
    Age,
    Attachment,
    CodeableReference,
    Coding,
    ContactPoint,
    Count,
    Distance,
    Duration,
    HumanName,
    Money,
    Quantity,
    Range,
    Ratio,
    RatioRange,
    SampledData,
    Signature,
    Timing,
    ContactDetail,
    DataRequirement,
    Expression,
    ParameterDefinition,
    RelatedArtifact,
    TriggerDefinition,
    UsageContext,
    Availability,
    ExtendedContactDetail,
    Dosage,
)
from .resource import Resource
from .domain_resource import DomainResource

class TransportRestriction(BackboneElement):
    """
    If the Transport.focus is a request resource and the transport is seeking fulfillment (i.e. is asking for the request to be actioned), this element identifies any limitations on what parts of the referenced request should be actioned.
    """

    repetitions: Optional[PositiveInt] = Field(
        description="How many times to repeat",
        default=None,
    )
    period: Optional[Period] = Field(
        description="When fulfillment sought",
        default=None,
    )
    recipient: Optional[ListType[Reference]] = Field(
        description="For whom is fulfillment sought?",
        default=None,
    )

class TransportInput(BackboneElement):
    """
    Additional information that may be needed in the execution of the transport.
    """

    type: Optional[CodeableConcept] = Field(
        description="Label for the input",
        default=None,
    )
    valueBase64Binary: Optional[Base64Binary] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueBoolean: Optional[Boolean] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueCanonical: Optional[Canonical] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueCode: Optional[Code] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueDate: Optional[Date] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueDateTime: Optional[DateTime] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueDecimal: Optional[Decimal] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueId: Optional[Id] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueInstant: Optional[Instant] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueInteger: Optional[Integer] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueInteger64: Optional[Integer64] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueMarkdown: Optional[Markdown] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueOid: Optional[Oid] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valuePositiveInt: Optional[PositiveInt] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueString: Optional[String] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueTime: Optional[Time] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueUnsignedInt: Optional[UnsignedInt] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueUri: Optional[Uri] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueUrl: Optional[Url] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueUuid: Optional[Uuid] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueAddress: Optional[Address] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueAge: Optional[Age] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueAnnotation: Optional[Annotation] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueAttachment: Optional[Attachment] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueCodeableConcept: Optional[CodeableConcept] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueCodeableReference: Optional[CodeableReference] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueCoding: Optional[Coding] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueContactPoint: Optional[ContactPoint] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueCount: Optional[Count] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueDistance: Optional[Distance] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueDuration: Optional[Duration] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueHumanName: Optional[HumanName] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueIdentifier: Optional[Identifier] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueMoney: Optional[Money] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valuePeriod: Optional[Period] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueRange: Optional[Range] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueRatio: Optional[Ratio] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueRatioRange: Optional[RatioRange] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueReference: Optional[Reference] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueSampledData: Optional[SampledData] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueSignature: Optional[Signature] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueTiming: Optional[Timing] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueContactDetail: Optional[ContactDetail] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueDataRequirement: Optional[DataRequirement] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueExpression: Optional[Expression] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueParameterDefinition: Optional[ParameterDefinition] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueRelatedArtifact: Optional[RelatedArtifact] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueTriggerDefinition: Optional[TriggerDefinition] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueUsageContext: Optional[UsageContext] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueAvailability: Optional[Availability] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueExtendedContactDetail: Optional[ExtendedContactDetail] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueDosage: Optional[Dosage] = Field(
        description="Content to use in performing the transport",
        default=None,
    )
    valueMeta: Optional[Meta] = Field(
        description="Content to use in performing the transport",
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
                Base64Binary,
                Boolean,
                Canonical,
                Code,
                Date,
                DateTime,
                Decimal,
                Id,
                Instant,
                Integer,
                Integer64,
                Markdown,
                Oid,
                PositiveInt,
                String,
                Time,
                UnsignedInt,
                Uri,
                Url,
                Uuid,
                Address,
                Age,
                Annotation,
                Attachment,
                CodeableConcept,
                CodeableReference,
                Coding,
                ContactPoint,
                Count,
                Distance,
                Duration,
                HumanName,
                Identifier,
                Money,
                Period,
                Quantity,
                Range,
                Ratio,
                RatioRange,
                Reference,
                SampledData,
                Signature,
                Timing,
                ContactDetail,
                DataRequirement,
                Expression,
                ParameterDefinition,
                RelatedArtifact,
                TriggerDefinition,
                UsageContext,
                Availability,
                ExtendedContactDetail,
                Dosage,
                Meta,
            ],
            field_name_base="value",
            required=True,
        )

class TransportOutput(BackboneElement):
    """
    Outputs produced by the Transport.
    """

    type: Optional[CodeableConcept] = Field(
        description="Label for output",
        default=None,
    )
    valueBase64Binary: Optional[Base64Binary] = Field(
        description="Result of output",
        default=None,
    )
    valueBoolean: Optional[Boolean] = Field(
        description="Result of output",
        default=None,
    )
    valueCanonical: Optional[Canonical] = Field(
        description="Result of output",
        default=None,
    )
    valueCode: Optional[Code] = Field(
        description="Result of output",
        default=None,
    )
    valueDate: Optional[Date] = Field(
        description="Result of output",
        default=None,
    )
    valueDateTime: Optional[DateTime] = Field(
        description="Result of output",
        default=None,
    )
    valueDecimal: Optional[Decimal] = Field(
        description="Result of output",
        default=None,
    )
    valueId: Optional[Id] = Field(
        description="Result of output",
        default=None,
    )
    valueInstant: Optional[Instant] = Field(
        description="Result of output",
        default=None,
    )
    valueInteger: Optional[Integer] = Field(
        description="Result of output",
        default=None,
    )
    valueInteger64: Optional[Integer64] = Field(
        description="Result of output",
        default=None,
    )
    valueMarkdown: Optional[Markdown] = Field(
        description="Result of output",
        default=None,
    )
    valueOid: Optional[Oid] = Field(
        description="Result of output",
        default=None,
    )
    valuePositiveInt: Optional[PositiveInt] = Field(
        description="Result of output",
        default=None,
    )
    valueString: Optional[String] = Field(
        description="Result of output",
        default=None,
    )
    valueTime: Optional[Time] = Field(
        description="Result of output",
        default=None,
    )
    valueUnsignedInt: Optional[UnsignedInt] = Field(
        description="Result of output",
        default=None,
    )
    valueUri: Optional[Uri] = Field(
        description="Result of output",
        default=None,
    )
    valueUrl: Optional[Url] = Field(
        description="Result of output",
        default=None,
    )
    valueUuid: Optional[Uuid] = Field(
        description="Result of output",
        default=None,
    )
    valueAddress: Optional[Address] = Field(
        description="Result of output",
        default=None,
    )
    valueAge: Optional[Age] = Field(
        description="Result of output",
        default=None,
    )
    valueAnnotation: Optional[Annotation] = Field(
        description="Result of output",
        default=None,
    )
    valueAttachment: Optional[Attachment] = Field(
        description="Result of output",
        default=None,
    )
    valueCodeableConcept: Optional[CodeableConcept] = Field(
        description="Result of output",
        default=None,
    )
    valueCodeableReference: Optional[CodeableReference] = Field(
        description="Result of output",
        default=None,
    )
    valueCoding: Optional[Coding] = Field(
        description="Result of output",
        default=None,
    )
    valueContactPoint: Optional[ContactPoint] = Field(
        description="Result of output",
        default=None,
    )
    valueCount: Optional[Count] = Field(
        description="Result of output",
        default=None,
    )
    valueDistance: Optional[Distance] = Field(
        description="Result of output",
        default=None,
    )
    valueDuration: Optional[Duration] = Field(
        description="Result of output",
        default=None,
    )
    valueHumanName: Optional[HumanName] = Field(
        description="Result of output",
        default=None,
    )
    valueIdentifier: Optional[Identifier] = Field(
        description="Result of output",
        default=None,
    )
    valueMoney: Optional[Money] = Field(
        description="Result of output",
        default=None,
    )
    valuePeriod: Optional[Period] = Field(
        description="Result of output",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="Result of output",
        default=None,
    )
    valueRange: Optional[Range] = Field(
        description="Result of output",
        default=None,
    )
    valueRatio: Optional[Ratio] = Field(
        description="Result of output",
        default=None,
    )
    valueRatioRange: Optional[RatioRange] = Field(
        description="Result of output",
        default=None,
    )
    valueReference: Optional[Reference] = Field(
        description="Result of output",
        default=None,
    )
    valueSampledData: Optional[SampledData] = Field(
        description="Result of output",
        default=None,
    )
    valueSignature: Optional[Signature] = Field(
        description="Result of output",
        default=None,
    )
    valueTiming: Optional[Timing] = Field(
        description="Result of output",
        default=None,
    )
    valueContactDetail: Optional[ContactDetail] = Field(
        description="Result of output",
        default=None,
    )
    valueDataRequirement: Optional[DataRequirement] = Field(
        description="Result of output",
        default=None,
    )
    valueExpression: Optional[Expression] = Field(
        description="Result of output",
        default=None,
    )
    valueParameterDefinition: Optional[ParameterDefinition] = Field(
        description="Result of output",
        default=None,
    )
    valueRelatedArtifact: Optional[RelatedArtifact] = Field(
        description="Result of output",
        default=None,
    )
    valueTriggerDefinition: Optional[TriggerDefinition] = Field(
        description="Result of output",
        default=None,
    )
    valueUsageContext: Optional[UsageContext] = Field(
        description="Result of output",
        default=None,
    )
    valueAvailability: Optional[Availability] = Field(
        description="Result of output",
        default=None,
    )
    valueExtendedContactDetail: Optional[ExtendedContactDetail] = Field(
        description="Result of output",
        default=None,
    )
    valueDosage: Optional[Dosage] = Field(
        description="Result of output",
        default=None,
    )
    valueMeta: Optional[Meta] = Field(
        description="Result of output",
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
                Base64Binary,
                Boolean,
                Canonical,
                Code,
                Date,
                DateTime,
                Decimal,
                Id,
                Instant,
                Integer,
                Integer64,
                Markdown,
                Oid,
                PositiveInt,
                String,
                Time,
                UnsignedInt,
                Uri,
                Url,
                Uuid,
                Address,
                Age,
                Annotation,
                Attachment,
                CodeableConcept,
                CodeableReference,
                Coding,
                ContactPoint,
                Count,
                Distance,
                Duration,
                HumanName,
                Identifier,
                Money,
                Period,
                Quantity,
                Range,
                Ratio,
                RatioRange,
                Reference,
                SampledData,
                Signature,
                Timing,
                ContactDetail,
                DataRequirement,
                Expression,
                ParameterDefinition,
                RelatedArtifact,
                TriggerDefinition,
                UsageContext,
                Availability,
                ExtendedContactDetail,
                Dosage,
                Meta,
            ],
            field_name_base="value",
            required=True,
        )

class Transport(DomainResource):
    """
    Record of transport.
    """

    _abstract = False
    _type = "Transport"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Transport"

    identifier: Optional[ListType[Identifier]] = Field(
        description="External identifier",
        default=None,
    )
    instantiatesCanonical: Optional[Canonical] = Field(
        description="Formal definition of transport",
        default=None,
    )
    instantiatesUri: Optional[Uri] = Field(
        description="Formal definition of transport",
        default=None,
    )
    basedOn: Optional[ListType[Reference]] = Field(
        description="Request fulfilled by this transport",
        default=None,
    )
    groupIdentifier: Optional[Identifier] = Field(
        description="Requisition or grouper id",
        default=None,
    )
    partOf: Optional[ListType[Reference]] = Field(
        description="Part of referenced event",
        default=None,
    )
    status: Optional[Code] = Field(
        description="in-progress | completed | abandoned | cancelled | planned | entered-in-error",
        default=None,
    )
    statusReason: Optional[CodeableConcept] = Field(
        description="Reason for current status",
        default=None,
    )
    intent: Optional[Code] = Field(
        description="unknown | proposal | plan | order | original-order | reflex-order | filler-order | instance-order | option",
        default=None,
    )
    priority: Optional[Code] = Field(
        description="routine | urgent | asap | stat",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="Transport Type",
        default=None,
    )
    description: Optional[String] = Field(
        description="Human-readable explanation of transport",
        default=None,
    )
    focus: Optional[Reference] = Field(
        description="What transport is acting on",
        default=None,
    )
    for_: Optional[Reference] = Field(
        description="Beneficiary of the Transport",
        default=None,
        alias="for",
    )
    encounter: Optional[Reference] = Field(
        description="Healthcare event during which this transport originated",
        default=None,
    )
    completionTime: Optional[DateTime] = Field(
        description="Completion time of the event (the occurrence)",
        default=None,
    )
    authoredOn: Optional[DateTime] = Field(
        description="Transport Creation Date",
        default=None,
    )
    lastModified: Optional[DateTime] = Field(
        description="Transport Last Modified Date",
        default=None,
    )
    requester: Optional[Reference] = Field(
        description="Who is asking for transport to be done",
        default=None,
    )
    performerType: Optional[ListType[CodeableConcept]] = Field(
        description="Requested performer",
        default=None,
    )
    owner: Optional[Reference] = Field(
        description="Responsible individual",
        default=None,
    )
    location: Optional[Reference] = Field(
        description="Where transport occurs",
        default=None,
    )
    insurance: Optional[ListType[Reference]] = Field(
        description="Associated insurance coverage",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Comments made about the transport",
        default=None,
    )
    relevantHistory: Optional[ListType[Reference]] = Field(
        description="Key events in history of the Transport",
        default=None,
    )
    restriction: Optional[TransportRestriction] = Field(
        description="Constraints on fulfillment transports",
        default=None,
    )
    input: Optional[ListType[TransportInput]] = Field(
        description="Information used to perform transport",
        default=None,
    )
    output: Optional[ListType[TransportOutput]] = Field(
        description="Information produced as part of transport",
        default=None,
    )
    requestedLocation: Optional[Reference] = Field(
        description="The desired location",
        default=None,
    )
    currentLocation: Optional[Reference] = Field(
        description="The entity current location",
        default=None,
    )
    reason: Optional[CodeableReference] = Field(
        description="Why transport is needed",
        default=None,
    )
    history: Optional[Reference] = Field(
        description="Parent (or preceding) transport",
        default=None,
    )
