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
    BackboneElement,
    CodeableConcept,
    Reference,
    RelatedArtifact,
    CodeableReference,
    Period,
    Annotation,
)
from .resource import Resource
from .domain_resource import DomainResource


class ResearchStudyLabel(BackboneElement):
    """
    Additional names for the study.
    """

    type: Optional[CodeableConcept] = Field(
        description="primary | official | scientific | plain-language | subtitle | short-title | acronym | earlier-title | language | auto-translated | human-use | machine-use | duplicate-uid",
        default=None,
    )
    value: Optional[fhir.string] = Field(
        description="The name",
        default=None,
    )


class ResearchStudyAssociatedParty(BackboneElement):
    """
    Sponsors, collaborators, and other parties.
    """

    name: Optional[fhir.string] = Field(
        description="Name of associated party",
        default=None,
    )
    role: Optional[CodeableConcept] = Field(
        description="sponsor | lead-sponsor | sponsor-investigator | primary-investigator | collaborator | funding-source | general-contact | recruitment-contact | sub-investigator | study-director | study-chair",
        default=None,
    )
    period: Optional[ListType[Period]] = Field(
        description="When active in the role",
        default=None,
    )
    classifier: Optional[ListType[CodeableConcept]] = Field(
        description="nih | fda | government | nonprofit | academic | industry",
        default=None,
    )
    party: Optional[Reference] = Field(
        description="Individual or organization associated with study (use practitionerRole to specify their organisation)",
        default=None,
    )


class ResearchStudyProgressStatus(BackboneElement):
    """
    Status of study with time for that status.
    """

    state: Optional[CodeableConcept] = Field(
        description="Label for status or state (e.g. recruitment status)",
        default=None,
    )
    actual: Optional[fhir.boolean] = Field(
        description="Actual if true else anticipated",
        default=None,
    )
    period: Optional[Period] = Field(
        description="Date range",
        default=None,
    )


class ResearchStudyRecruitment(BackboneElement):
    """
    Target or actual group of participants enrolled in study.
    """

    targetNumber: Optional[fhir.unsignedInt] = Field(
        description="Estimated total number of participants to be enrolled",
        default=None,
    )
    actualNumber: Optional[fhir.unsignedInt] = Field(
        description="Actual total number of participants enrolled in study",
        default=None,
    )
    eligibility: Optional[Reference] = Field(
        description="Inclusion and exclusion criteria",
        default=None,
    )
    actualGroup: Optional[Reference] = Field(
        description="Group of participants who were enrolled in study",
        default=None,
    )


class ResearchStudyComparisonGroup(BackboneElement):
    """
    Describes an expected event or sequence of events for one of the subjects of a study. E.g. for a living subject: exposure to drug A, wash-out, exposure to drug B, wash-out, follow-up. E.g. for a stability study: {store sample from lot A at 25 degrees for 1 month}, {store sample from lot A at 40 degrees for 1 month}.
    """

    linkId: Optional[fhir.id_] = Field(
        description="Allows the comparisonGroup for the study and the comparisonGroup for the subject to be linked easily",
        default=None,
    )
    name: Optional[fhir.string] = Field(
        description="Label for study comparisonGroup",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Categorization of study comparisonGroup",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
        description="Short explanation of study path",
        default=None,
    )
    intendedExposure: Optional[ListType[Reference]] = Field(
        description="Interventions or exposures in this comparisonGroup or cohort",
        default=None,
    )
    observedGroup: Optional[Reference] = Field(
        description="Group of participants who were enrolled in study comparisonGroup",
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
    description: Optional[fhir.markdown] = Field(
        description="Description of the objective",
        default=None,
    )


class ResearchStudyOutcomeMeasure(BackboneElement):
    """
    An "outcome measure", "endpoint", "effect measure" or "measure of effect" is a specific measurement or observation used to quantify the effect of experimental variables on the participants in a study, or for observational studies, to describe patterns of diseases or traits or associations with exposures, risk factors or treatment.
    """

    name: Optional[fhir.string] = Field(
        description="Label for the outcome",
        default=None,
    )
    type: Optional[ListType[CodeableConcept]] = Field(
        description="primary | secondary | exploratory",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
        description="Description of the outcome",
        default=None,
    )
    reference: Optional[Reference] = Field(
        description="Structured outcome definition",
        default=None,
    )


class ResearchStudy(DomainResource):
    """
    A scientific study of nature that sometimes includes processes involved in health and disease. For example, clinical trials are research studies that involve people. These studies may be related to new ways to screen, prevent, diagnose, and treat disease. They may also study certain outcomes and certain groups of people by looking at data collected in the past or future.
    """

    _abstract = False
    _type = "ResearchStudy"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/ResearchStudy"

    url: Optional[fhir.uri] = Field(
        description="canonical identifier for this study resource",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Business Identifier for study",
        default=None,
    )
    version: Optional[fhir.string] = Field(
        description="The business version for the study record",
        default=None,
    )
    name: Optional[fhir.string] = Field(
        description="Name for this study (computer friendly)",
        default=None,
    )
    title: Optional[fhir.string] = Field(
        description="Human readable name of the study",
        default=None,
    )
    label: Optional[ListType[ResearchStudyLabel]] = Field(
        description="Additional names for the study",
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
    relatedArtifact: Optional[ListType[RelatedArtifact]] = Field(
        description="References, URLs, and attachments",
        default=None,
    )
    date: Optional[fhir.dateTime] = Field(
        description="Date the resource last changed",
        default=None,
    )
    status: Optional[fhir.code] = Field(
        description="draft | active | retired | unknown",
        default=None,
    )
    primaryPurposeType: Optional[CodeableConcept] = Field(
        description="treatment | prevention | diagnostic | supportive-care | screening | health-services-research | basic-science | device-feasibility",
        default=None,
    )
    phase: Optional[CodeableConcept] = Field(
        description="n-a | early-phase-1 | phase-1 | phase-1-phase-2 | phase-2 | phase-2-phase-3 | phase-3 | phase-4",
        default=None,
    )
    studyDesign: Optional[ListType[CodeableConcept]] = Field(
        description="Classifications of the study design characteristics",
        default=None,
    )
    focus: Optional[ListType[CodeableReference]] = Field(
        description="Drugs, devices, etc. under study",
        default=None,
    )
    condition: Optional[ListType[CodeableConcept]] = Field(
        description="Condition being studied",
        default=None,
    )
    keyword: Optional[ListType[CodeableConcept]] = Field(
        description="Used to search for the study",
        default=None,
    )
    region: Optional[ListType[CodeableConcept]] = Field(
        description="Geographic area for the study",
        default=None,
    )
    descriptionSummary: Optional[fhir.markdown] = Field(
        description="Brief text explaining the study",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
        description="Detailed narrative of the study",
        default=None,
    )
    period: Optional[Period] = Field(
        description="When the study began and ended",
        default=None,
    )
    site: Optional[ListType[Reference]] = Field(
        description="Facility where study activities are conducted",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Comments made about the study",
        default=None,
    )
    classifier: Optional[ListType[CodeableConcept]] = Field(
        description="Classification for the study",
        default=None,
    )
    associatedParty: Optional[ListType[ResearchStudyAssociatedParty]] = Field(
        description="Sponsors, collaborators, and other parties",
        default=None,
    )
    progressStatus: Optional[ListType[ResearchStudyProgressStatus]] = Field(
        description="Status of study with time for that status",
        default=None,
    )
    whyStopped: Optional[CodeableConcept] = Field(
        description="accrual-goal-met | closed-due-to-toxicity | closed-due-to-lack-of-study-progress | temporarily-closed-per-study-design",
        default=None,
    )
    recruitment: Optional[ResearchStudyRecruitment] = Field(
        description="Target or actual group of participants enrolled in study",
        default=None,
    )
    comparisonGroup: Optional[ListType[ResearchStudyComparisonGroup]] = Field(
        description="Defined path through the study for a subject",
        default=None,
    )
    objective: Optional[ListType[ResearchStudyObjective]] = Field(
        description="A goal for the study",
        default=None,
    )
    outcomeMeasure: Optional[ListType[ResearchStudyOutcomeMeasure]] = Field(
        description="A variable measured during the study",
        default=None,
    )
    result: Optional[ListType[Reference]] = Field(
        description="Link to results generated during the study",
        default=None,
    )
