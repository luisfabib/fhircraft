"""
FHIRcraft: FHIR Resource Modeling and Processing Toolkit

This module provides high-level, intuitive imports for the most commonly used components.
Users can import everything they need from the top level without worrying about
internal package structure.
"""

__version__ = "0.8.3"

# Utility functions are safe to import directly (no circular dependencies)
from fhircraft.utils import capitalize, ensure_list, get_FHIR_release_from_version


# Use lazy imports for main components to avoid circular dependencies
def __getattr__(name):
    """Lazy loading of main components to avoid circular import issues."""
    if name == "FHIRStructureMapper":
        from fhircraft.fhir.mapper import FHIRStructureMapper

        return FHIRStructureMapper
    elif name == "FHIRMapper":
        # Backward-compat alias — use FHIRStructureMapper instead.
        from fhircraft.fhir.mapper import FHIRStructureMapper

        return FHIRStructureMapper
    elif name == "FHIRModelFactory":
        from fhircraft.fhir.resources.factory import FHIRModelFactory

        return FHIRModelFactory
    elif name == "FHIRBaseModel":
        from fhircraft.fhir.resources.base import FHIRBaseModel

        return FHIRBaseModel
    elif name == "StructureDefinitionRegistry":
        from fhircraft.fhir.resources.definitions.registry import (
            StructureDefinitionRegistry,
        )

        return StructureDefinitionRegistry
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
    elif name == "get_config":
        from fhircraft.config import get_config

        return get_config
    elif name == "configure":
        from fhircraft.config import configure

        return configure
    elif name == "override_config":
        from fhircraft.config import override_config

        return override_config
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
