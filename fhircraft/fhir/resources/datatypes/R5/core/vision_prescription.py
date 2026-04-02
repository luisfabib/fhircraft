from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from ..primitive import *

from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Reference,
    BackboneElement,
    CodeableConcept,
    Quantity,
    Annotation,
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
    base: Optional[Code] = Field(
        description="up | down | in | out",
        default=None,
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
    sphere: Optional[Decimal] = Field(
        description="Power of the lens",
        default=None,
    )
    cylinder: Optional[Decimal] = Field(
        description="Lens power for astigmatism",
        default=None,
    )
    axis: Optional[Integer] = Field(
        description="Lens meridian which contain no power for astigmatism",
        default=None,
    )
    prism: Optional[ListType[VisionPrescriptionLensSpecificationPrism]] = Field(
        description="Eye alignment compensation",
        default=None,
    )
    add: Optional[Decimal] = Field(
        description="Added power for multifocal levels",
        default=None,
    )
    power: Optional[Decimal] = Field(
        description="Contact lens power",
        default=None,
    )
    backCurve: Optional[Decimal] = Field(
        description="Contact lens back curvature",
        default=None,
    )
    diameter: Optional[Decimal] = Field(
        description="Contact lens diameter",
        default=None,
    )
    duration: Optional[Quantity] = Field(
        description="Lens wear duration",
        default=None,
    )
    color: Optional[String] = Field(
        description="Color required",
        default=None,
    )
    brand: Optional[String] = Field(
        description="Brand required",
        default=None,
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

    identifier: Optional[ListType[Identifier]] = Field(
        description="Business Identifier for vision prescription",
        default=None,
    )
    status: Optional[Code] = Field(
        description="active | cancelled | draft | entered-in-error",
        default=None,
    )
    created: Optional[DateTime] = Field(
        description="Response creation date",
        default=None,
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
    prescriber: Optional[Reference] = Field(
        description="Who authorized the vision prescription",
        default=None,
    )
    lensSpecification: Optional[ListType[VisionPrescriptionLensSpecification]] = Field(
        description="Vision lens authorization",
        default=None,
    )
