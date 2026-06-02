"""
FHIRPath Module
"""

# These imports work after fixing the circular dependency
from .engine import FHIRPath, FHIRPathCollection, FHIRPathCollectionItem
from .mixin import FHIRPathMixin
from .parser import FhirPathParser
from .utils import parse_fhirpath


# Use lazy imports to avoid circular dependencies
def __getattr__(name):
    """Lazy loading of resources components to avoid circular import issues."""
    if name == "fhirpath":
        from .parser import fhirpath as _fhirpath
        return _fhirpath
    else:
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

__all__ = [
    # Main FHIRPath functionality
    "FHIRPath",
    "FHIRPathCollectionItem",
    "FHIRPathCollection",
    # Mixin for adding FHIRPath to models
    "FHIRPathMixin",
    # Utilities
    "parse_fhirpath",
]
