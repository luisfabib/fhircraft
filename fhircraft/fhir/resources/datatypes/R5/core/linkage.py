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
    BackboneElement,
)
from .resource import Resource
from .domain_resource import DomainResource


class LinkageItem(BackboneElement):
    """
    Identifies which record considered as the reference to the same real-world occurrence as well as how the items should be evaluated within the collection of linked items.
    """

    type: fhir.code = Field(
        description="source | alternate | historical",
    )
    resource: Reference = Field(
        description="Resource being linked",
    )


class Linkage(DomainResource):
    """
    Identifies two or more records (resource instances) that refer to the same real-world "occurrence".
    """

    _abstract = False
    _type = "Linkage"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Linkage"

    active: Optional[fhir.boolean] = Field(
        description="Whether this linkage assertion is active or not",
        default=None,
    )
    author: Optional[Reference] = Field(
        description="Who is responsible for linkages",
        default=None,
    )
    item: ListType[LinkageItem] = Field(
        description="Item to be linked",
        min_length=1,
    )

    @model_validator(mode="after")
    def FHIR_lnk_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="item.count()>1",
            human="Must have at least two items",
            key="lnk-1",
            severity="error",
        )
