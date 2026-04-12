from typing import Optional

from pydantic import Field, model_validator

import fhircraft.fhir.resources.validators as fhir_validators

import fhircraft.fhir.resources.datatypes.R4.primitive as fhir
from .codeable_concept import CodeableConcept
from .element import Element
from .backbone_element import BackboneElement
from .quantity import Quantity
from .range import Range

class SubstanceAmount(BackboneElement):
    """
    Chemical substances are a single substance type whose primary defining element is the molecular structure. Chemical substances shall be defined on the basis of their complete covalent molecular structure; the presence of a salt (counter-ion) and/or solvates (water, alcohols) is also captured. Purity, grade, physical form or particle size are not taken into account in the definition of a chemical substance or in the assignment of a Substance ID
    """

    _type = "BackboneElement"

    amountQuantity: Optional[Quantity] = Field(
        description="Used to capture quantitative values for a variety of elements. If only limits are given, the arithmetic mean would be the average. If only a single definite value for a given element is given, it would be captured in this field",
        default=None,
    )
    amountRange: Optional[Range] = Field(
        description="Used to capture quantitative values for a variety of elements. If only limits are given, the arithmetic mean would be the average. If only a single definite value for a given element is given, it would be captured in this field",
        default=None,
    )
    amountString: Optional[fhir.string] = Field(
        description="Used to capture quantitative values for a variety of elements. If only limits are given, the arithmetic mean would be the average. If only a single definite value for a given element is given, it would be captured in this field",
        default=None,
    )
    amountType: Optional[CodeableConcept] = Field(
        description="Most elements that require a quantitative value will also have a field called amount type. Amount type should always be specified because the actual value of the amount is often dependent on it. EXAMPLE: In capturing the actual relative amounts of substances or molecular fragments it is essential to indicate whether the amount refers to a mole ratio or weight ratio. For any given element an effort should be made to use same the amount type for all related definitional elements",
        default=None,
    )
    amountText: Optional[fhir.string] = Field(
        description="A textual comment on a numeric value",
        default=None,
    )
    referenceRange: Optional[Element] = Field(
        description="Reference range of possible or expected values",
        default=None,
    )

    @model_validator(mode="after")
    def amount_type_choice_validator(self):
        return fhir_validators.validate_type_choice_element(
            self,
            field_types=["Quantity", "Range", fhir.String],
            field_name_base="amount",
        )

    @property
    def amount(self):
        return fhir_validators.get_type_choice_value_by_base(
            self,
            base="amount",
        )
