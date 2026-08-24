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
    CodeableReference,
    BackboneElement,
    CodeableConcept,
    Quantity,
    Range,
    Attachment,
    Count,
    Duration,
    Reference,
    ContactPoint,
    Annotation,
)
from .resource import Resource
from .domain_resource import DomainResource


class DeviceUdiCarrier(BackboneElement):
    """
    Unique device identifier (UDI) assigned to device label or package.  Note that the Device may include multiple udiCarriers as it either may include just the udiCarrier for the jurisdiction it is sold, or for multiple jurisdictions it could have been sold.
    """

    deviceIdentifier: fhir.string = Field(
        description="Mandatory fixed portion of UDI",
    )
    issuer: fhir.uri = Field(
        description="UDI Issuing Organization",
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
        description="barcode | rfid | manual | card | self-reported | electronic-transmission | unknown",
        default=None,
    )


class DeviceName(BackboneElement):
    """
    This represents the manufacturer's name of the device as provided by the device, from a UDI label, or by a person describing the Device.  This typically would be used when a person provides the name(s) or when the device represents one of the names available from DeviceDefinition.
    """

    value: fhir.string = Field(
        description="The term that names the device",
    )
    type: fhir.code = Field(
        description="registered-name | user-friendly-name | patient-reported-name",
    )
    display: Optional[fhir.boolean] = Field(
        description="The preferred device name",
        default=None,
    )


class DeviceVersion(BackboneElement):
    """
    The actual design of the device or software version running on the device.
    """

    type: Optional[CodeableConcept] = Field(
        description="The type of the device version, e.g. manufacturer, approved, internal",
        default=None,
    )
    component: Optional[Identifier] = Field(
        description="The hardware or software module of the device to which the version applies",
        default=None,
    )
    installDate: Optional[fhir.dateTime] = Field(
        description="The date the version was installed on the device",
        default=None,
    )
    value: fhir.string = Field(
        description="The version text",
    )


class DeviceConformsTo(BackboneElement):
    """
    Identifies the standards, specifications, or formal guidances for the capabilities supported by the device. The device may be certified as conformant to these specifications e.g., communication, performance, process, measurement, or specialization standards.
    """

    category: Optional[CodeableConcept] = Field(
        description="Describes the common type of the standard, specification, or formal guidance.  communication | performance | measurement",
        default=None,
    )
    specification: CodeableConcept = Field(
        description="Identifies the standard, specification, or formal guidance that the device adheres to",
    )
    version: Optional[fhir.string] = Field(
        description="Specific form or variant of the standard",
        default=None,
    )


class DeviceProperty(BackboneElement):
    """
    Static or essentially fixed characteristics or features of the device (e.g., time or timing attributes, resolution, accuracy, intended use or instructions for use, and physical attributes) that are not otherwise captured in more specific attributes.
    """

    type: CodeableConcept = Field(
        description="code that specifies the property being represented",
    )
    valueQuantity: Optional[Quantity] = Field(
        description="Value of the property",
        default=None,
    )
    valueCodeableConcept: Optional[CodeableConcept] = Field(
        description="Value of the property",
        default=None,
    )
    valueString: Optional[fhir.string] = Field(
        description="Value of the property",
        default=None,
    )
    valueBoolean: Optional[fhir.boolean] = Field(
        description="Value of the property",
        default=None,
    )
    valueInteger: Optional[fhir.integer] = Field(
        description="Value of the property",
        default=None,
    )
    valueRange: Optional[Range] = Field(
        description="Value of the property",
        default=None,
    )
    valueAttachment: Optional[Attachment] = Field(
        description="Value of the property",
        default=None,
    )

    @property
    def value(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="value",
        )

    @model_validator(mode="after")
    def value_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[
                Quantity,
                CodeableConcept,
                fhir.String,
                fhir.Boolean,
                fhir.Integer,
                Range,
                Attachment,
            ],
            field_name_base="value",
            required=True,
        )


class Device(DomainResource):
    """
    This resource describes the properties (regulated, has real time clock, etc.), adminstrative (manufacturer name, model number, serial number, firmware, etc.), and type (knee replacement, blood pressure cuff, MRI, etc.) of a physical unit (these values do not change much within a given module, for example the serail number, manufacturer name, and model number). An actual unit may consist of several modules in a distinct hierarchy and these are represented by multiple Device resources and bound through the 'parent' element.
    """

    _abstract = False
    _type = "Device"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Device"

    identifier: Optional[ListType[Identifier]] = Field(
        description="Instance identifier",
        default=None,
    )
    displayName: Optional[fhir.string] = Field(
        description="The name used to display by default when the device is referenced",
        default=None,
    )
    definition: Optional[CodeableReference] = Field(
        description="The reference to the definition for the device",
        default=None,
    )
    udiCarrier: Optional[ListType[DeviceUdiCarrier]] = Field(
        description="Unique Device Identifier (UDI) Barcode string",
        default=None,
    )
    status: Optional[fhir.code] = Field(
        description="active | inactive | entered-in-error",
        default=None,
    )
    availabilityStatus: Optional[CodeableConcept] = Field(
        description="lost | damaged | destroyed | available",
        default=None,
    )
    biologicalSourceEvent: Optional[Identifier] = Field(
        description="An identifier that supports traceability to the event during which material in this product from one or more biological entities was obtained or pooled",
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
    name: Optional[ListType[DeviceName]] = Field(
        description="The name or names of the device as known to the manufacturer and/or patient",
        default=None,
    )
    modelNumber: Optional[fhir.string] = Field(
        description="The manufacturer\u0027s model number for the device",
        default=None,
    )
    partNumber: Optional[fhir.string] = Field(
        description="The part number or catalog number of the device",
        default=None,
    )
    category: Optional[ListType[CodeableConcept]] = Field(
        description="Indicates a high-level grouping of the device",
        default=None,
    )
    type: Optional[ListType[CodeableConcept]] = Field(
        description="The kind or type of device",
        default=None,
    )
    version: Optional[ListType[DeviceVersion]] = Field(
        description="The actual design of the device or software version running on the device",
        default=None,
    )
    conformsTo: Optional[ListType[DeviceConformsTo]] = Field(
        description="Identifies the standards, specifications, or formal guidances for the capabilities supported by the device",
        default=None,
    )
    property_: Optional[ListType[DeviceProperty]] = Field(
        description="Inherent, essentially fixed, characteristics of the device.  e.g., time properties, size, material, etc.",
        default=None,
        alias="property",
    )
    mode: Optional[CodeableConcept] = Field(
        description="The designated condition for performing a task",
        default=None,
    )
    cycle: Optional[Count] = Field(
        description="The series of occurrences that repeats during the operation of the device",
        default=None,
    )
    duration: Optional[Duration] = Field(
        description="A measurement of time during the device\u0027s operation (e.g., days, hours, mins, etc.)",
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
    endpoint: Optional[ListType[Reference]] = Field(
        description="Technical endpoints providing access to electronic services provided by the device",
        default=None,
    )
    gateway: Optional[ListType[CodeableReference]] = Field(
        description="Linked device acting as a communication/data collector, translator or controller",
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
        description="The higher level or encompassing device that this device is a logical part of",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_dev_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.where(display=true).count() <= 1",
            human="only one Device.name.display SHALL be true when there is more than one Device.name",
            key="dev-1",
            severity="error",
        )
