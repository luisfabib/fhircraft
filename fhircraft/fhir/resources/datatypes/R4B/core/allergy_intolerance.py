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
    CodeableConcept,
    Reference,
    Age,
    Period,
    Range,
    Annotation,
    BackboneElement,
)
from .resource import Resource
from .domain_resource import DomainResource


class AllergyIntoleranceReaction(BackboneElement):
    """
    Details about each adverse reaction event linked to exposure to the identified substance.
    """

    substance: Optional[CodeableConcept] = Field(
        description="Specific substance or pharmaceutical product considered to be responsible for event",
        default=None,
    )
    manifestation: ListType[CodeableConcept] = Field(
        description="Clinical symptoms/signs associated with the Event",
     	min_length=1,
	)
    description: Optional[fhir.string] = Field(
        description="Description of the event as a whole",
        default=None,
    )
    onset: Optional[fhir.dateTime] = Field(
        description="Date(/time) when manifestations showed",
        default=None,
    )
    severity: Optional[fhir.code] = Field(
        description="mild | moderate | severe (of event as a whole)",
        default=None,
    )
    exposureRoute: Optional[CodeableConcept] = Field(
        description="How the subject was exposed to the substance",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Text about event not captured in other fields",
        default=None,
    )


class AllergyIntolerance(DomainResource):
    """
    Risk of harmful or undesirable, physiological response which is unique to an individual and associated with exposure to a substance.
    """

    _abstract = False
    _type = "AllergyIntolerance"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/AllergyIntolerance"

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
        description="External ids for this item",
        default=None,
    )
    clinicalStatus: Optional[CodeableConcept] = Field(
        description="active | inactive | resolved",
        default=None,
    )
    verificationStatus: Optional[CodeableConcept] = Field(
        description="unconfirmed | confirmed | refuted | entered-in-error",
        default=None,
    )
    type: Optional[fhir.code] = Field(
        description="allergy | intolerance - Underlying mechanism (if known)",
        default=None,
    )
    category: Optional[ListType[fhir.code]] = Field(
        description="food | medication | environment | biologic",
        default=None,
    )
    criticality: Optional[fhir.code] = Field(
        description="low | high | unable-to-assess",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="code that identifies the allergy or intolerance",
        default=None,
    )
    patient: Reference = Field(
        description="Who the sensitivity is for",
    )
    encounter: Optional[Reference] = Field(
        description="Encounter when the allergy or intolerance was asserted",
        default=None,
    )
    onsetDateTime: Optional[fhir.dateTime] = Field(
        description="When allergy or intolerance was identified",
        default=None,
    )
    onsetAge: Optional[Age] = Field(
        description="When allergy or intolerance was identified",
        default=None,
    )
    onsetPeriod: Optional[Period] = Field(
        description="When allergy or intolerance was identified",
        default=None,
    )
    onsetRange: Optional[Range] = Field(
        description="When allergy or intolerance was identified",
        default=None,
    )
    onsetString: Optional[fhir.string] = Field(
        description="When allergy or intolerance was identified",
        default=None,
    )
    recordedDate: Optional[fhir.dateTime] = Field(
        description="Date first version of the resource instance was recorded",
        default=None,
    )
    recorder: Optional[Reference] = Field(
        description="Who recorded the sensitivity",
        default=None,
    )
    asserter: Optional[Reference] = Field(
        description="Source of the information about the allergy",
        default=None,
    )
    lastOccurrence: Optional[fhir.dateTime] = Field(
        description="Date(/time) of last known occurrence of a reaction",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Additional text not captured in other fields",
        default=None,
    )
    reaction: Optional[ListType[AllergyIntoleranceReaction]] = Field(
        description="Adverse Reaction Events linked to exposure to substance",
        default=None,
    )

    @property
    def onset(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="onset",
        )

    @model_validator(mode="after")
    def onset_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.DateTime, Age, Period, Range, fhir.String],
            field_name_base="onset",
            required=False,
        )

    @model_validator(mode="after")
    def FHIR_ait_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(verificationStatus.exists() and verificationStatus.coding.where(system='http://terminology.hl7.org/CodeSystem/allergyintolerance-verification' and code='entered-in-error').exists().not()) implies clinicalStatus.exists()",
            human="AllergyIntolerance.clinicalStatus SHALL be present if verificationStatus is not entered-in-error.",
            key="ait-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ait_2_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(verificationStatus.coding.where(system='http://terminology.hl7.org/CodeSystem/allergyintolerance-verification' and code='entered-in-error').exists()) implies clinicalStatus.exists().not()",
            human="AllergyIntolerance.clinicalStatus SHALL NOT be present if verification Status is entered-in-error",
            key="ait-2",
            severity="error",
        )
