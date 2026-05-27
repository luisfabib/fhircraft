"""
Fhircraft Exceptions Module

This module provides a unified public API for all exceptions in fhircraft.
All exceptions inherit from FhircraftException and are organized by component.
"""

from typing import Optional


class FhircraftException(Exception):
    """
    Base exception for all fhircraft errors.

    All exceptions in fhircraft inherit from this class, allowing users to catch
    any fhircraft-related error with a single except clause.

    Attributes:
        message: Human-readable error message
        component: Optional component identifier (e.g., 'mapper', 'path', 'factory')
    """

    def __init__(self, message: str, component: Optional[str] = None):
        """
        Initialize a fhircraft exception.

        Args:
            message: Detailed error message describing what went wrong
            component: Optional identifier for which component raised the error
        """
        self.message = message
        self.component = component
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        """Format the exception message with optional component context."""
        if self.component:
            return f"[{self.component}] {self.message}"
        return self.message

    def __str__(self) -> str:
        """Return the formatted exception message."""
        return self._format_message()

    def __repr__(self) -> str:
        """Return a detailed representation of the exception."""
        class_name = self.__class__.__name__
        if self.component:
            return f"{class_name}(message={self.message!r}, component={self.component!r})"
        return f"{class_name}(message={self.message!r})"


# ============================================================================
# Mapper Exceptions
# ============================================================================


class MapperException(FhircraftException):
    """Base exception for all FHIR Mapper errors."""

    def __init__(self, message: str, component: str = "mapper"):
        super().__init__(message, component=component)


class MapperParsingError(MapperException):
    """Raised when FHIR Mapping Language syntax or parsing fails."""

    pass


class MapperValidationError(MapperException):
    """Raised when input data validation fails."""

    pass


class MapperScopeError(MapperException):
    """Raised when something accessing or modifying the mapping scope fails."""

    pass


class MapperDigestionError(MapperException):
    """Raised during the digestion of StructureMap definitions."""

    pass


class MapperGroupProcessingError(MapperException):
    """Raised when group processing fails."""

    pass


class MapperRuleProcessingError(MapperException):
    """Raised when rule processing fails."""

    pass


class MapperSourceProcessingError(MapperException):
    """Raised when source/input processing fails."""

    pass


class MapperTargetProcessingError(MapperException):
    """Raised when target/output processing fails."""

    pass


class MapperExecutionError(MapperException):
    """Raised when mapping execution fails."""

    pass


class MapperRegistryNotFoundError(MapperException, FileNotFoundError):
    """Raised when a required StructureMap cannot be resolved."""

    pass


# ============================================================================
# FHIRPath Exceptions
# ============================================================================


class FhirPathException(FhircraftException):
    """Base exception for all FHIRPath errors."""

    def __init__(self, message: str, component: str = "fhirpath"):
        super().__init__(message, component=component)


class FhirPathParsingError(FhirPathException):
    """
    Exception raised for errors encountered during the parsing of FHIRPath expressions.

    This error is typically thrown when the FHIRPath parser encounters invalid syntax
    or cannot interpret a given FHIRPath expression.
    """

    pass


class FhirPathLexingError(FhirPathException):
    """
    Exception raised for errors encountered during the lexical analysis of FHIRPath expressions.

    This error is typically thrown when the FHIRPath lexer encounters invalid tokens
    or cannot interpret a given FHIRPath expression.
    """

    pass


class FhirPathRuntimeError(FhirPathException, RuntimeError):
    """
    Exception raised for errors that occur during the runtime evaluation of FHIRPath expressions.

    This exception is intended to signal issues encountered while processing or executing FHIRPath logic,
    such as invalid operations, type mismatches, or other runtime-specific problems.
    """

    pass


class FhirPathTypeError(FhirPathException):
    """
    Exception raised when there are type mismatches during FHIRPath expression evaluation.

    This typically occurs when attempting incompatible operations on values of different types.
    """

    pass


class FhirPathOperationError(FhirPathException):
    """
    Exception raised when an unsupported or invalid operation is encountered during FHIRPath evaluation.

    This can occur when trying to call functions that don't exist or with incompatible arguments.
    """

    pass


class FhirPathWarning(Warning):
    """
    Warning raised for non-critical issues encountered during FHIRPath expression processing.

    This warning can be used to alert users to potential problems or unexpected behavior
    that do not necessarily prevent the execution of FHIRPath operations.
    """

    pass


# ============================================================================
# Factory Exceptions
# ============================================================================


class DefinitionNotFoundError(FhircraftException, FileNotFoundError):
    """Raised when a required structure definition cannot be resolved."""

    def __init__(self, message: str, component: str = "registry"):
        super().__init__(message, component=component)


class FactoryException(FhircraftException):
    """Base exception for all Factory component errors."""

    def __init__(self, message: str, component: str = "factory"):
        super().__init__(message, component=component)


class FactoryDefinitionIndexError(FactoryException):
    """Raised when a DefinitionIndex navigation or construction operation fails."""

    pass


class FactoryDefinitionResolutionError(FactoryException):
    """Raised when a SnapshotResolver or DefinitionIndex operation fails."""

    pass


class FactoryBuilderError(FactoryException):
    """Raised when a Builder operation fails."""

    pass


class FactoryBuildError(FactoryBuilderError):
    """Alias for FactoryBuilderError for backward compatibility."""

    pass


class FactoryTypeResolutionError(FactoryException, LookupError):
    """Raised when resolving a FHIR type fails."""

    pass


class FactoryAssemblerError(FactoryException, LookupError):
    """Raised when the assembler encounters an error."""

    pass


# ============================================================================
# Package Exceptions
# ============================================================================


class PackageException(FhircraftException):
    """Base exception for all Package Registry errors."""

    def __init__(self, message: str, component: str = "packages"):
        super().__init__(message, component=component)


class PackageNotFoundError(PackageException):
    """Raised when a package is not found in the registry."""

    pass


class PackageResolutionError(PackageException):
    """Raised when package resolution or loading fails."""

    pass


class PackageValidationError(PackageException):
    """Raised when package validation fails."""

    pass


# Public API list
__all__ = [
    # Root exception
    "FhircraftException",
    # Mapper exceptions
    "MapperException",
    "MapperParsingError",
    "MapperValidationError",
    "MapperScopeError",
    "MapperDigestionError",
    "MapperGroupProcessingError",
    "MapperRuleProcessingError",
    "MapperSourceProcessingError",
    "MapperTargetProcessingError",
    "MapperExecutionError",
    "MapperRegistryNotFoundError",
    # FHIRPath exceptions
    "FhirPathException",
    "FhirPathParsingError",
    "FhirPathLexingError",
    "FhirPathRuntimeError",
    "FhirPathTypeError",
    "FhirPathOperationError",
    "FhirPathWarning",
    # Factory exceptions
    "FactoryException",
    "FactoryDefinitionIndexError",
    "FactoryDefinitionResolutionError",
    "FactoryBuilderError",
    "FactoryBuildError",
    "FactoryTypeResolutionError",
    "FactoryAssemblerError",
    "DefinitionNotFoundError",
    # Package exceptions
    "PackageException",
    "PackageNotFoundError",
    "PackageResolutionError",
    "PackageValidationError",
]

