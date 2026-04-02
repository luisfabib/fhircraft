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
    CodeableConcept,
    HumanName,
    ContactPoint,
    Address,
    Attachment,
    Period,
    BackboneElement,
)
from .resource import Resource
from .domain_resource import DomainResource

class RelatedPersonCommunication(BackboneElement):
    """
    A language which may be used to communicate with the related person about the patient's health.
    """

    language: Optional[CodeableConcept] = Field(
        description="The language which can be used to communicate with the related person about the patient\u0027s health",
        default=None,
    )
    preferred: Optional[Boolean] = Field(
        description="Language preference indicator",
        default=None,
    )

class RelatedPerson(DomainResource):
    """
    Information about a person that is involved in a patient's health or the care for a patient, but who is not the target of healthcare, nor has a formal responsibility in the care process.
    """

    _abstract = False
    _type = "RelatedPerson"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/RelatedPerson"

    identifier: Optional[ListType[Identifier]] = Field(
        description="A human identifier for this person",
        default=None,
    )
    active: Optional[Boolean] = Field(
        description="Whether this related person\u0027s record is in active use",
        default=None,
    )
    patient: Optional[Reference] = Field(
        description="The patient this person is related to",
        default=None,
    )
    relationship: Optional[ListType[CodeableConcept]] = Field(
        description="The relationship of the related person to the patient",
        default=None,
    )
    name: Optional[ListType[HumanName]] = Field(
        description="A name associated with the person",
        default=None,
    )
    telecom: Optional[ListType[ContactPoint]] = Field(
        description="A contact detail for the person",
        default=None,
    )
    gender: Optional[Code] = Field(
        description="male | female | other | unknown",
        default=None,
    )
    birthDate: Optional[Date] = Field(
        description="The date on which the related person was born",
        default=None,
    )
    address: Optional[ListType[Address]] = Field(
        description="Address where the related person can be contacted or visited",
        default=None,
    )
    photo: Optional[ListType[Attachment]] = Field(
        description="Image of the person",
        default=None,
    )
    period: Optional[Period] = Field(
        description="Period of time that this relationship is considered valid",
        default=None,
    )
    communication: Optional[ListType[RelatedPersonCommunication]] = Field(
        description="A language which may be used to communicate with the related person about the patient\u0027s health",
        default=None,
    )
