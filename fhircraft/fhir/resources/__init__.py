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
from fhircraft.fhir.resources.definitions import ElementDefinition, StructureDefinition
from fhircraft.fhir.resources.factory import ResourceFactory, construct_resource_model
from fhircraft.fhir.resources.repository import (
    CompositeStructureDefinitionRepository,
    HttpStructureDefinitionRepository,
    PackageStructureDefinitionRepository,
    configure_repository,
)

__all__ = [
    "FHIRBaseModel",
    "FHIRSliceModel",
    "StructureDefinition",
    "ElementDefinition",
    "CompositeStructureDefinitionRepository",
    "HttpStructureDefinitionRepository",
    "PackageStructureDefinitionRepository",
    "configure_repository",
    "ResourceFactory",
    "construct_resource_model",
]
