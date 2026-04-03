import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)


from ..primitive import *
from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    CodeableConcept,
    Coding,
    Reference,
    Attachment,
    BackboneElement,
    Period,
)
from .resource import Resource
from .domain_resource import DomainResource

class ConsentPolicy(BackboneElement):
    """
    The references to the policies that are included in this consent scope. Policies may be organizational, but are often defined jurisdictionally, or in law.
    """

    authority: Optional[Uri] = Field(
        description="Enforcement source for policy",
        default=None,
    )
    uri: Optional[Uri] = Field(
        description="Specific policy covered by this consent",
        default=None,
    )

class ConsentVerification(BackboneElement):
    """
    Whether a treatment instruction (e.g. artificial respiration yes or no) was verified with the patient, his/her family or another authorized person.
    """

    verified: Optional[Boolean] = Field(
        description="Has been verified",
        default=None,
    )
    verifiedWith: Optional[Reference] = Field(
        description="Person who verified",
        default=None,
    )
    verificationDate: Optional[DateTime] = Field(
        description="When consent verified",
        default=None,
    )

class ConsentProvisionActor(BackboneElement):
    """
    Who or what is controlled by this rule. Use group to identify a set of actors by some property they share (e.g. 'admitting officers').
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
    The resources controlled by this rule if specific resources are referenced.
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

    type: Optional[Code] = Field(
        description="deny | permit",
        default=None,
    )
    period: Optional[Period] = Field(
        description="Timeframe for this rule",
        default=None,
    )
    actor: Optional[ListType[ConsentProvisionActor]] = Field(
        description="Who|what controlled by this rule (or group, by role)",
        default=None,
    )
    action: Optional[ListType[CodeableConcept]] = Field(
        description="Actions controlled by this rule",
        default=None,
    )
    securityLabel: Optional[ListType[Coding]] = Field(
        description="Security Labels that define affected resources",
        default=None,
    )
    purpose: Optional[ListType[Coding]] = Field(
        description="Context of activities covered by this rule",
        default=None,
    )
    class_: Optional[ListType[Coding]] = Field(
        description="e.g. Resource Type, Profile, CDA, etc.",
        default=None,
        alias="class",
    )
    code: Optional[ListType[CodeableConcept]] = Field(
        description="e.g. LOINC or SNOMED CT code, etc. in the content",
        default=None,
    )
    dataPeriod: Optional[Period] = Field(
        description="Timeframe for data controlled by this rule",
        default=None,
    )
    data: Optional[ListType[ConsentProvisionData]] = Field(
        description="Data controlled by this rule",
        default=None,
    )
    provision: Optional[ListType["ConsentProvision"]] = Field(
        description="Nested Exception Rules",
        default=None,
    )

class Consent(DomainResource):
    """
    A record of a healthcare consumer’s  choices, which permits or denies identified recipient(s) or recipient role(s) to perform one or more actions within a given policy context, for specific purposes and periods of time.
    """

    _abstract = False
    _type = "Consent"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Consent"

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
        description="Identifier for this record (external references)",
        default=None,
    )
    status: Optional[Code] = Field(
        description="draft | proposed | active | rejected | inactive | entered-in-error",
        default=None,
    )
    scope: Optional[CodeableConcept] = Field(
        description="Which of the four areas this resource covers (extensible)",
        default=None,
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description="Classification of the consent statement - for indexing/retrieval",
        default=None,
    )
    patient: Optional[Reference] = Field(
        description="Who the consent applies to",
        default=None,
    )
    dateTime: Optional[DateTime] = Field(
        description="When this Consent was created or indexed",
        default=None,
    )
    performer: Optional[ListType[Reference]] = Field(
        description="Who is agreeing to the policy and rules",
        default=None,
    )
    organization: Optional[ListType[Reference]] = Field(
        description="Custodian of the consent",
        default=None,
    )
    sourceAttachment: Optional[Attachment] = Field(
        description="Source from which this consent is taken",
        default=None,
    )
    sourceReference: Optional[Reference] = Field(
        description="Source from which this consent is taken",
        default=None,
    )
    policy: Optional[ListType[ConsentPolicy]] = Field(
        description="Policies covered by this consent",
        default=None,
    )
    policyRule: Optional[CodeableConcept] = Field(
        description="Regulation that this consents to",
        default=None,
    )
    verification: Optional[ListType[ConsentVerification]] = Field(
        description="Consent Verified by patient or family",
        default=None,
    )
    provision: Optional[ConsentProvision] = Field(
        description="Constraints to the base Consent.policyRule",
        default=None,
    )

    @property
    def source(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="source",
        )

    @model_validator(mode="after")
    def source_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Attachment, Reference],
            field_name_base="source",
            required=False,
        )

    @model_validator(mode="after")
    def FHIR_ppc_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="policy.exists() or policyRule.exists()",
            human="Either a Policy or PolicyRule",
            key="ppc-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ppc_2_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="patient.exists() or scope.coding.where(system='something' and code='patient-privacy').exists().not()",
            human="IF Scope=privacy, there must be a patient",
            key="ppc-2",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ppc_3_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="patient.exists() or scope.coding.where(system='something' and code='research').exists().not()",
            human="IF Scope=research, there must be a patient",
            key="ppc-3",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ppc_4_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="patient.exists() or scope.coding.where(system='something' and code='adr').exists().not()",
            human="IF Scope=adr, there must be a patient",
            key="ppc-4",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ppc_5_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="patient.exists() or scope.coding.where(system='something' and code='treatment').exists().not()",
            human="IF Scope=treatment, there must be a patient",
            key="ppc-5",
            severity="error",
        )
