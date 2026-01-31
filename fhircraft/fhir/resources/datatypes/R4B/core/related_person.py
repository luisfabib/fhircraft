import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    Boolean,
    Date,
)

from fhircraft.fhir.resources.datatypes.R4B.complex import (
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
    A language which may be used to communicate with about the patient's health.
    """

    language: Optional[CodeableConcept] = Field(
        description="The language which can be used to communicate with the patient about his or her health",
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
    Information about a person that is involved in the care for a patient, but who is not the target of healthcare, nor has a formal responsibility in the care process.
    """

    _abstract = False
    _type = "RelatedPerson"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/RelatedPerson"

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
    relationship: Optional[ListType[CodeableConcept]] = Field(
        description="The nature of the relationship",
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
        description="A language which may be used to communicate with about the patient\u0027s health",
        default=None,
    )
