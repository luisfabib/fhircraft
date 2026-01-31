import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import String, Uri, Code, Boolean

from fhircraft.fhir.resources.datatypes.R4B.complex import (
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

    type: Optional[Code] = Field(
        description="source | alternate | historical",
        default=None,
    )
    type_ext: Optional[Element] = Field(
        description="Placeholder element for type extensions",
        default=None,
        alias="_type",
    )
    resource: Optional[Reference] = Field(
        description="Resource being linked",
        default=None,
    )

class Linkage(DomainResource):
    """
    Identifies two or more records (resource instances) that refer to the same real-world "occurrence".
    """

    _abstract = False
    _type = "Linkage"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Linkage"

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
    active: Optional[Boolean] = Field(
        description="Whether this linkage assertion is active or not",
        default=None,
    )
    active_ext: Optional[Element] = Field(
        description="Placeholder element for active extensions",
        default=None,
        alias="_active",
    )
    author: Optional[Reference] = Field(
        description="Who is responsible for linkages",
        default=None,
    )
    item: Optional[ListType[LinkageItem]] = Field(
        description="Item to be linked",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_lnk_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="item.count()>1",
            human="Must have at least two items",
            key="lnk-1",
            severity="error",
        )
