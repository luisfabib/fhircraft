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
    Reference,
    Period,
    BackboneElement,
    CodeableConcept,
    Coding,
    Expression,
)
from .resource import Resource
from .domain_resource import DomainResource

class PermissionJustification(BackboneElement):
    """
    The asserted justification for using the data.
    """

    basis: Optional[ListType[CodeableConcept]] = Field(
        description="The regulatory grounds upon which this Permission builds",
        default=None,
    )
    evidence: Optional[ListType[Reference]] = Field(
        description="Justifing rational",
        default=None,
    )

class PermissionRuleDataResource(BackboneElement):
    """
    Explicit FHIR Resource references.
    """

    meaning: Optional[fhir.code] = Field(
        description="instance | related | dependents | authoredby",
        default=None,
    )
    reference: Optional[Reference] = Field(
        description="The actual data reference",
        default=None,
    )

class PermissionRuleData(BackboneElement):
    """
    A description or definition of which activities are allowed to be done on the data.
    """

    resource: Optional[ListType[PermissionRuleDataResource]] = Field(
        description="Explicit FHIR Resource references",
        default=None,
    )
    security: Optional[ListType[Coding]] = Field(
        description="Security tag code on .meta.security",
        default=None,
    )
    period: Optional[ListType[Period]] = Field(
        description="Timeframe encompasing data create/update",
        default=None,
    )
    expression: Optional[Expression] = Field(
        description="Expression identifying the data",
        default=None,
    )

class PermissionRuleActivity(BackboneElement):
    """
    A description or definition of which activities are allowed to be done on the data.
    """

    actor: Optional[ListType[Reference]] = Field(
        description="Authorized actor(s)",
        default=None,
    )
    action: Optional[ListType[CodeableConcept]] = Field(
        description="Actions controlled by this rule",
        default=None,
    )
    purpose: Optional[ListType[CodeableConcept]] = Field(
        description="The purpose for which the permission is given",
        default=None,
    )

class PermissionRule(BackboneElement):
    """
    A set of rules.
    """

    type: Optional[fhir.code] = Field(
        description="deny | permit",
        default=None,
    )
    data: Optional[ListType[PermissionRuleData]] = Field(
        description="The selection criteria to identify data that is within scope of this provision",
        default=None,
    )
    activity: Optional[ListType[PermissionRuleActivity]] = Field(
        description="A description or definition of which activities are allowed to be done on the data",
        default=None,
    )
    limit: Optional[ListType[CodeableConcept]] = Field(
        description="What limits apply to the use of the data",
        default=None,
    )

class Permission(DomainResource):
    """
    Permission resource holds access rules for a given data and context.
    """

    _abstract = False
    _type = "Permission"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Permission"

    status: Optional[fhir.code] = Field(
        description="active | entered-in-error | draft | rejected",
        default=None,
    )
    asserter: Optional[Reference] = Field(
        description="The person or entity that asserts the permission",
        default=None,
    )
    date: Optional[ListType[fhir.dateTime]] = Field(
        description="The date that permission was asserted",
        default=None,
    )
    validity: Optional[Period] = Field(
        description="The period in which the permission is active",
        default=None,
    )
    justification: Optional[PermissionJustification] = Field(
        description="The asserted justification for using the data",
        default=None,
    )
    combining: Optional[fhir.code] = Field(
        description="deny-overrides | permit-overrides | ordered-deny-overrides | ordered-permit-overrides | deny-unless-permit | permit-unless-deny",
        default=None,
    )
    rule: Optional[ListType[PermissionRule]] = Field(
        description="Constraints to the Permission",
        default=None,
    )
