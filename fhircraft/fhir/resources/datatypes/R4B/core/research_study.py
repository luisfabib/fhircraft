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
    Reference,
    CodeableConcept,
    ContactDetail,
    RelatedArtifact,
    Period,
    Annotation,
    BackboneElement,
)
from .resource import Resource
from .domain_resource import DomainResource

class ResearchStudyArm(BackboneElement):
    """
    Describes an expected sequence of events for one of the participants of a study.  E.g. Exposure to drug A, wash-out, exposure to drug B, wash-out, follow-up.
    """

    name: fhir.string = Field(
        description="Label for study arm",
    )
    type: Optional[CodeableConcept] = Field(
        description="Categorization of study arm",
        default=None,
    )
    description: Optional[fhir.string] = Field(
        description="Short explanation of study path",
        default=None,
    )

class ResearchStudyObjective(BackboneElement):
    """
    A goal that the study is aiming to achieve in terms of a scientific question to be answered by the analysis of data collected during the study.
    """

    name: Optional[fhir.string] = Field(
        description="Label for the objective",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="primary | secondary | exploratory",
        default=None,
    )

class ResearchStudy(DomainResource):
    """
    A process where a researcher or organization plans and then executes a series of steps intended to increase the field of healthcare-related knowledge.  This includes studies of safety, efficacy, comparative effectiveness and other information about medications, devices, therapies and other interventional and investigative techniques.  A ResearchStudy involves the gathering of information about human or animal subjects.
    """

    _abstract = False
    _type = "ResearchStudy"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/ResearchStudy"

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
        description="Business Identifier for study",
        default=None,
    )
    title: Optional[fhir.string] = Field(
        description="Name for this study",
        default=None,
    )
    protocol: Optional[ListType[Reference]] = Field(
        description="Steps followed in executing study",
        default=None,
    )
    partOf: Optional[ListType[Reference]] = Field(
        description="Part of larger study",
        default=None,
    )
    status: fhir.code = Field(
        description="active | administratively-completed | approved | closed-to-accrual | closed-to-accrual-and-intervention | completed | disapproved | in-review | temporarily-closed-to-accrual | temporarily-closed-to-accrual-and-intervention | withdrawn",
    )
    primaryPurposeType: Optional[CodeableConcept] = Field(
        description="treatment | prevention | diagnostic | supportive-care | screening | health-services-research | basic-science | device-feasibility",
        default=None,
    )
    phase: Optional[CodeableConcept] = Field(
        description="n-a | early-phase-1 | phase-1 | phase-1-phase-2 | phase-2 | phase-2-phase-3 | phase-3 | phase-4",
        default=None,
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description="Classifications for the study",
        default=None,
    )
    focus: Optional[ListType[CodeableConcept]] = Field(
        description="Drugs, devices, etc. under study",
        default=None,
    )
    condition: Optional[ListType[CodeableConcept]] = Field(
        description="Condition being studied",
        default=None,
    )
    contact: Optional[ListType[ContactDetail]] = Field(
        description="Contact details for the study",
        default=None,
    )
    relatedArtifact: Optional[ListType[RelatedArtifact]] = Field(
        description="References and dependencies",
        default=None,
    )
    keyword: Optional[ListType[CodeableConcept]] = Field(
        description="Used to search for the study",
        default=None,
    )
    location: Optional[ListType[CodeableConcept]] = Field(
        description="Geographic region(s) for study",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
        description="What this is study doing",
        default=None,
    )
    enrollment: Optional[ListType[Reference]] = Field(
        description="Inclusion \u0026 exclusion criteria",
        default=None,
    )
    period: Optional[Period] = Field(
        description="When the study began and ended",
        default=None,
    )
    sponsor: Optional[Reference] = Field(
        description="Organization that initiates and is legally responsible for the study",
        default=None,
    )
    principalInvestigator: Optional[Reference] = Field(
        description="Researcher who oversees multiple aspects of the study",
        default=None,
    )
    site: Optional[ListType[Reference]] = Field(
        description="Facility where study activities are conducted",
        default=None,
    )
    reasonStopped: Optional[CodeableConcept] = Field(
        description="accrual-goal-met | closed-due-to-toxicity | closed-due-to-lack-of-study-progress | temporarily-closed-per-study-design",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Comments made about the study",
        default=None,
    )
    arm: Optional[ListType[ResearchStudyArm]] = Field(
        description="Defined path through the study for a subject",
        default=None,
    )
    objective: Optional[ListType[ResearchStudyObjective]] = Field(
        description="A goal for the study",
        default=None,
    )
