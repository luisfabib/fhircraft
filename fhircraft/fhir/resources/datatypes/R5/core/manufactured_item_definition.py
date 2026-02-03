from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    Date,
    Boolean,
    Markdown,
)

from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    MarketingStatus,
    BackboneElement,
    Quantity,
    Attachment,
    CodeableReference,
)
from .resource import Resource
from .domain_resource import DomainResource


class ManufacturedItemDefinitionProperty(BackboneElement):
    """
    General characteristics of this item.
    """

    type: Optional[CodeableConcept] = Field(
        description="A code expressing the type of characteristic",
        default=None,
    )
    valueCodeableConcept: Optional[CodeableConcept] = Field(
        description="A value for the characteristic",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="A value for the characteristic",
        default=None,
    )
    valueDate: Optional[Date] = Field(
        description="A value for the characteristic",
        default=None,
    )
    valueDate_ext: Optional[Element] = Field(
        description="Placeholder element for valueDate extensions",
        default=None,
        alias="_valueDate",
    )
    valueBoolean: Optional[Boolean] = Field(
        description="A value for the characteristic",
        default=None,
    )
    valueBoolean_ext: Optional[Element] = Field(
        description="Placeholder element for valueBoolean extensions",
        default=None,
        alias="_valueBoolean",
    )
    valueMarkdown: Optional[Markdown] = Field(
        description="A value for the characteristic",
        default=None,
    )
    valueMarkdown_ext: Optional[Element] = Field(
        description="Placeholder element for valueMarkdown extensions",
        default=None,
        alias="_valueMarkdown",
    )
    valueAttachment: Optional[Attachment] = Field(
        description="A value for the characteristic",
        default=None,
    )
    valueReference: Optional[Reference] = Field(
        description="A value for the characteristic",
        default=None,
    )

    @property
    def value(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="value",
        )

    @model_validator(mode="after")
    def value_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[
                CodeableConcept,
                Quantity,
                Date,
                Boolean,
                Markdown,
                Attachment,
                Reference,
            ],
            field_name_base="value",
            required=False,
        )


class ManufacturedItemDefinitionComponentConstituent(BackboneElement):
    """
    A reference to a constituent of the manufactured item as a whole, linked here so that its component location within the item can be indicated. This not where the item's ingredient are primarily stated (for which see Ingredient.for or ManufacturedItemDefinition.ingredient).
    """

    amount: Optional[ListType[Quantity]] = Field(
        description="The measurable amount of the substance, expressable in different ways (e.g. by mass or volume)",
        default=None,
    )
    location: Optional[ListType[CodeableConcept]] = Field(
        description="The physical location of the constituent/ingredient within the component",
        default=None,
    )
    function: Optional[ListType[CodeableConcept]] = Field(
        description="The function of this constituent within the component e.g. binder",
        default=None,
    )
    hasIngredient: Optional[ListType[CodeableReference]] = Field(
        description="The ingredient that is the constituent of the given component",
        default=None,
    )


class ManufacturedItemDefinitionComponentProperty(BackboneElement):
    """
    General characteristics of this component.
    """

    type: Optional[CodeableConcept] = Field(
        description="A code expressing the type of characteristic",
        default=None,
    )
    valueCodeableConcept: Optional[CodeableConcept] = Field(
        description="A value for the characteristic",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="A value for the characteristic",
        default=None,
    )
    valueDate: Optional[Date] = Field(
        description="A value for the characteristic",
        default=None,
    )
    valueDate_ext: Optional[Element] = Field(
        description="Placeholder element for valueDate extensions",
        default=None,
        alias="_valueDate",
    )
    valueBoolean: Optional[Boolean] = Field(
        description="A value for the characteristic",
        default=None,
    )
    valueBoolean_ext: Optional[Element] = Field(
        description="Placeholder element for valueBoolean extensions",
        default=None,
        alias="_valueBoolean",
    )
    valueMarkdown: Optional[Markdown] = Field(
        description="A value for the characteristic",
        default=None,
    )
    valueMarkdown_ext: Optional[Element] = Field(
        description="Placeholder element for valueMarkdown extensions",
        default=None,
        alias="_valueMarkdown",
    )
    valueAttachment: Optional[Attachment] = Field(
        description="A value for the characteristic",
        default=None,
    )
    valueReference: Optional[Reference] = Field(
        description="A value for the characteristic",
        default=None,
    )

    @property
    def value(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="value",
        )

    @model_validator(mode="after")
    def value_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[
                CodeableConcept,
                Quantity,
                Date,
                Boolean,
                Markdown,
                Attachment,
                Reference,
            ],
            field_name_base="value",
            required=False,
        )


class ManufacturedItemDefinitionComponent(BackboneElement):
    """
    Physical parts of the manufactured item, that it is intrisically made from. This is distinct from the ingredients that are part of its chemical makeup.
    """

    type: Optional[CodeableConcept] = Field(
        description="Defining type of the component e.g. shell, layer, ink",
        default=None,
    )
    function: Optional[ListType[CodeableConcept]] = Field(
        description="The function of this component within the item e.g. delivers active ingredient, masks taste",
        default=None,
    )
    amount: Optional[ListType[Quantity]] = Field(
        description="The measurable amount of total quantity of all substances in the component, expressable in different ways (e.g. by mass or volume)",
        default=None,
    )
    constituent: Optional[ListType[ManufacturedItemDefinitionComponentConstituent]] = (
        Field(
            description="A reference to a constituent of the manufactured item as a whole, linked here so that its component location within the item can be indicated. This not where the item\u0027s ingredient are primarily stated (for which see Ingredient.for or ManufacturedItemDefinition.ingredient)",
            default=None,
        )
    )
    property_: Optional[ListType[ManufacturedItemDefinitionComponentProperty]] = Field(
        description="General characteristics of this component",
        default=None,
        alias="property",
    )
    component: Optional[ListType["ManufacturedItemDefinitionComponent"]] = Field(
        description="A component that this component contains or is made from",
        default=None,
    )


class ManufacturedItemDefinition(DomainResource):
    """
    The definition and characteristics of a medicinal manufactured item, such as a tablet or capsule, as contained in a packaged medicinal product.
    """

    _abstract = False
    _type = "ManufacturedItemDefinition"
    _canonical_url = (
        "http://hl7.org/fhir/StructureDefinition/ManufacturedItemDefinition"
    )

    identifier: Optional[ListType[Identifier]] = Field(
        description="Unique identifier",
        default=None,
    )
    status: Optional[Code] = Field(
        description="draft | active | retired | unknown",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    name: Optional[String] = Field(
        description="A descriptive name applied to this item",
        default=None,
    )
    name_ext: Optional[Element] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    manufacturedDoseForm: Optional[CodeableConcept] = Field(
        description="Dose form as manufactured (before any necessary transformation)",
        default=None,
    )
    unitOfPresentation: Optional[CodeableConcept] = Field(
        description="The \u201creal-world\u201d units in which the quantity of the item is described",
        default=None,
    )
    manufacturer: Optional[ListType[Reference]] = Field(
        description="Manufacturer of the item, one of several possible",
        default=None,
    )
    marketingStatus: Optional[ListType[MarketingStatus]] = Field(
        description="Allows specifying that an item is on the market for sale, or that it is not available, and the dates and locations associated",
        default=None,
    )
    ingredient: Optional[ListType[CodeableConcept]] = Field(
        description="The ingredients of this manufactured item. Only needed if these are not specified by incoming references from the Ingredient resource",
        default=None,
    )
    property_: Optional[ListType[ManufacturedItemDefinitionProperty]] = Field(
        description="General characteristics of this item",
        default=None,
        alias="property",
    )
    component: Optional[ListType[ManufacturedItemDefinitionComponent]] = Field(
        description="Physical parts of the manufactured item, that it is intrisically made from. This is distinct from the ingredients that are part of its chemical makeup",
        default=None,
    )
