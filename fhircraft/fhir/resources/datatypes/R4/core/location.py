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
    Coding,
    CodeableConcept,
    ContactPoint,
    Address,
    BackboneElement,
    Reference,
)
from .resource import Resource
from .domain_resource import DomainResource

class LocationPosition(BackboneElement):
    """
    The absolute geographic location of the Location, expressed using the WGS84 datum (This is the same co-ordinate system used in KML).
    """

    longitude: fhir.decimal = Field(
        description="Longitude with WGS84 datum",
    )
    latitude: fhir.decimal = Field(
        description="Latitude with WGS84 datum",
    )
    altitude: Optional[fhir.decimal] = Field(
        description="Altitude with WGS84 datum",
        default=None,
    )

class LocationHoursOfOperation(BackboneElement):
    """
    What days/times during a week is this location usually open.
    """

    daysOfWeek: Optional[ListType[fhir.code]] = Field(
        description="mon | tue | wed | thu | fri | sat | sun",
        default=None,
    )
    allDay: Optional[fhir.boolean] = Field(
        description="The Location is open all day",
        default=None,
    )
    openingTime: Optional[fhir.time_] = Field(
        description="time that the Location opens",
        default=None,
    )
    closingTime: Optional[fhir.time_] = Field(
        description="time that the Location closes",
        default=None,
    )

class Location(DomainResource):
    """
    Details and position information for a physical place where services are provided and resources and participants may be stored, found, contained, or accommodated.
    """

    _abstract = False
    _type = "Location"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Location"

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
        description="Unique code or number identifying the location to its users",
        default=None,
    )
    status: Optional[fhir.code] = Field(
        description="active | suspended | inactive",
        default=None,
    )
    operationalStatus: Optional[Coding] = Field(
        description="The operational status of the location (typically only for a bed/room)",
        default=None,
    )
    name: Optional[fhir.string] = Field(
        description="Name of the location as used by humans",
        default=None,
    )
    alias: Optional[ListType[fhir.string]] = Field(
        description="A list of alternate names that the location is known as, or was known as, in the past",
        default=None,
    )
    description: Optional[fhir.string] = Field(
        description="Additional details about the location that could be displayed as further information to identify the location beyond its name",
        default=None,
    )
    mode: Optional[fhir.code] = Field(
        description="instance | kind",
        default=None,
    )
    type: Optional[ListType[CodeableConcept]] = Field(
        description="Type of function performed",
        default=None,
    )
    telecom: Optional[ListType[ContactPoint]] = Field(
        description="Contact details of the location",
        default=None,
    )
    address: Optional[Address] = Field(
        description="Physical location",
        default=None,
    )
    physicalType: Optional[CodeableConcept] = Field(
        description="Physical form of the location",
        default=None,
    )
    position: Optional[LocationPosition] = Field(
        description="The absolute geographic location",
        default=None,
    )
    managingOrganization: Optional[Reference] = Field(
        description="Organization responsible for provisioning and upkeep",
        default=None,
    )
    partOf: Optional[Reference] = Field(
        description="Another Location this one is physically a part of",
        default=None,
    )
    hoursOfOperation: Optional[ListType[LocationHoursOfOperation]] = Field(
        description="What days/times during a week is this location usually open",
        default=None,
    )
    availabilityExceptions: Optional[fhir.string] = Field(
        description="Description of availability exceptions",
        default=None,
    )
    endpoint: Optional[ListType[Reference]] = Field(
        description="Technical endpoints providing access to services operated for the location",
        default=None,
    )
