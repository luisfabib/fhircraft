"""
FHIRcraft: FHIR Resource Modeling and Processing Toolkit

This module provides high-level, intuitive imports for the most commonly used components.
Users can import everything they need from the top level without worrying about
internal package structure.
"""

# Utility functions are safe to import directly (no circular dependencies)
from fhircraft.utils import capitalize, ensure_list, get_FHIR_release_from_version


# Use lazy imports for main components to avoid circular dependencies
def __getattr__(name):
    """Lazy loading of main components to avoid circular import issues."""
    if name == "FHIRMapper":
        from fhircraft.fhir.mapper import FHIRMapper

        return FHIRMapper
    elif name == "ResourceFactory":
        from fhircraft.fhir.resources.factory import ResourceFactory

        return ResourceFactory
    elif name == "FHIRBaseModel":
        from fhircraft.fhir.resources.base import FHIRBaseModel

        return FHIRBaseModel
    elif name == "CompositeStructureDefinitionRepository":
        from fhircraft.fhir.resources.repository import (
            CompositeStructureDefinitionRepository,
        )

        return CompositeStructureDefinitionRepository
    elif name == "StructureDefinition":
        from fhircraft.fhir.resources.definitions import StructureDefinition

        return StructureDefinition
    elif name == "ElementDefinition":
        from fhircraft.fhir.resources.definitions import ElementDefinition

        return ElementDefinition
    elif name == "FHIRPath":
        from fhircraft.fhir.path import FHIRPath

        return FHIRPath
    elif name == "FHIRPathCollection":
        from fhircraft.fhir.path import FHIRPathCollection

        return FHIRPathCollection
    elif name == "FHIRPathCollectionItem":
        from fhircraft.fhir.path import FHIRPathCollectionItem

        return FHIRPathCollectionItem
    # Configuration system
    elif name == "ValidationConfig":
        from fhircraft.config import ValidationConfig

        return ValidationConfig
    elif name == "FHIRValidationConfig":
        from fhircraft.config import FHIRValidationConfig

        return FHIRValidationConfig
    elif name == "FhircraftConfig":
        from fhircraft.config import FhircraftConfig

        return FhircraftConfig
    elif name == "get_config":
        from fhircraft.config import get_config

        return get_config
    elif name == "set_config":
        from fhircraft.config import set_config

        return set_config
    elif name == "configure":
        from fhircraft.config import configure

        return configure
    elif name == "with_config":
        from fhircraft.config import with_config

        return with_config
    elif name == "disable_constraint":
        from fhircraft.config import disable_constraint

        return disable_constraint
    elif name == "enable_constraint":
        from fhircraft.config import enable_constraint

        return enable_constraint
    elif name == "reset_config":
        from fhircraft.config import reset_config

        return reset_config
    elif name == "load_config_from_env":
        from fhircraft.config import load_config_from_env

        return load_config_from_env
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


__all__ = [
    # Utilities
    "get_FHIR_release_from_version",
    "capitalize",
    "ensure_list",
]
