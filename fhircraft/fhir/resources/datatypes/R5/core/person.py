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
    assurance_ext: Optional[Element] = Field(
        description="Placeholder element for assurance extensions",
        default=None,
        alias="_assurance",
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "assurance",
                "target",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class Person(DomainResource):
    """
    Demographics and administrative information about a person independent of a specific health-related context.
    """

    _abstract = False
    _type = "Person"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Person"

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
            profile=["http://hl7.org/fhir/StructureDefinition/Person"]
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
    contained: Optional[List[Resource]] = Field(
        description="Contained, inline Resources",
        default=None,
    )
    extension: Optional[List[Extension]] = Field(
        description="Additional content defined by implementations",
        default=None,
    )
    modifierExtension: Optional[List[Extension]] = Field(
        description="Extensions that cannot be ignored",
        default=None,
    )
    identifier: Optional[List[Identifier]] = Field(
        description="A human identifier for this person",
        default=None,
    )
    active: Optional[Boolean] = Field(
        description="This person\u0027s record is in active use",
        default=None,
    )
    active_ext: Optional[Element] = Field(
        description="Placeholder element for active extensions",
        default=None,
        alias="_active",
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
        description="The date on which the person was born",
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
        description="One or more addresses for the person",
        default=None,
    )
    maritalStatus: Optional[CodeableConcept] = Field(
        description="Marital (civil) status of a person",
        default=None,
    )
    photo: Optional[List[Attachment]] = Field(
        description="Image of the person",
        default=None,
    )
    communication: Optional[List[PersonCommunication]] = Field(
        description="A language which may be used to communicate with the person about his or her health",
        default=None,
    )
    managingOrganization: Optional[Reference] = Field(
        description="The organization that is the custodian of the person record",
        default=None,
    )
    link: Optional[List[PersonLink]] = Field(
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
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "link",
                "managingOrganization",
                "communication",
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
    def deceased_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Boolean, DateTime],
            field_name_base="deceased",
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
            expression="contained.where((('#'+id in (%resource.descendants().reference | %resource.descendants().ofType(canonical) | %resource.descendants().ofType(uri) | %resource.descendants().ofType(url))) or descendants().where(reference = '#').exists() or descendants().where(ofType(canonical) = '#').exists() or descendants().where(ofType(canonical) = '#').exists()).not()).trace('unmatched', id).empty()",
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
