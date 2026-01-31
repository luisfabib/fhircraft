import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import String, Uri, Code

from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Reference,
    Extension,
    Identifier,
    Period,
)
from .resource import Resource
from .domain_resource import DomainResource


class ResearchSubject(DomainResource):
    """
    A physical entity which is the primary unit of operational and/or administrative interest in a study.
    """

    _abstract = False
    _type = "ResearchSubject"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/ResearchSubject"

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
        description="Business Identifier for research subject in a study",
        default=None,
    )
    status: Optional[Code] = Field(
        description="candidate | eligible | follow-up | ineligible | not-registered | off-study | on-study | on-study-intervention | on-study-observation | pending-on-study | potential-candidate | screening | withdrawn",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    period: Optional[Period] = Field(
        description="Start and end of participation",
        default=None,
    )
    study: Optional[Reference] = Field(
        description="Study subject is part of",
        default=None,
    )
    individual: Optional[Reference] = Field(
        description="Who is part of study",
        default=None,
    )
    assignedArm: Optional[String] = Field(
        description="What path should be followed",
        default=None,
    )
    assignedArm_ext: Optional[Element] = Field(
        description="Placeholder element for assignedArm extensions",
        default=None,
        alias="_assignedArm",
    )
    actualArm: Optional[String] = Field(
        description="What path was followed",
        default=None,
    )
    actualArm_ext: Optional[Element] = Field(
        description="Placeholder element for actualArm extensions",
        default=None,
        alias="_actualArm",
    )
    consent: Optional[Reference] = Field(
        description="Agreement to participate in study",
        default=None,
    )
