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
    HumanName,
    ContactPoint,
    Address,
    Attachment,
    BackboneElement,
    CodeableConcept,
    Period,
    Reference,
)
from .resource import Resource
from .domain_resource import DomainResource

class PractitionerQualification(BackboneElement):
    """
        The official qualifications, certifications, accreditations, training, licenses (and other types of educations/skills/capabilities) that authorize or otherwise pertain to the provision of care by the practitioner.

    For example, a medical license issued by a medical board of licensure authorizing the practitioner to practice medicine within a certain locality.
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

class PractitionerCommunication(BackboneElement):
    """
        A language which may be used to communicate with the practitioner, often for correspondence/administrative purposes.

    The `PractitionerRole.communication` property should be used for publishing the languages that a practitioner is able to communicate with patients (on a per Organization/Role basis).
    """

    language: Optional[CodeableConcept] = Field(
        description="The language code used to communicate with the practitioner",
        default=None,
    )
    preferred: Optional[Boolean] = Field(
        description="Language preference indicator",
        default=None,
    )

class Practitioner(DomainResource):
    """
    A person who is directly or indirectly involved in the provisioning of healthcare or related services.
    """

    _abstract = False
    _type = "Practitioner"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Practitioner"

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
    gender: Optional[Code] = Field(
        description="male | female | other | unknown",
        default=None,
    )
    birthDate: Optional[Date] = Field(
        description="The date  on which the practitioner was born",
        default=None,
    )
    deceasedBoolean: Optional[Boolean] = Field(
        description="Indicates if the practitioner is deceased or not",
        default=None,
    )
    deceasedDateTime: Optional[DateTime] = Field(
        description="Indicates if the practitioner is deceased or not",
        default=None,
    )
    address: Optional[ListType[Address]] = Field(
        description="Address(es) of the practitioner that are not role specific (typically home address)",
        default=None,
    )
    photo: Optional[ListType[Attachment]] = Field(
        description="Image of the person",
        default=None,
    )
    qualification: Optional[ListType[PractitionerQualification]] = Field(
        description="Qualifications, certifications, accreditations, licenses, training, etc. pertaining to the provision of care",
        default=None,
    )
    communication: Optional[ListType[PractitionerCommunication]] = Field(
        description="A language which may be used to communicate with the practitioner",
        default=None,
    )

    @property
    def deceased(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="deceased",
        )

    @model_validator(mode="after")
    def deceased_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Boolean, DateTime],
            field_name_base="deceased",
            required=False,
        )
