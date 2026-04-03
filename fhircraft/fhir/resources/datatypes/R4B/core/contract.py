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
    CodeableConcept,
    Reference,
    Period,
    BackboneElement,
    Coding,
    Attachment,
    Quantity,
    Money,
    Timing,
    Annotation,
    Signature,
)
from .resource import Resource
from .domain_resource import DomainResource

class ContractContentDefinition(BackboneElement):
    """
    Precusory content developed with a focus and intent of supporting the formation a Contract instance, which may be associated with and transformable into a Contract.
    """

    type: Optional[CodeableConcept] = Field(
        description="Content structure and use",
        default=None,
    )
    subType: Optional[CodeableConcept] = Field(
        description="Detailed Content Type Definition",
        default=None,
    )
    publisher: Optional[Reference] = Field(
        description="Publisher Entity",
        default=None,
    )
    publicationDate: Optional[DateTime] = Field(
        description="When published",
        default=None,
    )
    publicationStatus: Optional[Code] = Field(
        description="amended | appended | cancelled | disputed | entered-in-error | executable | executed | negotiable | offered | policy | rejected | renewed | revoked | resolved | terminated",
        default=None,
    )
    copyright: Optional[Markdown] = Field(
        description="Publication Ownership",
        default=None,
    )

class ContractTermSecurityLabel(BackboneElement):
    """
    Security labels that protect the handling of information about the term and its elements, which may be specifically identified..
    """

    number: Optional[ListType[UnsignedInt]] = Field(
        description="Link to Security Labels",
        default=None,
    )
    classification: Optional[Coding] = Field(
        description="Confidentiality Protection",
        default=None,
    )
    category: Optional[ListType[Coding]] = Field(
        description="Applicable Policy",
        default=None,
    )
    control: Optional[ListType[Coding]] = Field(
        description="Handling Instructions",
        default=None,
    )

class ContractTermOfferParty(BackboneElement):
    """
    Offer Recipient.
    """

    reference: Optional[ListType[Reference]] = Field(
        description="Referenced entity",
        default=None,
    )
    role: Optional[CodeableConcept] = Field(
        description="Participant engagement type",
        default=None,
    )

class ContractTermOfferAnswer(BackboneElement):
    """
    Response to offer text.
    """

    valueBoolean: Optional[Boolean] = Field(
        description="The actual answer response",
        default=None,
    )
    valueDecimal: Optional[Decimal] = Field(
        description="The actual answer response",
        default=None,
    )
    valueInteger: Optional[Integer] = Field(
        description="The actual answer response",
        default=None,
    )
    valueDate: Optional[Date] = Field(
        description="The actual answer response",
        default=None,
    )
    valueDateTime: Optional[DateTime] = Field(
        description="The actual answer response",
        default=None,
    )
    valueTime: Optional[Time] = Field(
        description="The actual answer response",
        default=None,
    )
    valueString: Optional[String] = Field(
        description="The actual answer response",
        default=None,
    )
    valueUri: Optional[Uri] = Field(
        description="The actual answer response",
        default=None,
    )
    valueAttachment: Optional[Attachment] = Field(
        description="The actual answer response",
        default=None,
    )
    valueCoding: Optional[Coding] = Field(
        description="The actual answer response",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="The actual answer response",
        default=None,
    )
    valueReference: Optional[Reference] = Field(
        description="The actual answer response",
        default=None,
    )

    @property
    def value(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="value",
        )

    @model_validator(mode="after")
    def value_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[
                Boolean,
                Decimal,
                Integer,
                Date,
                DateTime,
                Time,
                String,
                Uri,
                Attachment,
                Coding,
                Quantity,
                Reference,
            ],
            field_name_base="value",
            required=True,
        )

class ContractTermOffer(BackboneElement):
    """
    The matter of concern in the context of this provision of the agrement.
    """

    identifier: Optional[ListType[Identifier]] = Field(
        description="Offer business ID",
        default=None,
    )
    party: Optional[ListType[ContractTermOfferParty]] = Field(
        description="Offer Recipient",
        default=None,
    )
    topic: Optional[Reference] = Field(
        description="Negotiable offer asset",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Contract Offer Type or Form",
        default=None,
    )
    decision: Optional[CodeableConcept] = Field(
        description="Accepting party choice",
        default=None,
    )
    decisionMode: Optional[ListType[CodeableConcept]] = Field(
        description="How decision is conveyed",
        default=None,
    )
    answer: Optional[ListType[ContractTermOfferAnswer]] = Field(
        description="Response to offer text",
        default=None,
    )
    text: Optional[String] = Field(
        description="Human readable offer text",
        default=None,
    )
    linkId: Optional[ListType[String]] = Field(
        description="Pointer to text",
        default=None,
    )
    securityLabelNumber: Optional[ListType[UnsignedInt]] = Field(
        description="Offer restriction numbers",
        default=None,
    )

class ContractTermAssetContext(BackboneElement):
    """
    Circumstance of the asset.
    """

    reference: Optional[Reference] = Field(
        description="Creator,custodian or owner",
        default=None,
    )
    code: Optional[ListType[CodeableConcept]] = Field(
        description="Codeable asset context",
        default=None,
    )
    text: Optional[String] = Field(
        description="Context description",
        default=None,
    )

class ContractTermAssetAnswer(BackboneElement):
    """
    Response to assets.
    """

    valueBoolean: Optional[Boolean] = Field(
        description="The actual answer response",
        default=None,
    )
    valueDecimal: Optional[Decimal] = Field(
        description="The actual answer response",
        default=None,
    )
    valueInteger: Optional[Integer] = Field(
        description="The actual answer response",
        default=None,
    )
    valueDate: Optional[Date] = Field(
        description="The actual answer response",
        default=None,
    )
    valueDateTime: Optional[DateTime] = Field(
        description="The actual answer response",
        default=None,
    )
    valueTime: Optional[Time] = Field(
        description="The actual answer response",
        default=None,
    )
    valueString: Optional[String] = Field(
        description="The actual answer response",
        default=None,
    )
    valueUri: Optional[Uri] = Field(
        description="The actual answer response",
        default=None,
    )
    valueAttachment: Optional[Attachment] = Field(
        description="The actual answer response",
        default=None,
    )
    valueCoding: Optional[Coding] = Field(
        description="The actual answer response",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="The actual answer response",
        default=None,
    )
    valueReference: Optional[Reference] = Field(
        description="The actual answer response",
        default=None,
    )

    @property
    def value(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="value",
        )

    @model_validator(mode="after")
    def value_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[
                Boolean,
                Decimal,
                Integer,
                Date,
                DateTime,
                Time,
                String,
                Uri,
                Attachment,
                Coding,
                Quantity,
                Reference,
            ],
            field_name_base="value",
            required=True,
        )

class ContractTermAssetValuedItem(BackboneElement):
    """
    Contract Valued Item List.
    """

    entityCodeableConcept: Optional[CodeableConcept] = Field(
        description="Contract Valued Item Type",
        default=None,
    )
    entityReference: Optional[Reference] = Field(
        description="Contract Valued Item Type",
        default=None,
    )
    identifier: Optional[Identifier] = Field(
        description="Contract Valued Item Number",
        default=None,
    )
    effectiveTime: Optional[DateTime] = Field(
        description="Contract Valued Item Effective Tiem",
        default=None,
    )
    quantity: Optional[Quantity] = Field(
        description="Count of Contract Valued Items",
        default=None,
    )
    unitPrice: Optional[Money] = Field(
        description="Contract Valued Item fee, charge, or cost",
        default=None,
    )
    factor: Optional[Decimal] = Field(
        description="Contract Valued Item Price Scaling Factor",
        default=None,
    )
    points: Optional[Decimal] = Field(
        description="Contract Valued Item Difficulty Scaling Factor",
        default=None,
    )
    net: Optional[Money] = Field(
        description="Total Contract Valued Item Value",
        default=None,
    )
    payment: Optional[String] = Field(
        description="Terms of valuation",
        default=None,
    )
    paymentDate: Optional[DateTime] = Field(
        description="When payment is due",
        default=None,
    )
    responsible: Optional[Reference] = Field(
        description="Who will make payment",
        default=None,
    )
    recipient: Optional[Reference] = Field(
        description="Who will receive payment",
        default=None,
    )
    linkId: Optional[ListType[String]] = Field(
        description="Pointer to specific item",
        default=None,
    )
    securityLabelNumber: Optional[ListType[UnsignedInt]] = Field(
        description="Security Labels that define affected terms",
        default=None,
    )

    @property
    def entity(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="entity",
        )

    @model_validator(mode="after")
    def entity_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[CodeableConcept, Reference],
            field_name_base="entity",
            required=False,
        )

class ContractTermAsset(BackboneElement):
    """
    Contract Term Asset List.
    """

    scope: Optional[CodeableConcept] = Field(
        description="Range of asset",
        default=None,
    )
    type: Optional[ListType[CodeableConcept]] = Field(
        description="Asset category",
        default=None,
    )
    typeReference: Optional[ListType[Reference]] = Field(
        description="Associated entities",
        default=None,
    )
    subtype: Optional[ListType[CodeableConcept]] = Field(
        description="Asset sub-category",
        default=None,
    )
    relationship: Optional[Coding] = Field(
        description="Kinship of the asset",
        default=None,
    )
    context: Optional[ListType[ContractTermAssetContext]] = Field(
        description="Circumstance of the asset",
        default=None,
    )
    condition: Optional[String] = Field(
        description="Quality desctiption of asset",
        default=None,
    )
    periodType: Optional[ListType[CodeableConcept]] = Field(
        description="Asset availability types",
        default=None,
    )
    period: Optional[ListType[Period]] = Field(
        description="Time period of the asset",
        default=None,
    )
    usePeriod: Optional[ListType[Period]] = Field(
        description="Time period",
        default=None,
    )
    text: Optional[String] = Field(
        description="Asset clause or question text",
        default=None,
    )
    linkId: Optional[ListType[String]] = Field(
        description="Pointer to asset text",
        default=None,
    )
    answer: Optional[ListType[ContractTermAssetAnswer]] = Field(
        description="Response to assets",
        default=None,
    )
    securityLabelNumber: Optional[ListType[UnsignedInt]] = Field(
        description="Asset restriction numbers",
        default=None,
    )
    valuedItem: Optional[ListType[ContractTermAssetValuedItem]] = Field(
        description="Contract Valued Item List",
        default=None,
    )

class ContractTermActionSubject(BackboneElement):
    """
    Entity of the action.
    """

    reference: Optional[ListType[Reference]] = Field(
        description="Entity of the action",
        default=None,
    )
    role: Optional[CodeableConcept] = Field(
        description="Role type of the agent",
        default=None,
    )

class ContractTermAction(BackboneElement):
    """
    An actor taking a role in an activity for which it can be assigned some degree of responsibility for the activity taking place.
    """

    doNotPerform: Optional[Boolean] = Field(
        description="True if the term prohibits the  action",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Type or form of the action",
        default=None,
    )
    subject: Optional[ListType[ContractTermActionSubject]] = Field(
        description="Entity of the action",
        default=None,
    )
    intent: Optional[CodeableConcept] = Field(
        description="Purpose for the Contract Term Action",
        default=None,
    )
    linkId: Optional[ListType[String]] = Field(
        description="Pointer to specific item",
        default=None,
    )
    status: Optional[CodeableConcept] = Field(
        description="State of the action",
        default=None,
    )
    context: Optional[Reference] = Field(
        description="Episode associated with action",
        default=None,
    )
    contextLinkId: Optional[ListType[String]] = Field(
        description="Pointer to specific item",
        default=None,
    )
    occurrenceDateTime: Optional[DateTime] = Field(
        description="When action happens",
        default=None,
    )
    occurrencePeriod: Optional[Period] = Field(
        description="When action happens",
        default=None,
    )
    occurrenceTiming: Optional[Timing] = Field(
        description="When action happens",
        default=None,
    )
    requester: Optional[ListType[Reference]] = Field(
        description="Who asked for action",
        default=None,
    )
    requesterLinkId: Optional[ListType[String]] = Field(
        description="Pointer to specific item",
        default=None,
    )
    performerType: Optional[ListType[CodeableConcept]] = Field(
        description="Kind of service performer",
        default=None,
    )
    performerRole: Optional[CodeableConcept] = Field(
        description="Competency of the performer",
        default=None,
    )
    performer: Optional[Reference] = Field(
        description="Actor that wil execute (or not) the action",
        default=None,
    )
    performerLinkId: Optional[ListType[String]] = Field(
        description="Pointer to specific item",
        default=None,
    )
    reasonCode: Optional[ListType[CodeableConcept]] = Field(
        description="Why is action (not) needed?",
        default=None,
    )
    reasonReference: Optional[ListType[Reference]] = Field(
        description="Why is action (not) needed?",
        default=None,
    )
    reason: Optional[ListType[String]] = Field(
        description="Why action is to be performed",
        default=None,
    )
    reasonLinkId: Optional[ListType[String]] = Field(
        description="Pointer to specific item",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Comments about the action",
        default=None,
    )
    securityLabelNumber: Optional[ListType[UnsignedInt]] = Field(
        description="Action restriction numbers",
        default=None,
    )

    @property
    def occurrence(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="occurrence",
        )

    @model_validator(mode="after")
    def occurrence_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[DateTime, Period, Timing],
            field_name_base="occurrence",
            required=False,
        )

class ContractTerm(BackboneElement):
    """
    One or more Contract Provisions, which may be related and conveyed as a group, and may contain nested groups.
    """

    identifier: Optional[Identifier] = Field(
        description="Contract Term Number",
        default=None,
    )
    issued: Optional[DateTime] = Field(
        description="Contract Term Issue Date Time",
        default=None,
    )
    applies: Optional[Period] = Field(
        description="Contract Term Effective Time",
        default=None,
    )
    topicCodeableConcept: Optional[CodeableConcept] = Field(
        description="Term Concern",
        default=None,
    )
    topicReference: Optional[Reference] = Field(
        description="Term Concern",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Contract Term Type or Form",
        default=None,
    )
    subType: Optional[CodeableConcept] = Field(
        description="Contract Term Type specific classification",
        default=None,
    )
    text: Optional[String] = Field(
        description="Term Statement",
        default=None,
    )
    securityLabel: Optional[ListType[ContractTermSecurityLabel]] = Field(
        description="Protection for the Term",
        default=None,
    )
    offer: Optional[ContractTermOffer] = Field(
        description="Context of the Contract term",
        default=None,
    )
    asset: Optional[ListType[ContractTermAsset]] = Field(
        description="Contract Term Asset List",
        default=None,
    )
    action: Optional[ListType[ContractTermAction]] = Field(
        description="Entity being ascribed responsibility",
        default=None,
    )
    group: Optional[ListType["ContractTerm"]] = Field(
        description="Nested Contract Term Group",
        default=None,
    )

    @property
    def topic(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="topic",
        )

    @model_validator(mode="after")
    def topic_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[CodeableConcept, Reference],
            field_name_base="topic",
            required=False,
        )

class ContractSigner(BackboneElement):
    """
    Parties with legal standing in the Contract, including the principal parties, the grantor(s) and grantee(s), which are any person or organization bound by the contract, and any ancillary parties, which facilitate the execution of the contract such as a notary or witness.
    """

    type: Optional[Coding] = Field(
        description="Contract Signatory Role",
        default=None,
    )
    party: Optional[Reference] = Field(
        description="Contract Signatory Party",
        default=None,
    )
    signature: Optional[ListType[Signature]] = Field(
        description="Contract Documentation Signature",
        default=None,
    )

class ContractFriendly(BackboneElement):
    """
    The "patient friendly language" versionof the Contract in whole or in parts. "Patient friendly language" means the representation of the Contract and Contract Provisions in a manner that is readily accessible and understandable by a layperson in accordance with best practices for communication styles that ensure that those agreeing to or signing the Contract understand the roles, actions, obligations, responsibilities, and implication of the agreement.
    """

    contentAttachment: Optional[Attachment] = Field(
        description="Easily comprehended representation of this Contract",
        default=None,
    )
    contentReference: Optional[Reference] = Field(
        description="Easily comprehended representation of this Contract",
        default=None,
    )

    @property
    def content(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="content",
        )

    @model_validator(mode="after")
    def content_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Attachment, Reference],
            field_name_base="content",
            required=True,
        )

class ContractLegal(BackboneElement):
    """
    List of Legal expressions or representations of this Contract.
    """

    contentAttachment: Optional[Attachment] = Field(
        description="Contract Legal Text",
        default=None,
    )
    contentReference: Optional[Reference] = Field(
        description="Contract Legal Text",
        default=None,
    )

    @property
    def content(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="content",
        )

    @model_validator(mode="after")
    def content_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Attachment, Reference],
            field_name_base="content",
            required=True,
        )

class ContractRule(BackboneElement):
    """
    List of Computable Policy Rule Language Representations of this Contract.
    """

    contentAttachment: Optional[Attachment] = Field(
        description="Computable Contract Rules",
        default=None,
    )
    contentReference: Optional[Reference] = Field(
        description="Computable Contract Rules",
        default=None,
    )

    @property
    def content(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="content",
        )

    @model_validator(mode="after")
    def content_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Attachment, Reference],
            field_name_base="content",
            required=True,
        )

class Contract(DomainResource):
    """
    Legally enforceable, formally recorded unilateral or bilateral directive i.e., a policy or agreement.
    """

    _abstract = False
    _type = "Contract"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Contract"

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
        description="Contract number",
        default=None,
    )
    url: Optional[Uri] = Field(
        description="Basal definition",
        default=None,
    )
    version: Optional[String] = Field(
        description="Business edition",
        default=None,
    )
    status: Optional[Code] = Field(
        description="amended | appended | cancelled | disputed | entered-in-error | executable | executed | negotiable | offered | policy | rejected | renewed | revoked | resolved | terminated",
        default=None,
    )
    legalState: Optional[CodeableConcept] = Field(
        description="Negotiation status",
        default=None,
    )
    instantiatesCanonical: Optional[Reference] = Field(
        description="Source Contract Definition",
        default=None,
    )
    instantiatesUri: Optional[Uri] = Field(
        description="External Contract Definition",
        default=None,
    )
    contentDerivative: Optional[CodeableConcept] = Field(
        description="Content derived from the basal information",
        default=None,
    )
    issued: Optional[DateTime] = Field(
        description="When this Contract was issued",
        default=None,
    )
    applies: Optional[Period] = Field(
        description="Effective time",
        default=None,
    )
    expirationType: Optional[CodeableConcept] = Field(
        description="Contract cessation cause",
        default=None,
    )
    subject: Optional[ListType[Reference]] = Field(
        description="Contract Target Entity",
        default=None,
    )
    authority: Optional[ListType[Reference]] = Field(
        description="Authority under which this Contract has standing",
        default=None,
    )
    domain: Optional[ListType[Reference]] = Field(
        description="A sphere of control governed by an authoritative jurisdiction, organization, or person",
        default=None,
    )
    site: Optional[ListType[Reference]] = Field(
        description="Specific Location",
        default=None,
    )
    name: Optional[String] = Field(
        description="Computer friendly designation",
        default=None,
    )
    title: Optional[String] = Field(
        description="Human Friendly name",
        default=None,
    )
    subtitle: Optional[String] = Field(
        description="Subordinate Friendly name",
        default=None,
    )
    alias: Optional[ListType[String]] = Field(
        description="Acronym or short name",
        default=None,
    )
    author: Optional[Reference] = Field(
        description="Source of Contract",
        default=None,
    )
    scope: Optional[CodeableConcept] = Field(
        description="Range of Legal Concerns",
        default=None,
    )
    topicCodeableConcept: Optional[CodeableConcept] = Field(
        description="Focus of contract interest",
        default=None,
    )
    topicReference: Optional[Reference] = Field(
        description="Focus of contract interest",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Legal instrument category",
        default=None,
    )
    subType: Optional[ListType[CodeableConcept]] = Field(
        description="Subtype within the context of type",
        default=None,
    )
    contentDefinition: Optional[ContractContentDefinition] = Field(
        description="Contract precursor content",
        default=None,
    )
    term: Optional[ListType[ContractTerm]] = Field(
        description="Contract Term List",
        default=None,
    )
    supportingInfo: Optional[ListType[Reference]] = Field(
        description="Extra Information",
        default=None,
    )
    relevantHistory: Optional[ListType[Reference]] = Field(
        description="Key event in Contract History",
        default=None,
    )
    signer: Optional[ListType[ContractSigner]] = Field(
        description="Contract Signatory",
        default=None,
    )
    friendly: Optional[ListType[ContractFriendly]] = Field(
        description="Contract Friendly Language",
        default=None,
    )
    legal: Optional[ListType[ContractLegal]] = Field(
        description="Contract Legal Language",
        default=None,
    )
    rule: Optional[ListType[ContractRule]] = Field(
        description="Computable Contract Language",
        default=None,
    )
    legallyBindingAttachment: Optional[Attachment] = Field(
        description="Binding Contract",
        default=None,
    )
    legallyBindingReference: Optional[Reference] = Field(
        description="Binding Contract",
        default=None,
    )

    @property
    def topic(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="topic",
        )

    @property
    def legallyBinding(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="legallyBinding",
        )

    @model_validator(mode="after")
    def topic_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[CodeableConcept, Reference],
            field_name_base="topic",
            required=False,
        )

    @model_validator(mode="after")
    def legallyBinding_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Attachment, Reference],
            field_name_base="legallyBinding",
            required=False,
        )
