"""
Custom exceptions for the factory pipeline.
"""


class DefinitionIndexError(Exception):
    """Raised when a DefinitionIndex navigation or construction operation fails."""


class DefinitionResolutionError(Exception):
    """Raised when a SnapshotResolver or DefinitionIndex operation fails."""


class BuilderError(Exception):
    """Raised when a Builder operation fails."""


class TypeResolutionError(LookupError):
    """Raised when resolving a FHIR type fails."""


class AssemblerError(LookupError):
    """Raised when the assembler encounters an error."""
