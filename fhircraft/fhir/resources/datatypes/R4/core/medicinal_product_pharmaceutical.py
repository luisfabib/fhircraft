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
    Identifier,
    CodeableConcept,
    Reference,
    BackboneElement,
    Quantity,
    Duration,
    Ratio,
)
from .resource import Resource
from .domain_resource import DomainResource

class MedicinalProductPharmaceuticalCharacteristics(BackboneElement):
    """
    Characteristics e.g. a products onset of action.
    """

    code: Optional[CodeableConcept] = Field(
        description="A coded characteristic",
        default=None,
    )
    status: Optional[CodeableConcept] = Field(
        description="The status of characteristic e.g. assigned or pending",
        default=None,
    )

class MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpeciesWithdrawalPeriod(
    BackboneElement
):
    """
    A species specific time during which consumption of animal product is not appropriate.
    """

    tissue: Optional[CodeableConcept] = Field(
        description="Coded expression for the type of tissue for which the withdrawal period applues, e.g. meat, milk",
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

class MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpecies(BackboneElement):
    """
    A species for which this route applies.
    """

    code: Optional[CodeableConcept] = Field(
        description="Coded expression for the species",
        default=None,
    )
    withdrawalPeriod: Optional[
        ListType[
            MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpeciesWithdrawalPeriod
        ]
    ] = Field(
        description="A species specific time during which consumption of animal product is not appropriate",
        default=None,
    )

class MedicinalProductPharmaceuticalRouteOfAdministration(BackboneElement):
    """
    The path by which the pharmaceutical product is taken into or makes contact with the body.
    """

    code: Optional[CodeableConcept] = Field(
        description="Coded expression for the route",
        default=None,
    )
    firstDose: Optional[Quantity] = Field(
        description="The first dose (dose quantity) administered in humans can be specified, for a product under investigation, using a numerical value and its unit of measurement",
        default=None,
    )
    maxSingleDose: Optional[Quantity] = Field(
        description="The maximum single dose that can be administered as per the protocol of a clinical trial can be specified using a numerical value and its unit of measurement",
        default=None,
    )
    maxDosePerDay: Optional[Quantity] = Field(
        description="The maximum dose per day (maximum dose quantity to be administered in any one 24-h period) that can be administered as per the protocol referenced in the clinical trial authorisation",
        default=None,
    )
    maxDosePerTreatmentPeriod: Optional[Ratio] = Field(
        description="The maximum dose per treatment period that can be administered as per the protocol referenced in the clinical trial authorisation",
        default=None,
    )
    maxTreatmentPeriod: Optional[Duration] = Field(
        description="The maximum treatment period during which an Investigational Medicinal Product can be administered as per the protocol referenced in the clinical trial authorisation",
        default=None,
    )
    targetSpecies: Optional[
        ListType[MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpecies]
    ] = Field(
        description="A species for which this route applies",
        default=None,
    )

class MedicinalProductPharmaceutical(DomainResource):
    """
    A pharmaceutical product described in terms of its composition and dose form.
    """

    _abstract = False
    _type = "MedicinalProductPharmaceutical"
    _canonical_url = (
        "http://hl7.org/fhir/StructureDefinition/MedicinalProductPharmaceutical"
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
        description="An identifier for the pharmaceutical medicinal product",
        default=None,
    )
    administrableDoseForm: Optional[CodeableConcept] = Field(
        description="The administrable dose form, after necessary reconstitution",
        default=None,
    )
    unitOfPresentation: Optional[CodeableConcept] = Field(
        description="Todo",
        default=None,
    )
    ingredient: Optional[ListType[Reference]] = Field(
        description="Ingredient",
        default=None,
    )
    device: Optional[ListType[Reference]] = Field(
        description="Accompanying device",
        default=None,
    )
    characteristics: Optional[
        ListType[MedicinalProductPharmaceuticalCharacteristics]
    ] = Field(
        description="Characteristics e.g. a products onset of action",
        default=None,
    )
    routeOfAdministration: Optional[
        ListType[MedicinalProductPharmaceuticalRouteOfAdministration]
    ] = Field(
        description="The path by which the pharmaceutical product is taken into or makes contact with the body",
        default=None,
    )
