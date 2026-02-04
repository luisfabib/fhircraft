class MappingError(Exception):
    """Base exception for mapping engine errors."""

    pass


class ValidationError(MappingError):
    """Raised when input data validation fails."""

    pass


class SourceTypeError(MappingError):
    """Raised when a source's type condition fails."""

    pass


class SourceConditionError(MappingError):
    """Raised when a source's condition fails."""

    pass


class SourceAssertionError(MappingError):
    """Raised when a source's assertion fails."""

    pass


class SourceProcessingError(MappingError):
    """Raised when source processing fails."""

    pass


class RuleProcessingError(MappingError):
    """Raised when rule processing fails."""

    pass
