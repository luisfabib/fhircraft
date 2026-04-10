import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)


import fhircraft.fhir.resources.datatypes.R4.primitive as fhir
from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Annotation,
    Narrative,
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    Period,
    Attachment,
)
from .resource import Resource
from .domain_resource import DomainResource


class Media(DomainResource):
    """
    A photo, video, or audio recording acquired or used in healthcare. The actual content may be inline or provided by direct reference.
    """

    _abstract = False
    _type = "Media"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Media"

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
        description="Identifier(s) for the image",
        default=None,
    )
    basedOn: Optional[ListType[Reference]] = Field(
        description="Procedure that caused this media to be created",
        default=None,
    )
    partOf: Optional[ListType[Reference]] = Field(
        description="Part of referenced event",
        default=None,
    )
    status: Optional[fhir.code] = Field(
        description="preparation | in-progress | not-done | on-hold | stopped | completed | entered-in-error | unknown",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="Classification of media as image, video, or audio",
        default=None,
    )
    modality: Optional[CodeableConcept] = Field(
        description="The type of acquisition equipment/process",
        default=None,
    )
    view: Optional[CodeableConcept] = Field(
        description="Imaging view, e.g. Lateral or Antero-posterior",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="Who/What this Media is a record of",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="Encounter associated with media",
        default=None,
    )
    createdDateTime: Optional[fhir.dateTime] = Field(
        description="When Media was collected",
        default=None,
    )
    createdPeriod: Optional[Period] = Field(
        description="When Media was collected",
        default=None,
    )
    issued: Optional[fhir.instant] = Field(
        description="Date/time this version was made available",
        default=None,
    )
    operator: Optional[Reference] = Field(
        description="The person who generated the image",
        default=None,
    )
    reasonCode: Optional[ListType[CodeableConcept]] = Field(
        description="Why was event performed?",
        default=None,
    )
    bodySite: Optional[CodeableConcept] = Field(
        description="Observed body part",
        default=None,
    )
    deviceName: Optional[fhir.string] = Field(
        description="Name of the device/manufacturer",
        default=None,
    )
    device: Optional[Reference] = Field(
        description="Observing Device",
        default=None,
    )
    height: Optional[fhir.positiveInt] = Field(
        description="Height of the image in pixels (photo/video)",
        default=None,
    )
    width: Optional[fhir.positiveInt] = Field(
        description="Width of the image in pixels (photo/video)",
        default=None,
    )
    frames: Optional[fhir.positiveInt] = Field(
        description="Number of frames if \u003e 1 (photo)",
        default=None,
    )
    duration: Optional[fhir.decimal] = Field(
        description="Length in seconds (audio / video)",
        default=None,
    )
    content: Optional[Attachment] = Field(
        description="Actual Media - reference or data",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Comments made about the media",
        default=None,
    )

    @property
    def created(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="created",
        )

    @model_validator(mode="after")
    def created_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.dateTime, Period],
            field_name_base="created",
            required=False,
        )
