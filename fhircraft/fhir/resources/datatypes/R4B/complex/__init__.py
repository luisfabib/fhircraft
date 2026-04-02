"""
FHIR R4B Complex Data Types

This module contains all the complex data types defined in the FHIR R4B specification.
Each data type is defined in its own module for better organization and maintainability.
"""

# Important: import order matters to avoid circular import errors
from .element import Element
from .extension import Extension
from .period import Period
from .coding import Coding
from .codeable_concept import CodeableConcept
from .meta import Meta
from .identifier import Identifier
from .reference import Reference
from .xhtml import xhtml
from .narrative import Narrative
from .backbone_element import BackboneElement
from .attachment import Attachment
from .contact_point import ContactPoint
from .contact_detail import ContactDetail
from .contributor import Contributor
from .address import Address
from .annotation import Annotation
from .quantity import Quantity
from .age import Age
from .count import Count
from .distance import Distance
from .duration import Duration
from .data_requirement import (
    DataRequirement,
    DataRequirementCodeFilter,
    DataRequirementDateFilter,
    DataRequirementSort,
)
from .expression import Expression
from .human_name import HumanName
from .marketing_status import MarketingStatus
from .codeable_reference import CodeableReference
from .money import Money
from .money_quantity import MoneyQuantity
from .parameter_definition import ParameterDefinition
from .prod_characteristic import ProdCharacteristic
from .product_shelf_life import ProductShelfLife
from .range import Range
from .ratio import Ratio
from .ratio_range import RatioRange
from .related_artifact import RelatedArtifact
from .sampled_data import SampledData
from .signature import Signature
from .simple_quantity import SimpleQuantity
from .timing import Timing, TimingRepeat
from .trigger_definition import TriggerDefinition
from .usage_context import UsageContext
from .population import Population
from .dosage import Dosage, DosageDoseAndRate
from .element_definition import (
    ElementDefinition,
    ElementDefinitionType,
    ElementDefinitionBase,
    ElementDefinitionBinding,
    ElementDefinitionConstraint,
    ElementDefinitionSlicing,
    ElementDefinitionSlicingDiscriminator,
    ElementDefinitionExample,
    ElementDefinitionMapping,
)

__all__ = [
    "Address",
    "Age",
    "Annotation",
    "Attachment",
    "BackboneElement",
    "CodeableConcept",
    "CodeableReference",
    "Coding",
    "ContactDetail",
    "ContactPoint",
    "Contributor",
    "Count",
    "DataRequirement",
    "DataRequirementCodeFilter",
    "DataRequirementDateFilter",
    "DataRequirementSort",
    "Distance",
    "Dosage",
    "DosageDoseAndRate",
    "Duration",
    "Element",
    "ElementDefinitionType",
    "ElementDefinitionBase",
    "ElementDefinitionBinding",
    "ElementDefinitionConstraint",
    "ElementDefinitionSlicing",
    "ElementDefinitionSlicingDiscriminator",
    "ElementDefinitionExample",
    "ElementDefinitionMapping",
    "ElementDefinition",
    "Expression",
    "Extension",
    "HumanName",
    "Identifier",
    "MarketingStatus",
    "Meta",
    "Money",
    "MoneyQuantity",
    "Narrative",
    "ParameterDefinition",
    "Period",
    "Population",
    "ProdCharacteristic",
    "ProductShelfLife",
    "Quantity",
    "Range",
    "Ratio",
    "RatioRange",
    "Reference",
    "RelatedArtifact",
    "SampledData",
    "Signature",
    "SimpleQuantity",
    "Timing",
    "TimingRepeat",
    "TriggerDefinition",
    "UsageContext",
    "xhtml",
]
