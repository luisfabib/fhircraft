"""
FHIR Resources Module

This module provides all FHIR resource-related functionality including:
- FHIRBaseModel: Base class for all FHIR resources
- FHIRModelFactory: Factory for constructing FHIR resource models
- Repository classes: For managing FHIR structure definitions
- Definitions: StructureDefinition and ElementDefinition models
"""

from fhircraft.fhir.resources.base import FHIRBaseModel, FHIRSliceModel
from fhircraft.fhir.resources.factory import FHIRModelFactory
from fhircraft.fhir.resources.datatypes.registry import (
    get_fhir_type,
    get_fhir_type_by_url,
)

__all__ = [
    "FHIRBaseModel",
    "FHIRSliceModel",
    "FHIRModelFactory",
    "get_fhir_type",
    "get_fhir_type_by_url",
]


def __getattr__(name: str):
    """Lazy import of heavyweight components to avoid loading the factory (and
    transitively all 450+ FHIR resource classes) on every import of this package."""
    if name == "FHIRModelFactory":
        from fhircraft.fhir.resources.factory import FHIRModelFactory

        globals()["FHIRModelFactory"] = FHIRModelFactory
        return FHIRModelFactory
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
