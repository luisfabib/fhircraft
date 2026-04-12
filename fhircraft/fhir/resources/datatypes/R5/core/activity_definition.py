from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators


import fhircraft.fhir.resources.datatypes.R5.primitive as fhir
from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    Identifier,
    Coding,
    CodeableConcept,
    Reference,
    ContactDetail,
    UsageContext,
    Period,
    RelatedArtifact,
    Timing,
    Age,
    Range,
    Duration,
    CodeableReference,
    BackboneElement,
    Quantity,
    Dosage,
    Expression,
)
from .domain_resource import DomainResource


class ActivityDefinitionParticipant(BackboneElement):
    """
    Indicates who should participate in performing the action described.
    """

    type: Optional[fhir.code] = Field(
        description="careteam | device | group | healthcareservice | location | organization | patient | practitioner | practitionerrole | relatedperson",
        default=None,
    )
    typeCanonical: Optional[fhir.canonical] = Field(
        description="Who or what can participate",
        default=None,
    )
    typeReference: Optional[Reference] = Field(
        description="Who or what can participate",
        default=None,
    )
    role: Optional[CodeableConcept] = Field(
        description="E.g. Nurse, Surgeon, Parent, etc",
        default=None,
    )
    function: Optional[CodeableConcept] = Field(
        description="E.g. Author, Reviewer, Witness, etc",
        default=None,
    )


class ActivityDefinitionDynamicValue(BackboneElement):
    """
    Dynamic values that will be evaluated to produce values for elements of the resulting resource. For example, if the dosage of a medication must be computed based on the patient's weight, a dynamic value would be used to specify an expression that calculated the weight, and the path on the request resource that would contain the result.
    """

    path: Optional[fhir.string] = Field(
        description="The path to the element to be set dynamically",
        default=None,
    )
    expression: Optional[Expression] = Field(
        description="An expression that provides the dynamic value for the customization",
        default=None,
    )


class ActivityDefinition(DomainResource):
    """
    This resource allows for the definition of some activity to be performed, independent of a particular patient, practitioner, or other performance context.
    """

    _abstract = False
    _type = "ActivityDefinition"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/ActivityDefinition"

    url: Optional[fhir.uri] = Field(
        description="canonical identifier for this activity definition, represented as a URI (globally unique)",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Additional identifier for the activity definition",
        default=None,
    )
    version: Optional[fhir.string] = Field(
        description="Business version of the activity definition",
        default=None,
    )
    versionAlgorithmString: Optional[fhir.string] = Field(
        description="How to compare versions",
        default=None,
    )
    versionAlgorithmCoding: Optional[Coding] = Field(
        description="How to compare versions",
        default=None,
    )
    name: Optional[fhir.string] = Field(
        description="Name for this activity definition (computer friendly)",
        default=None,
    )
    title: Optional[fhir.string] = Field(
        description="Name for this activity definition (human friendly)",
        default=None,
    )
    subtitle: Optional[fhir.string] = Field(
        description="Subordinate title of the activity definition",
        default=None,
    )
    status: Optional[fhir.code] = Field(
        description="draft | active | retired | unknown",
        default=None,
    )
    experimental: Optional[fhir.boolean] = Field(
        description="For testing purposes, not real usage",
        default=None,
    )
    subjectCodeableConcept: Optional[CodeableConcept] = Field(
        description="Type of individual the activity definition is intended for",
        default=None,
    )
    subjectReference: Optional[Reference] = Field(
        description="Type of individual the activity definition is intended for",
        default=None,
    )
    subjectCanonical: Optional[fhir.canonical] = Field(
        description="Type of individual the activity definition is intended for",
        default=None,
    )
    date: Optional[fhir.dateTime] = Field(
        description="Date last changed",
        default=None,
    )
    publisher: Optional[fhir.string] = Field(
        description="Name of the publisher/steward (organization or individual)",
        default=None,
    )
    contact: Optional[ListType[ContactDetail]] = Field(
        description="Contact details for the publisher",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
        description="Natural language description of the activity definition",
        default=None,
    )
    useContext: Optional[ListType[UsageContext]] = Field(
        description="The context that the content is intended to support",
        default=None,
    )
    jurisdiction: Optional[ListType[CodeableConcept]] = Field(
        description="Intended jurisdiction for activity definition (if applicable)",
        default=None,
    )
    purpose: Optional[fhir.markdown] = Field(
        description="Why this activity definition is defined",
        default=None,
    )
    usage: Optional[fhir.markdown] = Field(
        description="Describes the clinical usage of the activity definition",
        default=None,
    )
    copyright: Optional[fhir.markdown] = Field(
        description="Use and/or publishing restrictions",
        default=None,
    )
    copyrightLabel: Optional[fhir.string] = Field(
        description="Copyright holder and year(s)",
        default=None,
    )
    approvalDate: Optional[fhir.date_] = Field(
        description="When the activity definition was approved by publisher",
        default=None,
    )
    lastReviewDate: Optional[fhir.date_] = Field(
        description="When the activity definition was last reviewed by the publisher",
        default=None,
    )
    effectivePeriod: Optional[Period] = Field(
        description="When the activity definition is expected to be used",
        default=None,
    )
    topic: Optional[ListType[CodeableConcept]] = Field(
        description="E.g. Education, Treatment, Assessment, etc",
        default=None,
    )
    author: Optional[ListType[ContactDetail]] = Field(
        description="Who authored the content",
        default=None,
    )
    editor: Optional[ListType[ContactDetail]] = Field(
        description="Who edited the content",
        default=None,
    )
    reviewer: Optional[ListType[ContactDetail]] = Field(
        description="Who reviewed the content",
        default=None,
    )
    endorser: Optional[ListType[ContactDetail]] = Field(
        description="Who endorsed the content",
        default=None,
    )
    relatedArtifact: Optional[ListType[RelatedArtifact]] = Field(
        description="Additional documentation, citations, etc",
        default=None,
    )
    library: Optional[ListType[fhir.canonical]] = Field(
        description="Logic used by the activity definition",
        default=None,
    )
    kind: Optional[fhir.code] = Field(
        description="Kind of resource",
        default=None,
    )
    profile: Optional[fhir.canonical] = Field(
        description="What profile the resource needs to conform to",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="Detail type of activity",
        default=None,
    )
    intent: Optional[fhir.code] = Field(
        description="proposal | plan | directive | order | original-order | reflex-order | filler-order | instance-order | option",
        default=None,
    )
    priority: Optional[fhir.code] = Field(
        description="routine | urgent | asap | stat",
        default=None,
    )
    doNotPerform: Optional[fhir.boolean] = Field(
        description="True if the activity should not be performed",
        default=None,
    )
    timingTiming: Optional[Timing] = Field(
        description="When activity is to occur",
        default=None,
    )
    timingAge: Optional[Age] = Field(
        description="When activity is to occur",
        default=None,
    )
    timingRange: Optional[Range] = Field(
        description="When activity is to occur",
        default=None,
    )
    timingDuration: Optional[Duration] = Field(
        description="When activity is to occur",
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
    location: Optional[CodeableReference] = Field(
        description="Where it should happen",
        default=None,
    )
    participant: Optional[ListType[ActivityDefinitionParticipant]] = Field(
        description="Who should participate in the action",
        default=None,
    )
    productReference: Optional[Reference] = Field(
        description="What\u0027s administered/supplied",
        default=None,
    )
    productCodeableConcept: Optional[CodeableConcept] = Field(
        description="What\u0027s administered/supplied",
        default=None,
    )
    quantity: Optional[Quantity] = Field(
        description="How much is administered/consumed/supplied",
        default=None,
    )
    dosage: Optional[ListType[Dosage]] = Field(
        description="Detailed dosage instructions",
        default=None,
    )
    bodySite: Optional[ListType[CodeableConcept]] = Field(
        description="What part of body to perform on",
        default=None,
    )
    specimenRequirement: Optional[ListType[fhir.canonical]] = Field(
        description="What specimens are required to perform this action",
        default=None,
    )
    observationRequirement: Optional[ListType[fhir.canonical]] = Field(
        description="What observations are required to perform this action",
        default=None,
    )
    observationResultRequirement: Optional[ListType[fhir.canonical]] = Field(
        description="What observations must be produced by this action",
        default=None,
    )
    transform: Optional[fhir.canonical] = Field(
        description="Transform to apply the template",
        default=None,
    )
    dynamicValue: Optional[ListType[ActivityDefinitionDynamicValue]] = Field(
        description="Dynamic aspects of the definition",
        default=None,
    )

    @property
    def versionAlgorithm(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="versionAlgorithm",
        )

    @property
    def subject(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="subject",
        )

    @property
    def timing(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="timing",
        )

    @property
    def asNeeded(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="asNeeded",
        )

    @property
    def product(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="product",
        )

    @model_validator(mode="after")
    def versionAlgorithm_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.String, Coding],
            field_name_base="versionAlgorithm",
            required=False,
        )

    @model_validator(mode="after")
    def subject_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[CodeableConcept, Reference, fhir.Canonical],
            field_name_base="subject",
            required=False,
        )

    @model_validator(mode="after")
    def timing_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Timing, Age, Range, Duration],
            field_name_base="timing",
            required=False,
        )

    @model_validator(mode="after")
    def asNeeded_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.Boolean, CodeableConcept],
            field_name_base="asNeeded",
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

    @model_validator(mode="after")
    def FHIR_cnl_0_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.exists() implies name.matches('^[A-Z]([A-Za-z0-9_]){1,254}$')",
            human="Name should be usable as an identifier for the module by machine processing applications such as code generation",
            key="cnl-0",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_cnl_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("url",),
            expression="exists() implies matches('^[^|# ]+$')",
            human="URL should not contain | or # - these characters make processing canonical references problematic",
            key="cnl-1",
            severity="warning",
        )
