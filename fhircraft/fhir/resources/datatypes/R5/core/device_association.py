from pydantic import Field, model_validator
from typing import Optional, List as ListType

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators

from fhircraft.fhir.resources.datatypes.primitives import String, Uri, Code

from fhircraft.fhir.resources.datatypes.R5.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    Reference,
    CodeableConcept,
    Period,
    BackboneElement,
)
from .resource import Resource
from .domain_resource import DomainResource


class DeviceAssociationOperation(BackboneElement):
    """
    The details about the device when it is in use to describe its operation.
    """

    status: Optional[CodeableConcept] = Field(
        description="Device operational condition",
        default=None,
    )
    operator: Optional[ListType[Reference]] = Field(
        description="The individual performing the action enabled by the device",
        default=None,
    )
    period: Optional[Period] = Field(
        description="Begin and end dates and times for the device\u0027s operation",
        default=None,
    )


class DeviceAssociation(DomainResource):
    """
    A record of association of a device.
    """

    _abstract = False
    _type = "DeviceAssociation"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/DeviceAssociation"

    identifier: Optional[ListType[Identifier]] = Field(
        description="Instance identifier",
        default=None,
    )
    device: Optional[Reference] = Field(
        description="Reference to the devices associated with the patient or group",
        default=None,
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description="Describes the relationship between the device and subject",
        default=None,
    )
    status: Optional[CodeableConcept] = Field(
        description="implanted | explanted | attached | entered-in-error | unknown",
        default=None,
    )
    statusReason: Optional[ListType[CodeableConcept]] = Field(
        description="The reasons given for the current association status",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="The individual, group of individuals or device that the device is on or associated with",
        default=None,
    )
    bodyStructure: Optional[Reference] = Field(
        description="Current anatomical location of the device in/on subject",
        default=None,
    )
    period: Optional[Period] = Field(
        description="Begin and end dates and times for the device association",
        default=None,
    )
    operation: Optional[ListType[DeviceAssociationOperation]] = Field(
        description="The details about the device when it is in use to describe its operation",
        default=None,
    )
