import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import String, Uri, Code

from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Reference,
    CodeableConcept,
    BackboneElement,
)
from .resource import Resource
from .domain_resource import DomainResource


class MedicinalProductInteractionInteractant(BackboneElement):
    """
    The specific medication, food or laboratory test that interacts.
    """

    itemReference: Optional[Reference] = Field(
        description="The specific medication, food or laboratory test that interacts",
        default=None,
    )
    itemCodeableConcept: Optional[CodeableConcept] = Field(
        description="The specific medication, food or laboratory test that interacts",
        default=None,
    )

    @property
    def item(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="item",
        )

    @model_validator(mode="after")
    def item_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Reference, CodeableConcept],
            field_name_base="item",
            required=True,
        )


class MedicinalProductInteraction(DomainResource):
    """
    The interactions of the medicinal product with other medicinal products, or other forms of interactions.
    """

    _abstract = False
    _type = "MedicinalProductInteraction"
    _canonical_url = (
        "http://hl7.org/fhir/StructureDefinition/MedicinalProductInteraction"
    )

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
            profile=[
                "http://hl7.org/fhir/StructureDefinition/MedicinalProductInteraction"
            ]
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
    subject: Optional[ListType[Reference]] = Field(
        description="The medication for which this is a described interaction",
        default=None,
    )
    description: Optional[String] = Field(
        description="The interaction described",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    interactant: Optional[ListType[MedicinalProductInteractionInteractant]] = Field(
        description="The specific medication, food or laboratory test that interacts",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="The type of the interaction e.g. drug-drug interaction, drug-food interaction, drug-lab test interaction",
        default=None,
    )
    effect: Optional[CodeableConcept] = Field(
        description='The effect of the interaction, for example "reduced gastric absorption of primary medication"',
        default=None,
    )
    incidence: Optional[CodeableConcept] = Field(
        description="The incidence of the interaction, e.g. theoretical, observed",
        default=None,
    )
    management: Optional[CodeableConcept] = Field(
        description="Actions for managing the interaction",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "management",
                "incidence",
                "effect",
                "type",
                "interactant",
                "description",
                "subject",
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
