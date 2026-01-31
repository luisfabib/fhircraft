import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    DateTime,
    Decimal,
    Integer,
)

from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Reference,
    BackboneElement,
    CodeableConcept,
    Annotation,
    Quantity,
)
from .resource import Resource
from .domain_resource import DomainResource


class VisionPrescriptionLensSpecificationPrism(BackboneElement):
    """
    Allows for adjustment on two axis.
    """

    amount: Optional[Decimal] = Field(
        description="Amount of adjustment",
        default=None,
    )
    amount_ext: Optional[Element] = Field(
        description="Placeholder element for amount extensions",
        default=None,
        alias="_amount",
    )
    base: Optional[Code] = Field(
        description="up | down | in | out",
        default=None,
    )
    base_ext: Optional[Element] = Field(
        description="Placeholder element for base extensions",
        default=None,
        alias="_base",
    )


class VisionPrescriptionLensSpecification(BackboneElement):
    """
    Contain the details of  the individual lens specifications and serves as the authorization for the fullfillment by certified professionals.
    """

    product: Optional[CodeableConcept] = Field(
        description="Product to be supplied",
        default=None,
    )
    eye: Optional[Code] = Field(
        description="right | left",
        default=None,
    )
    eye_ext: Optional[Element] = Field(
        description="Placeholder element for eye extensions",
        default=None,
        alias="_eye",
    )
    sphere: Optional[Decimal] = Field(
        description="Power of the lens",
        default=None,
    )
    sphere_ext: Optional[Element] = Field(
        description="Placeholder element for sphere extensions",
        default=None,
        alias="_sphere",
    )
    cylinder: Optional[Decimal] = Field(
        description="Lens power for astigmatism",
        default=None,
    )
    cylinder_ext: Optional[Element] = Field(
        description="Placeholder element for cylinder extensions",
        default=None,
        alias="_cylinder",
    )
    axis: Optional[Integer] = Field(
        description="Lens meridian which contain no power for astigmatism",
        default=None,
    )
    axis_ext: Optional[Element] = Field(
        description="Placeholder element for axis extensions",
        default=None,
        alias="_axis",
    )
    prism: Optional[ListType[VisionPrescriptionLensSpecificationPrism]] = Field(
        description="Eye alignment compensation",
        default=None,
    )
    add: Optional[Decimal] = Field(
        description="Added power for multifocal levels",
        default=None,
    )
    add_ext: Optional[Element] = Field(
        description="Placeholder element for add extensions",
        default=None,
        alias="_add",
    )
    power: Optional[Decimal] = Field(
        description="Contact lens power",
        default=None,
    )
    power_ext: Optional[Element] = Field(
        description="Placeholder element for power extensions",
        default=None,
        alias="_power",
    )
    backCurve: Optional[Decimal] = Field(
        description="Contact lens back curvature",
        default=None,
    )
    backCurve_ext: Optional[Element] = Field(
        description="Placeholder element for backCurve extensions",
        default=None,
        alias="_backCurve",
    )
    diameter: Optional[Decimal] = Field(
        description="Contact lens diameter",
        default=None,
    )
    diameter_ext: Optional[Element] = Field(
        description="Placeholder element for diameter extensions",
        default=None,
        alias="_diameter",
    )
    duration: Optional[Quantity] = Field(
        description="Lens wear duration",
        default=None,
    )
    color: Optional[String] = Field(
        description="Color required",
        default=None,
    )
    color_ext: Optional[Element] = Field(
        description="Placeholder element for color extensions",
        default=None,
        alias="_color",
    )
    brand: Optional[String] = Field(
        description="Brand required",
        default=None,
    )
    brand_ext: Optional[Element] = Field(
        description="Placeholder element for brand extensions",
        default=None,
        alias="_brand",
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Notes for coatings",
        default=None,
    )


class VisionPrescription(DomainResource):
    """
    An authorization for the provision of glasses and/or contact lenses to a patient.
    """

    _abstract = False
    _type = "VisionPrescription"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/VisionPrescription"

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
        description="Business Identifier for vision prescription",
        default=None,
    )
    status: Optional[Code] = Field(
        description="active | cancelled | draft | entered-in-error",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    created: Optional[DateTime] = Field(
        description="Response creation date",
        default=None,
    )
    created_ext: Optional[Element] = Field(
        description="Placeholder element for created extensions",
        default=None,
        alias="_created",
    )
    patient: Optional[Reference] = Field(
        description="Who prescription is for",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="Created during encounter / admission / stay",
        default=None,
    )
    dateWritten: Optional[DateTime] = Field(
        description="When prescription was authorized",
        default=None,
    )
    dateWritten_ext: Optional[Element] = Field(
        description="Placeholder element for dateWritten extensions",
        default=None,
        alias="_dateWritten",
    )
    prescriber: Optional[Reference] = Field(
        description="Who authorized the vision prescription",
        default=None,
    )
    lensSpecification: Optional[ListType[VisionPrescriptionLensSpecification]] = Field(
        description="Vision lens authorization",
        default=None,
    )
