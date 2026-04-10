import fhircraft.fhir.resources.validators as fhir_validators
from pydantic import Field, model_validator
from typing import Optional, List as ListType, Literal

NoneType = type(None)


import fhircraft.fhir.resources.datatypes.R4B.primitive as fhir
from fhircraft.fhir.resources.datatypes.R4B.complex import (
    Element,
    Meta,
    Narrative,
    Extension,
    Identifier,
    CodeableConcept,
    Reference,
    Period,
    Age,
    Range,
    Annotation,
    BackboneElement,
)
from .resource import Resource
from .domain_resource import DomainResource


class FamilyMemberHistoryCondition(BackboneElement):
    """
    The significant Conditions (or condition) that the family member had. This is a repeating section to allow a system to represent more than one condition per resource, though there is nothing stopping multiple resources - one per condition.
    """

    code: Optional[CodeableConcept] = Field(
        description="Condition suffered by relation",
        default=None,
    )
    outcome: Optional[CodeableConcept] = Field(
        description="deceased | permanent disability | etc.",
        default=None,
    )
    contributedToDeath: Optional[fhir.boolean] = Field(
        description="Whether the condition contributed to the cause of death",
        default=None,
    )
    onsetAge: Optional[Age] = Field(
        description="When condition first manifested",
        default=None,
    )
    onsetRange: Optional[Range] = Field(
        description="When condition first manifested",
        default=None,
    )
    onsetPeriod: Optional[Period] = Field(
        description="When condition first manifested",
        default=None,
    )
    onsetString: Optional[fhir.string] = Field(
        description="When condition first manifested",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="Extra information about condition",
        default=None,
    )

    @property
    def onset(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="onset",
        )

    @model_validator(mode="after")
    def onset_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Age, Range, Period, fhir.String],
            field_name_base="onset",
            required=False,
        )


class FamilyMemberHistory(DomainResource):
    """
    Significant health conditions for a person related to the patient relevant in the context of care for the patient.
    """

    _abstract = False
    _type = "FamilyMemberHistory"
    _canonical_url = "http://hl7.org/fhir/StructureDefinition/FamilyMemberHistory"

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
        description="External id_(s) for this record",
        default=None,
    )
    instantiatesCanonical: Optional[ListType[fhir.canonical]] = Field(
        description="Instantiates FHIR protocol or definition",
        default=None,
    )
    instantiatesUri: Optional[ListType[fhir.uri]] = Field(
        description="Instantiates external protocol or definition",
        default=None,
    )
    status: Optional[fhir.code] = Field(
        description="partial | completed | entered-in-error | health-unknown",
        default=None,
    )
    dataAbsentReason: Optional[CodeableConcept] = Field(
        description="subject-unknown | withheld | unable-to-obtain | deferred",
        default=None,
    )
    patient: Optional[Reference] = Field(
        description="Patient history is about",
        default=None,
    )
    date: Optional[fhir.dateTime] = Field(
        description="When history was recorded or last updated",
        default=None,
    )
    name: Optional[fhir.string] = Field(
        description="The family member described",
        default=None,
    )
    relationship: Optional[CodeableConcept] = Field(
        description="Relationship to the subject",
        default=None,
    )
    sex: Optional[CodeableConcept] = Field(
        description="male | female | other | unknown",
        default=None,
    )
    bornPeriod: Optional[Period] = Field(
        description="(approximate) date of birth",
        default=None,
    )
    bornDate: Optional[fhir.date_] = Field(
        description="(approximate) date of birth",
        default=None,
    )
    bornString: Optional[fhir.string] = Field(
        description="(approximate) date of birth",
        default=None,
    )
    ageAge: Optional[Age] = Field(
        description="(approximate) age",
        default=None,
    )
    ageRange: Optional[Range] = Field(
        description="(approximate) age",
        default=None,
    )
    ageString: Optional[fhir.string] = Field(
        description="(approximate) age",
        default=None,
    )
    estimatedAge: Optional[fhir.boolean] = Field(
        description="Age is estimated?",
        default=None,
    )
    deceasedBoolean: Optional[fhir.boolean] = Field(
        description="Dead? How old/when?",
        default=None,
    )
    deceasedAge: Optional[Age] = Field(
        description="Dead? How old/when?",
        default=None,
    )
    deceasedRange: Optional[Range] = Field(
        description="Dead? How old/when?",
        default=None,
    )
    deceasedDate: Optional[fhir.date_] = Field(
        description="Dead? How old/when?",
        default=None,
    )
    deceasedString: Optional[fhir.string] = Field(
        description="Dead? How old/when?",
        default=None,
    )
    reasonCode: Optional[ListType[CodeableConcept]] = Field(
        description="Why was family member history performed?",
        default=None,
    )
    reasonReference: Optional[ListType[Reference]] = Field(
        description="Why was family member history performed?",
        default=None,
    )
    note: Optional[ListType[Annotation]] = Field(
        description="General note about related person",
        default=None,
    )
    condition: Optional[ListType[FamilyMemberHistoryCondition]] = Field(
        description="Condition that the related person had",
        default=None,
    )

    @property
    def born(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="born",
        )

    @property
    def age(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="age",
        )

    @property
    def deceased(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="deceased",
        )

    @model_validator(mode="after")
    def born_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Period, fhir.Date, fhir.String],
            field_name_base="born",
            required=False,
        )

    @model_validator(mode="after")
    def age_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Age, Range, fhir.String],
            field_name_base="age",
            required=False,
        )

    @model_validator(mode="after")
    def deceased_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[fhir.Boolean, Age, Range, fhir.Date, fhir.String],
            field_name_base="deceased",
            required=False,
        )

    @model_validator(mode="after")
    def FHIR_fhs_1_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="age.empty() or born.empty()",
            human="Can have age[x] or born[x], but not both",
            key="fhs-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_fhs_2_constraint_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="age.exists() or estimatedAge.empty()",
            human="Can only have estimatedAge if age[x] is present",
            key="fhs-2",
            severity="error",
        )
