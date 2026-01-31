from typing import Optional, List as ListType

NoneType = type(None)

from pydantic import Field
from fhircraft.fhir.resources.datatypes.primitives import Date

from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    ContactDetail,
    CodeableConcept,
    Period,
    RelatedArtifact,
)
from .canonical_resource import CanonicalResource


class MetadataResource(CanonicalResource):
    """
    Common Interface declaration for conformance and knowledge artifact resources.
    """

    _abstract = True
    _type = "MetadataResource"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/MetadataResource"

    approvalDate: Optional[Date] = Field(
        description="When the {{title}} was approved by publisher",
        default=None,
    )
    approvalDate_ext: Optional[Element] = Field(
        description="Placeholder element for approvalDate extensions",
        default=None,
        alias="_approvalDate",
    )
    lastReviewDate: Optional[Date] = Field(
        description="When the {{title}} was last reviewed by the publisher",
        default=None,
    )
    lastReviewDate_ext: Optional[Element] = Field(
        description="Placeholder element for lastReviewDate extensions",
        default=None,
        alias="_lastReviewDate",
    )
    effectivePeriod: Optional[Period] = Field(
        description="When the {{title}} is expected to be used",
        default=None,
    )
    topic: Optional[ListType[CodeableConcept]] = Field(
        description="E.g. Education, Treatment, Assessment, etc",
        default=None,
    )
    author: Optional[ListType[ContactDetail]] = Field(
        description="Who authored the {{title}}",
        default=None,
    )
    editor: Optional[ListType[ContactDetail]] = Field(
        description="Who edited the {{title}}",
        default=None,
    )
    reviewer: Optional[ListType[ContactDetail]] = Field(
        description="Who reviewed the {{title}}",
        default=None,
    )
    endorser: Optional[ListType[ContactDetail]] = Field(
        description="Who endorsed the {{title}}",
        default=None,
    )
    relatedArtifact: Optional[ListType[RelatedArtifact]] = Field(
        description="Additional documentation, citations, etc",
        default=None,
    )
