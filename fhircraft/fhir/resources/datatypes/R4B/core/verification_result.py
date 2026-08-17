import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)


import fhircraft.fhir.resources.datatypes.R4B.primitive as fhir
from fhircraft.fhir.resources.datatypes.R4B.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Reference,
    CodeableConcept,
    Timing,
    BackboneElement,
    Signature,
)
from .resource import Resource
from .domain_resource import DomainResource

class VerificationResultPrimarySource(BackboneElement):
    """
    Information about the primary source(s) involved in validation.
    """

    who: Optional[Reference] = Field(
        description="Reference to the primary source",
        default=None,
    )
    type: Optional[ListType[CodeableConcept]] = Field(
        description="Type of primary source (License Board; Primary Education; Continuing Education; Postal Service; Relationship owner; Registration Authority; legal source; issuing source; authoritative source)",
        default=None,
    )
    communicationMethod: Optional[ListType[CodeableConcept]] = Field(
        description="Method for exchanging information with the primary source",
        default=None,
    )
    validationStatus: Optional[CodeableConcept] = Field(
        description="successful | failed | unknown",
        default=None,
    )
    validationDate: Optional[fhir.dateTime] = Field(
        description="When the target was validated against the primary source",
        default=None,
    )
    canPushUpdates: Optional[CodeableConcept] = Field(
        description="yes | no | undetermined",
        default=None,
    )
    pushTypeAvailable: Optional[ListType[CodeableConcept]] = Field(
        description="specific | any | source",
        default=None,
    )

class VerificationResultAttestation(BackboneElement):
    """
    Information about the entity attesting to information.
    """

    who: Optional[Reference] = Field(
        description="The individual or organization attesting to information",
        default=None,
    )
    onBehalfOf: Optional[Reference] = Field(
        description="When the who is asserting on behalf of another (organization or individual)",
        default=None,
    )
    communicationMethod: Optional[CodeableConcept] = Field(
        description="The method by which attested information was submitted/retrieved",
        default=None,
    )
    date: Optional[fhir.date_] = Field(
        description="The date the information was attested to",
        default=None,
    )
    sourceIdentityCertificate: Optional[fhir.string] = Field(
        description="A digital identity certificate associated with the attestation source",
        default=None,
    )
    proxyIdentityCertificate: Optional[fhir.string] = Field(
        description="A digital identity certificate associated with the proxy entity submitting attested information on behalf of the attestation source",
        default=None,
    )
    proxySignature: Optional[Signature] = Field(
        description="Proxy signature",
        default=None,
    )
    sourceSignature: Optional[Signature] = Field(
        description="Attester signature",
        default=None,
    )

class VerificationResultValidator(BackboneElement):
    """
    Information about the entity validating information.
    """

    organization: Reference = Field(
        description="Reference to the organization validating information",
    )
    identityCertificate: Optional[fhir.string] = Field(
        description="A digital identity certificate associated with the validator",
        default=None,
    )
    attestationSignature: Optional[Signature] = Field(
        description="Validator signature",
        default=None,
    )

class VerificationResult(DomainResource):
    """
    Describes validation requirements, source(s), status and dates for one or more elements.
    """

    _abstract = False
    _type = "VerificationResult"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/VerificationResult"

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
    target: Optional[ListType[Reference]] = Field(
        description="A resource that was validated",
        default=None,
    )
    targetLocation: Optional[ListType[fhir.string]] = Field(
        description="The fhirpath location(s) within the resource that was validated",
        default=None,
    )
    need: Optional[CodeableConcept] = Field(
        description="none | initial | periodic",
        default=None,
    )
    status: fhir.code = Field(
        description="attested | validated | in-process | req-revalid | val-fail | reval-fail",
    )
    statusDate: Optional[fhir.dateTime] = Field(
        description="When the validation status was updated",
        default=None,
    )
    validationType: Optional[CodeableConcept] = Field(
        description="nothing | primary | multiple",
        default=None,
    )
    validationProcess: Optional[ListType[CodeableConcept]] = Field(
        description="The primary process by which the target is validated (edit check; value set; primary source; multiple sources; standalone; in context)",
        default=None,
    )
    frequency: Optional[Timing] = Field(
        description="Frequency of revalidation",
        default=None,
    )
    lastPerformed: Optional[fhir.dateTime] = Field(
        description="The date/time validation was last completed (including failed validations)",
        default=None,
    )
    nextScheduled: Optional[fhir.date_] = Field(
        description="The date when target is next validated, if appropriate",
        default=None,
    )
    failureAction: Optional[CodeableConcept] = Field(
        description="fatal | warn | rec-only | none",
        default=None,
    )
    primarySource: Optional[ListType[VerificationResultPrimarySource]] = Field(
        description="Information about the primary source(s) involved in validation",
        default=None,
    )
    attestation: Optional[VerificationResultAttestation] = Field(
        description="Information about the entity attesting to information",
        default=None,
    )
    validator: Optional[ListType[VerificationResultValidator]] = Field(
        description="Information about the entity validating information",
        default=None,
    )
