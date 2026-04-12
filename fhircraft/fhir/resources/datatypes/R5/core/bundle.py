from pydantic import Field, model_validator
from typing import List as ListType, Optional

NoneType = type(None)

import fhircraft.fhir.resources.validators as fhir_validators
import fhircraft.fhir.resources.datatypes.R5.primitive as fhir
from fhircraft.fhir.resources.datatypes.R5.complex import (
    BackboneElement,
    Element,
    Identifier,
    Meta,
    Signature,
)
from .resource import Resource


class BundleLink(BackboneElement):
    """
    A series of links that provide context to this bundle.
    """

    relation: Optional[fhir.code] = Field(
        description="See http://www.iana.org/assignments/link-relations/link-relations.xhtml#link-relations-1",
        default=None,
    )
    url: Optional[fhir.uri] = Field(
        description="Reference details for the link",
        default=None,
    )


class BundleEntryLink(BackboneElement):
    """
    A series of links that provide context to this entry.
    """

    relation: Optional[fhir.code] = Field(
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
        description="match | include - why this is in the result set",
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

    method: Optional[fhir.code] = Field(
        description="GET | HEAD | POST | PUT | DELETE | PATCH",
        default=None,
    )
    url: Optional[fhir.uri] = Field(
        description="URL for HTTP equivalent of this entry",
        default=None,
    )
    ifNoneMatch: Optional[fhir.string] = Field(
        description="For managing cache validation",
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

    status: Optional[fhir.string] = Field(
        description="Status response code (text optional)",
        default=None,
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
        description="URI for resource (e.g. the absolute URL server address, URI for UUID/OID, etc.)",
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
    type: Optional[fhir.code] = Field(
        description="document | message | transaction | transaction-response | batch | batch-response | history | searchset | collection | subscription-notification",
        default=None,
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
    issues: Optional[Resource] = Field(
        description="Issues with the Bundle",
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
            expression="(type = 'searchset') or entry.search.empty()",
            human="entry.search only when a search",
            key="bdl-2",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_bdl_3a_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="type in ('document' | 'message' | 'searchset' | 'collection') implies entry.all(resource.exists() and request.empty() and response.empty())",
            human="For collections of type document, message, searchset or collection, all entries must contain resources, and not have request or response elements",
            key="bdl-3a",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_bdl_3b_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="type = 'history' implies entry.all(request.exists() and response.exists() and ((request.method in ('POST' | 'PATCH' | 'PUT')) = resource.exists()))",
            human="For collections of type history, all entries must contain request or response elements, and resources if the method is POST, PUT or PATCH",
            key="bdl-3b",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_bdl_3c_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="type in ('transaction' | 'batch') implies entry.all(request.method.exists() and ((request.method in ('POST' | 'PATCH' | 'PUT')) = resource.exists()))",
            human="For collections of type transaction or batch, all entries must contain request elements, and resources if the method is POST, PUT or PATCH",
            key="bdl-3c",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_bdl_3d_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="type in ('transaction-response' | 'batch-response') implies entry.all(response.exists())",
            human="For collections of type transaction-response or batch-response, all entries must contain response elements",
            key="bdl-3d",
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
            expression="(type = 'history') or entry.where(fullUrl.exists()).select(fullUrl&iif(resource.meta.versionId.exists(), resource.meta.versionId, '')).isDistinct()",
            human="FullUrl must be unique in a bundle, or else entries with the same fullUrl must have different meta.versionId (except in history bundles)",
            key="bdl-7",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_bdl_8_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("entry",),
            expression="fullUrl.exists() implies fullUrl.contains('/_history/').not()",
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

    @model_validator(mode="after")
    def FHIR_bdl_13_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="type = 'subscription-notification' implies entry.first().resource.is(SubscriptionStatus)",
            human="A subscription-notification must have a SubscriptionStatus as the first resource",
            key="bdl-13",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_bdl_14_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="type = 'history' implies entry.request.method != 'PATCH'",
            human="entry.request.method PATCH not allowed for history",
            key="bdl-14",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_bdl_15_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="type='transaction' or type='transaction-response' or type='batch' or type='batch-response' or entry.all(fullUrl.exists() or request.method='POST')",
            human="Bundle resources where type is not transaction, transaction-response, batch, or batch-response or when the request is a POST SHALL have Bundle.entry.fullUrl populated",
            key="bdl-15",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_bdl_16_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="issues.exists() implies (issues.issue.severity = 'information' or issues.issue.severity = 'warning')",
            human="Issue.severity for all issues within the OperationOutcome must be either 'information' or 'warning'.",
            key="bdl-16",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_bdl_17_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="type = 'document' implies issues.empty()",
            human="Use and meaning of issues for documents has not been validated because the content will not be rendered in the document.",
            key="bdl-17",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_bdl_18_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="type = 'searchset' implies link.where(relation = 'self' and url.exists()).exists()",
            human="Self link is required for searchsets.",
            key="bdl-18",
            severity="error",
        )
