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
    CodeableConcept,
    Attachment,
    BackboneElement,
    Reference,
)
from .resource import Resource
from .domain_resource import DomainResource

class PersonCommunication(BackboneElement):
    """
    A language which may be used to communicate with the person about his or her health.
    """

    language: Optional[CodeableConcept] = Field(
        description="The language which can be used to communicate with the person about his or her health",
        default=None,
    )
    preferred: Optional[Boolean] = Field(
        description="Language preference indicator",
        default=None,
    )

class PersonLink(BackboneElement):
    """
    Link to a resource that concerns the same actual person.
    """

    target: Optional[Reference] = Field(
        description="The resource to which this actual person is associated",
        default=None,
    )
    assurance: Optional[Code] = Field(
        description="level1 | level2 | level3 | level4",
        default=None,
    )

class Person(DomainResource):
    """
    Demographics and administrative information about a person independent of a specific health-related context.
    """

    _abstract = False
    _type = "Person"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Person"

    identifier: Optional[ListType[Identifier]] = Field(
        description="A human identifier for this person",
        default=None,
    )
    active: Optional[Boolean] = Field(
        description="This person\u0027s record is in active use",
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
        description="The date on which the person was born",
        default=None,
    )
    deceasedBoolean: Optional[Boolean] = Field(
        description="Indicates if the individual is deceased or not",
        default=None,
    )
    deceasedDateTime: Optional[DateTime] = Field(
        description="Indicates if the individual is deceased or not",
        default=None,
    )
    address: Optional[ListType[Address]] = Field(
        description="One or more addresses for the person",
        default=None,
    )
    maritalStatus: Optional[CodeableConcept] = Field(
        description="Marital (civil) status of a person",
        default=None,
    )
    photo: Optional[ListType[Attachment]] = Field(
        description="Image of the person",
        default=None,
    )
    communication: Optional[ListType[PersonCommunication]] = Field(
        description="A language which may be used to communicate with the person about his or her health",
        default=None,
    )
    managingOrganization: Optional[Reference] = Field(
        description="The organization that is the custodian of the person record",
        default=None,
    )
    link: Optional[ListType[PersonLink]] = Field(
        description="Link to a resource that concerns the same actual person",
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
