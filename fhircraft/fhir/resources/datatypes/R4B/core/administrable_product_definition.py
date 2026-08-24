import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)


import fhircraft.fhir.resources.datatypes.R4B.primitive as fhir
from fhircraft.fhir.resources.datatypes.R4B.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    BackboneElement,
    Quantity,
    Attachment,
    Ratio,
    Duration,
)
from .resource import Resource
from .domain_resource import DomainResource


class AdministrableProductDefinitionProperty(BackboneElement):
    """
    Characteristics e.g. a product's onset of action.
    """

    type: CodeableConcept = Field(
        description="A code expressing the type of characteristic",
    )
    valueCodeableConcept: Optional[CodeableConcept] = Field(
        description="A value for the characteristic",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="A value for the characteristic",
        default=None,
    )
    valueDate: Optional[fhir.date_] = Field(
        description="A value for the characteristic",
        default=None,
    )
    valueBoolean: Optional[fhir.boolean] = Field(
        description="A value for the characteristic",
        default=None,
    )
    valueAttachment: Optional[Attachment] = Field(
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
                fhir.Date,
                fhir.Boolean,
                Attachment,
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

    tissue: CodeableConcept = Field(
        description="The type of tissue for which the withdrawal period applies, e.g. meat, milk",
    )
    value: Quantity = Field(
        description="A value for the time",
    )
    supportingInformation: Optional[fhir.string] = Field(
        description="Extra information about the withdrawal period",
        default=None,
    )


class AdministrableProductDefinitionRouteOfAdministrationTargetSpecies(BackboneElement):
    """
    A species for which this route applies.
    """

    code: CodeableConcept = Field(
        description="Coded expression for the species",
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

    code: CodeableConcept = Field(
        description="Coded expression for the route",
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
        description="An identifier for the administrable product",
        default=None,
    )
    status: fhir.code = Field(
        description="draft | active | retired | unknown",
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
            expression="(AdministrableProductDefinition.routeOfAdministration.code.count() + AdministrableProductDefinition.formOf.resolve().route.count())  < 2",
            human="RouteOfAdministration cannot be used when the 'formOf' product already uses MedicinalProductDefinition.route (and vice versa)",
            key="apd-1",
            severity="error",
        )
