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
)
from .resource import Resource
from .domain_resource import DomainResource

class FormularyItem(DomainResource):
    """
    This resource describes a product or service that is available through a program and includes the conditions and constraints of availability.  All of the information in this resource is specific to the inclusion of the item in the formulary and is not inherent to the item itself.
    """

    _abstract = False
    _type = "FormularyItem"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/FormularyItem"

    identifier: Optional[ListType[Identifier]] = Field(
        description="Business identifier for this formulary item",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="Codes that identify this formulary item",
        default=None,
    )
    status: Optional[Code] = Field(
        description="active | entered-in-error | inactive",
        default=None,
    )
