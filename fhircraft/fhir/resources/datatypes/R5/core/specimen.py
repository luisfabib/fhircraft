from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators


import fhircraft.fhir.resources.datatypes.R5.primitive as fhir
from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    BackboneElement,
    Period,
    Duration,
    Quantity,
    CodeableReference,
    Annotation,
)
from .resource import Resource
from .domain_resource import DomainResource


class SpecimenFeature(BackboneElement):
    """
    A physical feature or landmark on a specimen, highlighted for context by the collector of the specimen (e.g. surgeon), that identifies the type of feature as well as its meaning (e.g. the red ink indicating the resection margin of the right lobe of the excised prostate tissue or wire loop at radiologically suspected tumor location).
    """

    type: Optional[CodeableConcept] = Field(
        description="Highlighted feature",
        default=None,
    )
    description: Optional[fhir.string] = Field(
        description="Information about the feature",
        default=None,
    )


class SpecimenCollection(BackboneElement):
    """
    Details concerning the specimen collection.
    """

    collector: Optional[Reference] = Field(
        description="Who collected the specimen",
        default=None,
    )
    collectedDateTime: Optional[fhir.dateTime] = Field(
        description="Collection time",
        default=None,
    )
    collectedPeriod: Optional[Period] = Field(
        description="Collection time",
        default=None,
    )
    duration: Optional[Duration] = Field(
        description="How long it took to collect specimen",
        default=None,
    )
    quantity: Optional[Quantity] = Field(
        description="The quantity of specimen collected",
        default=None,
    )
    method: Optional[CodeableConcept] = Field(
        description="Technique used to perform collection",
        default=None,
    )
    device: Optional[CodeableReference] = Field(
        description="Device used to perform collection",
        default=None,
    )
    procedure: Optional[Reference] = Field(
        description="The procedure that collects the specimen",
        default=None,
    )
    bodySite: Optional[CodeableReference] = Field(
        description="Anatomical collection site",
        default=None,
    )
    fastingStatusCodeableConcept: Optional[CodeableConcept] = Field(
        description="Whether or how long patient abstained from food and/or drink",
        default=None,
    )
    fastingStatusDuration: Optional[Duration] = Field(
        description="Whether or how long patient abstained from food and/or drink",
        default=None,
    )

    @property
    def collected(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="collected",
        )

    @property
    def fastingStatus(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="fastingStatus",
        )

    @model_validator(mode="after")
    def collected_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.dateTime, Period],
            field_name_base="collected",
            required=False,
        )

    @model_validator(mode="after")
    def fastingStatus_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[CodeableConcept, Duration],
            field_name_base="fastingStatus",
            required=False,
        )


class SpecimenProcessing(BackboneElement):
    """
    Details concerning processing and processing steps for the specimen.
    """

    description: Optional[fhir.string] = Field(
        description="Textual description of procedure",
        default=None,
    )
    method: Optional[CodeableConcept] = Field(
        description="Indicates the treatment step  applied to the specimen",
        default=None,
    )
    additive: Optional[ListType[Reference]] = Field(
        description="Material used in the processing step",
        default=None,
    )
    timeDateTime: Optional[fhir.dateTime] = Field(
        description="Date and time of specimen processing",
        default=None,
    )
    timePeriod: Optional[Period] = Field(
        description="Date and time of specimen processing",
        default=None,
    )

    @property
    def time(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="time",
        )

    @model_validator(mode="after")
    def time_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.dateTime, Period],
            field_name_base="time",
            required=False,
        )


class SpecimenContainer(BackboneElement):
    """
    The container holding the specimen.  The recursive nature of containers; i.e. blood in tube in tray in rack is not addressed here.
    """

    device: Optional[Reference] = Field(
        description="Device resource for the container",
        default=None,
    )
    location: Optional[Reference] = Field(
        description="Where the container is",
        default=None,
    )
    specimenQuantity: Optional[Quantity] = Field(
        description="Quantity of specimen within container",
        default=None,
    )


class Specimen(DomainResource):
    """
    A sample to be used for analysis.
    """

    _abstract = False
    _type = "Specimen"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Specimen"

    identifier: Optional[ListType[Identifier]] = Field(
        description="External Identifier",
        default=None,
    )
    accessionIdentifier: Optional[Identifier] = Field(
        description="Identifier assigned by the lab",
        default=None,
    )
    status: Optional[fhir.code] = Field(
        description="available | unavailable | unsatisfactory | entered-in-error",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Kind of material that forms the specimen",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="Where the specimen came from. This may be from patient(s), from a location (e.g., the source of an environmental sample), or a sampling of a substance, a biologically-derived product, or a device",
        default=None,
    )
    receivedTime: Optional[fhir.dateTime] = Field(
        description="The time when specimen is received by the testing laboratory",
        default=None,
    )
    parent: Optional[ListType[Reference]] = Field(
        description="Specimen from which this specimen originated",
        default=None,
    )
    request: Optional[ListType[Reference]] = Field(
        description="Why the specimen was collected",
        default=None,
    )
    combined: Optional[fhir.code] = Field(
        description="grouped | pooled",
        default=None,
    )
    role: Optional[ListType[CodeableConcept]] = Field(
        description="The role the specimen serves",
        default=None,
    )
    feature: Optional[ListType[SpecimenFeature]] = Field(
        description="The physical feature of a specimen",
        default=None,
    )
    collection: Optional[SpecimenCollection] = Field(
        description="Collection details",
        default=None,
    )
    processing: Optional[ListType[SpecimenProcessing]] = Field(
        description="Processing and processing step details",
        default=None,
    )
    container: Optional[ListType[SpecimenContainer]] = Field(
        description="Direct container of specimen (tube/slide, etc.)",
        default=None,
    )
    condition: Optional[ListType[CodeableConcept]] = Field(
        description="State of the specimen",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Comments",
        default=None,
    )
