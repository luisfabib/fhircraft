import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)


import fhircraft.fhir.resources.datatypes.R4.primitive as fhir
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

    amount: Optional[fhir.decimal] = Field(
        description="Amount of adjustment",
        default=None,
    )
    base: Optional[fhir.code] = Field(
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
    eye: Optional[fhir.code] = Field(
        description="right | left",
        default=None,
    )
    sphere: Optional[fhir.decimal] = Field(
        description="Power of the lens",
        default=None,
    )
    cylinder: Optional[fhir.decimal] = Field(
        description="Lens power for astigmatism",
        default=None,
    )
    axis: Optional[fhir.integer] = Field(
        description="Lens meridian which contain no power for astigmatism",
        default=None,
    )
    prism: Optional[ListType[VisionPrescriptionLensSpecificationPrism]] = Field(
        description="Eye alignment compensation",
        default=None,
    )
    add: Optional[fhir.decimal] = Field(
        description="Added power for multifocal levels",
        default=None,
    )
    power: Optional[fhir.decimal] = Field(
        description="Contact lens power",
        default=None,
    )
    backCurve: Optional[fhir.decimal] = Field(
        description="Contact lens back curvature",
        default=None,
    )
    diameter: Optional[fhir.decimal] = Field(
        description="Contact lens diameter",
        default=None,
    )
    duration: Optional[Quantity] = Field(
        description="Lens wear duration",
        default=None,
    )
    color: Optional[fhir.string] = Field(
        description="Color required",
        default=None,
    )
    brand: Optional[fhir.string] = Field(
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
    status: Optional[fhir.code] = Field(
        description="active | cancelled | draft | entered-in-error",
        default=None,
    )
    created: Optional[fhir.dateTime] = Field(
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
    dateWritten: Optional[fhir.dateTime] = Field(
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
