from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from ..primitive import *

from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Reference,
    BackboneElement,
    CodeableConcept,
    Quantity,
    RelatedArtifact,
)
from .resource import Resource
from .domain_resource import DomainResource

class ArtifactAssessmentContent(BackboneElement):
    """
    A component comment, classifier, or rating of the artifact.
    """

    informationType: Optional[Code] = Field(
        description="comment | classifier | rating | container | response | change-request",
        default=None,
    )
    summary: Optional[Markdown] = Field(
        description="Brief summary of the content",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="What type of content",
        default=None,
    )
    classifier: Optional[ListType[CodeableConcept]] = Field(
        description="Rating, classifier, or assessment",
        default=None,
    )
    quantity: Optional[Quantity] = Field(
        description="Quantitative rating",
        default=None,
    )
    author: Optional[Reference] = Field(
        description="Who authored the content",
        default=None,
    )
    path: Optional[ListType[Uri]] = Field(
        description="What the comment is directed to",
        default=None,
    )
    relatedArtifact: Optional[ListType[RelatedArtifact]] = Field(
        description="Additional information",
        default=None,
    )
    freeToShare: Optional[Boolean] = Field(
        description="Acceptable to publicly share the resource content",
        default=None,
    )
    component: Optional[ListType["ArtifactAssessmentContent"]] = Field(
        description="Contained content",
        default=None,
    )

class ArtifactAssessment(DomainResource):
    """
    This Resource provides one or more comments, classifiers or ratings about a Resource and supports attribution and rights management metadata for the added content.
    """

    _abstract = False
    _type = "ArtifactAssessment"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/ArtifactAssessment"

    identifier: Optional[ListType[Identifier]] = Field(
        description="Additional identifier for the artifact assessment",
        default=None,
    )
    title: Optional[String] = Field(
        description="A short title for the assessment for use in displaying and selecting",
        default=None,
    )
    citeAsReference: Optional[Reference] = Field(
        description="How to cite the comment or rating",
        default=None,
    )
    citeAsMarkdown: Optional[Markdown] = Field(
        description="How to cite the comment or rating",
        default=None,
    )
    date: Optional[DateTime] = Field(
        description="Date last changed",
        default=None,
    )
    copyright: Optional[Markdown] = Field(
        description="Use and/or publishing restrictions",
        default=None,
    )
    approvalDate: Optional[Date] = Field(
        description="When the artifact assessment was approved by publisher",
        default=None,
    )
    lastReviewDate: Optional[Date] = Field(
        description="When the artifact assessment was last reviewed by the publisher",
        default=None,
    )
    artifactReference: Optional[Reference] = Field(
        description="The artifact assessed, commented upon or rated",
        default=None,
    )
    artifactCanonical: Optional[Canonical] = Field(
        description="The artifact assessed, commented upon or rated",
        default=None,
    )
    artifactUri: Optional[Uri] = Field(
        description="The artifact assessed, commented upon or rated",
        default=None,
    )
    content: Optional[ListType[ArtifactAssessmentContent]] = Field(
        description="Comment, classifier, or rating content",
        default=None,
    )
    workflowStatus: Optional[Code] = Field(
        description="submitted | triaged | waiting-for-input | resolved-no-change | resolved-change-required | deferred | duplicate | applied | published | entered-in-error",
        default=None,
    )
    disposition: Optional[Code] = Field(
        description="unresolved | not-persuasive | persuasive | persuasive-with-modification | not-persuasive-with-modification",
        default=None,
    )

    @property
    def citeAs(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="citeAs",
        )

    @property
    def artifact(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="artifact",
        )

    @model_validator(mode="after")
    def citeAs_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Reference, Markdown],
            field_name_base="citeAs",
            required=False,
        )

    @model_validator(mode="after")
    def artifact_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Reference, Canonical, Uri],
            field_name_base="artifact",
            required=True,
        )
