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
    Identifier,
    Coding,
    ContactDetail,
    UsageContext,
    CodeableConcept,
    BackboneElement,
    Quantity,
    Reference,
)
from .resource import Resource
from .domain_resource import DomainResource


class ConditionDefinitionObservation(BackboneElement):
    """
    Observations particularly relevant to this condition.
    """

    category: Optional[CodeableConcept] = Field(
        description="Category that is relevant",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="code for relevant Observation",
        default=None,
    )


class ConditionDefinitionMedication(BackboneElement):
    """
    Medications particularly relevant for this condition.
    """

    category: Optional[CodeableConcept] = Field(
        description="Category that is relevant",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="code for relevant Medication",
        default=None,
    )


class ConditionDefinitionPrecondition(BackboneElement):
    """
    An observation that suggests that this condition applies.
    """

    type: Optional[fhir.code] = Field(
        description="sensitive | specific",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="code for relevant Observation",
        default=None,
    )
    valueCodeableConcept: Optional[CodeableConcept] = Field(
        description="Value of Observation",
        default=None,
    )
    valueQuantity: Optional[Quantity] = Field(
        description="Value of Observation",
        default=None,
    )

    @property
    def value(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="value",
        )

    @model_validator(mode="after")
    def value_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[CodeableConcept, Quantity],
            field_name_base="value",
            required=False,
        )


class ConditionDefinitionQuestionnaire(BackboneElement):
    """
    Questionnaire for this condition.
    """

    purpose: Optional[fhir.code] = Field(
        description="preadmit | diff-diagnosis | outcome",
        default=None,
    )
    reference: Optional[Reference] = Field(
        description="Specific Questionnaire",
        default=None,
    )


class ConditionDefinitionPlan(BackboneElement):
    """
    Plan that is appropriate.
    """

    role: Optional[CodeableConcept] = Field(
        description="Use for the plan",
        default=None,
    )
    reference: Optional[Reference] = Field(
        description="The actual plan",
        default=None,
    )


class ConditionDefinition(DomainResource):
    """
    A definition of a condition and information relevant to managing it.
    """

    _abstract = False
    _type = "ConditionDefinition"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/ConditionDefinition"

    url: Optional[fhir.uri] = Field(
        description="canonical identifier for this condition definition, represented as a URI (globally unique)",
        default=None,
    )
    identifier: Optional[ListType[Identifier]] = Field(
        description="Additional identifier for the condition definition",
        default=None,
    )
    version: Optional[fhir.string] = Field(
        description="Business version of the condition definition",
        default=None,
    )
    versionAlgorithmString: Optional[fhir.string] = Field(
        description="How to compare versions",
        default=None,
    )
    versionAlgorithmCoding: Optional[Coding] = Field(
        description="How to compare versions",
        default=None,
    )
    name: Optional[fhir.string] = Field(
        description="Name for this condition definition (computer friendly)",
        default=None,
    )
    title: Optional[fhir.string] = Field(
        description="Name for this condition definition (human friendly)",
        default=None,
    )
    subtitle: Optional[fhir.string] = Field(
        description="Subordinate title of the event definition",
        default=None,
    )
    status: Optional[fhir.code] = Field(
        description="draft | active | retired | unknown",
        default=None,
    )
    experimental: Optional[fhir.boolean] = Field(
        description="For testing purposes, not real usage",
        default=None,
    )
    date: Optional[fhir.dateTime] = Field(
        description="Date last changed",
        default=None,
    )
    publisher: Optional[fhir.string] = Field(
        description="Name of the publisher/steward (organization or individual)",
        default=None,
    )
    contact: Optional[ListType[ContactDetail]] = Field(
        description="Contact details for the publisher",
        default=None,
    )
    description: Optional[fhir.markdown] = Field(
        description="Natural language description of the condition definition",
        default=None,
    )
    useContext: Optional[ListType[UsageContext]] = Field(
        description="The context that the content is intended to support",
        default=None,
    )
    jurisdiction: Optional[ListType[CodeableConcept]] = Field(
        description="Intended jurisdiction for condition definition (if applicable)",
        default=None,
    )
    code: Optional[CodeableConcept] = Field(
        description="Identification of the condition, problem or diagnosis",
        default=None,
    )
    severity: Optional[CodeableConcept] = Field(
        description="Subjective severity of condition",
        default=None,
    )
    bodySite: Optional[CodeableConcept] = Field(
        description="Anatomical location, if relevant",
        default=None,
    )
    stage: Optional[CodeableConcept] = Field(
        description="Stage/grade, usually assessed formally",
        default=None,
    )
    hasSeverity: Optional[fhir.boolean] = Field(
        description="Whether Severity is appropriate",
        default=None,
    )
    hasBodySite: Optional[fhir.boolean] = Field(
        description="Whether bodySite is appropriate",
        default=None,
    )
    hasStage: Optional[fhir.boolean] = Field(
        description="Whether stage is appropriate",
        default=None,
    )
    definition: Optional[ListType[fhir.uri]] = Field(
        description="Formal Definition for the condition",
        default=None,
    )
    observation: Optional[ListType[ConditionDefinitionObservation]] = Field(
        description="Observations particularly relevant to this condition",
        default=None,
    )
    medication: Optional[ListType[ConditionDefinitionMedication]] = Field(
        description="Medications particularly relevant for this condition",
        default=None,
    )
    precondition: Optional[ListType[ConditionDefinitionPrecondition]] = Field(
        description="Observation that suggets this condition",
        default=None,
    )
    team: Optional[ListType[Reference]] = Field(
        description="Appropriate team for this condition",
        default=None,
    )
    questionnaire: Optional[ListType[ConditionDefinitionQuestionnaire]] = Field(
        description="Questionnaire for this condition",
        default=None,
    )
    plan: Optional[ListType[ConditionDefinitionPlan]] = Field(
        description="Plan that is appropriate",
        default=None,
    )

    @property
    def versionAlgorithm(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="versionAlgorithm",
        )

    @model_validator(mode="after")
    def versionAlgorithm_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.string, Coding],
            field_name_base="versionAlgorithm",
            required=False,
        )

    @model_validator(mode="after")
    def FHIR_cnl_0_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="name.exists() implies name.matches('^[A-Z]([A-Za-z0-9_]){1,254}$')",
            human="Name should be usable as an identifier for the module by machine processing applications such as code generation",
            key="cnl-0",
            severity="warning",
        )

    @model_validator(mode="after")
    def FHIR_cnl_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=("url",),
            expression="exists() implies matches('^[^|# ]+$')",
            human="URL should not contain | or # - these characters make processing canonical references problematic",
            key="cnl-1",
            severity="warning",
        )
