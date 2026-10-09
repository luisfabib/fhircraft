"""
FHIRPath Module
"""

# These imports work after fixing the circular dependency
from .engine import FHIRPathNode
from .collection import FHIRPathCollection, FHIRPathCollectionItem
from .mixin import FHIRPathMixin
from .utils import parse_fhirpath

__all__ = [
    # Main FHIRPath functionality
    "FHIRPathNode",
    "FHIRPathCollectionItem",
    "FHIRPathCollection",
    # Mixin for adding FHIRPath to models
    "FHIRPathMixin",
    # Utilities
    "parse_fhirpath",
]
