import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)


import fhircraft.fhir.resources.datatypes.R4.primitive as fhir
from fhircraft.fhir.resources.datatypes.R4.complex import (
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
    Reference,
)
from .resource import Resource
from .domain_resource import DomainResource

class PersonLink(BackboneElement):
    """
    Link to a resource that concerns the same actual person.
    """

    target: Optional[Reference] = Field(
        description="The resource to which this actual person is associated",
        default=None,
    )
    assurance: Optional[fhir.code] = Field(
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
    name: Optional[ListType[HumanName]] = Field(
        description="A name associated with the person",
        default=None,
    )
    telecom: Optional[ListType[ContactPoint]] = Field(
        description="A contact detail for the person",
        default=None,
    )
    gender: Optional[fhir.code] = Field(
        description="male | female | other | unknown",
        default=None,
    )
    birthDate: Optional[fhir.date_] = Field(
        description="The date on which the person was born",
        default=None,
    )
    address: Optional[ListType[Address]] = Field(
        description="One or more addresses for the person",
        default=None,
    )
    photo: Optional[Attachment] = Field(
        description="Image of the person",
        default=None,
    )
    managingOrganization: Optional[Reference] = Field(
        description="The organization that is the custodian of the person record",
        default=None,
    )
    active: Optional[fhir.boolean] = Field(
        description="This person\u0027s record is in active use",
        default=None,
    )
    link: Optional[ListType[PersonLink]] = Field(
        description="Link to a resource that concerns the same actual person",
        default=None,
    )
