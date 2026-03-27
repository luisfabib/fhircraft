from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Code,
    Markdown,
    Date,
    Boolean,
)

from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    Meta,
    Identifier,
    Reference,
    CodeableConcept,
    BackboneElement,
    Quantity,
    Attachment,
    Ratio,
    Duration,
)
from .domain_resource import DomainResource


class AdministrableProductDefinitionProperty(BackboneElement):
    """
    Characteristics e.g. a product's onset of action.
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
    status: Optional[CodeableConcept] = Field(
        description="The status of characteristic e.g. assigned or pending",
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


class AdministrableProductDefinitionRouteOfAdministrationTargetSpeciesWithdrawalPeriod(
    BackboneElement
):
    """
    A species specific time during which consumption of animal product is not appropriate.
    """

    tissue: Optional[CodeableConcept] = Field(
        description="The type of tissue for which the withdrawal period applies, e.g. meat, milk",
        default=None,
    )
    value: Optional[Quantity] = Field(
        description="A value for the time",
        default=None,
    )
    supportingInformation: Optional[String] = Field(
        description="Extra information about the withdrawal period",
        default=None,
    )
    supportingInformation_ext: Optional[Element] = Field(
        description="Placeholder element for supportingInformation extensions",
        default=None,
        alias="_supportingInformation",
    )


class AdministrableProductDefinitionRouteOfAdministrationTargetSpecies(BackboneElement):
    """
    A species for which this route applies.
    """

    code: Optional[CodeableConcept] = Field(
        description="Coded expression for the species",
        default=None,
    )
    withdrawalPeriod: Optional[
        ListType[
            AdministrableProductDefinitionRouteOfAdministrationTargetSpeciesWithdrawalPeriod
        ]
    ] = Field(
        description="A species specific time during which consumption of animal product is not appropriate",
        default=None,
    )


class AdministrableProductDefinitionRouteOfAdministration(BackboneElement):
    """
    The path by which the product is taken into or makes contact with the body. In some regions this is referred to as the licenced or approved route. RouteOfAdministration cannot be used when the 'formOf' product already uses MedicinalProductDefinition.route (and vice versa).
    """

    code: Optional[CodeableConcept] = Field(
        description="Coded expression for the route",
        default=None,
    )
    firstDose: Optional[Quantity] = Field(
        description="The first dose (dose quantity) administered can be specified for the product",
        default=None,
    )
    maxSingleDose: Optional[Quantity] = Field(
        description="The maximum single dose that can be administered",
        default=None,
    )
    maxDosePerDay: Optional[Quantity] = Field(
        description="The maximum dose quantity to be administered in any one 24-h period",
        default=None,
    )
    maxDosePerTreatmentPeriod: Optional[Ratio] = Field(
        description="The maximum dose per treatment period that can be administered",
        default=None,
    )
    maxTreatmentPeriod: Optional[Duration] = Field(
        description="The maximum treatment period during which the product can be administered",
        default=None,
    )
    targetSpecies: Optional[
        ListType[AdministrableProductDefinitionRouteOfAdministrationTargetSpecies]
    ] = Field(
        description="A species for which this route applies",
        default=None,
    )


class AdministrableProductDefinition(DomainResource):
    """
    A medicinal product in the final form which is suitable for administering to a patient (after any mixing of multiple components, dissolution etc. has been performed).
    """

    _abstract = False
    _type = "AdministrableProductDefinition"
    _canonical_url = (
        "http://hl7.org/fhir/StructureDefinition/AdministrableProductDefinition"
    )

    identifier: Optional[ListType[Identifier]] = Field(
        description="An identifier for the administrable product",
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
    formOf: Optional[ListType[Reference]] = Field(
        description="References a product from which one or more of the constituent parts of that product can be prepared and used as described by this administrable product",
        default=None,
    )
    administrableDoseForm: Optional[CodeableConcept] = Field(
        description="The dose form of the final product after necessary reconstitution or processing",
        default=None,
    )
    unitOfPresentation: Optional[CodeableConcept] = Field(
        description="The presentation type in which this item is given to a patient. e.g. for a spray - \u0027puff\u0027",
        default=None,
    )
    producedFrom: Optional[ListType[Reference]] = Field(
        description="Indicates the specific manufactured items that are part of the \u0027formOf\u0027 product that are used in the preparation of this specific administrable form",
        default=None,
    )
    ingredient: Optional[ListType[CodeableConcept]] = Field(
        description="The ingredients of this administrable medicinal product. This is only needed if the ingredients are not specified either using ManufacturedItemDefiniton, or using by incoming references from the Ingredient resource",
        default=None,
    )
    device: Optional[Reference] = Field(
        description='A device that is integral to the medicinal product, in effect being considered as an "ingredient" of the medicinal product',
        default=None,
    )
    description: Optional[Markdown] = Field(
        description="A general description of the product, when in its final form, suitable for administration e.g. effervescent blue liquid, to be swallowed",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    property_: Optional[ListType[AdministrableProductDefinitionProperty]] = Field(
        description="Characteristics e.g. a product\u0027s onset of action",
        default=None,
        alias="property",
    )
    routeOfAdministration: Optional[
        ListType[AdministrableProductDefinitionRouteOfAdministration]
    ] = Field(
        description="The path by which the product is taken into or makes contact with the body",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_apd_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="AdministrableProductDefinition.formOf.resolve().route.empty()",
            human="RouteOfAdministration cannot be used when the 'formOf' product already uses MedicinalProductDefinition.route (and vice versa)",
            key="apd-1",
            severity="error",
        )
