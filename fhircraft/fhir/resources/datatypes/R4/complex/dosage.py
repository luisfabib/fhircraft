from typing import List, Optional, TYPE_CHECKING

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators
from fhircraft.fhir.resources.base import FHIRBaseModel
from fhircraft.fhir.resources.datatypes.primitives import *

from .codeable_concept import CodeableConcept
from .element import Element
from .backbone_element import BackboneElement
from .simple_quantity import SimpleQuantity
from .range import Range
from .ratio import Ratio
from .timing import Timing


class DosageDoseAndRate(BackboneElement):
    """
    Amount of medication administered
    """

    _type = "BackboneElement"

    type: Optional[CodeableConcept] = Field(
        description="The kind of dose or rate specified",
        default=None,
    )
    doseRange: Optional[Range] = Field(
        description="Amount of medication per dose",
        default=None,
    )
    doseQuantity: Optional[SimpleQuantity] = Field(
        description="Amount of medication per dose",
        default=None,
    )
    rateRatio: Optional[Ratio] = Field(
        description="Amount of medication per unit of time",
        default=None,
    )
    rateRange: Optional[Range] = Field(
        description="Amount of medication per unit of time",
        default=None,
    )
    rateQuantity: Optional[SimpleQuantity] = Field(
        description="Amount of medication per unit of time",
        default=None,
    )

    @model_validator(mode="after")
    def dose_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=["Range", "SimpleQuantity"],
            field_name_base="dose",
        )

    @property
    def dose(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="dose",
        )

    @model_validator(mode="after")
    def rate_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=["Ratio", "Range", "SimpleQuantity"],
            field_name_base="rate",
        )

    @property
    def rate(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="rate",
        )


class Dosage(BackboneElement):
    """
    How the medication is/was taken or should be taken
    """

    _type = "BackboneElement"

    sequence: Optional[Integer] = Field(
        description="The order of the dosage instructions",
        default=None,
    )
    sequence_ext: Optional[Element] = Field(
        description="Placeholder element for sequence extensions",
        default=None,
        alias="_sequence",
    )
    text: Optional[String] = Field(
        description="Free text dosage instructions e.g. SIG",
        default=None,
    )
    text_ext: Optional[Element] = Field(
        description="Placeholder element for text extensions",
        default=None,
        alias="_text",
    )
    additionalInstruction: Optional[List[CodeableConcept]] = Field(
        description='Supplemental instruction or warnings to the patient - e.g. "with meals", "may cause drowsiness"',
        default=None,
    )
    patientInstruction: Optional[String] = Field(
        description="Patient or consumer oriented instructions",
        default=None,
    )
    patientInstruction_ext: Optional[Element] = Field(
        description="Placeholder element for patientInstruction extensions",
        default=None,
        alias="_patientInstruction",
    )
    timing: Optional[Timing] = Field(
        description="When medication should be administered",
        default=None,
    )
    asNeededBoolean: Optional[Boolean] = Field(
        description='Take "as needed" (for x)',
        default=None,
    )
    asNeededCodeableConcept: Optional[CodeableConcept] = Field(
        description='Take "as needed" (for x)',
        default=None,
    )
    site: Optional[CodeableConcept] = Field(
        description="Body site to administer to",
        default=None,
    )
    route: Optional[CodeableConcept] = Field(
        description="How drug should enter body",
        default=None,
    )
    method: Optional[CodeableConcept] = Field(
        description="Technique for administering medication",
        default=None,
    )
    doseAndRate: Optional[List[DosageDoseAndRate]] = Field(
        description="Amount of medication administered",
        default=None,
    )
    maxDosePerPeriod: Optional[Ratio] = Field(
        description="Upper limit on medication per unit of time",
        default=None,
    )
    maxDosePerAdministration: Optional[SimpleQuantity] = Field(
        description="Upper limit on medication per administration",
        default=None,
    )
    maxDosePerLifetime: Optional[SimpleQuantity] = Field(
        description="Upper limit on medication per lifetime of the patient",
        default=None,
    )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "maxDosePerLifetime",
                "maxDosePerAdministration",
                "maxDosePerPeriod",
                "doseAndRate",
                "method",
                "route",
                "site",
                "timing",
                "patientInstruction",
                "additionalInstruction",
                "text",
                "sequence",
                "modifierExtension",
                "extension",
            ),
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ext_1_constraint_validator(self):
        return fhir_validators.validate_element_constraint(
            self,
            elements=(
                "modifierExtension",
                "extension",
            ),
            expression="extension.exists() != value.exists()",
            human="Must have either extensions or value[x], not both",
            key="ext-1",
            severity="error",
        )

    @model_validator(mode="after")
    def FHIR_ele_1_constraint_model_validator(self):
        return fhir_validators.validate_model_constraint(
            self,
            expression="hasValue() or (children().count() > id.count())",
            human="All FHIR elements must have a @value or children",
            key="ele-1",
            severity="error",
        )

    @model_validator(mode="after")
    def asNeeded_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=[Boolean, "CodeableConcept"],
            field_name_base="asNeeded",
        )

    @property
    def asNeeded(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="asNeeded",
        )
