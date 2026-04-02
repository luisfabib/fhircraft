import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from ..primitive import *

from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Reference,
    Timing,
    Annotation,
    Period,
    CodeableConcept,
)
from .resource import Resource
from .domain_resource import DomainResource

class DeviceUseStatement(DomainResource):
    """
    A record of a device being used by a patient where the record is the result of a report from the patient or another clinician.
    """

    _abstract = False
    _type = "DeviceUseStatement"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/DeviceUseStatement"

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
        description="External identifier for this record",
        default=None,
    )
    basedOn: Optional[ListType[Reference]] = Field(
        description="Fulfills plan, proposal or order",
        default=None,
    )
    status: Optional[Code] = Field(
        description="active | completed | entered-in-error +",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="Patient using device",
        default=None,
    )
    derivedFrom: Optional[ListType[Reference]] = Field(
        description="Supporting information",
        default=None,
    )
    timingTiming: Optional[Timing] = Field(
        description="How often  the device was used",
        default=None,
    )
    timingPeriod: Optional[Period] = Field(
        description="How often  the device was used",
        default=None,
    )
    timingDateTime: Optional[DateTime] = Field(
        description="How often  the device was used",
        default=None,
    )
    recordedOn: Optional[DateTime] = Field(
        description="When statement was recorded",
        default=None,
    )
    source: Optional[Reference] = Field(
        description="Who made the statement",
        default=None,
    )
    device: Optional[Reference] = Field(
        description="Reference to device used",
        default=None,
    )
    reasonCode: Optional[ListType[CodeableConcept]] = Field(
        description="Why device was used",
        default=None,
    )
    reasonReference: Optional[ListType[Reference]] = Field(
        description="Why was DeviceUseStatement performed?",
        default=None,
    )
    bodySite: Optional[CodeableConcept] = Field(
        description="Target body site",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Addition details (comments, instructions)",
        default=None,
    )

    @property
    def timing(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="timing",
        )

    @model_validator(mode="after")
    def timing_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Timing, Period, DateTime],
            field_name_base="timing",
            required=False,
        )
