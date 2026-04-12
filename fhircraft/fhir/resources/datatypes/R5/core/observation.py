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
    Reference,
    BackboneElement,
    CodeableConcept,
    Period,
    Timing,
    Quantity,
    Range,
    Ratio,
    SampledData,
    Attachment,
    Annotation,
)
from .resource import Resource
from .domain_resource import DomainResource


class ObservationTriggeredBy(BackboneElement):
    """
    Identifies the observation(s) that triggered the performance of this observation.
    """

    observation: Optional[Reference] = Field(
        description="Triggering observation",
        default=None,
    )
    type: Optional[fhir.code] = Field(
        description="reflex | repeat | re-run",
        default=None,
    )
    reason: Optional[fhir.string] = Field(
        description="Reason that the observation was triggered",
        default=None,
    )


class ObservationReferenceRange(BackboneElement):
    """
    Guidance on how to interpret the value by comparison to a normal or recommended range.  Multiple reference ranges are interpreted as an "OR".   In other words, to represent two distinct target populations, two `referenceRange` elements would be used.
    """

    low: Optional[Quantity] = Field(
        description="Low Range, if relevant",
        default=None,
    )
    high: Optional[Quantity] = Field(
        description="High Range, if relevant",
        default=None,
    )
    normalValue: Optional[CodeableConcept] = Field(
        description="Normal value, if relevant",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Reference range qualifier",
        default=None,
    )
    appliesTo: Optional[ListType[CodeableConcept]] = Field(
        description="Reference range population",
        default=None,
    )
    age: Optional[Range] = Field(
        description="Applicable age range, if relevant",
        default=None,
    )
    text: Optional[fhir.markdown] = Field(
        description="Text based reference range in an observation",
        default=None,
    )


class ObservationComponentReferenceRange(BackboneElement):
    """
    Guidance on how to interpret the value by comparison to a normal or recommended range.
    """

    low: Optional[Quantity] = Field(
        description="Low Range, if relevant",
        default=None,
    )
    high: Optional[Quantity] = Field(
        description="High Range, if relevant",
        default=None,
    )
    normalValue: Optional[CodeableConcept] = Field(
        description="Normal value, if relevant",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Reference range qualifier",
        default=None,
    )
    appliesTo: Optional[ListType[CodeableConcept]] = Field(
        description="Reference range population",
        default=None,
    )
    age: Optional[Range] = Field(
        description="Applicable age range, if relevant",
        default=None,
    )
    text: Optional[fhir.markdown] = Field(
        description="Text based reference range in an observation",
        default=None,
    )


class ObservationComponent(BackboneElement):
    """
    Some observations have multiple component observations.  These component observations are expressed as separate code value pairs that share the same attributes.  Examples include systolic and diastolic component observations for blood pressure measurement and multiple component observations for genetics observations.
    """

    code: Optional[CodeableConcept] = Field(
        description="Type of component observation (code / type)",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="Actual component result",
        default=None,
    )
    valueCodeableConcept: Optional[CodeableConcept] = Field(
        description="Actual component result",
        default=None,
    )
    valueString: Optional[fhir.string] = Field(
        description="Actual component result",
        default=None,
    )
    valueBoolean: Optional[fhir.boolean] = Field(
        description="Actual component result",
        default=None,
    )
    valueInteger: Optional[fhir.integer] = Field(
        description="Actual component result",
        default=None,
    )
    valueRange: Optional[Range] = Field(
        description="Actual component result",
        default=None,
    )
    valueRatio: Optional[Ratio] = Field(
        description="Actual component result",
        default=None,
    )
    valueSampledData: Optional[SampledData] = Field(
        description="Actual component result",
        default=None,
    )
    valueTime: Optional[fhir.time_] = Field(
        description="Actual component result",
        default=None,
    )
    valueDateTime: Optional[fhir.dateTime] = Field(
        description="Actual component result",
        default=None,
    )
    valuePeriod: Optional[Period] = Field(
        description="Actual component result",
        default=None,
    )
    valueAttachment: Optional[Attachment] = Field(
        description="Actual component result",
        default=None,
    )
    valueReference: Optional[Reference] = Field(
        description="Actual component result",
        default=None,
    )
    dataAbsentReason: Optional[CodeableConcept] = Field(
        description="Why the component result is missing",
        default=None,
    )
    interpretation: Optional[ListType[CodeableConcept]] = Field(
        description="High, low, normal, etc",
        default=None,
    )
    referenceRange: Optional[ListType[ObservationComponentReferenceRange]] = Field(
        description="Provides guide for interpretation of component result",
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
                CodeableConcept,
                fhir.String,
                fhir.Boolean,
                fhir.Integer,
                Range,
                Ratio,
                SampledData,
                fhir.Time,
                fhir.DateTime,
                Period,
                Attachment,
                Reference,
            ],
            field_name_base="value",
            required=False,
        )


class Observation(DomainResource):
    """
    Measurements and simple assertions made about a patient, device or other subject.
    """

    _abstract = False
    _type = "Observation"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Observation"

    identifier: Optional[ListType[Identifier]] = Field(
        description="Business Identifier for observation",
        default=None,
    )
    instantiatesCanonical: Optional[fhir.canonical] = Field(
        description="Instantiates FHIR ObservationDefinition",
        default=None,
    )
    instantiatesReference: Optional[Reference] = Field(
        description="Instantiates FHIR ObservationDefinition",
        default=None,
    )
    basedOn: Optional[ListType[Reference]] = Field(
        description="Fulfills plan, proposal or order",
        default=None,
    )
    triggeredBy: Optional[ListType[ObservationTriggeredBy]] = Field(
        description="Triggering observation(s)",
        default=None,
    )
    partOf: Optional[ListType[Reference]] = Field(
        description="Part of referenced event",
        default=None,
    )
    status: Optional[fhir.code] = Field(
        description="registered | preliminary | final | amended +",
        default=None,
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description="Classification of  type of observation",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="Type of observation (code / type)",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="Who and/or what the observation is about",
        default=None,
    )
    focus: Optional[ListType[Reference]] = Field(
        description="What the observation is about, when it is not about the subject of record",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="Healthcare event during which this observation is made",
        default=None,
    )
    effectiveDateTime: Optional[fhir.dateTime] = Field(
        description="Clinically relevant time/time-period for observation",
        default=None,
    )
    effectivePeriod: Optional[Period] = Field(
        description="Clinically relevant time/time-period for observation",
        default=None,
    )
    effectiveTiming: Optional[Timing] = Field(
        description="Clinically relevant time/time-period for observation",
        default=None,
    )
    effectiveInstant: Optional[fhir.instant] = Field(
        description="Clinically relevant time/time-period for observation",
        default=None,
    )
    issued: Optional[fhir.instant] = Field(
        description="Date/time this version was made available",
        default=None,
    )
    performer: Optional[ListType[Reference]] = Field(
        description="Who is responsible for the observation",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="Actual result",
        default=None,
    )
    valueCodeableConcept: Optional[CodeableConcept] = Field(
        description="Actual result",
        default=None,
    )
    valueString: Optional[fhir.string] = Field(
        description="Actual result",
        default=None,
    )
    valueBoolean: Optional[fhir.boolean] = Field(
        description="Actual result",
        default=None,
    )
    valueInteger: Optional[fhir.integer] = Field(
        description="Actual result",
        default=None,
    )
    valueRange: Optional[Range] = Field(
        description="Actual result",
        default=None,
    )
    valueRatio: Optional[Ratio] = Field(
        description="Actual result",
        default=None,
    )
    valueSampledData: Optional[SampledData] = Field(
        description="Actual result",
        default=None,
    )
    valueTime: Optional[fhir.time_] = Field(
        description="Actual result",
        default=None,
    )
    valueDateTime: Optional[fhir.dateTime] = Field(
        description="Actual result",
        default=None,
    )
    valuePeriod: Optional[Period] = Field(
        description="Actual result",
        default=None,
    )
    valueAttachment: Optional[Attachment] = Field(
        description="Actual result",
        default=None,
    )
    valueReference: Optional[Reference] = Field(
        description="Actual result",
        default=None,
    )
    dataAbsentReason: Optional[CodeableConcept] = Field(
        description="Why the result is missing",
        default=None,
    )
    interpretation: Optional[ListType[CodeableConcept]] = Field(
        description="High, low, normal, etc",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Comments about the observation",
        default=None,
    )
    bodySite: Optional[CodeableConcept] = Field(
        description="Observed body part",
        default=None,
    )
    bodyStructure: Optional[Reference] = Field(
        description="Observed body structure",
        default=None,
    )
    method: Optional[CodeableConcept] = Field(
        description="How it was done",
        default=None,
    )
    specimen: Optional[Reference] = Field(
        description="Specimen used for this observation",
        default=None,
    )
    device: Optional[Reference] = Field(
        description="A reference to the device that generates the measurements or the device settings for the device",
        default=None,
    )
    referenceRange: Optional[ListType[ObservationReferenceRange]] = Field(
        description="Provides guide for interpretation",
        default=None,
    )
    hasMember: Optional[ListType[Reference]] = Field(
        description="Related resource that belongs to the Observation group",
        default=None,
    )
    derivedFrom: Optional[ListType[Reference]] = Field(
        description="Related resource from which the observation is made",
        default=None,
    )
    component: Optional[ListType[ObservationComponent]] = Field(
        description="Component results",
        default=None,
    )

    @property
    def instantiates(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="instantiates",
        )

    @property
    def effective(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="effective",
        )

    @property
    def value(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="value",
        )

    @model_validator(mode="after")
    def instantiates_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.Canonical, Reference],
            field_name_base="instantiates",
            required=False,
        )

    @model_validator(mode="after")
    def effective_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.DateTime, Period, Timing, fhir.Instant],
            field_name_base="effective",
            required=False,
        )

    @model_validator(mode="after")
    def value_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[
                Quantity,
                CodeableConcept,
                fhir.String,
                fhir.Boolean,
                fhir.Integer,
                Range,
                Ratio,
                SampledData,
                fhir.Time,
                fhir.DateTime,
                Period,
                Attachment,
                Reference,
            ],
            field_name_base="value",
            required=False,
        )

    @model_validator(mode="after")
    def FHIR_obs_3_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("referenceRange",),
            expression="low.exists() or high.exists() or text.exists()",
            human="Must have at least a low or a high or text",
            key="obs-3",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_obs_6_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="dataAbsentReason.empty() or value.empty()",
            human="dataAbsentReason SHALL only be present if Observation.value[x] is not present",
            key="obs-6",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_obs_7_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="value.empty() or component.code.where(coding.intersect(%resource.code.coding).exists()).empty()",
            human="If Observation.component.code is the same as Observation.code, then Observation.value SHALL NOT be present (the Observation.component.value[x] holds the value).",
            key="obs-7",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_obs_8_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="bodySite.exists() implies bodyStructure.empty()",
            human="bodyStructure SHALL only be present if Observation.bodySite is not present",
            key="obs-8",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_obs_9_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("specimen",),
            expression="(reference.resolve().exists() and reference.resolve() is Group) implies reference.resolve().member.entity.resolve().all($this is Specimen)",
            human="If Observation.specimen is a reference to Group, the group can only have specimens",
            key="obs-9",
            severity="error",
        )
