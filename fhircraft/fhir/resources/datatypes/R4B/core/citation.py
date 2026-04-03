import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)


from ..primitive import *
from fhircraft.fhir.resources.datatypes.R4B.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    ContactDetail,
    UsageContext,
    CodeableConcept,
    Period,
    BackboneElement,
    Annotation,
    Reference,
    Attachment,
    HumanName,
    Address,
    ContactPoint,
)
from .resource import Resource
from .domain_resource import DomainResource

class CitationSummary(BackboneElement):
    """
    A human-readable display of the citation.
    """

    style: Optional[CodeableConcept] = Field(
        description="Format for display of the citation",
        default=None,
    )
    text: Optional[Markdown] = Field(
        description="The human-readable display of the citation",
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
    An effective date or period for a status of the citation.
    """

    activity: Optional[CodeableConcept] = Field(
        description="Classification of the status",
        default=None,
    )
    actual: Optional[Boolean] = Field(
        description="Either occurred or expected",
        default=None,
    )
    period: Optional[Period] = Field(
        description="When the status started and/or ended",
        default=None,
    )

class CitationRelatesTo(BackboneElement):
    """
    Artifact related to the Citation Resource.
    """

    relationshipType: Optional[CodeableConcept] = Field(
        description="How the Citation resource relates to the target artifact",
        default=None,
    )
    targetClassifier: Optional[ListType[CodeableConcept]] = Field(
        description="The clasification of the related artifact",
        default=None,
    )
    targetUri: Optional[Uri] = Field(
        description="The article or artifact that the Citation Resource is related to",
        default=None,
    )
    targetIdentifier: Optional[Identifier] = Field(
        description="The article or artifact that the Citation Resource is related to",
        default=None,
    )
    targetReference: Optional[Reference] = Field(
        description="The article or artifact that the Citation Resource is related to",
        default=None,
    )
    targetAttachment: Optional[Attachment] = Field(
        description="The article or artifact that the Citation Resource is related to",
        default=None,
    )

    @property
    def target(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="target",
        )

    @model_validator(mode="after")
    def target_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Uri, Identifier, Reference, Attachment],
            field_name_base="target",
            required=True,
        )

class CitationCitedArtifactVersion(BackboneElement):
    """
    The defined version of the cited artifact.
    """

    value: Optional[String] = Field(
        description="The version number or other version identifier",
        default=None,
    )
    baseCitation: Optional[Reference] = Field(
        description="Citation for the main version of the cited artifact",
        default=None,
    )

class CitationCitedArtifactStatusDate(BackboneElement):
    """
    An effective date or period for a status of the cited artifact.
    """

    activity: Optional[CodeableConcept] = Field(
        description="Classification of the status",
        default=None,
    )
    actual: Optional[Boolean] = Field(
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
    text: Optional[Markdown] = Field(
        description="The title of the article or artifact",
        default=None,
    )

class CitationCitedArtifactAbstract(BackboneElement):
    """
    Summary of the article or artifact.
    """

    type: Optional[CodeableConcept] = Field(
        description="The kind of abstract",
        default=None,
    )
    language: Optional[CodeableConcept] = Field(
        description="Used to express the specific language",
        default=None,
    )
    text: Optional[Markdown] = Field(
        description="Abstract content",
        default=None,
    )
    copyright: Optional[Markdown] = Field(
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
    value: Optional[String] = Field(
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

    relationshipType: Optional[CodeableConcept] = Field(
        description="How the cited artifact relates to the target artifact",
        default=None,
    )
    targetClassifier: Optional[ListType[CodeableConcept]] = Field(
        description="The clasification of the related artifact",
        default=None,
    )
    targetUri: Optional[Uri] = Field(
        description="The article or artifact that the cited artifact is related to",
        default=None,
    )
    targetIdentifier: Optional[Identifier] = Field(
        description="The article or artifact that the cited artifact is related to",
        default=None,
    )
    targetReference: Optional[Reference] = Field(
        description="The article or artifact that the cited artifact is related to",
        default=None,
    )
    targetAttachment: Optional[Attachment] = Field(
        description="The article or artifact that the cited artifact is related to",
        default=None,
    )

    @property
    def target(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="target",
        )

    @model_validator(mode="after")
    def target_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Uri, Identifier, Reference, Attachment],
            field_name_base="target",
            required=True,
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
    title: Optional[String] = Field(
        description="Name of the database or title of the book or journal",
        default=None,
    )
    publisher: Optional[Reference] = Field(
        description="Name of the publisher",
        default=None,
    )
    publisherLocation: Optional[String] = Field(
        description="Geographic location of the publisher",
        default=None,
    )

class CitationCitedArtifactPublicationFormPeriodicReleaseDateOfPublication(
    BackboneElement
):
    """
    Defining the date on which the issue of the journal was published.
    """

    date: Optional[Date] = Field(
        description="Date on which the issue of the journal was published",
        default=None,
    )
    year: Optional[String] = Field(
        description="Year on which the issue of the journal was published",
        default=None,
    )
    month: Optional[String] = Field(
        description="Month on which the issue of the journal was published",
        default=None,
    )
    day: Optional[String] = Field(
        description="Day on which the issue of the journal was published",
        default=None,
    )
    season: Optional[String] = Field(
        description="Season on which the issue of the journal was published",
        default=None,
    )
    text: Optional[String] = Field(
        description="Text representation of the date of which the issue of the journal was published",
        default=None,
    )

class CitationCitedArtifactPublicationFormPeriodicRelease(BackboneElement):
    """
    The specific issue in which the cited article resides.
    """

    citedMedium: Optional[CodeableConcept] = Field(
        description="Internet or Print",
        default=None,
    )
    volume: Optional[String] = Field(
        description="Volume number of journal in which the article is published",
        default=None,
    )
    issue: Optional[String] = Field(
        description="Issue, part or supplement of journal in which the article is published",
        default=None,
    )
    dateOfPublication: Optional[
        CitationCitedArtifactPublicationFormPeriodicReleaseDateOfPublication
    ] = Field(
        description="Defining the date on which the issue of the journal was published",
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
    periodicRelease: Optional[CitationCitedArtifactPublicationFormPeriodicRelease] = (
        Field(
            description="The specific issue in which the cited article resides",
            default=None,
        )
    )
    articleDate: Optional[DateTime] = Field(
        description="The date the article was added to the database, or the date the article was released",
        default=None,
    )
    lastRevisionDate: Optional[DateTime] = Field(
        description="The date the article was last revised or updated in the database",
        default=None,
    )
    language: Optional[ListType[CodeableConcept]] = Field(
        description="Language in which this form of the article is published",
        default=None,
    )
    accessionNumber: Optional[String] = Field(
        description="Entry number or identifier for inclusion in a database",
        default=None,
    )
    pageString: Optional[String] = Field(
        description="Used for full display of pagination",
        default=None,
    )
    firstPage: Optional[String] = Field(
        description="Used for isolated representation of first page",
        default=None,
    )
    lastPage: Optional[String] = Field(
        description="Used for isolated representation of last page",
        default=None,
    )
    pageCount: Optional[String] = Field(
        description="Number of pages or screens",
        default=None,
    )
    copyright: Optional[Markdown] = Field(
        description="Copyright notice for the full article or artifact",
        default=None,
    )

class CitationCitedArtifactWebLocation(BackboneElement):
    """
    Used for any URL for the article or artifact cited.
    """

    type: Optional[CodeableConcept] = Field(
        description="Code the reason for different URLs, e.g. abstract and full-text",
        default=None,
    )
    url: Optional[Uri] = Field(
        description="The specific URL",
        default=None,
    )

class CitationCitedArtifactClassificationWhoClassified(BackboneElement):
    """
    Provenance and copyright of classification.
    """

    person: Optional[Reference] = Field(
        description="Person who created the classification",
        default=None,
    )
    organization: Optional[Reference] = Field(
        description="Organization who created the classification",
        default=None,
    )
    publisher: Optional[Reference] = Field(
        description="The publisher of the classification, not the publisher of the article or artifact being cited",
        default=None,
    )
    classifierCopyright: Optional[String] = Field(
        description="Rights management statement for the classification",
        default=None,
    )
    freeToShare: Optional[Boolean] = Field(
        description="Acceptable to re-use the classification",
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
    whoClassified: Optional[CitationCitedArtifactClassificationWhoClassified] = Field(
        description="Provenance and copyright of classification",
        default=None,
    )

class CitationCitedArtifactContributorshipEntryAffiliationInfo(BackboneElement):
    """
    Organization affiliated with the entity.
    """

    affiliation: Optional[String] = Field(
        description="Display for the organization",
        default=None,
    )
    role: Optional[String] = Field(
        description="Role within the organization, such as professional title",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Identifier for the organization",
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
    time: Optional[DateTime] = Field(
        description="The time that the contribution was made",
        default=None,
    )

class CitationCitedArtifactContributorshipEntry(BackboneElement):
    """
    An individual entity named in the author list or contributor list.
    """

    name: Optional[HumanName] = Field(
        description="A name associated with the person",
        default=None,
    )
    initials: Optional[String] = Field(
        description="Initials for forename",
        default=None,
    )
    collectiveName: Optional[String] = Field(
        description="Used for collective or corporate name as an author",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Author identifier, eg ORCID",
        default=None,
    )
    affiliationInfo: Optional[
        ListType[CitationCitedArtifactContributorshipEntryAffiliationInfo]
    ] = Field(
        description="Organizational affiliation",
        default=None,
    )
    address: Optional[ListType[Address]] = Field(
        description="Physical mailing address",
        default=None,
    )
    telecom: Optional[ListType[ContactPoint]] = Field(
        description="Email or telephone contact methods for the author or contributor",
        default=None,
    )
    contributionType: Optional[ListType[CodeableConcept]] = Field(
        description="The specific contribution",
        default=None,
    )
    role: Optional[CodeableConcept] = Field(
        description="The role of the contributor (e.g. author, editor, reviewer)",
        default=None,
    )
    contributionInstance: Optional[
        ListType[CitationCitedArtifactContributorshipEntryContributionInstance]
    ] = Field(
        description="Contributions with accounting for time or number",
        default=None,
    )
    correspondingContact: Optional[Boolean] = Field(
        description="Indication of which contributor is the corresponding contributor for the role",
        default=None,
    )
    listOrder: Optional[PositiveInt] = Field(
        description="Used to code order of authors",
        default=None,
    )

class CitationCitedArtifactContributorshipSummary(BackboneElement):
    """
    Used to record a display of the author/contributor list without separate coding for each list member.
    """

    type: Optional[CodeableConcept] = Field(
        description="Either authorList or contributorshipStatement",
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
    value: Optional[Markdown] = Field(
        description="The display string for the author list, contributor list, or contributorship statement",
        default=None,
    )

class CitationCitedArtifactContributorship(BackboneElement):
    """
    This element is used to list authors and other contributors, their contact information, specific contributions, and summary statements.
    """

    complete: Optional[Boolean] = Field(
        description="Indicates if the list includes all authors and/or contributors",
        default=None,
    )
    entry: Optional[ListType[CitationCitedArtifactContributorshipEntry]] = Field(
        description="An individual entity named in the list",
        default=None,
    )
    summary: Optional[ListType[CitationCitedArtifactContributorshipSummary]] = Field(
        description="Used to record a display of the author/contributor list without separate coding for each list member",
        default=None,
    )

class CitationCitedArtifact(BackboneElement):
    """
    The article or artifact being described.
    """

    identifier: Optional[ListType[Identifier]] = Field(
        description="May include DOI, PMID, PMCID, etc.",
        default=None,
    )
    relatedIdentifier: Optional[ListType[Identifier]] = Field(
        description="May include trial registry identifiers",
        default=None,
    )
    dateAccessed: Optional[DateTime] = Field(
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
    url: Optional[Uri] = Field(
        description="Canonical identifier for this citation, represented as a globally unique URI",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Identifier for the Citation resource itself",
        default=None,
    )
    version: Optional[String] = Field(
        description="Business version of the citation",
        default=None,
    )
    name: Optional[String] = Field(
        description="Name for this citation (computer friendly)",
        default=None,
    )
    title: Optional[String] = Field(
        description="Name for this citation (human friendly)",
        default=None,
    )
    status: Optional[Code] = Field(
        description="draft | active | retired | unknown",
        default=None,
    )
    experimental: Optional[Boolean] = Field(
        description="For testing purposes, not real usage",
        default=None,
    )
    date: Optional[DateTime] = Field(
        description="Date last changed",
        default=None,
    )
    publisher: Optional[String] = Field(
        description="The publisher of the Citation, not the publisher of the article or artifact being cited",
        default=None,
    )
    contact: Optional[ListType[ContactDetail]] = Field(
        description="Contact details for the publisher of the Citation Resource",
        default=None,
    )
    description: Optional[Markdown] = Field(
        description="Natural language description of the citation",
        default=None,
    )
    useContext: Optional[ListType[UsageContext]] = Field(
        description="The context that the Citation Resource content is intended to support",
        default=None,
    )
    jurisdiction: Optional[ListType[CodeableConcept]] = Field(
        description="Intended jurisdiction for citation (if applicable)",
        default=None,
    )
    purpose: Optional[Markdown] = Field(
        description="Why this citation is defined",
        default=None,
    )
    copyright: Optional[Markdown] = Field(
        description="Use and/or publishing restrictions for the Citation, not for the cited artifact",
        default=None,
    )
    approvalDate: Optional[Date] = Field(
        description="When the citation was approved by publisher",
        default=None,
    )
    lastReviewDate: Optional[Date] = Field(
        description="When the citation was last reviewed",
        default=None,
    )
    effectivePeriod: Optional[Period] = Field(
        description="When the citation is expected to be used",
        default=None,
    )
    author: Optional[ListType[ContactDetail]] = Field(
        description="Who authored the Citation",
        default=None,
    )
    editor: Optional[ListType[ContactDetail]] = Field(
        description="Who edited the Citation",
        default=None,
    )
    reviewer: Optional[ListType[ContactDetail]] = Field(
        description="Who reviewed the Citation",
        default=None,
    )
    endorser: Optional[ListType[ContactDetail]] = Field(
        description="Who endorsed the Citation",
        default=None,
    )
    summary: Optional[ListType[CitationSummary]] = Field(
        description="A human-readable display of the citation",
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
        description="The status of the citation",
        default=None,
    )
    statusDate: Optional[ListType[CitationStatusDate]] = Field(
        description="An effective date or period for a status of the citation",
        default=None,
    )
    relatesTo: Optional[ListType[CitationRelatesTo]] = Field(
        description="Artifact related to the Citation Resource",
        default=None,
    )
    citedArtifact: Optional[CitationCitedArtifact] = Field(
        description="The article or artifact being described",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_cnl_0_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.exists() implies name.matches('[A-Z]([A-Za-z0-9_]){0,254}')",
            human="Name should be usable as an identifier for the module by machine processing applications such as code generation",
            key="cnl-0",
            severity="warning",
        )
