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
    BackboneElement,
    Period,
    Reference,
    CodeableConcept,
    RelatedArtifact,
    ProductShelfLife,
    Quantity,
    Range,
    Attachment,
    ContactPoint,
    Coding,
    CodeableReference,
    Annotation,
    UsageContext,
)
from .resource import Resource
from .domain_resource import DomainResource

class DeviceDefinitionUdiDeviceIdentifier(BackboneElement):
    """
    Unique device identifier (UDI) assigned to device label or package.  Note that the Device may include multiple udiCarriers as it either may include just the udiCarrier for the jurisdiction it is sold, or for multiple jurisdictions it could have been sold.
    """

    deviceIdentifier: Optional[String] = Field(
        description="The identifier that is to be associated with every Device that references this DeviceDefintiion for the issuer and jurisdiction provided in the DeviceDefinition.udiDeviceIdentifier",
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
    marketDistribution: Optional[
        ListType["DeviceDefinitionUdiDeviceIdentifierMarketDistribution"]
    ] = Field(
        description="Indicates whether and when the device is available on the market",
        default=None,
    )

class DeviceDefinitionRegulatoryIdentifier(BackboneElement):
    """
    Identifier associated with the regulatory documentation (certificates, technical documentation, post-market surveillance documentation and reports) of a set of device models sharing the same intended purpose, risk class and essential design and manufacturing characteristics. One example is the Basic UDI-DI in Europe.
    """

    type: Optional[Code] = Field(
        description="basic | master | license",
        default=None,
    )
    deviceIdentifier: Optional[String] = Field(
        description="The identifier itself",
        default=None,
    )
    issuer: Optional[Uri] = Field(
        description="The organization that issued this identifier",
        default=None,
    )
    jurisdiction: Optional[Uri] = Field(
        description="The jurisdiction to which the deviceIdentifier applies",
        default=None,
    )

class DeviceDefinitionDeviceName(BackboneElement):
    """
    The name or names of the device as given by the manufacturer.
    """

    name: Optional[String] = Field(
        description="A name that is used to refer to the device",
        default=None,
    )
    type: Optional[Code] = Field(
        description="registered-name | user-friendly-name | patient-reported-name",
        default=None,
    )

class DeviceDefinitionClassification(BackboneElement):
    """
    What kind of device or device system this is.
    """

    type: Optional[CodeableConcept] = Field(
        description="A classification or risk class of the device model",
        default=None,
    )
    justification: Optional[ListType[RelatedArtifact]] = Field(
        description="Further information qualifying this classification of the device model",
        default=None,
    )

class DeviceDefinitionConformsTo(BackboneElement):
    """
    Identifies the standards, specifications, or formal guidances for the capabilities supported by the device. The device may be certified as conformant to these specifications e.g., communication, performance, process, measurement, or specialization standards.
    """

    category: Optional[CodeableConcept] = Field(
        description="Describes the common type of the standard, specification, or formal guidance",
        default=None,
    )
    specification: Optional[CodeableConcept] = Field(
        description="Identifies the standard, specification, or formal guidance that the device adheres to the Device Specification type",
        default=None,
    )
    version: Optional[ListType[String]] = Field(
        description="The specific form or variant of the standard, specification or formal guidance",
        default=None,
    )
    source: Optional[ListType[RelatedArtifact]] = Field(
        description="Standard, regulation, certification, or guidance website, document, or other publication, or similar, supporting the conformance",
        default=None,
    )

class DeviceDefinitionHasPart(BackboneElement):
    """
    A device that is part (for example a component) of the present device.
    """

    reference: Optional[Reference] = Field(
        description="Reference to the part",
        default=None,
    )
    count: Optional[Integer] = Field(
        description="Number of occurrences of the part",
        default=None,
    )

class DeviceDefinitionPackagingDistributor(BackboneElement):
    """
    An organization that distributes the packaged device.
    """

    name: Optional[String] = Field(
        description="Distributor\u0027s human-readable name",
        default=None,
    )
    organizationReference: Optional[ListType[Reference]] = Field(
        description="Distributor as an Organization resource",
        default=None,
    )

class DeviceDefinitionUdiDeviceIdentifierMarketDistribution(BackboneElement):
    """
    Indicates where and when the device is available on the market.
    """

    marketPeriod: Optional[Period] = Field(
        description="Begin and end dates for the commercial distribution of the device",
        default=None,
    )
    subJurisdiction: Optional[Uri] = Field(
        description="National state or territory where the device is commercialized",
        default=None,
    )

class DeviceDefinitionPackagingUdiDeviceIdentifier(BackboneElement):
    """
    Unique Device Identifier (UDI) Barcode string on the packaging.
    """

    deviceIdentifier: Optional[String] = Field(
        description="The identifier that is to be associated with every Device that references this DeviceDefintiion for the issuer and jurisdiction provided in the DeviceDefinition.udiDeviceIdentifier",
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
    marketDistribution: Optional[
        ListType[DeviceDefinitionUdiDeviceIdentifierMarketDistribution]
    ] = Field(
        description="Indicates whether and when the device is available on the market",
        default=None,
    )

class DeviceDefinitionPackaging(BackboneElement):
    """
    Information about the packaging of the device, i.e. how the device is packaged.
    """

    identifier: Optional[Identifier] = Field(
        description="Business identifier of the packaged medication",
        default=None,
    )
    type: Optional[CodeableConcept] = Field(
        description="A code that defines the specific type of packaging",
        default=None,
    )
    count: Optional[Integer] = Field(
        description="The number of items contained in the package (devices or sub-packages)",
        default=None,
    )
    distributor: Optional[ListType[DeviceDefinitionPackagingDistributor]] = Field(
        description="An organization that distributes the packaged device",
        default=None,
    )
    udiDeviceIdentifier: Optional[
        ListType[DeviceDefinitionPackagingUdiDeviceIdentifier]
    ] = Field(
        description="Unique Device Identifier (UDI) Barcode string on the packaging",
        default=None,
    )
    packaging: Optional[ListType["DeviceDefinitionPackaging"]] = Field(
        description="Allows packages within packages",
        default=None,
    )

class DeviceDefinitionVersion(BackboneElement):
    """
    The version of the device or software.
    """

    type: Optional[CodeableConcept] = Field(
        description="The type of the device version, e.g. manufacturer, approved, internal",
        default=None,
    )
    component: Optional[Identifier] = Field(
        description="The hardware or software module of the device to which the version applies",
        default=None,
    )
    value: Optional[String] = Field(
        description="The version text",
        default=None,
    )

class DeviceDefinitionProperty(BackboneElement):
    """
    Static or essentially fixed characteristics or features of this kind of device that are otherwise not captured in more specific attributes, e.g., time or timing attributes, resolution, accuracy, and physical attributes.
    """

    type: Optional[CodeableConcept] = Field(
        description="Code that specifies the property being represented",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="Value of the property",
        default=None,
    )
    valueCodeableConcept: Optional[CodeableConcept] = Field(
        description="Value of the property",
        default=None,
    )
    valueString: Optional[String] = Field(
        description="Value of the property",
        default=None,
    )
    valueBoolean: Optional[Boolean] = Field(
        description="Value of the property",
        default=None,
    )
    valueInteger: Optional[Integer] = Field(
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
                String,
                Boolean,
                Integer,
                Range,
                Attachment,
            ],
            field_name_base="value",
            required=True,
        )

class DeviceDefinitionLink(BackboneElement):
    """
    An associated device, attached to, used with, communicating with or linking a previous or new device model to the focal device.
    """

    relation: Optional[Coding] = Field(
        description="The type indicates the relationship of the related device to the device instance",
        default=None,
    )
    relatedDevice: Optional[CodeableReference] = Field(
        description="A reference to the linked device",
        default=None,
    )

class DeviceDefinitionMaterial(BackboneElement):
    """
    A substance used to create the material(s) of which the device is made.
    """

    substance: Optional[CodeableConcept] = Field(
        description="A relevant substance that the device contains, may contain, or is made of",
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

class DeviceDefinitionGuideline(BackboneElement):
    """
    Information aimed at providing directions for the usage of this model of device.
    """

    useContext: Optional[ListType[UsageContext]] = Field(
        description="The circumstances that form the setting for using the device",
        default=None,
    )
    usageInstruction: Optional[Markdown] = Field(
        description="Detailed written and visual directions for the user on how to use the device",
        default=None,
    )
    relatedArtifact: Optional[ListType[RelatedArtifact]] = Field(
        description="A source of information or reference for this guideline",
        default=None,
    )
    indication: Optional[ListType[CodeableConcept]] = Field(
        description="A clinical condition for which the device was designed to be used",
        default=None,
    )
    contraindication: Optional[ListType[CodeableConcept]] = Field(
        description="A specific situation when a device should not be used because it may cause harm",
        default=None,
    )
    warning: Optional[ListType[CodeableConcept]] = Field(
        description="Specific hazard alert information that a user needs to know before using the device",
        default=None,
    )
    intendedUse: Optional[String] = Field(
        description="A description of the general purpose or medical use of the device or its function",
        default=None,
    )

class DeviceDefinitionCorrectiveAction(BackboneElement):
    """
    Tracking of latest field safety corrective action.
    """

    recall: Optional[Boolean] = Field(
        description="Whether the corrective action was a recall",
        default=None,
    )
    scope: Optional[Code] = Field(
        description="model | lot-numbers | serial-numbers",
        default=None,
    )
    period: Optional[Period] = Field(
        description="Start and end dates of the  corrective action",
        default=None,
    )

class DeviceDefinitionChargeItem(BackboneElement):
    """
    Billing code or reference associated with the device.
    """

    chargeItemCode: Optional[CodeableReference] = Field(
        description="The code or reference for the charge item",
        default=None,
    )
    count: Optional[Quantity] = Field(
        description="Coefficient applicable to the billing code",
        default=None,
    )
    effectivePeriod: Optional[Period] = Field(
        description="A specific time period in which this charge item applies",
        default=None,
    )
    useContext: Optional[ListType[UsageContext]] = Field(
        description="The context to which this charge item applies",
        default=None,
    )

class DeviceDefinition(DomainResource):
    """
    This is a specialized resource that defines the characteristics and capabilities of a device.
    """

    _abstract = False
    _type = "DeviceDefinition"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/DeviceDefinition"

    description: Optional[Markdown] = Field(
        description="Additional information to describe the device",
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
    regulatoryIdentifier: Optional[ListType[DeviceDefinitionRegulatoryIdentifier]] = (
        Field(
            description="Regulatory identifier(s) associated with this device",
            default=None,
        )
    )
    partNumber: Optional[String] = Field(
        description="The part number or catalog number of the device",
        default=None,
    )
    manufacturer: Optional[Reference] = Field(
        description="Name of device manufacturer",
        default=None,
    )
    deviceName: Optional[ListType[DeviceDefinitionDeviceName]] = Field(
        description="The name or names of the device as given by the manufacturer",
        default=None,
    )
    modelNumber: Optional[String] = Field(
        description="The catalog or model number for the device for example as defined by the manufacturer",
        default=None,
    )
    classification: Optional[ListType[DeviceDefinitionClassification]] = Field(
        description="What kind of device or device system this is",
        default=None,
    )
    conformsTo: Optional[ListType[DeviceDefinitionConformsTo]] = Field(
        description="Identifies the standards, specifications, or formal guidances for the capabilities supported by the device",
        default=None,
    )
    hasPart: Optional[ListType[DeviceDefinitionHasPart]] = Field(
        description="A device, part of the current one",
        default=None,
    )
    packaging: Optional[ListType[DeviceDefinitionPackaging]] = Field(
        description="Information about the packaging of the device, i.e. how the device is packaged",
        default=None,
    )
    version: Optional[ListType[DeviceDefinitionVersion]] = Field(
        description="The version of the device or software",
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
    languageCode: Optional[ListType[CodeableConcept]] = Field(
        description="Language code for the human-readable text strings produced by the device (all supported)",
        default=None,
    )
    property_: Optional[ListType[DeviceDefinitionProperty]] = Field(
        description="Inherent, essentially fixed, characteristics of this kind of device, e.g., time properties, size, etc",
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
    link: Optional[ListType[DeviceDefinitionLink]] = Field(
        description="An associated device, attached to, used with, communicating with or linking a previous or new device model to the focal device",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Device notes and comments",
        default=None,
    )
    material: Optional[ListType[DeviceDefinitionMaterial]] = Field(
        description="A substance used to create the material(s) of which the device is made",
        default=None,
    )
    productionIdentifierInUDI: Optional[ListType[Code]] = Field(
        description="lot-number | manufactured-date | serial-number | expiration-date | biological-source | software-version",
        default=None,
    )
    guideline: Optional[DeviceDefinitionGuideline] = Field(
        description="Information aimed at providing directions for the usage of this model of device",
        default=None,
    )
    correctiveAction: Optional[DeviceDefinitionCorrectiveAction] = Field(
        description="Tracking of latest field safety corrective action",
        default=None,
    )
    chargeItem: Optional[ListType[DeviceDefinitionChargeItem]] = Field(
        description="Billing code or reference associated with the device",
        default=None,
    )
