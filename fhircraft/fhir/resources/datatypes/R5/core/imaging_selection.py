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
    CodeableReference,
    Coding,
)
from .resource import Resource
from .domain_resource import DomainResource

class ImagingSelectionPerformer(BackboneElement):
    """
    Selector of the instances – human or machine.
    """

    function: Optional[CodeableConcept] = Field(
        description="Type of performer",
        default=None,
    )
    actor: Optional[Reference] = Field(
        description="Author (human or machine)",
        default=None,
    )

class ImagingSelectionInstanceImageRegion2D(BackboneElement):
    """
    Each imaging selection instance or frame list might includes an image region, specified by a region type and a set of 2D coordinates.
       If the parent imagingSelection.instance contains a subset element of type frame, the image region applies to all frames in the subset list.
    """

    regionType: Optional[Code] = Field(
        description="point | polyline | interpolated | circle | ellipse",
        default=None,
    )
    coordinate: Optional[ListType[Decimal]] = Field(
        description="Specifies the coordinates that define the image region",
        default=None,
    )

class ImagingSelectionInstanceImageRegion3D(BackboneElement):
    """
    Each imaging selection might includes a 3D image region, specified by a region type and a set of 3D coordinates.
    """

    regionType: Optional[Code] = Field(
        description="point | multipoint | polyline | polygon | ellipse | ellipsoid",
        default=None,
    )
    coordinate: Optional[ListType[Decimal]] = Field(
        description="Specifies the coordinates that define the image region",
        default=None,
    )

class ImagingSelectionInstance(BackboneElement):
    """
    Each imaging selection includes one or more selected DICOM SOP instances.
    """

    uid: Optional[Id] = Field(
        description="DICOM SOP Instance UID",
        default=None,
    )
    number: Optional[UnsignedInt] = Field(
        description="DICOM Instance Number",
        default=None,
    )
    sopClass: Optional[Coding] = Field(
        description="DICOM SOP Class UID",
        default=None,
    )
    subset: Optional[ListType[String]] = Field(
        description="The selected subset of the SOP Instance",
        default=None,
    )
    imageRegion2D: Optional[ListType[ImagingSelectionInstanceImageRegion2D]] = Field(
        description="A specific 2D region in a DICOM image / frame",
        default=None,
    )
    imageRegion3D: Optional[ListType[ImagingSelectionInstanceImageRegion3D]] = Field(
        description="A specific 3D region in a DICOM frame of reference",
        default=None,
    )

class ImagingSelection(DomainResource):
    """
    A selection of DICOM SOP instances and/or frames within a single Study and Series. This might include additional specifics such as an image region, an Observation UID or a Segmentation Number, allowing linkage to an Observation Resource or transferring this information along with the ImagingStudy Resource.
    """

    _abstract = False
    _type = "ImagingSelection"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/ImagingSelection"

    identifier: Optional[ListType[Identifier]] = Field(
        description="Business Identifier for Imaging Selection",
        default=None,
    )
    status: Optional[Code] = Field(
        description="available | entered-in-error | unknown",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="Subject of the selected instances",
        default=None,
    )
    issued: Optional[Instant] = Field(
        description="Date / Time when this imaging selection was created",
        default=None,
    )
    performer: Optional[ListType[ImagingSelectionPerformer]] = Field(
        description="Selector of the instances (human or machine)",
        default=None,
    )
    basedOn: Optional[ListType[Reference]] = Field(
        description="Associated request",
        default=None,
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description="Classifies the imaging selection",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="Imaging Selection purpose text or code",
        default=None,
    )
    studyUid: Optional[Id] = Field(
        description="DICOM Study Instance UID",
        default=None,
    )
    derivedFrom: Optional[ListType[Reference]] = Field(
        description="The imaging study from which the imaging selection is derived",
        default=None,
    )
    endpoint: Optional[ListType[Reference]] = Field(
        description="The network service providing retrieval for the images referenced in the imaging selection",
        default=None,
    )
    seriesUid: Optional[Id] = Field(
        description="DICOM Series Instance UID",
        default=None,
    )
    seriesNumber: Optional[UnsignedInt] = Field(
        description="DICOM Series Number",
        default=None,
    )
    frameOfReferenceUid: Optional[Id] = Field(
        description="The Frame of Reference UID for the selected images",
        default=None,
    )
    bodySite: Optional[CodeableReference] = Field(
        description="Body part examined",
        default=None,
    )
    focus: Optional[ListType[Reference]] = Field(
        description="Related resource that is the focus for the imaging selection",
        default=None,
    )
    instance: Optional[ListType[ImagingSelectionInstance]] = Field(
        description="The selected instances",
        default=None,
    )
