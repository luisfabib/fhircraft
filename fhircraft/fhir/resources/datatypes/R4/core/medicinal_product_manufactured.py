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
    CodeableConcept,
    Quantity,
    ProdCharacteristic,
    Reference,
)
from .resource import Resource
from .domain_resource import DomainResource

class MedicinalProductManufactured(DomainResource):
    """
    The manufactured item as contained in the packaged medicinal product.
    """

    _abstract = False
    _type = "MedicinalProductManufactured"
    _canonical_url = (
        "http://hl7.org/fhir/StructureDefinition/MedicinalProductManufactured"
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
    manufacturedDoseForm: Optional[CodeableConcept] = Field(
        description="Dose form as manufactured and before any transformation into the pharmaceutical product",
        default=None,
    )
    unitOfPresentation: Optional[CodeableConcept] = Field(
        description="The \u201creal world\u201d units in which the quantity of the manufactured item is described",
        default=None,
    )
    quantity: Optional[Quantity] = Field(
        description='The quantity or "count number" of the manufactured item',
        default=None,
    )
    manufacturer: Optional[ListType[Reference]] = Field(
        description='Manufacturer of the item (Note that this should be named "manufacturer" but it currently causes technical issues)',
        default=None,
    )
    ingredient: Optional[ListType[Reference]] = Field(
        description="Ingredient",
        default=None,
    )
    physicalCharacteristics: Optional[ProdCharacteristic] = Field(
        description="Dimensions, color etc.",
        default=None,
    )
    otherCharacteristics: Optional[ListType[CodeableConcept]] = Field(
        description="Other codeable characteristics",
        default=None,
    )
