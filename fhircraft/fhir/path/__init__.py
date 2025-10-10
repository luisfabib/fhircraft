"""
FHIR Path Module

This module provides FHIRPath expression evaluation functionality:
- FHIRPath: Main class for parsing and evaluating FHIRPath expressions
- FHIRPathCollection: Collection of FHIRPath results
- FHIRPathMixin: Mixin for adding FHIRPath functionality to models

Recommended imports:
    from fhircraft.fhir.path import FHIRPath
    from fhircraft.fhir.path import FHIRPathMixin
"""

# These imports work after fixing the circular dependency
from .engine import FHIRPath, FHIRPathCollection, FHIRPathCollectionItem
from .mixin import FHIRPathMixin
from .parser import FhirPathParser
from .utils import import_fhirpath_engine


# Use lazy imports to avoid circular dependencies
def __getattr__(name):
    """Lazy loading of resources components to avoid circular import issues."""
    if name == "fhirpath":
        return FhirPathParser()
    else:
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


__all__ = [
    # Main FHIRPath functionality
    "FHIRPath",
    "FHIRPathCollectionItem",
    "FHIRPathCollection",
    # Mixin for adding FHIRPath to models
    "FHIRPathMixin",
    # Parser
    "FhirPathParser",
    # Utilities
    "import_fhirpath_engine",
]
