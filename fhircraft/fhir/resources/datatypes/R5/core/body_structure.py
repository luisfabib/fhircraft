from pydantic import Field, model_validator
from typing import Optional, List

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
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
        List["BodyStructureIncludedStructureBodyLandmarkOrientation"]
    ] = Field(
        description="Landmark relative location",
        default=None,
    )
    spatialReference: Optional[List[Reference]] = Field(
        description="Cartesian reference for structure",
        default=None,
    )
    qualifier: Optional[List[CodeableConcept]] = Field(
        description="Code that represents the included structure qualifier",
        default=None,
    )


class BodyStructureIncludedStructureBodyLandmarkOrientationDistanceFromLandmark(
    BackboneElement
):
    """
    The distance in centimeters a certain observation is made from a body landmark.
    """

    device: Optional[List[CodeableReference]] = Field(
        description="Measurement device",
        default=None,
    )
    value: Optional[List[Quantity]] = Field(
        description="Measured distance from body landmark",
        default=None,
    )


class BodyStructureIncludedStructureBodyLandmarkOrientation(BackboneElement):
    """
    Body locations in relation to a specific body landmark (tatoo, scar, other body structure).
    """

    landmarkDescription: Optional[List[CodeableConcept]] = Field(
        description="Body ]andmark description",
        default=None,
    )
    clockFacePosition: Optional[List[CodeableConcept]] = Field(
        description="Clockface orientation",
        default=None,
    )
    distanceFromLandmark: Optional[
        List[BodyStructureIncludedStructureBodyLandmarkOrientationDistanceFromLandmark]
    ] = Field(
        description="Landmark relative location",
        default=None,
    )
    surfaceOrientation: Optional[List[CodeableConcept]] = Field(
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
        List[BodyStructureIncludedStructureBodyLandmarkOrientation]
    ] = Field(
        description="Landmark relative location",
        default=None,
    )
    spatialReference: Optional[List[Reference]] = Field(
        description="Cartesian reference for structure",
        default=None,
    )
    qualifier: Optional[List[CodeableConcept]] = Field(
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

    identifier: Optional[List[Identifier]] = Field(
        description="Bodystructure identifier",
        default=None,
    )
    active: Optional[Boolean] = Field(
        description="Whether this record is in active use",
        default=None,
    )
    active_ext: Optional[Element] = Field(
        description="Placeholder element for active extensions",
        default=None,
        alias="_active",
    )
    morphology: Optional[CodeableConcept] = Field(
        description="Kind of Structure",
        default=None,
    )
    includedStructure: Optional[List[BodyStructureIncludedStructure]] = Field(
        description="Included anatomic location(s)",
        default=None,
    )
    excludedStructure: Optional[List[BodyStructureExcludedStructure]] = Field(
        description="Excluded anatomic locations(s)",
        default=None,
    )
    description: Optional[Markdown] = Field(
        description="Text description",
        default=None,
    )
    description_ext: Optional[Element] = Field(
        description="Placeholder element for description extensions",
        default=None,
        alias="_description",
    )
    image: Optional[List[Attachment]] = Field(
        description="Attached images",
        default=None,
    )
    patient: Optional[Reference] = Field(
        description="Who this is about",
        default=None,
    )
