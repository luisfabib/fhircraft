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
    DateTime,
    Integer,
)

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
    Period,
)
from .resource import Resource
from .domain_resource import DomainResource


class PatientContact(BackboneElement):
    """
    A contact party (e.g. guardian, partner, friend) for the patient.
    """

    relationship: Optional[List[CodeableConcept]] = Field(
        description="The kind of relationship",
        default=None,
    )
    name: Optional[HumanName] = Field(
        description="A name associated with the contact person",
        default=None,
    )
    telecom: Optional[List[ContactPoint]] = Field(
        description="A contact detail for the person",
        default=None,
    )
    address: Optional[Address] = Field(
        description="Address for the contact person",
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
    organization: Optional[Reference] = Field(
        description="Organization that is associated with the contact",
        default=None,
    )
    period: Optional[Period] = Field(
        description="The period during which this contact person or organization is valid to be contacted relating to this patient",
        default=None,
    )


class PatientCommunication(BackboneElement):
    """
    A language which may be used to communicate with the patient about his or her health.
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


class PatientLink(BackboneElement):
    """
    Link to a Patient or RelatedPerson resource that concerns the same actual individual.
    """

    other: Optional[Reference] = Field(
        description="The other patient or related person resource that the link refers to",
        default=None,
    )
    type: Optional[Code] = Field(
        description="replaced-by | replaces | refer | seealso",
        default=None,
    )
    type_ext: Optional[Element] = Field(
        description="Placeholder element for type extensions",
        default=None,
        alias="_type",
    )


class Patient(DomainResource):
    """
    Demographics and other administrative information about an individual or animal receiving care or other health-related services.
    """

    _abstract = False
    _type = "Patient"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Patient"

    identifier: Optional[List[Identifier]] = Field(
        description="An identifier for this patient",
        default=None,
    )
    active: Optional[Boolean] = Field(
        description="Whether this patient\u0027s record is in active use",
        default=None,
    )
    active_ext: Optional[Element] = Field(
        description="Placeholder element for active extensions",
        default=None,
        alias="_active",
    )
    name: Optional[List[HumanName]] = Field(
        description="A name associated with the patient",
        default=None,
    )
    telecom: Optional[List[ContactPoint]] = Field(
        description="A contact detail for the individual",
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
        description="The date of birth for the individual",
        default=None,
    )
    birthDate_ext: Optional[Element] = Field(
        description="Placeholder element for birthDate extensions",
        default=None,
        alias="_birthDate",
    )
    deceasedBoolean: Optional[Boolean] = Field(
        description="Indicates if the individual is deceased or not",
        default=None,
    )
    deceasedBoolean_ext: Optional[Element] = Field(
        description="Placeholder element for deceasedBoolean extensions",
        default=None,
        alias="_deceasedBoolean",
    )
    deceasedDateTime: Optional[DateTime] = Field(
        description="Indicates if the individual is deceased or not",
        default=None,
    )
    deceasedDateTime_ext: Optional[Element] = Field(
        description="Placeholder element for deceasedDateTime extensions",
        default=None,
        alias="_deceasedDateTime",
    )
    address: Optional[List[Address]] = Field(
        description="An address for the individual",
        default=None,
    )
    maritalStatus: Optional[CodeableConcept] = Field(
        description="Marital (civil) status of a patient",
        default=None,
    )
    multipleBirthBoolean: Optional[Boolean] = Field(
        description="Whether patient is part of a multiple birth",
        default=None,
    )
    multipleBirthBoolean_ext: Optional[Element] = Field(
        description="Placeholder element for multipleBirthBoolean extensions",
        default=None,
        alias="_multipleBirthBoolean",
    )
    multipleBirthInteger: Optional[Integer] = Field(
        description="Whether patient is part of a multiple birth",
        default=None,
    )
    multipleBirthInteger_ext: Optional[Element] = Field(
        description="Placeholder element for multipleBirthInteger extensions",
        default=None,
        alias="_multipleBirthInteger",
    )
    photo: Optional[List[Attachment]] = Field(
        description="Image of the patient",
        default=None,
    )
    contact: Optional[List[PatientContact]] = Field(
        description="A contact party (e.g. guardian, partner, friend) for the patient",
        default=None,
    )
    communication: Optional[List[PatientCommunication]] = Field(
        description="A language which may be used to communicate with the patient about his or her health",
        default=None,
    )
    generalPractitioner: Optional[List[Reference]] = Field(
        description="Patient\u0027s nominated primary care provider",
        default=None,
    )
    managingOrganization: Optional[Reference] = Field(
        description="Organization that is the custodian of the patient record",
        default=None,
    )
    link: Optional[List[PatientLink]] = Field(
        description="Link to a Patient or RelatedPerson resource that concerns the same actual individual",
        default=None,
    )

    @property
    def deceased(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="deceased",
        )

    @property
    def multipleBirth(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="multipleBirth",
        )

    @model_validator(mode="after")
    def FHIR_pat_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("contact",),
            expression="name.exists() or telecom.exists() or address.exists() or organization.exists()",
            human="SHALL at least contain a contact's details or a reference to an organization",
            key="pat-1",
            severity="error",
        )

    @model_validator(mode="after")
    def deceased_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Boolean, DateTime],
            field_name_base="deceased",
            required=False,
        )

    @model_validator(mode="after")
    def multipleBirth_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Boolean, Integer],
            field_name_base="multipleBirth",
            required=False,
        )
