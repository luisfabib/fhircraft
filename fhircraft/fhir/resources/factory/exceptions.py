"""
Custom exceptions for the factory pipeline.
"""


class DefinitionIndexError(Exception):
    """Raised when a DefinitionIndex navigation or construction operation fails."""


class DefinitionResolutionError(Exception):
    """Raised when a SnapshotResolver or DefinitionIndex operation fails."""


class UnregisteredTypeError(LookupError):
    """Raised when TypeRegistry cannot resolve a type code or canonical URL."""
