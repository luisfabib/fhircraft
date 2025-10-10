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


# Use lazy imports to avoid circular dependencies
def __getattr__(name):
    """Lazy loading of resources components to avoid circular import issues."""
    if name == "FHIRBaseModel":
        from .base import FHIRBaseModel

        return FHIRBaseModel
    elif name == "FHIRSliceModel":
        from .base import FHIRSliceModel

        return FHIRSliceModel
    elif name == "StructureDefinition":
        from .definitions import StructureDefinition

        return StructureDefinition
    elif name == "ElementDefinition":
        from .definitions import ElementDefinition

        return ElementDefinition
    elif name == "CompositeStructureDefinitionRepository":
        from .repository import CompositeStructureDefinitionRepository

        return CompositeStructureDefinitionRepository
    elif name == "HttpStructureDefinitionRepository":
        from .repository import HttpStructureDefinitionRepository

        return HttpStructureDefinitionRepository
    elif name == "PackageStructureDefinitionRepository":
        from .repository import PackageStructureDefinitionRepository

        return PackageStructureDefinitionRepository
    elif name == "configure_repository":
        from .repository import configure_repository

        return configure_repository
    elif name == "ResourceFactory":
        from .factory import ResourceFactory

        return ResourceFactory
    elif name == "construct_resource_model":
        from .factory import construct_resource_model

        return construct_resource_model
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
