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
    Quantity,
    Annotation,
    ContactPoint,
)
from .resource import Resource
from .domain_resource import DomainResource


class DeviceUdiCarrier(BackboneElement):
    """
    Unique device identifier (UDI) assigned to device label or package.  Note that the Device may include multiple udiCarriers as it either may include just the udiCarrier for the jurisdiction it is sold, or for multiple jurisdictions it could have been sold.
    """

    deviceIdentifier: Optional[fhir.string] = Field(
        description="Mandatory fixed portion of UDI",
        default=None,
    )
    issuer: Optional[fhir.uri] = Field(
        description="UDI Issuing Organization",
        default=None,
    )
    jurisdiction: Optional[fhir.uri] = Field(
        description="Regional UDI authority",
        default=None,
    )
    carrierAIDC: Optional[fhir.base64Binary] = Field(
        description="UDI Machine Readable Barcode string",
        default=None,
    )
    carrierHRF: Optional[fhir.string] = Field(
        description="UDI Human Readable Barcode string",
        default=None,
    )
    entryType: Optional[fhir.code] = Field(
        description="barcode | rfid | manual +",
        default=None,
    )


class DeviceDeviceName(BackboneElement):
    """
    This represents the manufacturer's name of the device as provided by the device, from a UDI label, or by a person describing the Device.  This typically would be used when a person provides the name(s) or when the device represents one of the names available from DeviceDefinition.
    """

    name: fhir.string = Field(
        description="The name of the device",
    )
    type: fhir.code = Field(
        description="udi-label-name | user-friendly-name | patient-reported-name | manufacturer-name | model-name | other",
    )


class DeviceSpecialization(BackboneElement):
    """
    The capabilities supported on a  device, the standards to which the device conforms for a particular purpose, and used for the communication.
    """

    systemType: CodeableConcept = Field(
        description="The standard that is used to operate and communicate",
    )
    version: Optional[fhir.string] = Field(
        description="The version of the standard that is used to operate and communicate",
        default=None,
    )


class DeviceVersion(BackboneElement):
    """
    The actual design of the device or software version running on the device.
    """

    type: Optional[CodeableConcept] = Field(
        description="The type of the device version",
        default=None,
    )
    component: Optional[Identifier] = Field(
        description="A single component of the device version",
        default=None,
    )
    value: fhir.string = Field(
        description="The version text",
    )


class DeviceProperty(BackboneElement):
    """
    The actual configuration settings of a device as it actually operates, e.g., regulation status, time properties.
    """

    type: CodeableConcept = Field(
        description="code that specifies the property DeviceDefinitionPropetyCode (Extensible)",
    )
    valueQuantity: Optional[ListType[Quantity]] = Field(
        description="Property value as a quantity",
        default=None,
    )
    valueCode: Optional[ListType[CodeableConcept]] = Field(
        description="Property value as a code, e.g., NTP4 (synced to NTP)",
        default=None,
    )


class Device(DomainResource):
    """
    A type of a manufactured item that is used in the provision of healthcare without being substantially changed through that activity. The device may be a medical or non-medical device.
    """

    _abstract = False
    _type = "Device"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Device"

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
        description="Instance identifier",
        default=None,
    )
    definition: Optional[Reference] = Field(
        description="The reference to the definition for the device",
        default=None,
    )
    udiCarrier: Optional[ListType[DeviceUdiCarrier]] = Field(
        description="Unique Device Identifier (UDI) Barcode string",
        default=None,
    )
    status: Optional[fhir.code] = Field(
        description="active | inactive | entered-in-error | unknown",
        default=None,
    )
    statusReason: Optional[ListType[CodeableConcept]] = Field(
        description="online | paused | standby | offline | not-ready | transduc-discon | hw-discon | off",
        default=None,
    )
    distinctIdentifier: Optional[fhir.string] = Field(
        description="The distinct identification string",
        default=None,
    )
    manufacturer: Optional[fhir.string] = Field(
        description="Name of device manufacturer",
        default=None,
    )
    manufactureDate: Optional[fhir.dateTime] = Field(
        description="Date when the device was made",
        default=None,
    )
    expirationDate: Optional[fhir.dateTime] = Field(
        description="Date and time of expiry of this device (if applicable)",
        default=None,
    )
    lotNumber: Optional[fhir.string] = Field(
        description="Lot number of manufacture",
        default=None,
    )
    serialNumber: Optional[fhir.string] = Field(
        description="Serial number assigned by the manufacturer",
        default=None,
    )
    deviceName: Optional[ListType[DeviceDeviceName]] = Field(
        description="The name of the device as given by the manufacturer",
        default=None,
    )
    modelNumber: Optional[fhir.string] = Field(
        description="The model number for the device",
        default=None,
    )
    partNumber: Optional[fhir.string] = Field(
        description="The part number of the device",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="The kind or type of device",
        default=None,
    )
    specialization: Optional[ListType[DeviceSpecialization]] = Field(
        description="The capabilities supported on a  device, the standards to which the device conforms for a particular purpose, and used for the communication",
        default=None,
    )
    version: Optional[ListType[DeviceVersion]] = Field(
        description="The actual design of the device or software version running on the device",
        default=None,
    )
    property_: Optional[ListType[DeviceProperty]] = Field(
        description="The actual configuration settings of a device as it actually operates, e.g., regulation status, time properties",
        default=None,
        alias="property",
    )
    patient: Optional[Reference] = Field(
        description="Patient to whom Device is affixed",
        default=None,
    )
    owner: Optional[Reference] = Field(
        description="Organization responsible for device",
        default=None,
    )
    contact: Optional[ListType[ContactPoint]] = Field(
        description="Details for human/organization for support",
        default=None,
    )
    location: Optional[Reference] = Field(
        description="Where the device is found",
        default=None,
    )
    url: Optional[fhir.uri] = Field(
        description="Network address to contact device",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Device notes and comments",
        default=None,
    )
    safety: Optional[ListType[CodeableConcept]] = Field(
        description="Safety Characteristics of Device",
        default=None,
    )
    parent: Optional[Reference] = Field(
        description="The parent device",
        default=None,
    )
