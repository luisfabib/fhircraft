from pydantic import Field, model_validator
from typing import Optional, List

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from fhircraft.fhir.resources.datatypes.primitives import String, Uri, Code, DateTime

from fhircraft.fhir.resources.datatypes.R5.complex import (
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
    BackboneElement,
    Annotation,
    CodeableReference,
)
from .resource import Resource
from .domain_resource import DomainResource


class AllergyIntoleranceParticipant(BackboneElement):
    """
    Indicates who or what participated in the activities related to the allergy or intolerance and how they were involved.
    """

    function: Optional[CodeableConcept] = Field(
        description="Type of involvement",
        default=None,
    )
    actor: Optional[Reference] = Field(
        description="Who or what participated in the activities related to the allergy or intolerance",
        default=None,
    )


class AllergyIntoleranceReaction(BackboneElement):
    """
    Details about each adverse reaction event linked to exposure to the identified substance.
    """

    substance: Optional[CodeableConcept] = Field(
        description="Specific substance or pharmaceutical product considered to be responsible for event",
        default=None,
    )
    manifestation: Optional[List[CodeableReference]] = Field(
        description="Clinical symptoms/signs associated with the Event",
        default=None,
    )
    description: Optional[String] = Field(
        description="Description of the event as a whole",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    onset: Optional[DateTime] = Field(
        description="Date(/time) when manifestations showed",
        default=None,
    )
    onset_ext: Optional[Element] = Field(
        description="Placeholder element for onset extensions",
        default=None,
        alias="_onset",
    )
    severity: Optional[Code] = Field(
        description="mild | moderate | severe (of event as a whole)",
        default=None,
    )
    severity_ext: Optional[Element] = Field(
        description="Placeholder element for severity extensions",
        default=None,
        alias="_severity",
    )
    exposureRoute: Optional[CodeableConcept] = Field(
        description="How the subject was exposed to the substance",
        default=None,
    )
    note: Optional[List[Annotation]] = Field(
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

    identifier: Optional[List[Identifier]] = Field(
        description="External ids for this item",
        default=None,
    )
    clinicalStatus: Optional[CodeableConcept] = Field(
        description="active | inactive | resolved",
        default=None,
    )
    verificationStatus: Optional[CodeableConcept] = Field(
        description="unconfirmed | presumed | confirmed | refuted | entered-in-error",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="allergy | intolerance - Underlying mechanism (if known)",
        default=None,
    )
    category: Optional[List[Code]] = Field(
        description="food | medication | environment | biologic",
        default=None,
    )
    category_ext: Optional[List[Optional[Element]]] = Field(
        description="Placeholder element for category extensions",
        default=None,
        alias="_category",
    )
    criticality: Optional[Code] = Field(
        description="low | high | unable-to-assess",
        default=None,
    )
    criticality_ext: Optional[Element] = Field(
        description="Placeholder element for criticality extensions",
        default=None,
        alias="_criticality",
    )
    code: Optional[CodeableConcept] = Field(
        description="Code that identifies the allergy or intolerance",
        default=None,
    )
    patient: Optional[Reference] = Field(
        description="Who the allergy or intolerance is for",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="Encounter when the allergy or intolerance was asserted",
        default=None,
    )
    onsetDateTime: Optional[DateTime] = Field(
        description="When allergy or intolerance was identified",
        default=None,
    )
    onsetDateTime_ext: Optional[Element] = Field(
        description="Placeholder element for onsetDateTime extensions",
        default=None,
        alias="_onsetDateTime",
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
    onsetString: Optional[String] = Field(
        description="When allergy or intolerance was identified",
        default=None,
    )
    onsetString_ext: Optional[Element] = Field(
        description="Placeholder element for onsetString extensions",
        default=None,
        alias="_onsetString",
    )
    recordedDate: Optional[DateTime] = Field(
        description="Date allergy or intolerance was first recorded",
        default=None,
    )
    recordedDate_ext: Optional[Element] = Field(
        description="Placeholder element for recordedDate extensions",
        default=None,
        alias="_recordedDate",
    )
    participant: Optional[List[AllergyIntoleranceParticipant]] = Field(
        description="Who or what participated in the activities related to the allergy or intolerance and how they were involved",
        default=None,
    )
    lastOccurrence: Optional[DateTime] = Field(
        description="Date(/time) of last known occurrence of a reaction",
        default=None,
    )
    lastOccurrence_ext: Optional[Element] = Field(
        description="Placeholder element for lastOccurrence extensions",
        default=None,
        alias="_lastOccurrence",
    )
    note: Optional[List[Annotation]] = Field(
        description="Additional text not captured in other fields",
        default=None,
    )
    reaction: Optional[List[AllergyIntoleranceReaction]] = Field(
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
            field_types=[DateTime, Age, Period, Range, String],
            field_name_base="onset",
            required=False,
        )
