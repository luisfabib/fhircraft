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
    Reference,
    CodeableReference,
    Annotation,
    BackboneElement,
    Coding,
)
from .resource import Resource
from .domain_resource import DomainResource

class ImagingStudySeriesPerformer(BackboneElement):
    """
    Indicates who or what performed the series and how they were involved.
    """

    function: Optional[CodeableConcept] = Field(
        description="Type of performance",
        default=None,
    )
    actor: Optional[Reference] = Field(
        description="Who performed the series",
        default=None,
    )

class ImagingStudySeriesInstance(BackboneElement):
    """
    A single SOP instance within the series, e.g. an image, or presentation state.
    """

    uid: Optional[Id] = Field(
        description="DICOM SOP Instance UID",
        default=None,
    )
    sopClass: Optional[Coding] = Field(
        description="DICOM class type",
        default=None,
    )
    number: Optional[UnsignedInt] = Field(
        description="The number of this instance in the series",
        default=None,
    )
    title: Optional[String] = Field(
        description="Description of instance",
        default=None,
    )

class ImagingStudySeries(BackboneElement):
    """
    Each study has one or more series of images or other content.
    """

    uid: Optional[Id] = Field(
        description="DICOM Series Instance UID for the series",
        default=None,
    )
    number: Optional[UnsignedInt] = Field(
        description="Numeric identifier of this series",
        default=None,
    )
    modality: Optional[CodeableConcept] = Field(
        description="The modality used for this series",
        default=None,
    )
    description: Optional[String] = Field(
        description="A short human readable summary of the series",
        default=None,
    )
    numberOfInstances: Optional[UnsignedInt] = Field(
        description="Number of Series Related Instances",
        default=None,
    )
    endpoint: Optional[ListType[Reference]] = Field(
        description="Series access endpoint",
        default=None,
    )
    bodySite: Optional[CodeableReference] = Field(
        description="Body part examined",
        default=None,
    )
    laterality: Optional[CodeableConcept] = Field(
        description="Body part laterality",
        default=None,
    )
    specimen: Optional[ListType[Reference]] = Field(
        description="Specimen imaged",
        default=None,
    )
    started: Optional[DateTime] = Field(
        description="When the series started",
        default=None,
    )
    performer: Optional[ListType[ImagingStudySeriesPerformer]] = Field(
        description="Who performed the series",
        default=None,
    )
    instance: Optional[ListType[ImagingStudySeriesInstance]] = Field(
        description="A single SOP instance from the series",
        default=None,
    )

class ImagingStudy(DomainResource):
    """
    Representation of the content produced in a DICOM imaging study. A study comprises a set of series, each of which includes a set of Service-Object Pair Instances (SOP Instances - images or other data) acquired or produced in a common context.  A series is of only one modality (e.g. X-ray, CT, MR, ultrasound), but a study may have multiple series of different modalities.
    """

    _abstract = False
    _type = "ImagingStudy"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/ImagingStudy"

    identifier: Optional[ListType[Identifier]] = Field(
        description="Identifiers for the whole study",
        default=None,
    )
    status: Optional[Code] = Field(
        description="registered | available | cancelled | entered-in-error | unknown",
        default=None,
    )
    modality: Optional[ListType[CodeableConcept]] = Field(
        description="All of the distinct values for series\u0027 modalities",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="Who or what is the subject of the study",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="Encounter with which this imaging study is associated",
        default=None,
    )
    started: Optional[DateTime] = Field(
        description="When the study was started",
        default=None,
    )
    basedOn: Optional[ListType[Reference]] = Field(
        description="Request fulfilled",
        default=None,
    )
    partOf: Optional[ListType[Reference]] = Field(
        description="Part of referenced event",
        default=None,
    )
    referrer: Optional[Reference] = Field(
        description="Referring physician",
        default=None,
    )
    endpoint: Optional[ListType[Reference]] = Field(
        description="Study access endpoint",
        default=None,
    )
    numberOfSeries: Optional[UnsignedInt] = Field(
        description="Number of Study Related Series",
        default=None,
    )
    numberOfInstances: Optional[UnsignedInt] = Field(
        description="Number of Study Related Instances",
        default=None,
    )
    procedure: Optional[ListType[CodeableReference]] = Field(
        description="The performed procedure or code",
        default=None,
    )
    location: Optional[Reference] = Field(
        description="Where ImagingStudy occurred",
        default=None,
    )
    reason: Optional[ListType[CodeableReference]] = Field(
        description="Why the study was requested / performed",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="User-defined comments",
        default=None,
    )
    description: Optional[String] = Field(
        description="Institution-generated description",
        default=None,
    )
    series: Optional[ListType[ImagingStudySeries]] = Field(
        description="Each study has one or more series of instances",
        default=None,
    )
