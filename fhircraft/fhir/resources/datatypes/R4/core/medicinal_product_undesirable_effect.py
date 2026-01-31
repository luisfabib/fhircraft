import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from fhircraft.fhir.resources.datatypes.primitives import String, Uri, Code

from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Reference,
    Population,
    CodeableConcept,
)
from .resource import Resource
from .domain_resource import DomainResource


class MedicinalProductUndesirableEffect(DomainResource):
    """
    Describe the undesirable effects of the medicinal product.
    """

    _abstract = False
    _type = "MedicinalProductUndesirableEffect"
    _canonical_url = (
        "http://hl7.org/fhir/StructureDefinition/MedicinalProductUndesirableEffect"
    )

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
    subject: Optional[ListType[Reference]] = Field(
        description="The medication for which this is an indication",
        default=None,
    )
    symptomConditionEffect: Optional[CodeableConcept] = Field(
        description="The symptom, condition or undesirable effect",
        default=None,
    )
    classification: Optional[CodeableConcept] = Field(
        description="Classification of the effect",
        default=None,
    )
    frequencyOfOccurrence: Optional[CodeableConcept] = Field(
        description="The frequency of occurrence of the effect",
        default=None,
    )
    population: Optional[ListType[Population]] = Field(
        description="The population group to which this applies",
        default=None,
    )
