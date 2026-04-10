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
    BackboneElement,
)
from .resource import Resource
from .domain_resource import DomainResource

class AdverseEventSuspectEntityCausality(BackboneElement):
    """
    Information on the possible cause of the event.
    """

    assessment: Optional[CodeableConcept] = Field(
        description="Assessment of if the entity caused the event",
        default=None,
    )
    productRelatedness: Optional[fhir.string] = Field(
        description="AdverseEvent.suspectEntity.causalityProductRelatedness",
        default=None,
    )
    author: Optional[Reference] = Field(
        description="AdverseEvent.suspectEntity.causalityAuthor",
        default=None,
    )
    method: Optional[CodeableConcept] = Field(
        description="ProbabilityScale | Bayesian | Checklist",
        default=None,
    )

class AdverseEventSuspectEntity(BackboneElement):
    """
    Describes the entity that is suspected to have caused the adverse event.
    """

    instance: Optional[Reference] = Field(
        description="Refers to the specific entity that caused the adverse event",
        default=None,
    )
    causality: Optional[ListType[AdverseEventSuspectEntityCausality]] = Field(
        description="Information on the possible cause of the event",
        default=None,
    )

class AdverseEvent(DomainResource):
    """
    Actual or  potential/avoided event causing unintended physical injury resulting from or contributed to by medical care, a research study or other healthcare setting factors that requires additional monitoring, treatment, or hospitalization, or that results in death.
    """

    _abstract = False
    _type = "AdverseEvent"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/AdverseEvent"

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
    identifier: Optional[Identifier] = Field(
        description="Business identifier for the event",
        default=None,
    )
    actuality: Optional[fhir.code] = Field(
        description="actual | potential",
        default=None,
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description="product-problem | product-quality | product-use-error | wrong-dose | incorrect-prescribing-information | wrong-technique | wrong-route-of-administration | wrong-rate | wrong-duration | wrong-time | expired-drug | medical-device-use-error | problem-different-manufacturer | unsafe-physical-environment",
        default=None,
    )
    event: Optional[CodeableConcept] = Field(
        description="Type of the event itself in relation to the subject",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="Subject impacted by event",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="Encounter created as part of",
        default=None,
    )
    date: Optional[fhir.dateTime] = Field(
        description="When the event occurred",
        default=None,
    )
    detected: Optional[fhir.dateTime] = Field(
        description="When the event was detected",
        default=None,
    )
    recordedDate: Optional[fhir.dateTime] = Field(
        description="When the event was recorded",
        default=None,
    )
    resultingCondition: Optional[ListType[Reference]] = Field(
        description="Effect on the subject due to this event",
        default=None,
    )
    location: Optional[Reference] = Field(
        description="Location where adverse event occurred",
        default=None,
    )
    seriousness: Optional[CodeableConcept] = Field(
        description="Seriousness of the event",
        default=None,
    )
    severity: Optional[CodeableConcept] = Field(
        description="mild | moderate | severe",
        default=None,
    )
    outcome: Optional[CodeableConcept] = Field(
        description="resolved | recovering | ongoing | resolvedWithSequelae | fatal | unknown",
        default=None,
    )
    recorder: Optional[Reference] = Field(
        description="Who recorded the adverse event",
        default=None,
    )
    contributor: Optional[ListType[Reference]] = Field(
        description="Who  was involved in the adverse event or the potential adverse event",
        default=None,
    )
    suspectEntity: Optional[ListType[AdverseEventSuspectEntity]] = Field(
        description="The suspected agent causing the adverse event",
        default=None,
    )
    subjectMedicalHistory: Optional[ListType[Reference]] = Field(
        description="AdverseEvent.subjectMedicalHistory",
        default=None,
    )
    referenceDocument: Optional[ListType[Reference]] = Field(
        description="AdverseEvent.referenceDocument",
        default=None,
    )
    study: Optional[ListType[Reference]] = Field(
        description="AdverseEvent.study",
        default=None,
    )
