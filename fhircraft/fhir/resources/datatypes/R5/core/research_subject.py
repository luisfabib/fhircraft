from pydantic import Field, model_validator
from typing import Optional, List

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    DateTime,
    Id,
)

from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    BackboneElement,
    CodeableConcept,
    Period,
    Reference,
)
from .resource import Resource
from .domain_resource import DomainResource


class ResearchSubjectProgress(BackboneElement):
    """
    The current state (status) of the subject and resons for status change where appropriate.
    """

    type: Optional[CodeableConcept] = Field(
        description="state | milestone",
        default=None,
    )
    subjectState: Optional[CodeableConcept] = Field(
        description="candidate | eligible | follow-up | ineligible | not-registered | off-study | on-study | on-study-intervention | on-study-observation | pending-on-study | potential-candidate | screening | withdrawn",
        default=None,
    )
    milestone: Optional[CodeableConcept] = Field(
        description="SignedUp | Screened | Randomized",
        default=None,
    )
    reason: Optional[CodeableConcept] = Field(
        description="State change reason",
        default=None,
    )
    startDate: Optional[DateTime] = Field(
        description="State change date",
        default=None,
    )
    startDate_ext: Optional[Element] = Field(
        description="Placeholder element for startDate extensions",
        default=None,
        alias="_startDate",
    )
    endDate: Optional[DateTime] = Field(
        description="State change date",
        default=None,
    )
    endDate_ext: Optional[Element] = Field(
        description="Placeholder element for endDate extensions",
        default=None,
        alias="_endDate",
    )


class ResearchSubject(DomainResource):
    """
    A ResearchSubject is a participant or object which is the recipient of investigative activities in a research study.
    """

    _abstract = False
    _type = "ResearchSubject"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/ResearchSubject"

    identifier: Optional[List[Identifier]] = Field(
        description="Business Identifier for research subject in a study",
        default=None,
    )
    status: Optional[Code] = Field(
        description="draft | active | retired | unknown",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    progress: Optional[List[ResearchSubjectProgress]] = Field(
        description="Subject status",
        default=None,
    )
    period: Optional[Period] = Field(
        description="Start and end of participation",
        default=None,
    )
    study: Optional[Reference] = Field(
        description="Study subject is part of",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="Who or what is part of study",
        default=None,
    )
    assignedComparisonGroup: Optional[Id] = Field(
        description="What path should be followed",
        default=None,
    )
    assignedComparisonGroup_ext: Optional[Element] = Field(
        description="Placeholder element for assignedComparisonGroup extensions",
        default=None,
        alias="_assignedComparisonGroup",
    )
    actualComparisonGroup: Optional[Id] = Field(
        description="What path was followed",
        default=None,
    )
    actualComparisonGroup_ext: Optional[Element] = Field(
        description="Placeholder element for actualComparisonGroup extensions",
        default=None,
        alias="_actualComparisonGroup",
    )
    consent: Optional[List[Reference]] = Field(
        description="Agreement to participate in study",
        default=None,
    )
