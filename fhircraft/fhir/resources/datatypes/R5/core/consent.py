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
    CodeableConcept,
    Reference,
    Period,
    Attachment,
    BackboneElement,
    Coding,
    Expression,
)
from .resource import Resource
from .domain_resource import DomainResource

class ConsentPolicyBasis(BackboneElement):
    """
    A Reference or URL used to uniquely identify the policy the organization will enforce for this Consent. This Reference or URL should be specific to the version of the policy and should be dereferencable to a computable policy of some form.
    """

    reference: Optional[Reference] = Field(
        description="Reference backing policy resource",
        default=None,
    )
    url: Optional[Url] = Field(
        description="URL to a computable backing policy",
        default=None,
    )

class ConsentVerification(BackboneElement):
    """
    Whether a treatment instruction (e.g. artificial respiration: yes or no) was verified with the patient, his/her family or another authorized person.
    """

    verified: Optional[Boolean] = Field(
        description="Has been verified",
        default=None,
    )
    verificationType: Optional[CodeableConcept] = Field(
        description="Business case of verification",
        default=None,
    )
    verifiedBy: Optional[Reference] = Field(
        description="Person conducting verification",
        default=None,
    )
    verifiedWith: Optional[Reference] = Field(
        description="Person who verified",
        default=None,
    )
    verificationDate: Optional[ListType[DateTime]] = Field(
        description="When consent verified",
        default=None,
    )

class ConsentProvisionActor(BackboneElement):
    """
    Who or what is controlled by this provision. Use group to identify a set of actors by some property they share (e.g. 'admitting officers').
    """

    role: Optional[CodeableConcept] = Field(
        description="How the actor is involved",
        default=None,
    )
    reference: Optional[Reference] = Field(
        description="Resource for the actor (or group, by role)",
        default=None,
    )

class ConsentProvisionData(BackboneElement):
    """
    The resources controlled by this provision if specific resources are referenced.
    """

    meaning: Optional[Code] = Field(
        description="instance | related | dependents | authoredby",
        default=None,
    )
    reference: Optional[Reference] = Field(
        description="The actual data reference",
        default=None,
    )

class ConsentProvision(BackboneElement):
    """
    An exception to the base policy of this consent. An exception can be an addition or removal of access permissions.
    """

    period: Optional[Period] = Field(
        description="Timeframe for this provision",
        default=None,
    )
    actor: Optional[ListType[ConsentProvisionActor]] = Field(
        description="Who|what controlled by this provision (or group, by role)",
        default=None,
    )
    action: Optional[ListType[CodeableConcept]] = Field(
        description="Actions controlled by this provision",
        default=None,
    )
    securityLabel: Optional[ListType[Coding]] = Field(
        description="Security Labels that define affected resources",
        default=None,
    )
    purpose: Optional[ListType[Coding]] = Field(
        description="Context of activities covered by this provision",
        default=None,
    )
    documentType: Optional[ListType[Coding]] = Field(
        description="e.g. Resource Type, Profile, CDA, etc",
        default=None,
    )
    code: Optional[ListType[CodeableConcept]] = Field(
        description="e.g. LOINC or SNOMED CT code, etc. in the content",
        default=None,
    )
    dataPeriod: Optional[Period] = Field(
        description="Timeframe for data controlled by this provision",
        default=None,
    )
    data: Optional[ListType[ConsentProvisionData]] = Field(
        description="Data controlled by this provision",
        default=None,
    )
    expression: Optional[Expression] = Field(
        description="A computable expression of the consent",
        default=None,
    )
    provision: Optional[ListType["ConsentProvision"]] = Field(
        description="Nested Exception Provisions",
        default=None,
    )

class Consent(DomainResource):
    """
    A record of a healthcare consumer’s  choices  or choices made on their behalf by a third party, which permits or denies identified recipient(s) or recipient role(s) to perform one or more actions within a given policy context, for specific purposes and periods of time.
    """

    _abstract = False
    _type = "Consent"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Consent"

    identifier: Optional[ListType[Identifier]] = Field(
        description="Identifier for this record (external references)",
        default=None,
    )
    status: Optional[Code] = Field(
        description="draft | active | inactive | not-done | entered-in-error | unknown",
        default=None,
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description="Classification of the consent statement - for indexing/retrieval",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="Who the consent applies to",
        default=None,
    )
    date: Optional[Date] = Field(
        description="Fully executed date of the consent",
        default=None,
    )
    period: Optional[Period] = Field(
        description="Effective period for this Consent",
        default=None,
    )
    grantor: Optional[ListType[Reference]] = Field(
        description="Who is granting rights according to the policy and rules",
        default=None,
    )
    grantee: Optional[ListType[Reference]] = Field(
        description="Who is agreeing to the policy and rules",
        default=None,
    )
    manager: Optional[ListType[Reference]] = Field(
        description="Consent workflow management",
        default=None,
    )
    controller: Optional[ListType[Reference]] = Field(
        description="Consent Enforcer",
        default=None,
    )
    sourceAttachment: Optional[ListType[Attachment]] = Field(
        description="Source from which this consent is taken",
        default=None,
    )
    sourceReference: Optional[ListType[Reference]] = Field(
        description="Source from which this consent is taken",
        default=None,
    )
    regulatoryBasis: Optional[ListType[CodeableConcept]] = Field(
        description="Regulations establishing base Consent",
        default=None,
    )
    policyBasis: Optional[ConsentPolicyBasis] = Field(
        description="Computable version of the backing policy",
        default=None,
    )
    policyText: Optional[ListType[Reference]] = Field(
        description="Human Readable Policy",
        default=None,
    )
    verification: Optional[ListType[ConsentVerification]] = Field(
        description="Consent Verified by patient or family",
        default=None,
    )
    decision: Optional[Code] = Field(
        description="deny | permit",
        default=None,
    )
    provision: Optional[ListType[ConsentProvision]] = Field(
        description="Constraints to the base Consent.policyRule/Consent.policy",
        default=None,
    )
