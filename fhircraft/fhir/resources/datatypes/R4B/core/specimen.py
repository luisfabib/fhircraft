import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from ..primitive import *

from fhircraft.fhir.resources.datatypes.R4B.complex import (
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
    Annotation,
)
from .resource import Resource
from .domain_resource import DomainResource

class SpecimenCollection(BackboneElement):
    """
    Details concerning the specimen collection.
    """

    collector: Optional[Reference] = Field(
        description="Who collected the specimen",
        default=None,
    )
    collectedDateTime: Optional[DateTime] = Field(
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
    bodySite: Optional[CodeableConcept] = Field(
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
            field_types=[DateTime, Period],
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

    description: Optional[String] = Field(
        description="Textual description of procedure",
        default=None,
    )
    procedure: Optional[CodeableConcept] = Field(
        description="Indicates the treatment step  applied to the specimen",
        default=None,
    )
    additive: Optional[ListType[Reference]] = Field(
        description="Material used in the processing step",
        default=None,
    )
    timeDateTime: Optional[DateTime] = Field(
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
            field_types=[DateTime, Period],
            field_name_base="time",
            required=False,
        )

class SpecimenContainer(BackboneElement):
    """
    The container holding the specimen.  The recursive nature of containers; i.e. blood in tube in tray in rack is not addressed here.
    """

    identifier: Optional[ListType[Identifier]] = Field(
        description="Id for the container",
        default=None,
    )
    description: Optional[String] = Field(
        description="Textual description of the container",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Kind of container directly associated with specimen",
        default=None,
    )
    capacity: Optional[Quantity] = Field(
        description="Container volume or size",
        default=None,
    )
    specimenQuantity: Optional[Quantity] = Field(
        description="Quantity of specimen within container",
        default=None,
    )
    additiveCodeableConcept: Optional[CodeableConcept] = Field(
        description="Additive associated with container",
        default=None,
    )
    additiveReference: Optional[Reference] = Field(
        description="Additive associated with container",
        default=None,
    )

    @property
    def additive(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="additive",
        )

    @model_validator(mode="after")
    def additive_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[CodeableConcept, Reference],
            field_name_base="additive",
            required=False,
        )

class Specimen(DomainResource):
    """
    A sample to be used for analysis.
    """

    _abstract = False
    _type = "Specimen"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Specimen"

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
        description="External Identifier",
        default=None,
    )
    accessionIdentifier: Optional[Identifier] = Field(
        description="Identifier assigned by the lab",
        default=None,
    )
    status: Optional[Code] = Field(
        description="available | unavailable | unsatisfactory | entered-in-error",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Kind of material that forms the specimen",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="Where the specimen came from. This may be from patient(s), from a location (e.g., the source of an environmental sample), or a sampling of a substance or a device",
        default=None,
    )
    receivedTime: Optional[DateTime] = Field(
        description="The time when specimen was received for processing",
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
