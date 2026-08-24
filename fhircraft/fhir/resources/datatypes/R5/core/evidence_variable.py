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
    Coding,
    ContactDetail,
    Annotation,
    UsageContext,
    Period,
    RelatedArtifact,
    BackboneElement,
    Reference,
    CodeableConcept,
    Expression,
    Quantity,
    Range,
)
from .resource import Resource
from .domain_resource import DomainResource


class EvidenceVariableCharacteristicDefinitionByTypeAndValue(BackboneElement):
    """
    Defines the characteristic using both a type and value[x] elements.
    """

    type: CodeableConcept = Field(
        description="Expresses the type of characteristic",
    )
    method: Optional[ListType[CodeableConcept]] = Field(
        description="Method for how the characteristic value was determined",
        default=None,
    )
    device: Optional[Reference] = Field(
        description="Device used for determining characteristic",
        default=None,
    )
    valueCodeableConcept: Optional[CodeableConcept] = Field(
        description="Defines the characteristic when coupled with characteristic.type",
        default=None,
    )
    valueBoolean: Optional[fhir.boolean] = Field(
        description="Defines the characteristic when coupled with characteristic.type",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="Defines the characteristic when coupled with characteristic.type",
        default=None,
    )
    valueRange: Optional[Range] = Field(
        description="Defines the characteristic when coupled with characteristic.type",
        default=None,
    )
    valueReference: Optional[Reference] = Field(
        description="Defines the characteristic when coupled with characteristic.type",
        default=None,
    )
    valueId: Optional[fhir.id_] = Field(
        description="Defines the characteristic when coupled with characteristic.type",
        default=None,
    )
    offset: Optional[CodeableConcept] = Field(
        description="Reference point for valueQuantity or valueRange",
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
                CodeableConcept,
                fhir.Boolean,
                Quantity,
                Range,
                Reference,
                fhir.Id,
            ],
            field_name_base="value",
            required=True,
        )


class EvidenceVariableCharacteristicDefinitionByCombination(BackboneElement):
    """
    Defines the characteristic as a combination of two or more characteristics.
    """

    code: fhir.code = Field(
        description="all-of | any-of | at-least | at-most | statistical | net-effect | dataset",
    )
    threshold: Optional[fhir.positiveInt] = Field(
        description='Provides the value of "n" when "at-least" or "at-most" codes are used',
        default=None,
    )
    characteristic: ListType["EvidenceVariableCharacteristic"] = Field(
        description="A defining factor of the characteristic",
    )


class EvidenceVariableCharacteristicTimeFromEvent(BackboneElement):
    """
    Timing in which the characteristic is determined.
    """

    description: Optional[fhir.markdown] = Field(
        description="Human readable description",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Used for footnotes or explanatory notes",
        default=None,
    )
    eventCodeableConcept: Optional[CodeableConcept] = Field(
        description="The event used as a base point (reference point) in time",
        default=None,
    )
    eventReference: Optional[Reference] = Field(
        description="The event used as a base point (reference point) in time",
        default=None,
    )
    eventDateTime: Optional[fhir.dateTime] = Field(
        description="The event used as a base point (reference point) in time",
        default=None,
    )
    eventId: Optional[fhir.id_] = Field(
        description="The event used as a base point (reference point) in time",
        default=None,
    )
    quantity: Optional[Quantity] = Field(
        description="Used to express the observation at a defined amount of time before or after the event",
        default=None,
    )
    range: Optional[Range] = Field(
        description="Used to express the observation within a period before and/or after the event",
        default=None,
    )

    @property
    def event(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="event",
        )

    @model_validator(mode="after")
    def event_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[CodeableConcept, Reference, fhir.DateTime, fhir.Id],
            field_name_base="event",
            required=False,
        )


class EvidenceVariableCharacteristic(BackboneElement):
    """
    A defining factor of the EvidenceVariable. Multiple characteristics are applied with "and" semantics.
    """

    linkId: Optional[fhir.id_] = Field(
        description="Label for internal linking",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
        description="Natural language description of the characteristic",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Used for footnotes or explanatory notes",
        default=None,
    )
    exclude: Optional[fhir.boolean] = Field(
        description="Whether the characteristic is an inclusion criterion or exclusion criterion",
        default=None,
    )
    definitionReference: Optional[Reference] = Field(
        description="Defines the characteristic (without using type and value) by a Reference",
        default=None,
    )
    definitionCanonical: Optional[fhir.canonical] = Field(
        description="Defines the characteristic (without using type and value) by a canonical",
        default=None,
    )
    definitionCodeableConcept: Optional[CodeableConcept] = Field(
        description="Defines the characteristic (without using type and value) by a CodeableConcept",
        default=None,
    )
    definitionExpression: Optional[Expression] = Field(
        description="Defines the characteristic (without using type and value) by an expression",
        default=None,
    )
    definitionId: Optional[fhir.id_] = Field(
        description="Defines the characteristic (without using type and value) by an id",
        default=None,
    )
    definitionByTypeAndValue: Optional[
        EvidenceVariableCharacteristicDefinitionByTypeAndValue
    ] = Field(
        description="Defines the characteristic using type and value",
        default=None,
    )
    definitionByCombination: Optional[
        EvidenceVariableCharacteristicDefinitionByCombination
    ] = Field(
        description="Used to specify how two or more characteristics are combined",
        default=None,
    )
    instancesQuantity: Optional[Quantity] = Field(
        description="Number of occurrences meeting the characteristic",
        default=None,
    )
    instancesRange: Optional[Range] = Field(
        description="Number of occurrences meeting the characteristic",
        default=None,
    )
    durationQuantity: Optional[Quantity] = Field(
        description="Length of time in which the characteristic is met",
        default=None,
    )
    durationRange: Optional[Range] = Field(
        description="Length of time in which the characteristic is met",
        default=None,
    )
    timeFromEvent: Optional[ListType[EvidenceVariableCharacteristicTimeFromEvent]] = (
        Field(
            description="Timing in which the characteristic is determined",
            default=None,
        )
    )

    @property
    def instances(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="instances",
        )

    @property
    def duration(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="duration",
        )

    @model_validator(mode="after")
    def instances_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Quantity, Range],
            field_name_base="instances",
            required=False,
        )

    @model_validator(mode="after")
    def duration_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Quantity, Range],
            field_name_base="duration",
            required=False,
        )


class EvidenceVariableCategory(BackboneElement):
    """
    A grouping for ordinal or polychotomous variables.
    """

    name: Optional[fhir.string] = Field(
        description="Description of the grouping",
        default=None,
    )
    valueCodeableConcept: Optional[CodeableConcept] = Field(
        description="Definition of the grouping",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="Definition of the grouping",
        default=None,
    )
    valueRange: Optional[Range] = Field(
        description="Definition of the grouping",
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
            field_types=[CodeableConcept, Quantity, Range],
            field_name_base="value",
            required=False,
        )


class EvidenceVariable(DomainResource):
    """
    The EvidenceVariable resource describes an element that knowledge (Evidence) is about.
    """

    _abstract = False
    _type = "EvidenceVariable"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/EvidenceVariable"

    url: Optional[fhir.uri] = Field(
        description="canonical identifier for this evidence variable, represented as a URI (globally unique)",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Additional identifier for the evidence variable",
        default=None,
    )
    version: Optional[fhir.string] = Field(
        description="Business version of the evidence variable",
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
        description="Name for this evidence variable (computer friendly)",
        default=None,
    )
    title: Optional[fhir.string] = Field(
        description="Name for this evidence variable (human friendly)",
        default=None,
    )
    shortTitle: Optional[fhir.string] = Field(
        description="Title for use in informal contexts",
        default=None,
    )
    status: fhir.code = Field(
        description="draft | active | retired | unknown",
    )
    experimental: Optional[fhir.boolean] = Field(
        description="For testing purposes, not real usage",
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
        description="Natural language description of the evidence variable",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Used for footnotes or explanatory notes",
        default=None,
    )
    useContext: Optional[ListType[UsageContext]] = Field(
        description="The context that the content is intended to support",
        default=None,
    )
    purpose: Optional[fhir.markdown] = Field(
        description="Why this EvidenceVariable is defined",
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
        description="When the resource was approved by publisher",
        default=None,
    )
    lastReviewDate: Optional[fhir.date_] = Field(
        description="When the resource was last reviewed by the publisher",
        default=None,
    )
    effectivePeriod: Optional[Period] = Field(
        description="When the resource is expected to be used",
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
    actual: Optional[fhir.boolean] = Field(
        description="Actual or conceptual",
        default=None,
    )
    characteristic: Optional[ListType[EvidenceVariableCharacteristic]] = Field(
        description="A defining factor of the EvidenceVariable",
        default=None,
    )
    handling: Optional[fhir.code] = Field(
        description="continuous | dichotomous | ordinal | polychotomous",
        default=None,
    )
    category: Optional[ListType[EvidenceVariableCategory]] = Field(
        description="A grouping for ordinal or polychotomous variables",
        default=None,
    )

    @property
    def versionAlgorithm(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="versionAlgorithm",
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

    @model_validator(mode="after")
    def FHIR_evv_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("characteristic",),
            expression="(definitionReference.count() + definitionCanonical.count() + definitionCodeableConcept.count() + definitionId.count() + definitionByTypeAndValue.count() + definitionByCombination.count())  < 2",
            human="In a characteristic, at most one of these six elements shall be used: definitionReference or definitionCanonical or definitionCodeableConcept or definitionId or definitionByTypeAndValue or definitionByCombination",
            key="evv-1",
            severity="error",
        )
