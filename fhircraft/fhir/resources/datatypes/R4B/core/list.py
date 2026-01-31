from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.datatypes.primitives import *

NoneType = type(None)

from typing import List as ListType, Optional

from fhircraft.fhir.resources.datatypes.primitives import (
    Boolean,
    Code,
    DateTime,
    String,
)
from fhircraft.fhir.resources.datatypes.R4B.complex import (
    Annotation,
    BackboneElement,
    CodeableConcept,
    Element,
    Extension,
    Identifier,
    Reference,
)
from .resource import Resource
from .domain_resource import DomainResource


class ListEntry(BackboneElement):
    """
    Entries in this list.
    """

    flag: Optional[CodeableConcept] = Field(
        description="Status/Workflow information about this item",
        default=None,
    )
    deleted: Optional[Boolean] = Field(
        description="If this item is actually marked as deleted",
        default=None,
    )
    deleted_ext: Optional[Element] = Field(
        description="Placeholder element for deleted extensions",
        default=None,
        alias="_deleted",
    )
    date: Optional[DateTime] = Field(
        description="When item added to list",
        default=None,
    )
    date_ext: Optional[Element] = Field(
        description="Placeholder element for date extensions",
        default=None,
        alias="_date",
    )
    item: Optional[Reference] = Field(
        description="Actual entry",
        default=None,
    )


class List(DomainResource):
    """
    A list is a curated collection of resources.
    """

    _abstract = False
    _type = "List"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/List"

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
        description="Business identifier",
        default=None,
    )
    status: Optional[Code] = Field(
        description="current | retired | entered-in-error",
        default=None,
    )
    status_ext: Optional[Element] = Field(
        description="Placeholder element for status extensions",
        default=None,
        alias="_status",
    )
    mode: Optional[Code] = Field(
        description="working | snapshot | changes",
        default=None,
    )
    mode_ext: Optional[Element] = Field(
        description="Placeholder element for mode extensions",
        default=None,
        alias="_mode",
    )
    title: Optional[String] = Field(
        description="Descriptive name for the list",
        default=None,
    )
    title_ext: Optional[Element] = Field(
        description="Placeholder element for title extensions",
        default=None,
        alias="_title",
    )
    code: Optional[CodeableConcept] = Field(
        description="What the purpose of this list is",
        default=None,
    )
    subject: Optional[Reference] = Field(
        description="If all resources have the same subject",
        default=None,
    )
    encounter: Optional[Reference] = Field(
        description="Context in which list created",
        default=None,
    )
    date: Optional[DateTime] = Field(
        description="When the list was prepared",
        default=None,
    )
    date_ext: Optional[Element] = Field(
        description="Placeholder element for date extensions",
        default=None,
        alias="_date",
    )
    source: Optional[Reference] = Field(
        description="Who and/or what defined the list contents (aka Author)",
        default=None,
    )
    orderedBy: Optional[CodeableConcept] = Field(
        description="What order the list has",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Comments about the list",
        default=None,
    )
    entry: Optional[ListType[ListEntry]] = Field(
        description="Entries in the list",
        default=None,
    )
    emptyReason: Optional[CodeableConcept] = Field(
        description="Why list is empty",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_lst_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="emptyReason.empty() or entry.empty()",
            human="A list can only have an emptyReason if it is empty",
            key="lst-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_lst_2_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="mode = 'changes' or entry.deleted.empty()",
            human='The deleted flag can only be used if the mode of the list is "changes"',
            key="lst-2",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_lst_3_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="mode = 'working' or entry.date.empty()",
            human='An entry date can only be used if the mode of the list is "working"',
            key="lst-3",
            severity="error",
        )
