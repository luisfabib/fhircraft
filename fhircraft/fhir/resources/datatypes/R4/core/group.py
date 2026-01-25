import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    Boolean,
    UnsignedInt,
)

from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    BackboneElement,
    Quantity,
    Period,
    Range,
)
from .resource import Resource
from .domain_resource import DomainResource


class GroupCharacteristic(BackboneElement):
    """
    Identifies traits whose presence r absence is shared by members of the group.
    """

    code: Optional[CodeableConcept] = Field(
        description="Kind of characteristic",
        default=None,
    )
    valueCodeableConcept: Optional[CodeableConcept] = Field(
        description="Value held by characteristic",
        default=None,
    )
    valueBoolean: Optional[Boolean] = Field(
        description="Value held by characteristic",
        default=None,
    )
    valueBoolean_ext: Optional[Element] = Field(
        description="Placeholder element for valueBoolean extensions",
        default=None,
        alias="_valueBoolean",
    )
    valueQuantity: Optional[Quantity] = Field(
        description="Value held by characteristic",
        default=None,
    )
    valueRange: Optional[Range] = Field(
        description="Value held by characteristic",
        default=None,
    )
    valueReference: Optional[Reference] = Field(
        description="Value held by characteristic",
        default=None,
    )
    exclude: Optional[Boolean] = Field(
        description="Group includes or excludes",
        default=None,
    )
    exclude_ext: Optional[Element] = Field(
        description="Placeholder element for exclude extensions",
        default=None,
        alias="_exclude",
    )
    period: Optional[Period] = Field(
        description="Period over which characteristic is tested",
        default=None,
    )

    @property
    def value(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="value",
        )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "period",
                "exclude",
                "code",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def value_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[CodeableConcept, Boolean, Quantity, Range, Reference],
            field_name_base="value",
            required=True,
        )


class GroupMember(BackboneElement):
    """
    Identifies the resource instances that are members of the group.
    """

    entity: Optional[Reference] = Field(
        description="Reference to the group member",
        default=None,
    )
    period: Optional[Period] = Field(
        description="Period member belonged to the group",
        default=None,
    )
    inactive: Optional[Boolean] = Field(
        description="If member is no longer in group",
        default=None,
    )
    inactive_ext: Optional[Element] = Field(
        description="Placeholder element for inactive extensions",
        default=None,
        alias="_inactive",
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "inactive",
                "period",
                "entity",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )


class Group(DomainResource):
    """
    Represents a defined collection of entities that may be discussed or acted upon collectively but which are not expected to act collectively, and are not formally or legally recognized; i.e. a collection of entities that isn't an Organization.
    """

    _abstract = False
    _type = "Group"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Group"

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
            profile=["http://hl7.org/fhir/StructureDefinition/Group"]
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
        description="Unique id",
        default=None,
    )
    active: Optional[Boolean] = Field(
        description="Whether this group\u0027s record is in active use",
        default=None,
    )
    active_ext: Optional[Element] = Field(
        description="Placeholder element for active extensions",
        default=None,
        alias="_active",
    )
    type: Optional[Code] = Field(
        description="person | animal | practitioner | device | medication | substance",
        default=None,
    )
    type_ext: Optional[Element] = Field(
        description="Placeholder element for type extensions",
        default=None,
        alias="_type",
    )
    actual: Optional[Boolean] = Field(
        description="Descriptive or actual",
        default=None,
    )
    actual_ext: Optional[Element] = Field(
        description="Placeholder element for actual extensions",
        default=None,
        alias="_actual",
    )
    code: Optional[CodeableConcept] = Field(
        description="Kind of Group members",
        default=None,
    )
    name: Optional[String] = Field(
        description="Label for Group",
        default=None,
    )
    name_ext: Optional[Element] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    quantity: Optional[UnsignedInt] = Field(
        description="Number of members",
        default=None,
    )
    quantity_ext: Optional[Element] = Field(
        description="Placeholder element for quantity extensions",
        default=None,
        alias="_quantity",
    )
    managingEntity: Optional[Reference] = Field(
        description="Entity that is the custodian of the Group\u0027s definition",
        default=None,
    )
    characteristic: Optional[ListType[GroupCharacteristic]] = Field(
        description="Include / Exclude group members by Trait",
        default=None,
    )
    member: Optional[ListType[GroupMember]] = Field(
        description="Who or what is in group",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "member",
                "characteristic",
                "managingEntity",
                "quantity",
                "name",
                "code",
                "actual",
                "type",
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

    @model_validator(mode="after")
    def FHIR_grp_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="member.empty() or (actual = true)",
            human='Can only have members if group is "actual"',
            key="grp-1",
            severity="error",
        )
