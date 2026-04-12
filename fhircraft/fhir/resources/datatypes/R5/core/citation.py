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
    Coding,
    ContactDetail,
    UsageContext,
    CodeableConcept,
    Period,
    BackboneElement,
    Annotation,
    RelatedArtifact,
    Reference,
    Attachment,
)
from .resource import Resource
from .domain_resource import DomainResource


class CitationSummary(BackboneElement):
    """
    A human-readable display of key concepts to represent the citation.
    """

    style: Optional[CodeableConcept] = Field(
        description="Format for display of the citation summary",
        default=None,
    )
    text: Optional[fhir.markdown] = Field(
        description="The human-readable display of the citation summary",
        default=None,
    )


class CitationClassification(BackboneElement):
    """
    The assignment to an organizing scheme.
    """

    type: Optional[CodeableConcept] = Field(
        description="The kind of classifier (e.g. publication type, keyword)",
        default=None,
    )
    classifier: Optional[ListType[CodeableConcept]] = Field(
        description="The specific classification value",
        default=None,
    )


class CitationStatusDate(BackboneElement):
    """
    The state or status of the citation record paired with an effective date or period for that state.
    """

    activity: Optional[CodeableConcept] = Field(
        description="Classification of the status",
        default=None,
    )
    actual: Optional[fhir.boolean] = Field(
        description="Either occurred or expected",
        default=None,
    )
    period: Optional[Period] = Field(
        description="When the status started and/or ended",
        default=None,
    )


class CitationCitedArtifactVersion(BackboneElement):
    """
    The defined version of the cited artifact.
    """

    value: Optional[fhir.string] = Field(
        description="The version number or other version identifier",
        default=None,
    )
    baseCitation: Optional[Reference] = Field(
        description="Citation for the main version of the cited artifact",
        default=None,
    )


class CitationCitedArtifactStatusDate(BackboneElement):
    """
    An effective date or period, historical or future, actual or expected, for a status of the cited artifact.
    """

    activity: Optional[CodeableConcept] = Field(
        description="Classification of the status",
        default=None,
    )
    actual: Optional[fhir.boolean] = Field(
        description="Either occurred or expected",
        default=None,
    )
    period: Optional[Period] = Field(
        description="When the status started and/or ended",
        default=None,
    )


class CitationCitedArtifactTitle(BackboneElement):
    """
    The title details of the article or artifact.
    """

    type: Optional[ListType[CodeableConcept]] = Field(
        description="The kind of title",
        default=None,
    )
    language: Optional[CodeableConcept] = Field(
        description="Used to express the specific language",
        default=None,
    )
    text: Optional[fhir.markdown] = Field(
        description="The title of the article or artifact",
        default=None,
    )


class CitationCitedArtifactAbstract(BackboneElement):
    """
    The abstract may be used to convey article-contained abstracts, externally-created abstracts, or other descriptive summaries.
    """

    type: Optional[CodeableConcept] = Field(
        description="The kind of abstract",
        default=None,
    )
    language: Optional[CodeableConcept] = Field(
        description="Used to express the specific language",
        default=None,
    )
    text: Optional[fhir.markdown] = Field(
        description="Abstract content",
        default=None,
    )
    copyright: Optional[fhir.markdown] = Field(
        description="Copyright notice for the abstract",
        default=None,
    )


class CitationCitedArtifactPart(BackboneElement):
    """
    The component of the article or artifact.
    """

    type: Optional[CodeableConcept] = Field(
        description="The kind of component",
        default=None,
    )
    value: Optional[fhir.string] = Field(
        description="The specification of the component",
        default=None,
    )
    baseCitation: Optional[Reference] = Field(
        description="The citation for the full article or artifact",
        default=None,
    )


class CitationCitedArtifactRelatesTo(BackboneElement):
    """
    The artifact related to the cited artifact.
    """

    type: Optional[fhir.code] = Field(
        description="documentation | justification | citation | predecessor | successor | derived-from | depends-on | composed-of | part-of | amends | amended-with | appends | appended-with | cites | cited-by | comments-on | comment-in | contains | contained-in | corrects | correction-in | replaces | replaced-with | retracts | retracted-by | signs | similar-to | supports | supported-with | transforms | transformed-into | transformed-with | documents | specification-of | created-with | cite-as | reprint | reprint-of",
        default=None,
    )
    classifier: Optional[ListType[CodeableConcept]] = Field(
        description="Additional classifiers",
        default=None,
    )
    label: Optional[fhir.string] = Field(
        description="Short label",
        default=None,
    )
    display: Optional[fhir.string] = Field(
        description="Brief description of the related artifact",
        default=None,
    )
    citation: Optional[fhir.markdown] = Field(
        description="Bibliographic citation for the artifact",
        default=None,
    )
    document: Optional[Attachment] = Field(
        description="What document is being referenced",
        default=None,
    )
    resource: Optional[fhir.canonical] = Field(
        description="What artifact is being referenced",
        default=None,
    )
    resourceReference: Optional[Reference] = Field(
        description="What artifact, if not a conformance resource",
        default=None,
    )


class CitationCitedArtifactPublicationFormPublishedIn(BackboneElement):
    """
    The collection the cited article or artifact is published in.
    """

    type: Optional[CodeableConcept] = Field(
        description="Kind of container (e.g. Periodical, database, or book)",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Journal identifiers include ISSN, ISO Abbreviation and NLMuniqueID; Book identifiers include ISBN",
        default=None,
    )
    title: Optional[fhir.string] = Field(
        description="Name of the database or title of the book or journal",
        default=None,
    )
    publisher: Optional[Reference] = Field(
        description="Name of or resource describing the publisher",
        default=None,
    )
    publisherLocation: Optional[fhir.string] = Field(
        description="Geographic location of the publisher",
        default=None,
    )


class CitationCitedArtifactPublicationForm(BackboneElement):
    """
    If multiple, used to represent alternative forms of the article that are not separate citations.
    """

    publishedIn: Optional[CitationCitedArtifactPublicationFormPublishedIn] = Field(
        description="The collection the cited article or artifact is published in",
        default=None,
    )
    citedMedium: Optional[CodeableConcept] = Field(
        description="Internet or Print",
        default=None,
    )
    volume: Optional[fhir.string] = Field(
        description="Volume number of journal or other collection in which the article is published",
        default=None,
    )
    issue: Optional[fhir.string] = Field(
        description="Issue, part or supplement of journal or other collection in which the article is published",
        default=None,
    )
    articleDate: Optional[fhir.dateTime] = Field(
        description="The date the article was added to the database, or the date the article was released",
        default=None,
    )
    publicationDateText: Optional[fhir.string] = Field(
        description="Text representation of the date on which the issue of the cited artifact was published",
        default=None,
    )
    publicationDateSeason: Optional[fhir.string] = Field(
        description="Season in which the cited artifact was published",
        default=None,
    )
    lastRevisionDate: Optional[fhir.dateTime] = Field(
        description="The date the article was last revised or updated in the database",
        default=None,
    )
    language: Optional[ListType[CodeableConcept]] = Field(
        description="Language(s) in which this form of the article is published",
        default=None,
    )
    accessionNumber: Optional[fhir.string] = Field(
        description="Entry number or identifier for inclusion in a database",
        default=None,
    )
    pageString: Optional[fhir.string] = Field(
        description="Used for full display of pagination",
        default=None,
    )
    firstPage: Optional[fhir.string] = Field(
        description="Used for isolated representation of first page",
        default=None,
    )
    lastPage: Optional[fhir.string] = Field(
        description="Used for isolated representation of last page",
        default=None,
    )
    pageCount: Optional[fhir.string] = Field(
        description="Number of pages or screens",
        default=None,
    )
    copyright: Optional[fhir.markdown] = Field(
        description="Copyright notice for the full article or artifact",
        default=None,
    )


class CitationCitedArtifactWebLocation(BackboneElement):
    """
    Used for any URL for the article or artifact cited.
    """

    classifier: Optional[ListType[CodeableConcept]] = Field(
        description="code the reason for different URLs, e.g. abstract and full-text",
        default=None,
    )
    url: Optional[fhir.uri] = Field(
        description="The specific URL",
        default=None,
    )


class CitationCitedArtifactClassification(BackboneElement):
    """
    The assignment to an organizing scheme.
    """

    type: Optional[CodeableConcept] = Field(
        description="The kind of classifier (e.g. publication type, keyword)",
        default=None,
    )
    classifier: Optional[ListType[CodeableConcept]] = Field(
        description="The specific classification value",
        default=None,
    )
    artifactAssessment: Optional[ListType[Reference]] = Field(
        description="Complex or externally created classification",
        default=None,
    )


class CitationCitedArtifactContributorshipEntryContributionInstance(BackboneElement):
    """
    Contributions with accounting for time or number.
    """

    type: Optional[CodeableConcept] = Field(
        description="The specific contribution",
        default=None,
    )
    time: Optional[fhir.dateTime] = Field(
        description="The time that the contribution was made",
        default=None,
    )


class CitationCitedArtifactContributorshipEntry(BackboneElement):
    """
    An individual entity named as a contributor, for example in the author list or contributor list.
    """

    contributor: Optional[Reference] = Field(
        description="The identity of the individual contributor",
        default=None,
    )
    forenameInitials: Optional[fhir.string] = Field(
        description="For citation styles that use initials",
        default=None,
    )
    affiliation: Optional[ListType[Reference]] = Field(
        description="Organizational affiliation",
        default=None,
    )
    contributionType: Optional[ListType[CodeableConcept]] = Field(
        description="The specific contribution",
        default=None,
    )
    role: Optional[CodeableConcept] = Field(
        description="The role of the contributor (e.g. author, editor, reviewer, funder)",
        default=None,
    )
    contributionInstance: Optional[
        ListType[CitationCitedArtifactContributorshipEntryContributionInstance]
    ] = Field(
        description="Contributions with accounting for time or number",
        default=None,
    )
    correspondingContact: Optional[fhir.boolean] = Field(
        description="Whether the contributor is the corresponding contributor for the role",
        default=None,
    )
    rankingOrder: Optional[fhir.positiveInt] = Field(
        description="Ranked order of contribution",
        default=None,
    )


class CitationCitedArtifactContributorshipSummary(BackboneElement):
    """
    Used to record a display of the author/contributor list without separate data element for each list member.
    """

    type: Optional[CodeableConcept] = Field(
        description="Such as author list, contributorship statement, funding statement, acknowledgements statement, or conflicts of interest statement",
        default=None,
    )
    style: Optional[CodeableConcept] = Field(
        description="The format for the display string",
        default=None,
    )
    source: Optional[CodeableConcept] = Field(
        description="Used to code the producer or rule for creating the display string",
        default=None,
    )
    value: Optional[fhir.markdown] = Field(
        description="The display string for the author list, contributor list, or contributorship statement",
        default=None,
    )


class CitationCitedArtifactContributorship(BackboneElement):
    """
    This element is used to list authors and other contributors, their contact information, specific contributions, and summary statements.
    """

    complete: Optional[fhir.boolean] = Field(
        description="Indicates if the list includes all authors and/or contributors",
        default=None,
    )
    entry: Optional[ListType[CitationCitedArtifactContributorshipEntry]] = Field(
        description="An individual entity named as a contributor",
        default=None,
    )
    summary: Optional[ListType[CitationCitedArtifactContributorshipSummary]] = Field(
        description="Used to record a display of the author/contributor list without separate data element for each list member",
        default=None,
    )


class CitationCitedArtifact(BackboneElement):
    """
    The article or artifact being described.
    """

    identifier: Optional[ListType[Identifier]] = Field(
        description="Unique identifier. May include DOI, PMID, PMCID, etc",
        default=None,
    )
    relatedIdentifier: Optional[ListType[Identifier]] = Field(
        description="Identifier not unique to the cited artifact. May include trial registry identifiers",
        default=None,
    )
    dateAccessed: Optional[fhir.dateTime] = Field(
        description="When the cited artifact was accessed",
        default=None,
    )
    version: Optional[CitationCitedArtifactVersion] = Field(
        description="The defined version of the cited artifact",
        default=None,
    )
    currentState: Optional[ListType[CodeableConcept]] = Field(
        description="The status of the cited artifact",
        default=None,
    )
    statusDate: Optional[ListType[CitationCitedArtifactStatusDate]] = Field(
        description="An effective date or period for a status of the cited artifact",
        default=None,
    )
    title: Optional[ListType[CitationCitedArtifactTitle]] = Field(
        description="The title details of the article or artifact",
        default=None,
    )
    abstract: Optional[ListType[CitationCitedArtifactAbstract]] = Field(
        description="Summary of the article or artifact",
        default=None,
    )
    part: Optional[CitationCitedArtifactPart] = Field(
        description="The component of the article or artifact",
        default=None,
    )
    relatesTo: Optional[ListType[CitationCitedArtifactRelatesTo]] = Field(
        description="The artifact related to the cited artifact",
        default=None,
    )
    publicationForm: Optional[ListType[CitationCitedArtifactPublicationForm]] = Field(
        description="If multiple, used to represent alternative forms of the article that are not separate citations",
        default=None,
    )
    webLocation: Optional[ListType[CitationCitedArtifactWebLocation]] = Field(
        description="Used for any URL for the article or artifact cited",
        default=None,
    )
    classification: Optional[ListType[CitationCitedArtifactClassification]] = Field(
        description="The assignment to an organizing scheme",
        default=None,
    )
    contributorship: Optional[CitationCitedArtifactContributorship] = Field(
        description="Attribution of authors and other contributors",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Any additional information or content for the article or artifact",
        default=None,
    )


class Citation(DomainResource):
    """
    The Citation Resource enables reference to any knowledge artifact for purposes of identification and attribution. The Citation Resource supports existing reference structures and developing publication practices such as versioning, expressing complex contributorship roles, and referencing computable resources.
    """

    _abstract = False
    _type = "Citation"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Citation"

    url: Optional[fhir.uri] = Field(
        description="canonical identifier for this citation record, represented as a globally unique URI",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Identifier for the citation record itself",
        default=None,
    )
    version: Optional[fhir.string] = Field(
        description="Business version of the citation record",
        default=None,
    )
    versionAlgorithmString: Optional[fhir.string] = Field(
        description="How to compare versions",
        default=None,
    )
    versionAlgorithmCoding: Optional[Coding] = Field(
        description="How to compare versions",
        default=None,
    )
    name: Optional[fhir.string] = Field(
        description="Name for this citation record (computer friendly)",
        default=None,
    )
    title: Optional[fhir.string] = Field(
        description="Name for this citation record (human friendly)",
        default=None,
    )
    status: Optional[fhir.code] = Field(
        description="draft | active | retired | unknown",
        default=None,
    )
    experimental: Optional[fhir.boolean] = Field(
        description="For testing purposes, not real usage",
        default=None,
    )
    date: Optional[fhir.dateTime] = Field(
        description="Date last changed",
        default=None,
    )
    publisher: Optional[fhir.string] = Field(
        description="The publisher of the citation record, not the publisher of the article or artifact being cited",
        default=None,
    )
    contact: Optional[ListType[ContactDetail]] = Field(
        description="Contact details for the publisher of the citation record",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
        description="Natural language description of the citation",
        default=None,
    )
    useContext: Optional[ListType[UsageContext]] = Field(
        description="The context that the citation record content is intended to support",
        default=None,
    )
    jurisdiction: Optional[ListType[CodeableConcept]] = Field(
        description="Intended jurisdiction for citation record (if applicable)",
        default=None,
    )
    purpose: Optional[fhir.markdown] = Field(
        description="Why this citation is defined",
        default=None,
    )
    copyright: Optional[fhir.markdown] = Field(
        description="Use and/or publishing restrictions for the citation record, not for the cited artifact",
        default=None,
    )
    copyrightLabel: Optional[fhir.string] = Field(
        description="Copyright holder and year(s) for the ciation record, not for the cited artifact",
        default=None,
    )
    approvalDate: Optional[fhir.date_] = Field(
        description="When the citation record was approved by publisher",
        default=None,
    )
    lastReviewDate: Optional[fhir.date_] = Field(
        description="When the citation record was last reviewed by the publisher",
        default=None,
    )
    effectivePeriod: Optional[Period] = Field(
        description="When the citation record is expected to be used",
        default=None,
    )
    author: Optional[ListType[ContactDetail]] = Field(
        description="Who authored the citation record",
        default=None,
    )
    editor: Optional[ListType[ContactDetail]] = Field(
        description="Who edited the citation record",
        default=None,
    )
    reviewer: Optional[ListType[ContactDetail]] = Field(
        description="Who reviewed the citation record",
        default=None,
    )
    endorser: Optional[ListType[ContactDetail]] = Field(
        description="Who endorsed the citation record",
        default=None,
    )
    summary: Optional[ListType[CitationSummary]] = Field(
        description="A human-readable display of key concepts to represent the citation",
        default=None,
    )
    classification: Optional[ListType[CitationClassification]] = Field(
        description="The assignment to an organizing scheme",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Used for general notes and annotations not coded elsewhere",
        default=None,
    )
    currentState: Optional[ListType[CodeableConcept]] = Field(
        description="The status of the citation record",
        default=None,
    )
    statusDate: Optional[ListType[CitationStatusDate]] = Field(
        description="An effective date or period for a status of the citation record",
        default=None,
    )
    relatedArtifact: Optional[ListType[RelatedArtifact]] = Field(
        description="Artifact related to the citation record",
        default=None,
    )
    citedArtifact: Optional[CitationCitedArtifact] = Field(
        description="The article or artifact being described",
        default=None,
    )

    @property
    def versionAlgorithm(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="versionAlgorithm",
        )

    @model_validator(mode="after")
    def versionAlgorithm_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.String, Coding],
            field_name_base="versionAlgorithm",
            required=False,
        )

    @model_validator(mode="after")
    def FHIR_cnl_0_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.exists() implies name.matches('^[A-Z]([A-Za-z0-9_]){1,254}$')",
            human="Name should be usable as an identifier for the module by machine processing applications such as code generation",
            key="cnl-0",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_cnl_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("url",),
            expression="exists() implies matches('^[^|# ]+$')",
            human="URL should not contain | or # - these characters make processing canonical references problematic",
            key="cnl-1",
            severity="warning",
        )
