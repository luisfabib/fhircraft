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
    CodeableConcept,
    Reference,
    ContactPoint,
    Period,
    BackboneElement,
)
from .resource import Resource
from .domain_resource import DomainResource

class EndpointPayload(BackboneElement):
    """
    The set of payloads that are provided/available at this endpoint.
    """

    type: Optional[ListType[CodeableConcept]] = Field(
        description="The type of content that may be used at this endpoint (e.g. XDS Discharge summaries)",
        default=None,
    )
    mimeType: Optional[ListType[Code]] = Field(
        description="Mimetype to send. If not specified, the content could be anything (including no payload, if the connectionType defined this)",
        default=None,
    )

class Endpoint(DomainResource):
    """
    The technical details of an endpoint that can be used for electronic services, such as for web services providing XDS.b, a REST endpoint for another FHIR server, or a s/Mime email address. This may include any security context information.
    """

    _abstract = False
    _type = "Endpoint"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Endpoint"

    identifier: Optional[ListType[Identifier]] = Field(
        description="Identifies this endpoint across multiple systems",
        default=None,
    )
    status: Optional[Code] = Field(
        description="active | suspended | error | off | entered-in-error | test",
        default=None,
    )
    connectionType: Optional[ListType[CodeableConcept]] = Field(
        description="Protocol/Profile/Standard to be used with this endpoint connection",
        default=None,
    )
    name: Optional[String] = Field(
        description="A name that this endpoint can be identified by",
        default=None,
    )
    description: Optional[String] = Field(
        description="Additional details about the endpoint that could be displayed as further information to identify the description beyond its name",
        default=None,
    )
    environmentType: Optional[ListType[CodeableConcept]] = Field(
        description="The type of environment(s) exposed at this endpoint",
        default=None,
    )
    managingOrganization: Optional[Reference] = Field(
        description="Organization that manages this endpoint (might not be the organization that exposes the endpoint)",
        default=None,
    )
    contact: Optional[ListType[ContactPoint]] = Field(
        description="Contact details for source (e.g. troubleshooting)",
        default=None,
    )
    period: Optional[Period] = Field(
        description="Interval the endpoint is expected to be operational",
        default=None,
    )
    payload: Optional[ListType[EndpointPayload]] = Field(
        description="Set of payloads that are provided by this endpoint",
        default=None,
    )
    address: Optional[Url] = Field(
        description="The technical base address for connecting to this endpoint",
        default=None,
    )
    header: Optional[ListType[String]] = Field(
        description="Usage depends on the channel type",
        default=None,
    )
