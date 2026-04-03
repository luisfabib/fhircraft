import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)


from ..primitive import *
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
