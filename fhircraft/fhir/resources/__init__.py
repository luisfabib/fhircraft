"""
FHIR Resources Module

This module provides all FHIR resource-related functionality including:
- FHIRBaseModel: Base class for all FHIR resources
- ResourceFactory: Factory for constructing FHIR resource models
- Repository classes: For managing FHIR structure definitions
- Definitions: StructureDefinition and ElementDefinition models

Recommended imports:
    from fhircraft.fhir.resources import ResourceFactory, FHIRBaseModel
    from fhircraft.fhir.resources import CompositeStructureDefinitionRepository
"""

from fhircraft.fhir.resources.base import FHIRBaseModel, FHIRSliceModel
from fhircraft.fhir.resources.datatypes.registry import (
    get_fhir_type,
    get_fhir_type_by_url,
)
from fhircraft.fhir.resources.factory import (
    ResourceFactory,
    FHIRStructureFactory,
)

__all__ = [
    "FHIRBaseModel",
    "FHIRSliceModel",
    "ResourceFactory",
    "FHIRStructureFactory",
    "get_fhir_type",
    "get_fhir_type_by_url",
]
