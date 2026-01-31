from pydantic import Field, model_validator
from typing import Optional, List

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    Boolean,
    Date,
)

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
    preferred_ext: Optional[Element] = Field(
        description="Placeholder element for preferred extensions",
        default=None,
        alias="_preferred",
    )


class RelatedPerson(DomainResource):
    """
    Information about a person that is involved in a patient's health or the care for a patient, but who is not the target of healthcare, nor has a formal responsibility in the care process.
    """

    _abstract = False
    _type = "RelatedPerson"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/RelatedPerson"

    identifier: Optional[List[Identifier]] = Field(
        description="A human identifier for this person",
        default=None,
    )
    active: Optional[Boolean] = Field(
        description="Whether this related person\u0027s record is in active use",
        default=None,
    )
    active_ext: Optional[Element] = Field(
        description="Placeholder element for active extensions",
        default=None,
        alias="_active",
    )
    patient: Optional[Reference] = Field(
        description="The patient this person is related to",
        default=None,
    )
    relationship: Optional[List[CodeableConcept]] = Field(
        description="The relationship of the related person to the patient",
        default=None,
    )
    name: Optional[List[HumanName]] = Field(
        description="A name associated with the person",
        default=None,
    )
    telecom: Optional[List[ContactPoint]] = Field(
        description="A contact detail for the person",
        default=None,
    )
    gender: Optional[Code] = Field(
        description="male | female | other | unknown",
        default=None,
    )
    gender_ext: Optional[Element] = Field(
        description="Placeholder element for gender extensions",
        default=None,
        alias="_gender",
    )
    birthDate: Optional[Date] = Field(
        description="The date on which the related person was born",
        default=None,
    )
    birthDate_ext: Optional[Element] = Field(
        description="Placeholder element for birthDate extensions",
        default=None,
        alias="_birthDate",
    )
    address: Optional[List[Address]] = Field(
        description="Address where the related person can be contacted or visited",
        default=None,
    )
    photo: Optional[List[Attachment]] = Field(
        description="Image of the person",
        default=None,
    )
    period: Optional[Period] = Field(
        description="Period of time that this relationship is considered valid",
        default=None,
    )
    communication: Optional[List[RelatedPersonCommunication]] = Field(
        description="A language which may be used to communicate with the related person about the patient\u0027s health",
        default=None,
    )
