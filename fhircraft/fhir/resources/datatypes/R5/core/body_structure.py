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
    CodeableConcept,
    BackboneElement,
    CodeableReference,
    Quantity,
    Reference,
    Attachment,
)
from .resource import Resource
from .domain_resource import DomainResource

class BodyStructureIncludedStructure(BackboneElement):
    """
    The anatomical location(s) or region(s) of the specimen, lesion, or body structure.
    """

    structure: Optional[CodeableConcept] = Field(
        description="Code that represents the included structure",
        default=None,
    )
    laterality: Optional[CodeableConcept] = Field(
        description="Code that represents the included structure laterality",
        default=None,
    )
    bodyLandmarkOrientation: Optional[
        ListType["BodyStructureIncludedStructureBodyLandmarkOrientation"]
    ] = Field(
        description="Landmark relative location",
        default=None,
    )
    spatialReference: Optional[ListType[Reference]] = Field(
        description="Cartesian reference for structure",
        default=None,
    )
    qualifier: Optional[ListType[CodeableConcept]] = Field(
        description="Code that represents the included structure qualifier",
        default=None,
    )

class BodyStructureIncludedStructureBodyLandmarkOrientationDistanceFromLandmark(
    BackboneElement
):
    """
    The distance in centimeters a certain observation is made from a body landmark.
    """

    device: Optional[ListType[CodeableReference]] = Field(
        description="Measurement device",
        default=None,
    )
    value: Optional[ListType[Quantity]] = Field(
        description="Measured distance from body landmark",
        default=None,
    )

class BodyStructureIncludedStructureBodyLandmarkOrientation(BackboneElement):
    """
    Body locations in relation to a specific body landmark (tatoo, scar, other body structure).
    """

    landmarkDescription: Optional[ListType[CodeableConcept]] = Field(
        description="Body ]andmark description",
        default=None,
    )
    clockFacePosition: Optional[ListType[CodeableConcept]] = Field(
        description="Clockface orientation",
        default=None,
    )
    distanceFromLandmark: Optional[
        ListType[
            BodyStructureIncludedStructureBodyLandmarkOrientationDistanceFromLandmark
        ]
    ] = Field(
        description="Landmark relative location",
        default=None,
    )
    surfaceOrientation: Optional[ListType[CodeableConcept]] = Field(
        description="Relative landmark surface orientation",
        default=None,
    )

class BodyStructureExcludedStructure(BackboneElement):
    """
    The anatomical location(s) or region(s) not occupied or represented by the specimen, lesion, or body structure.
    """

    structure: Optional[CodeableConcept] = Field(
        description="Code that represents the included structure",
        default=None,
    )
    laterality: Optional[CodeableConcept] = Field(
        description="Code that represents the included structure laterality",
        default=None,
    )
    bodyLandmarkOrientation: Optional[
        ListType[BodyStructureIncludedStructureBodyLandmarkOrientation]
    ] = Field(
        description="Landmark relative location",
        default=None,
    )
    spatialReference: Optional[ListType[Reference]] = Field(
        description="Cartesian reference for structure",
        default=None,
    )
    qualifier: Optional[ListType[CodeableConcept]] = Field(
        description="Code that represents the included structure qualifier",
        default=None,
    )

class BodyStructure(DomainResource):
    """
    Record details about an anatomical structure.  This resource may be used when a coded concept does not provide the necessary detail needed for the use case.
    """

    _abstract = False
    _type = "BodyStructure"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/BodyStructure"

    identifier: Optional[ListType[Identifier]] = Field(
        description="Bodystructure identifier",
        default=None,
    )
    active: Optional[Boolean] = Field(
        description="Whether this record is in active use",
        default=None,
    )
    morphology: Optional[CodeableConcept] = Field(
        description="Kind of Structure",
        default=None,
    )
    includedStructure: Optional[ListType[BodyStructureIncludedStructure]] = Field(
        description="Included anatomic location(s)",
        default=None,
    )
    excludedStructure: Optional[ListType[BodyStructureExcludedStructure]] = Field(
        description="Excluded anatomic locations(s)",
        default=None,
    )
    description: Optional[Markdown] = Field(
        description="Text description",
        default=None,
    )
    image: Optional[ListType[Attachment]] = Field(
        description="Attached images",
        default=None,
    )
    patient: Optional[Reference] = Field(
        description="Who this is about",
        default=None,
    )
