from typing import Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
import fhircraft.fhir.resources.datatypes.R4B.primitive as fhir
from fhircraft.fhir.resources.base import FHIRBaseModel
from fhircraft.fhir.resources.datatypes.R4B.complex import Element, Meta


class Resource(FHIRBaseModel):
    """
    Base Resource
    """

    _fhir_release = "R4B"
    _abstract = True
    _type = "Resource"
    _kind = "resource"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/Resource"

    id: Optional[fhir.id_] = Field(
        description="Logical id of this artifact",
        default=None,
    )
    meta: Optional["Meta"] = Field(
        description="Metadata about the resource",
        default=None,
    )
    implicitRules: Optional[fhir.uri] = Field(
        description="A set of rules under which this content was created",
        default=None,
    )
    language: Optional[fhir.code] = Field(
        description="Language of the resource content",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )
