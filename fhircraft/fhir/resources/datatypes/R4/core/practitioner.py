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
    HumanName,
    Reference,
    ContactPoint,
    Address,
    Attachment,
    BackboneElement,
    CodeableConcept,
    Period,
)
from .resource import Resource
from .domain_resource import DomainResource

class PractitionerQualification(BackboneElement):
    """
    The official certifications, training, and licenses that authorize or otherwise pertain to the provision of care by the practitioner.  For example, a medical license issued by a medical board authorizing the practitioner to practice medicine within a certian locality.
    """

    identifier: Optional[ListType[Identifier]] = Field(
        description="An identifier for this qualification for the practitioner",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="Coded representation of the qualification",
        default=None,
    )
    period: Optional[Period] = Field(
        description="Period during which the qualification is valid",
        default=None,
    )
    issuer: Optional[Reference] = Field(
        description="Organization that regulates and issues the qualification",
        default=None,
    )

class Practitioner(DomainResource):
    """
    A person who is directly or indirectly involved in the provisioning of healthcare.
    """

    _abstract = False
    _type = "Practitioner"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Practitioner"

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
        description="An identifier for the person as this agent",
        default=None,
    )
    active: Optional[Boolean] = Field(
        description="Whether this practitioner\u0027s record is in active use",
        default=None,
    )
    name: Optional[ListType[HumanName]] = Field(
        description="The name(s) associated with the practitioner",
        default=None,
    )
    telecom: Optional[ListType[ContactPoint]] = Field(
        description="A contact detail for the practitioner (that apply to all roles)",
        default=None,
    )
    address: Optional[ListType[Address]] = Field(
        description="Address(es) of the practitioner that are not role specific (typically home address)",
        default=None,
    )
    gender: Optional[Code] = Field(
        description="male | female | other | unknown",
        default=None,
    )
    birthDate: Optional[Date] = Field(
        description="The date  on which the practitioner was born",
        default=None,
    )
    photo: Optional[ListType[Attachment]] = Field(
        description="Image of the person",
        default=None,
    )
    qualification: Optional[ListType[PractitionerQualification]] = Field(
        description="Certification, licenses, or training pertaining to the provision of care",
        default=None,
    )
    communication: Optional[ListType[CodeableConcept]] = Field(
        description="A language the practitioner can use in patient communication",
        default=None,
    )
