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
    BackboneElement,
    Reference,
    CodeableConcept,
    ProductShelfLife,
    Annotation,
    ProdCharacteristic,
    Quantity,
    ContactPoint,
)
from .resource import Resource
from .domain_resource import DomainResource

class DeviceDefinitionUdiDeviceIdentifier(BackboneElement):
    """
    Unique device identifier (UDI) assigned to device label or package.  Note that the Device may include multiple udiCarriers as it either may include just the udiCarrier for the jurisdiction it is sold, or for multiple jurisdictions it could have been sold.
    """

    deviceIdentifier: Optional[String] = Field(
        description="The identifier that is to be associated with every Device that references this DeviceDefintiion for the issuer and jurisdication porvided in the DeviceDefinition.udiDeviceIdentifier",
        default=None,
    )
    issuer: Optional[Uri] = Field(
        description="The organization that assigns the identifier algorithm",
        default=None,
    )
    jurisdiction: Optional[Uri] = Field(
        description="The jurisdiction to which the deviceIdentifier applies",
        default=None,
    )

class DeviceDefinitionDeviceName(BackboneElement):
    """
    A name given to the device to identify it.
    """

    name: Optional[String] = Field(
        description="The name of the device",
        default=None,
    )
    type: Optional[Code] = Field(
        description="udi-label-name | user-friendly-name | patient-reported-name | manufacturer-name | model-name | other",
        default=None,
    )

class DeviceDefinitionSpecialization(BackboneElement):
    """
    The capabilities supported on a  device, the standards to which the device conforms for a particular purpose, and used for the communication.
    """

    systemType: Optional[String] = Field(
        description="The standard that is used to operate and communicate",
        default=None,
    )
    version: Optional[String] = Field(
        description="The version of the standard that is used to operate and communicate",
        default=None,
    )

class DeviceDefinitionCapability(BackboneElement):
    """
    Device capabilities.
    """

    type: Optional[CodeableConcept] = Field(
        description="Type of capability",
        default=None,
    )
    description: Optional[ListType[CodeableConcept]] = Field(
        description="Description of capability",
        default=None,
    )

class DeviceDefinitionProperty(BackboneElement):
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

class DeviceDefinitionMaterial(BackboneElement):
    """
    A substance used to create the material(s) of which the device is made.
    """

    substance: Optional[CodeableConcept] = Field(
        description="The substance",
        default=None,
    )
    alternate: Optional[Boolean] = Field(
        description="Indicates an alternative material of the device",
        default=None,
    )
    allergenicIndicator: Optional[Boolean] = Field(
        description="Whether the substance is a known or suspected allergen",
        default=None,
    )

class DeviceDefinition(DomainResource):
    """
    The characteristics, operational status and capabilities of a medical-related component of a medical device.
    """

    _abstract = False
    _type = "DeviceDefinition"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/DeviceDefinition"

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
    udiDeviceIdentifier: Optional[ListType[DeviceDefinitionUdiDeviceIdentifier]] = (
        Field(
            description="Unique Device Identifier (UDI) Barcode string",
            default=None,
        )
    )
    manufacturerString: Optional[String] = Field(
        description="Name of device manufacturer",
        default=None,
    )
    manufacturerReference: Optional[Reference] = Field(
        description="Name of device manufacturer",
        default=None,
    )
    deviceName: Optional[ListType[DeviceDefinitionDeviceName]] = Field(
        description="A name given to the device to identify it",
        default=None,
    )
    modelNumber: Optional[String] = Field(
        description="The model number for the device",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="What kind of device or device system this is",
        default=None,
    )
    specialization: Optional[ListType[DeviceDefinitionSpecialization]] = Field(
        description="The capabilities supported on a  device, the standards to which the device conforms for a particular purpose, and used for the communication",
        default=None,
    )
    version: Optional[ListType[String]] = Field(
        description="Available versions",
        default=None,
    )
    safety: Optional[ListType[CodeableConcept]] = Field(
        description="Safety characteristics of the device",
        default=None,
    )
    shelfLifeStorage: Optional[ListType[ProductShelfLife]] = Field(
        description="Shelf Life and storage information",
        default=None,
    )
    physicalCharacteristics: Optional[ProdCharacteristic] = Field(
        description="Dimensions, color etc.",
        default=None,
    )
    languageCode: Optional[ListType[CodeableConcept]] = Field(
        description="Language code for the human-readable text strings produced by the device (all supported)",
        default=None,
    )
    capability: Optional[ListType[DeviceDefinitionCapability]] = Field(
        description="Device capabilities",
        default=None,
    )
    property_: Optional[ListType[DeviceDefinitionProperty]] = Field(
        description="The actual configuration settings of a device as it actually operates, e.g., regulation status, time properties",
        default=None,
        alias="property",
    )
    owner: Optional[Reference] = Field(
        description="Organization responsible for device",
        default=None,
    )
    contact: Optional[ListType[ContactPoint]] = Field(
        description="Details for human/organization for support",
        default=None,
    )
    url: Optional[Uri] = Field(
        description="Network address to contact device",
        default=None,
    )
    onlineInformation: Optional[Uri] = Field(
        description="Access to on-line information",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Device notes and comments",
        default=None,
    )
    quantity: Optional[Quantity] = Field(
        description="The quantity of the device present in the packaging (e.g. the number of devices present in a pack, or the number of devices in the same package of the medicinal product)",
        default=None,
    )
    parentDevice: Optional[Reference] = Field(
        description="The parent device it can be part of",
        default=None,
    )
    material: Optional[ListType[DeviceDefinitionMaterial]] = Field(
        description="A substance used to create the material(s) of which the device is made",
        default=None,
    )

    @property
    def manufacturer(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="manufacturer",
        )

    @model_validator(mode="after")
    def manufacturer_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[String, Reference],
            field_name_base="manufacturer",
            required=False,
        )
