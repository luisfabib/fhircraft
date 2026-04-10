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

    informationType: Optional[fhir.code] = Field(
        description="comment | classifier | rating | container | response | change-request",
        default=None,
    )
    summary: Optional[fhir.markdown] = Field(
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
    path: Optional[ListType[fhir.uri]] = Field(
        description="What the comment is directed to",
        default=None,
    )
    relatedArtifact: Optional[ListType[RelatedArtifact]] = Field(
        description="Additional information",
        default=None,
    )
    freeToShare: Optional[fhir.boolean] = Field(
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
    title: Optional[fhir.string] = Field(
        description="A short title for the assessment for use in displaying and selecting",
        default=None,
    )
    citeAsReference: Optional[Reference] = Field(
        description="How to cite the comment or rating",
        default=None,
    )
    citeAsMarkdown: Optional[fhir.markdown] = Field(
        description="How to cite the comment or rating",
        default=None,
    )
    date: Optional[fhir.dateTime] = Field(
        description="Date last changed",
        default=None,
    )
    copyright: Optional[fhir.markdown] = Field(
        description="Use and/or publishing restrictions",
        default=None,
    )
    approvalDate: Optional[fhir.date_] = Field(
        description="When the artifact assessment was approved by publisher",
        default=None,
    )
    lastReviewDate: Optional[fhir.date_] = Field(
        description="When the artifact assessment was last reviewed by the publisher",
        default=None,
    )
    artifactReference: Optional[Reference] = Field(
        description="The artifact assessed, commented upon or rated",
        default=None,
    )
    artifactCanonical: Optional[fhir.canonical] = Field(
        description="The artifact assessed, commented upon or rated",
        default=None,
    )
    artifactUri: Optional[fhir.uri] = Field(
        description="The artifact assessed, commented upon or rated",
        default=None,
    )
    content: Optional[ListType[ArtifactAssessmentContent]] = Field(
        description="Comment, classifier, or rating content",
        default=None,
    )
    workflowStatus: Optional[fhir.code] = Field(
        description="submitted | triaged | waiting-for-input | resolved-no-change | resolved-change-required | deferred | duplicate | applied | published | entered-in-error",
        default=None,
    )
    disposition: Optional[fhir.code] = Field(
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
            field_types=[Reference, fhir.markdown],
            field_name_base="citeAs",
            required=False,
        )

    @model_validator(mode="after")
    def artifact_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Reference, fhir.canonical, fhir.uri],
            field_name_base="artifact",
            required=True,
        )
