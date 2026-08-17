from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators

from typing import List as ListType, Optional

NoneType = type(None)

import fhircraft.fhir.resources.datatypes.R4.primitive as fhir
from fhircraft.fhir.resources.datatypes.R4.complex import (
    BackboneElement,
    Element,
    Identifier,
    Signature,
    Meta,
)
from .resource import Resource


class BundleLink(BackboneElement):
    """
    A series of links that provide context to this bundle.
    """

    relation: fhir.string = Field(
        description="See http://www.iana.org/assignments/link-relations/link-relations.xhtml#link-relations-1",
    )
    url: fhir.uri = Field(
        description="Reference details for the link",
    )


class BundleEntryLink(BackboneElement):
    """
    A series of links that provide context to this entry.
    """

    relation: Optional[fhir.string] = Field(
        description="See http://www.iana.org/assignments/link-relations/link-relations.xhtml#link-relations-1",
        default=None,
    )
    url: Optional[fhir.uri] = Field(
        description="Reference details for the link",
        default=None,
    )


class BundleEntrySearch(BackboneElement):
    """
    Information about the search process that lead to the creation of this entry.
    """

    mode: Optional[fhir.code] = Field(
        description="match | include | outcome - why this is in the result set",
        default=None,
    )
    score: Optional[fhir.decimal] = Field(
        description="Search ranking (between 0 and 1)",
        default=None,
    )


class BundleEntryRequest(BackboneElement):
    """
    Additional information about how this entry should be processed as part of a transaction or batch.  For history, it shows how the entry was processed to create the version contained in the entry.
    """

    method: fhir.code = Field(
        description="GET | HEAD | POST | PUT | DELETE | PATCH",
    )
    url: fhir.uri = Field(
        description="URL for HTTP equivalent of this entry",
    )
    ifNoneMatch: Optional[fhir.string] = Field(
        description="For managing cache currency",
        default=None,
    )
    ifModifiedSince: Optional[fhir.instant] = Field(
        description="For managing cache currency",
        default=None,
    )
    ifMatch: Optional[fhir.string] = Field(
        description="For managing update contention",
        default=None,
    )
    ifNoneExist: Optional[fhir.string] = Field(
        description="For conditional creates",
        default=None,
    )


class BundleEntryResponse(BackboneElement):
    """
    Indicates the results of processing the corresponding 'request' entry in the batch or transaction being responded to or what the results of an operation where when returning history.
    """

    status: fhir.string = Field(
        description="Status response code (text optional)",
    )
    location: Optional[fhir.uri] = Field(
        description="The location (if the operation returns a location)",
        default=None,
    )
    etag: Optional[fhir.string] = Field(
        description="The Etag for the resource (if relevant)",
        default=None,
    )
    lastModified: Optional[fhir.instant] = Field(
        description="Server\u0027s date time modified",
        default=None,
    )
    outcome: Optional[Resource] = Field(
        description="OperationOutcome with hints and warnings (for batch/transaction)",
        default=None,
    )


class BundleEntry(BackboneElement):
    """
    An entry in a bundle resource - will either contain a resource or information about a resource (transactions and history only).
    """

    link: Optional[ListType[BundleEntryLink]] = Field(
        description="Links related to this entry",
        default=None,
    )
    fullUrl: Optional[fhir.uri] = Field(
        description="URI for resource (Absolute URL server address or URI for UUID/OID)",
        default=None,
    )
    resource: Optional[Resource] = Field(
        description="A resource in the bundle",
        default=None,
    )
    search: Optional[BundleEntrySearch] = Field(
        description="Search related information",
        default=None,
    )
    request: Optional[BundleEntryRequest] = Field(
        description="Additional execution information (transaction/batch/history)",
        default=None,
    )
    response: Optional[BundleEntryResponse] = Field(
        description="Results of execution (transaction/batch/history)",
        default=None,
    )


class Bundle(Resource):
    """
    A container for a collection of resources.
    """

    _abstract = False
    _type = "Bundle"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Bundle"

    identifier: Optional[Identifier] = Field(
        description="Persistent identifier for the bundle",
        default=None,
    )
    type: fhir.code = Field(
        description="document | message | transaction | transaction-response | batch | batch-response | history | searchset | collection",
    )
    timestamp: Optional[fhir.instant] = Field(
        description="When the bundle was assembled",
        default=None,
    )
    total: Optional[fhir.unsignedInt] = Field(
        description="If search, the total number of matches",
        default=None,
    )
    link: Optional[ListType[BundleLink]] = Field(
        description="Links related to this Bundle",
        default=None,
    )
    entry: Optional[ListType[BundleEntry]] = Field(
        description="Entry in the bundle - will have a resource or information",
        default=None,
    )
    signature: Optional[Signature] = Field(
        description="Digital Signature",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_bdl_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="total.empty() or (type = 'searchset') or (type = 'history')",
            human="total only when a search or history",
            key="bdl-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_bdl_2_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="entry.search.empty() or (type = 'searchset')",
            human="entry.search only when a search",
            key="bdl-2",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_bdl_3_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="entry.all(request.exists() = (%resource.type = 'batch' or %resource.type = 'transaction' or %resource.type = 'history'))",
            human="entry.request mandatory for batch/transaction/history, otherwise prohibited",
            key="bdl-3",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_bdl_4_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="entry.all(response.exists() = (%resource.type = 'batch-response' or %resource.type = 'transaction-response' or %resource.type = 'history'))",
            human="entry.response mandatory for batch-response/transaction-response/history, otherwise prohibited",
            key="bdl-4",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_bdl_5_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("entry",),
            expression="resource.exists() or request.exists() or response.exists()",
            human="must be a resource unless there's a request or response",
            key="bdl-5",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_bdl_7_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="(type = 'history') or entry.where(fullUrl.exists()).select(fullUrl&resource.meta.versionId).isDistinct()",
            human="FullUrl must be unique in a bundle, or else entries with the same fullUrl must have different meta.versionId (except in history bundles)",
            key="bdl-7",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_bdl_8_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("entry",),
            expression="fullUrl.contains('/_history/').not()",
            human="fullUrl cannot be a version specific reference",
            key="bdl-8",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_bdl_9_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="type = 'document' implies (identifier.system.exists() and identifier.value.exists())",
            human="A document must have an identifier with a system and a value",
            key="bdl-9",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_bdl_10_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="type = 'document' implies (timestamp.hasValue())",
            human="A document must have a date",
            key="bdl-10",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_bdl_11_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="type = 'document' implies entry.first().resource.is(Composition)",
            human="A document must have a Composition as the first resource",
            key="bdl-11",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_bdl_12_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="type = 'message' implies entry.first().resource.is(MessageHeader)",
            human="A message must have a MessageHeader as the first resource",
            key="bdl-12",
            severity="error",
        )
