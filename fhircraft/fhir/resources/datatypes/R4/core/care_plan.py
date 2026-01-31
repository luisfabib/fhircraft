import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    Canonical,
    DateTime,
    Boolean,
)

from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    Period,
    BackboneElement,
    Annotation,
    Timing,
    Quantity,
)
from .resource import Resource
from .domain_resource import DomainResource


class CarePlanActivityDetail(BackboneElement):
    """
    A simple summary of a planned activity suitable for a general care plan system (e.g. form driven) that doesn't know about specific resources such as procedure etc.
    """

    kind: Optional[Code] = Field(
        description="Appointment | CommunicationRequest | DeviceRequest | MedicationRequest | NutritionOrder | Task | ServiceRequest | VisionPrescription",
        default=None,
    )
    kind_ext: Optional[Element] = Field(
        description="Placeholder element for kind extensions",
        default=None,
        alias="_kind",
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
    code: Optional[CodeableConcept] = Field(
        description="Detail type of activity",
        default=None,
    )
    reasonCode: Optional[ListType[CodeableConcept]] = Field(
        description="Why activity should be done or why activity was prohibited",
        default=None,
    )
    reasonReference: Optional[ListType[Reference]] = Field(
        description="Why activity is needed",
        default=None,
    )
    goal: Optional[ListType[Reference]] = Field(
        description="Goals this activity relates to",
        default=None,
    )
    status: Optional[Code] = Field(
        description="not-started | scheduled | in-progress | on-hold | completed | cancelled | stopped | unknown | entered-in-error",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    statusReason: Optional[CodeableConcept] = Field(
        description="Reason for current status",
        default=None,
    )
    doNotPerform: Optional[Boolean] = Field(
        description="If true, activity is prohibiting action",
        default=None,
    )
    doNotPerform_ext: Optional[Element] = Field(
        description="Placeholder element for doNotPerform extensions",
        default=None,
        alias="_doNotPerform",
    )
    scheduledTiming: Optional[Timing] = Field(
        description="When activity is to occur",
        default=None,
    )
    scheduledPeriod: Optional[Period] = Field(
        description="When activity is to occur",
        default=None,
    )
    scheduledString: Optional[String] = Field(
        description="When activity is to occur",
        default=None,
    )
    scheduledString_ext: Optional[Element] = Field(
        description="Placeholder element for scheduledString extensions",
        default=None,
        alias="_scheduledString",
    )
    location: Optional[Reference] = Field(
        description="Where it should happen",
        default=None,
    )
    performer: Optional[ListType[Reference]] = Field(
        description="Who will be responsible?",
        default=None,
    )
    productCodeableConcept: Optional[CodeableConcept] = Field(
        description="What is to be administered/supplied",
        default=None,
    )
    productReference: Optional[Reference] = Field(
        description="What is to be administered/supplied",
        default=None,
    )
    dailyAmount: Optional[Quantity] = Field(
        description="How to consume/day?",
        default=None,
    )
    quantity: Optional[Quantity] = Field(
        description="How much to administer/supply/consume",
        default=None,
    )
    description: Optional[String] = Field(
        description="Extra info describing activity to perform",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )

    @property
    def scheduled(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="scheduled",
        )

    @property
    def product(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="product",
        )

    @model_validator(mode="after")
    def scheduled_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Timing, Period, String],
            field_name_base="scheduled",
            required=False,
        )

    @model_validator(mode="after")
    def product_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[CodeableConcept, Reference],
            field_name_base="product",
            required=False,
        )


class CarePlanActivity(BackboneElement):
    """
    Identifies a planned action to occur as part of the plan.  For example, a medication to be used, lab tests to perform, self-monitoring, education, etc.
    """

    outcomeCodeableConcept: Optional[ListType[CodeableConcept]] = Field(
        description="Results of the activity",
        default=None,
    )
    outcomeReference: Optional[ListType[Reference]] = Field(
        description="Appointment, Encounter, Procedure, etc.",
        default=None,
    )
    progress: Optional[ListType[Annotation]] = Field(
        description="Comments about the activity status/progress",
        default=None,
    )
    reference: Optional[Reference] = Field(
        description="Activity details defined in specific resource",
        default=None,
    )
    detail: Optional[CarePlanActivityDetail] = Field(
        description="In-line definition of activity",
        default=None,
    )


class CarePlan(DomainResource):
    """
    Describes the intention of how one or more practitioners intend to deliver care for a particular patient, group or community for a period of time, possibly limited to care for a specific condition or set of conditions.
    """

    _abstract = False
    _type = "CarePlan"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/CarePlan"

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
        description="External Ids for this plan",
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
        description="Fulfills CarePlan",
        default=None,
    )
    replaces: Optional[ListType[Reference]] = Field(
        description="CarePlan replaced by this CarePlan",
        default=None,
    )
    partOf: Optional[ListType[Reference]] = Field(
        description="Part of referenced CarePlan",
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
        description="proposal | plan | order | option",
        default=None,
    )
    intent_ext: Optional[Element] = Field(
        description="Placeholder element for intent extensions",
        default=None,
        alias="_intent",
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description="Type of plan",
        default=None,
    )
    title: Optional[String] = Field(
        description="Human-friendly name for the care plan",
        default=None,
    )
    title_ext: Optional[Element] = Field(
        description="Placeholder element for title extensions",
        default=None,
        alias="_title",
    )
    description: Optional[String] = Field(
        description="Summary of nature of plan",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    subject: Optional[Reference] = Field(
        description="Who the care plan is for",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="Encounter created as part of",
        default=None,
    )
    period: Optional[Period] = Field(
        description="Time period plan covers",
        default=None,
    )
    created: Optional[DateTime] = Field(
        description="Date record was first recorded",
        default=None,
    )
    created_ext: Optional[Element] = Field(
        description="Placeholder element for created extensions",
        default=None,
        alias="_created",
    )
    author: Optional[Reference] = Field(
        description="Who is the designated responsible party",
        default=None,
    )
    contributor: Optional[ListType[Reference]] = Field(
        description="Who provided the content of the care plan",
        default=None,
    )
    careTeam: Optional[ListType[Reference]] = Field(
        description="Who\u0027s involved in plan?",
        default=None,
    )
    addresses: Optional[ListType[Reference]] = Field(
        description="Health issues this plan addresses",
        default=None,
    )
    supportingInfo: Optional[ListType[Reference]] = Field(
        description="Information considered as part of plan",
        default=None,
    )
    goal: Optional[ListType[Reference]] = Field(
        description="Desired outcome of plan",
        default=None,
    )
    activity: Optional[ListType[CarePlanActivity]] = Field(
        description="Action to occur as part of plan",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Comments about the plan",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_cpl_3_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("activity",),
            expression="detail.empty() or reference.empty()",
            human="Provide a reference or detail, not both",
            key="cpl-3",
            severity="error",
        )
