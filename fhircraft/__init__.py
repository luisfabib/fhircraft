"""
FHIRcraft: FHIR Resource Modeling and Processing Toolkit

This module provides high-level, intuitive imports for the most commonly used components.
Users can import everything they need from the top level without worrying about
internal package structure.

Example usage:
    from fhircraft import FHIRMapper, FHIRPath, ResourceFactory

    # Create a mapper
    mapper = FHIRMapper()

    # Create a resource factory
    factory = ResourceFactory()

    # Use FHIRPath expressions
    result = FHIRPath("Patient.name.family").evaluate(patient_data)
"""

__version__ = "0.3.2"

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
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


__all__ = [
    # Utilities
    "get_FHIR_release_from_version",
    "capitalize",
    "ensure_list",
]
