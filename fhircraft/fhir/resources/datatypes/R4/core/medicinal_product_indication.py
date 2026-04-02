import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)

from ..primitive import *

from fhircraft.fhir.resources.datatypes.R4.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Reference,
    CodeableConcept,
    Quantity,
    BackboneElement,
    Population,
)
from .resource import Resource
from .domain_resource import DomainResource

class MedicinalProductIndicationOtherTherapy(BackboneElement):
    """
    Information about the use of the medicinal product in relation to other therapies described as part of the indication.
    """

    therapyRelationshipType: Optional[CodeableConcept] = Field(
        description="The type of relationship between the medicinal product indication or contraindication and another therapy",
        default=None,
    )
    medicationCodeableConcept: Optional[CodeableConcept] = Field(
        description="Reference to a specific medication (active substance, medicinal product or class of products) as part of an indication or contraindication",
        default=None,
    )
    medicationReference: Optional[Reference] = Field(
        description="Reference to a specific medication (active substance, medicinal product or class of products) as part of an indication or contraindication",
        default=None,
    )

    @property
    def medication(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="medication",
        )

    @model_validator(mode="after")
    def medication_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[CodeableConcept, Reference],
            field_name_base="medication",
            required=True,
        )

class MedicinalProductIndication(DomainResource):
    """
    Indication for the Medicinal Product.
    """

    _abstract = False
    _type = "MedicinalProductIndication"
    _canonical_url = (
        "http://hl7.org/fhir/StructureDefinition/MedicinalProductIndication"
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
    diseaseSymptomProcedure: Optional[CodeableConcept] = Field(
        description="The disease, symptom or procedure that is the indication for treatment",
        default=None,
    )
    diseaseStatus: Optional[CodeableConcept] = Field(
        description="The status of the disease or symptom for which the indication applies",
        default=None,
    )
    comorbidity: Optional[ListType[CodeableConcept]] = Field(
        description="Comorbidity (concurrent condition) or co-infection as part of the indication",
        default=None,
    )
    intendedEffect: Optional[CodeableConcept] = Field(
        description="The intended effect, aim or strategy to be achieved by the indication",
        default=None,
    )
    duration: Optional[Quantity] = Field(
        description="Timing or duration information as part of the indication",
        default=None,
    )
    otherTherapy: Optional[ListType[MedicinalProductIndicationOtherTherapy]] = Field(
        description="Information about the use of the medicinal product in relation to other therapies described as part of the indication",
        default=None,
    )
    undesirableEffect: Optional[ListType[Reference]] = Field(
        description="Describe the undesirable effects of the medicinal product",
        default=None,
    )
    population: Optional[ListType[Population]] = Field(
        description="The population group to which this applies",
        default=None,
    )
