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

# Rebuild models to ensure all references are resolved
Element.model_rebuild()
Period.model_rebuild()
Coding.model_rebuild()
CodeableConcept.model_rebuild()
CodeableReference.model_rebuild()
Meta.model_rebuild()
Identifier.model_rebuild()
Reference.model_rebuild()
xhtml.model_rebuild()
Narrative.model_rebuild()
BackboneElement.model_rebuild()
Attachment.model_rebuild()
ContactPoint.model_rebuild()
ContactDetail.model_rebuild()
Contributor.model_rebuild()
Address.model_rebuild()
Annotation.model_rebuild()
Quantity.model_rebuild()
Age.model_rebuild()
Count.model_rebuild()
Distance.model_rebuild()
Duration.model_rebuild()
DataRequirement.model_rebuild()
DataRequirementCodeFilter.model_rebuild()
DataRequirementDateFilter.model_rebuild()
DataRequirementSort.model_rebuild()
Dosage.model_rebuild()
DosageDoseAndRate.model_rebuild()
Expression.model_rebuild()
HumanName.model_rebuild()
MarketingStatus.model_rebuild()
Money.model_rebuild()
MoneyQuantity.model_rebuild()
ParameterDefinition.model_rebuild()
Population.model_rebuild()
ProdCharacteristic.model_rebuild()
ProductShelfLife.model_rebuild()
Range.model_rebuild()
Ratio.model_rebuild()
RatioRange.model_rebuild()
RelatedArtifact.model_rebuild()
SampledData.model_rebuild()
Signature.model_rebuild()
SimpleQuantity.model_rebuild()
Timing.model_rebuild()
TimingRepeat.model_rebuild()
TriggerDefinition.model_rebuild()
UsageContext.model_rebuild()
ElementDefinition.model_rebuild()
ElementDefinitionType.model_rebuild()
ElementDefinitionBase.model_rebuild()
ElementDefinitionBinding.model_rebuild()
ElementDefinitionConstraint.model_rebuild()
ElementDefinitionSlicing.model_rebuild()
ElementDefinitionSlicingDiscriminator.model_rebuild()
ElementDefinitionExample.model_rebuild()
ElementDefinitionMapping.model_rebuild()
Extension.model_rebuild()
