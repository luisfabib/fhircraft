# Important: import order matters to avoid circular import errors
from .base import Base
from .element import Element
from .data_type import DataType
from .backbone_type import BackboneType
from .primitive_type import PrimitiveType
from .extension import Extension
from .backbone_element import BackboneElement
from .period import Period
from .coding import Coding
from .codeable_concept import CodeableConcept
from .codeable_reference import CodeableReference
from .meta import Meta
from .reference import Reference
from .identifier import Identifier
from .xhtml import Xhtml
from .narrative import Narrative
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
from .money_quantity import MoneyQuantity
from .simple_quantity import SimpleQuantity
from .availability import (
    Availability,
    AvailabilityAvailableTime,
    AvailabilityNotAvailableTime,
)
from .data_requirement import (
    DataRequirement,
    DataRequirementCodeFilter,
    DataRequirementDateFilter,
    DataRequirementValueFilter,
    DataRequirementSort,
)
from .expression import Expression
from .human_name import HumanName
from .marketing_status import MarketingStatus
from .money import Money
from .parameter_definition import ParameterDefinition
from .product_shelf_life import ProductShelfLife
from .range import Range
from .ratio import Ratio
from .ratio_range import RatioRange
from .related_artifact import RelatedArtifact
from .sampled_data import SampledData
from .signature import Signature
from .timing import Timing, TimingRepeat
from .trigger_definition import TriggerDefinition
from .usage_context import UsageContext
from .monetary_component import MonetaryComponent
from .extended_contact_detail import ExtendedContactDetail
from .virtual_service_detail import VirtualServiceDetail
from .dosage import Dosage, DosageDoseAndRate
from .element_definition import (
    ElementDefinition,
    ElementDefinitionType,
    ElementDefinitionBase,
    ElementDefinitionBinding,
    ElementDefinitionBindingAdditional,
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
    "Availability",
    "AvailabilityAvailableTime",
    "AvailabilityNotAvailableTime",
    "BackboneElement",
    "BackboneType",
    "Base",
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
    "DataRequirementValueFilter",
    "DataRequirementSort",
    "DataType",
    "Distance",
    "Dosage",
    "DosageDoseAndRate",
    "Duration",
    "Element",
    "ElementDefinitionType",
    "ElementDefinitionBase",
    "ElementDefinitionBinding",
    "ElementDefinitionBindingAdditional",
    "ElementDefinitionConstraint",
    "ElementDefinitionMapping",
    "ElementDefinitionSlicing",
    "ElementDefinitionSlicingDiscriminator",
    "ElementDefinitionExample",
    "ElementDefinition",
    "Expression",
    "ExtendedContactDetail",
    "Extension",
    "HumanName",
    "Identifier",
    "MarketingStatus",
    "Meta",
    "MonetaryComponent",
    "Money",
    "MoneyQuantity",
    "Narrative",
    "ParameterDefinition",
    "Period",
    "PrimitiveType",
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
    "VirtualServiceDetail",
    "Xhtml",
]

# Ensure all forward references (e.g. "Extension" in Base/Element) are
# resolved when types are imported directly from this package.
from ..primitive import *

import typing as _typing

_ns = {
    **vars(_typing),
    **{k: v for k, v in globals().items() if not k.startswith("__")},
}
for _name in __all__:
    _cls = globals().get(_name)
    if _cls is not None and not getattr(_cls, "__pydantic_complete__", True):
        _cls.model_rebuild(_types_namespace=_ns)
del _name, _cls, _ns, _typing  # type: ignore
