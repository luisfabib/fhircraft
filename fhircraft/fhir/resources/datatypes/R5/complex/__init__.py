"""
FHIR R5 Complex Data Types

This module contains all the complex data types defined in the FHIR R5 specification.
Each data type is defined in its own module for better organization and maintainability.
"""

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
from .xhtml import xhtml
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
from .availability import Availability
from .data_requirement import DataRequirement
from .resource import Resource
from .domain_resource import DomainResource
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
from .timing import Timing
from .trigger_definition import TriggerDefinition
from .usage_context import UsageContext
from .monetary_component import MonetaryComponent
from .extended_contact_detail import ExtendedContactDetail
from .virtual_service_detail import VirtualServiceDetail
from .dosage import Dosage
from .element_definition import ElementDefinition

__all__ = [
    "Address",
    "Age",
    "Annotation",
    "Attachment",
    "Availability",
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
    "DataType",
    "Distance",
    "DomainResource",
    "Dosage",
    "Duration",
    "Element",
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
    "Resource",
    "SampledData",
    "Signature",
    "SimpleQuantity",
    "Timing",
    "TriggerDefinition",
    "UsageContext",
    "VirtualServiceDetail",
    "xhtml",
]

# Rebuild models to ensure all references are resolved
Base.model_rebuild()
Element.model_rebuild()
DataType.model_rebuild()
BackboneElement.model_rebuild()
BackboneType.model_rebuild()
PrimitiveType.model_rebuild()
Period.model_rebuild()
Coding.model_rebuild()
CodeableConcept.model_rebuild()
CodeableReference.model_rebuild()
Meta.model_rebuild()
Identifier.model_rebuild()
Reference.model_rebuild()
xhtml.model_rebuild()
Narrative.model_rebuild()
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
MoneyQuantity.model_rebuild()
SimpleQuantity.model_rebuild()
Availability.model_rebuild()
DataRequirement.model_rebuild()
DomainResource.model_rebuild()
Dosage.model_rebuild()
Expression.model_rebuild()
ExtendedContactDetail.model_rebuild()
HumanName.model_rebuild()
MarketingStatus.model_rebuild()
MonetaryComponent.model_rebuild()
Money.model_rebuild()
ParameterDefinition.model_rebuild()
ProductShelfLife.model_rebuild()
Range.model_rebuild()
Ratio.model_rebuild()
RatioRange.model_rebuild()
RelatedArtifact.model_rebuild()
Resource.model_rebuild()
SampledData.model_rebuild()
Signature.model_rebuild()
Timing.model_rebuild()
TriggerDefinition.model_rebuild()
UsageContext.model_rebuild()
VirtualServiceDetail.model_rebuild()
ElementDefinition.model_rebuild()
Extension.model_rebuild()
