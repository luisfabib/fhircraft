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
    Reference,
    ContactPoint,
    Period,
)
from .resource import Resource
from .domain_resource import DomainResource

class Endpoint(DomainResource):
    """
    The technical details of an endpoint that can be used for electronic services, such as for web services providing XDS.b or a REST endpoint for another FHIR server. This may include any security context information.
    """

    _abstract = False
    _type = "Endpoint"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Endpoint"

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
        description="Identifies this endpoint across multiple systems",
        default=None,
    )
    status: fhir.code = Field(
        description="active | suspended | error | off | entered-in-error | test",
    )
    connectionType: Coding = Field(
        description="Protocol/Profile/Standard to be used with this endpoint connection",
    )
    name: Optional[fhir.string] = Field(
        description="A name that this endpoint can be identified by",
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
    payloadType: ListType[CodeableConcept] = Field(
        description="The type of content that may be used at this endpoint (e.g. XDS Discharge summaries)",
    )
    payloadMimeType: Optional[ListType[fhir.code]] = Field(
        description="Mimetype to send. If not specified, the content could be anything (including no payload, if the connectionType defined this)",
        default=None,
    )
    address: fhir.url = Field(
        description="The technical base address for connecting to this endpoint",
    )
    header: Optional[ListType[fhir.string]] = Field(
        description="Usage depends on the channel type",
        default=None,
    )
