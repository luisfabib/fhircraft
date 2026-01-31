import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import (
    String,
    Uri,
    Code,
    Base64Binary,
    DateTime,
)

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

    deviceIdentifier: Optional[String] = Field(
        description="Mandatory fixed portion of UDI",
        default=None,
    )
    deviceIdentifier_ext: Optional[Element] = Field(
        description="Placeholder element for deviceIdentifier extensions",
        default=None,
        alias="_deviceIdentifier",
    )
    issuer: Optional[Uri] = Field(
        description="UDI Issuing Organization",
        default=None,
    )
    issuer_ext: Optional[Element] = Field(
        description="Placeholder element for issuer extensions",
        default=None,
        alias="_issuer",
    )
    jurisdiction: Optional[Uri] = Field(
        description="Regional UDI authority",
        default=None,
    )
    jurisdiction_ext: Optional[Element] = Field(
        description="Placeholder element for jurisdiction extensions",
        default=None,
        alias="_jurisdiction",
    )
    carrierAIDC: Optional[Base64Binary] = Field(
        description="UDI Machine Readable Barcode String",
        default=None,
    )
    carrierAIDC_ext: Optional[Element] = Field(
        description="Placeholder element for carrierAIDC extensions",
        default=None,
        alias="_carrierAIDC",
    )
    carrierHRF: Optional[String] = Field(
        description="UDI Human Readable Barcode String",
        default=None,
    )
    carrierHRF_ext: Optional[Element] = Field(
        description="Placeholder element for carrierHRF extensions",
        default=None,
        alias="_carrierHRF",
    )
    entryType: Optional[Code] = Field(
        description="barcode | rfid | manual +",
        default=None,
    )
    entryType_ext: Optional[Element] = Field(
        description="Placeholder element for entryType extensions",
        default=None,
        alias="_entryType",
    )


class DeviceDeviceName(BackboneElement):
    """
    This represents the manufacturer's name of the device as provided by the device, from a UDI label, or by a person describing the Device.  This typically would be used when a person provides the name(s) or when the device represents one of the names available from DeviceDefinition.
    """

    name: Optional[String] = Field(
        description="The name of the device",
        default=None,
    )
    name_ext: Optional[Element] = Field(
        description="Placeholder element for name extensions",
        default=None,
        alias="_name",
    )
    type: Optional[Code] = Field(
        description="udi-label-name | user-friendly-name | patient-reported-name | manufacturer-name | model-name | other",
        default=None,
    )
    type_ext: Optional[Element] = Field(
        description="Placeholder element for type extensions",
        default=None,
        alias="_type",
    )


class DeviceSpecialization(BackboneElement):
    """
    The capabilities supported on a  device, the standards to which the device conforms for a particular purpose, and used for the communication.
    """

    systemType: Optional[CodeableConcept] = Field(
        description="The standard that is used to operate and communicate",
        default=None,
    )
    version: Optional[String] = Field(
        description="The version of the standard that is used to operate and communicate",
        default=None,
    )
    version_ext: Optional[Element] = Field(
        description="Placeholder element for version extensions",
        default=None,
        alias="_version",
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
    value: Optional[String] = Field(
        description="The version text",
        default=None,
    )
    value_ext: Optional[Element] = Field(
        description="Placeholder element for value extensions",
        default=None,
        alias="_value",
    )


class DeviceProperty(BackboneElement):
    """
    The actual configuration settings of a device as it actually operates, e.g., regulation status, time properties.
    """

    type: Optional[CodeableConcept] = Field(
        description="Code that specifies the property DeviceDefinitionPropetyCode (Extensible)",
        default=None,
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
    status: Optional[Code] = Field(
        description="active | inactive | entered-in-error | unknown",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    statusReason: Optional[ListType[CodeableConcept]] = Field(
        description="online | paused | standby | offline | not-ready | transduc-discon | hw-discon | off",
        default=None,
    )
    distinctIdentifier: Optional[String] = Field(
        description="The distinct identification string",
        default=None,
    )
    distinctIdentifier_ext: Optional[Element] = Field(
        description="Placeholder element for distinctIdentifier extensions",
        default=None,
        alias="_distinctIdentifier",
    )
    manufacturer: Optional[String] = Field(
        description="Name of device manufacturer",
        default=None,
    )
    manufacturer_ext: Optional[Element] = Field(
        description="Placeholder element for manufacturer extensions",
        default=None,
        alias="_manufacturer",
    )
    manufactureDate: Optional[DateTime] = Field(
        description="Date when the device was made",
        default=None,
    )
    manufactureDate_ext: Optional[Element] = Field(
        description="Placeholder element for manufactureDate extensions",
        default=None,
        alias="_manufactureDate",
    )
    expirationDate: Optional[DateTime] = Field(
        description="Date and time of expiry of this device (if applicable)",
        default=None,
    )
    expirationDate_ext: Optional[Element] = Field(
        description="Placeholder element for expirationDate extensions",
        default=None,
        alias="_expirationDate",
    )
    lotNumber: Optional[String] = Field(
        description="Lot number of manufacture",
        default=None,
    )
    lotNumber_ext: Optional[Element] = Field(
        description="Placeholder element for lotNumber extensions",
        default=None,
        alias="_lotNumber",
    )
    serialNumber: Optional[String] = Field(
        description="Serial number assigned by the manufacturer",
        default=None,
    )
    serialNumber_ext: Optional[Element] = Field(
        description="Placeholder element for serialNumber extensions",
        default=None,
        alias="_serialNumber",
    )
    deviceName: Optional[ListType[DeviceDeviceName]] = Field(
        description="The name of the device as given by the manufacturer",
        default=None,
    )
    modelNumber: Optional[String] = Field(
        description="The model number for the device",
        default=None,
    )
    modelNumber_ext: Optional[Element] = Field(
        description="Placeholder element for modelNumber extensions",
        default=None,
        alias="_modelNumber",
    )
    partNumber: Optional[String] = Field(
        description="The part number of the device",
        default=None,
    )
    partNumber_ext: Optional[Element] = Field(
        description="Placeholder element for partNumber extensions",
        default=None,
        alias="_partNumber",
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
    url: Optional[Uri] = Field(
        description="Network address to contact device",
        default=None,
    )
    url_ext: Optional[Element] = Field(
        description="Placeholder element for url extensions",
        default=None,
        alias="_url",
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
