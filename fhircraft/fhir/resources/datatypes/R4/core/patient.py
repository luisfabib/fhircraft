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
    DateTime,
    Integer,
)

from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    HumanName,
    ContactPoint,
    Address,
    CodeableConcept,
    Period,
    Attachment,
    BackboneElement,
    Reference,
)
from .resource import Resource
from .domain_resource import DomainResource


class PatientContact(BackboneElement):
    """
    A contact party (e.g. guardian, partner, friend) for the patient.
    """

    relationship: Optional[ListType[CodeableConcept]] = Field(
        description="The kind of relationship",
        default=None,
    )
    name: Optional[HumanName] = Field(
        description="A name associated with the contact person",
        default=None,
    )
    telecom: Optional[ListType[ContactPoint]] = Field(
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

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "period",
                "organization",
                "gender",
                "address",
                "telecom",
                "name",
                "relationship",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
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

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "preferred",
                "language",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class PatientLink(BackboneElement):
    """
    Link to another patient resource that concerns the same actual patient.
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

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "type",
                "other",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class Patient(DomainResource):
    """
    Demographics and other administrative information about an individual or animal receiving care or other health-related services.
    """

    _abstract = False
    _type = "Patient"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Patient"

    id: Optional[String] = Field(
        description="Logical id of this artifact",
        default=None,
    )
    id_ext: Optional[Element] = Field(
        description="Placeholder element for id extensions",
        default=None,
        alias="_id",
    )
    meta: Optional[Meta] = Field(
        description="Metadata about the resource.",
        default_factory=lambda: Meta(
            profile=["http://hl7.org/fhir/StructureDefinition/Patient"]
        ),
    )
    implicitRules: Optional[Uri] = Field(
        description="A set of rules under which this content was created",
        default=None,
    )
    implicitRules_ext: Optional[Element] = Field(
        description="Placeholder element for implicitRules extensions",
        default=None,
        alias="_implicitRules",
    )
    language: Optional[Code] = Field(
        description="Language of the resource content",
        default=None,
    )
    language_ext: Optional[Element] = Field(
        description="Placeholder element for language extensions",
        default=None,
        alias="_language",
    )
    text: Optional[Narrative] = Field(
        description="Text summary of the resource, for human interpretation",
        default=None,
    )
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
    name: Optional[ListType[HumanName]] = Field(
        description="A name associated with the patient",
        default=None,
    )
    telecom: Optional[ListType[ContactPoint]] = Field(
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
    address: Optional[ListType[Address]] = Field(
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
    photo: Optional[ListType[Attachment]] = Field(
        description="Image of the patient",
        default=None,
    )
    contact: Optional[ListType[PatientContact]] = Field(
        description="A contact party (e.g. guardian, partner, friend) for the patient",
        default=None,
    )
    communication: Optional[ListType[PatientCommunication]] = Field(
        description="A language which may be used to communicate with the patient about his or her health",
        default=None,
    )
    generalPractitioner: Optional[ListType[Reference]] = Field(
        description="Patient\u0027s nominated primary care provider",
        default=None,
    )
    managingOrganization: Optional[Reference] = Field(
        description="Organization that is the custodian of the patient record",
        default=None,
    )
    link: Optional[ListType[PatientLink]] = Field(
        description="Link to another patient resource that concerns the same actual person",
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
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "link",
                "managingOrganization",
                "generalPractitioner",
                "communication",
                "contact",
                "photo",
                "maritalStatus",
                "address",
                "birthDate",
                "gender",
                "telecom",
                "name",
                "active",
                "identifier",
                "modifierExtension",
                "extension",
                "text",
                "language",
                "implicitRules",
                "meta",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ext_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "modifierExtension",
                "extension",
            ),
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
            severity="error",
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

    @model_validator(mode="after")
    def FHIR_dom_2_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="contained.contained.empty()",
            human="If the resource is contained in another resource, it SHALL NOT contain nested Resources",
            key="dom-2",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_dom_3_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="contained.where((('#'+id in (%resource.descendants().reference | %resource.descendants().ofType(canonical) | %resource.descendants().ofType(uri) | %resource.descendants().ofType(url))) or descendants().where(reference = '#').exists() or descendants().where(as(canonical) = '#').exists() or descendants().where(as(canonical) = '#').exists()).not()).trace('unmatched', id).empty()",
            human="If the resource is contained in another resource, it SHALL be referred to from elsewhere in the resource or SHALL refer to the containing resource",
            key="dom-3",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_dom_4_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="contained.meta.versionId.empty() and contained.meta.lastUpdated.empty()",
            human="If a resource is contained in another resource, it SHALL NOT have a meta.versionId or a meta.lastUpdated",
            key="dom-4",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_dom_5_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="contained.meta.security.empty()",
            human="If a resource is contained in another resource, it SHALL NOT have a security label",
            key="dom-5",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_dom_6_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="text.`div`.exists()",
            human="A resource should have narrative for robust management",
            key="dom-6",
            severity="warning",
        )
