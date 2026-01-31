from pydantic import Field, model_validator
from typing import Optional, List

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from fhircraft.fhir.resources.datatypes.primitives import (
    Code,
    DateTime,
    Boolean,
)

from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    Identifier,
    CodeableConcept,
    Reference,
    Period,
    Timing,
    BackboneElement,
    Annotation,
)
from .domain_resource import DomainResource


class AdverseEventParticipant(BackboneElement):
    """
    Indicates who or what participated in the adverse event and how they were involved.
    """

    function: Optional[CodeableConcept] = Field(
        description="Type of involvement",
        default=None,
    )
    actor: Optional[Reference] = Field(
        description="Who was involved in the adverse event or the potential adverse event",
        default=None,
    )


class AdverseEventSuspectEntityCausality(BackboneElement):
    """
    Information on the possible cause of the event.
    """

    assessmentMethod: Optional[CodeableConcept] = Field(
        description="Method of evaluating the relatedness of the suspected entity to the event",
        default=None,
    )
    entityRelatedness: Optional[CodeableConcept] = Field(
        description="Result of the assessment regarding the relatedness of the suspected entity to the event",
        default=None,
    )
    author: Optional[Reference] = Field(
        description="Author of the information on the possible cause of the event",
        default=None,
    )


class AdverseEventSuspectEntity(BackboneElement):
    """
    Describes the entity that is suspected to have caused the adverse event.
    """

    instanceCodeableConcept: Optional[CodeableConcept] = Field(
        description="Refers to the specific entity that caused the adverse event",
        default=None,
    )
    instanceReference: Optional[Reference] = Field(
        description="Refers to the specific entity that caused the adverse event",
        default=None,
    )
    causality: Optional[AdverseEventSuspectEntityCausality] = Field(
        description="Information on the possible cause of the event",
        default=None,
    )

    @property
    def instance(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="instance",
        )

    @model_validator(mode="after")
    def instance_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[CodeableConcept, Reference],
            field_name_base="instance",
            required=True,
        )


class AdverseEventContributingFactor(BackboneElement):
    """
    The contributing factors suspected to have increased the probability or severity of the adverse event.
    """

    itemReference: Optional[Reference] = Field(
        description="Item suspected to have increased the probability or severity of the adverse event",
        default=None,
    )
    itemCodeableConcept: Optional[CodeableConcept] = Field(
        description="Item suspected to have increased the probability or severity of the adverse event",
        default=None,
    )

    @property
    def item(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="item",
        )

    @model_validator(mode="after")
    def item_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Reference, CodeableConcept],
            field_name_base="item",
            required=True,
        )


class AdverseEventPreventiveAction(BackboneElement):
    """
    Preventive actions that contributed to avoiding the adverse event.
    """

    itemReference: Optional[Reference] = Field(
        description="Action that contributed to avoiding the adverse event",
        default=None,
    )
    itemCodeableConcept: Optional[CodeableConcept] = Field(
        description="Action that contributed to avoiding the adverse event",
        default=None,
    )

    @property
    def item(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="item",
        )

    @model_validator(mode="after")
    def item_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Reference, CodeableConcept],
            field_name_base="item",
            required=True,
        )


class AdverseEventMitigatingAction(BackboneElement):
    """
    The ameliorating action taken after the adverse event occured in order to reduce the extent of harm.
    """

    itemReference: Optional[Reference] = Field(
        description="Ameliorating action taken after the adverse event occured in order to reduce the extent of harm",
        default=None,
    )
    itemCodeableConcept: Optional[CodeableConcept] = Field(
        description="Ameliorating action taken after the adverse event occured in order to reduce the extent of harm",
        default=None,
    )

    @property
    def item(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="item",
        )

    @model_validator(mode="after")
    def item_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Reference, CodeableConcept],
            field_name_base="item",
            required=True,
        )


class AdverseEventSupportingInfo(BackboneElement):
    """
    Supporting information relevant to the event.
    """

    itemReference: Optional[Reference] = Field(
        description="Subject medical history or document relevant to this adverse event",
        default=None,
    )
    itemCodeableConcept: Optional[CodeableConcept] = Field(
        description="Subject medical history or document relevant to this adverse event",
        default=None,
    )

    @property
    def item(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="item",
        )

    @model_validator(mode="after")
    def item_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Reference, CodeableConcept],
            field_name_base="item",
            required=True,
        )


class AdverseEvent(DomainResource):
    """
    An event (i.e. any change to current patient status) that may be related to unintended effects on a patient or research participant. The unintended effects may require additional monitoring, treatment, hospitalization, or may result in death. The AdverseEvent resource also extends to potential or avoided events that could have had such effects. There are two major domains where the AdverseEvent resource is expected to be used. One is in clinical care reported adverse events and the other is in reporting adverse events in clinical  research trial management.  Adverse events can be reported by healthcare providers, patients, caregivers or by medical products manufacturers.  Given the differences between these two concepts, we recommend consulting the domain specific implementation guides when implementing the AdverseEvent Resource. The implementation guides include specific extensions, value sets and constraints.
    """

    _abstract = False
    _type = "AdverseEvent"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/AdverseEvent"

    identifier: Optional[List[Identifier]] = Field(
        description="Business identifier for the event",
        default=None,
    )
    status: Optional[Code] = Field(
        description="in-progress | completed | entered-in-error | unknown",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    actuality: Optional[Code] = Field(
        description="actual | potential",
        default=None,
    )
    actuality_ext: Optional[Element] = Field(
        description="Placeholder element for actuality extensions",
        default=None,
        alias="_actuality",
    )
    category: Optional[List[CodeableConcept]] = Field(
        description="wrong-patient | procedure-mishap | medication-mishap | device | unsafe-physical-environment | hospital-aquired-infection | wrong-body-site",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="Event or incident that occurred or was averted",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="Subject impacted by event",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="The Encounter associated with the start of the AdverseEvent",
        default=None,
    )
    occurrenceDateTime: Optional[DateTime] = Field(
        description="When the event occurred",
        default=None,
    )
    occurrenceDateTime_ext: Optional[Element] = Field(
        description="Placeholder element for occurrenceDateTime extensions",
        default=None,
        alias="_occurrenceDateTime",
    )
    occurrencePeriod: Optional[Period] = Field(
        description="When the event occurred",
        default=None,
    )
    occurrenceTiming: Optional[Timing] = Field(
        description="When the event occurred",
        default=None,
    )
    detected: Optional[DateTime] = Field(
        description="When the event was detected",
        default=None,
    )
    detected_ext: Optional[Element] = Field(
        description="Placeholder element for detected extensions",
        default=None,
        alias="_detected",
    )
    recordedDate: Optional[DateTime] = Field(
        description="When the event was recorded",
        default=None,
    )
    recordedDate_ext: Optional[Element] = Field(
        description="Placeholder element for recordedDate extensions",
        default=None,
        alias="_recordedDate",
    )
    resultingEffect: Optional[List[Reference]] = Field(
        description="Effect on the subject due to this event",
        default=None,
    )
    location: Optional[Reference] = Field(
        description="Location where adverse event occurred",
        default=None,
    )
    seriousness: Optional[CodeableConcept] = Field(
        description="Seriousness or gravity of the event",
        default=None,
    )
    outcome: Optional[List[CodeableConcept]] = Field(
        description="Type of outcome from the adverse event",
        default=None,
    )
    recorder: Optional[Reference] = Field(
        description="Who recorded the adverse event",
        default=None,
    )
    participant: Optional[List[AdverseEventParticipant]] = Field(
        description="Who was involved in the adverse event or the potential adverse event and what they did",
        default=None,
    )
    study: Optional[List[Reference]] = Field(
        description="Research study that the subject is enrolled in",
        default=None,
    )
    expectedInResearchStudy: Optional[Boolean] = Field(
        description="Considered likely or probable or anticipated in the research study",
        default=None,
    )
    expectedInResearchStudy_ext: Optional[Element] = Field(
        description="Placeholder element for expectedInResearchStudy extensions",
        default=None,
        alias="_expectedInResearchStudy",
    )
    suspectEntity: Optional[List[AdverseEventSuspectEntity]] = Field(
        description="The suspected agent causing the adverse event",
        default=None,
    )
    contributingFactor: Optional[List[AdverseEventContributingFactor]] = Field(
        description="Contributing factors suspected to have increased the probability or severity of the adverse event",
        default=None,
    )
    preventiveAction: Optional[List[AdverseEventPreventiveAction]] = Field(
        description="Preventive actions that contributed to avoiding the adverse event",
        default=None,
    )
    mitigatingAction: Optional[List[AdverseEventMitigatingAction]] = Field(
        description="Ameliorating actions taken after the adverse event occured in order to reduce the extent of harm",
        default=None,
    )
    supportingInfo: Optional[List[AdverseEventSupportingInfo]] = Field(
        description="Supporting information relevant to the event",
        default=None,
    )
    note: Optional[List[Annotation]] = Field(
        description="Comment on adverse event",
        default=None,
    )

    @property
    def occurrence(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="occurrence",
        )

    @model_validator(mode="after")
    def occurrence_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[DateTime, Period, Timing],
            field_name_base="occurrence",
            required=False,
        )
