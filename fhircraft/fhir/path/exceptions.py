"""
A collection of exceptions and warnings used in the FHIRPath module.
"""


class FhirPathParserError(Exception):
    """
    Exception raised for errors encountered during the parsing of FHIRPath expressions.

    This error is typically thrown when the FHIRPath parser encounters invalid syntax
    or cannot interpret a given FHIRPath expression.
    """

    pass


class FhirPathLexerError(Exception):
    """
    Exception raised for errors encountered during the lexical analysis of FHIRPath expressions.

    This error is typically thrown when the FHIRPath lexer encounters invalid tokens
    or cannot interpret a given FHIRPath expression.
    """

    pass


class FHIRPathRuntimeError(RuntimeError):
    """
    Exception raised for errors that occur during the runtime evaluation of FHIRPath expressions.

    This exception is intended to signal issues encountered while processing or executing FHIRPath logic,
    such as invalid operations, type mismatches, or other runtime-specific problems.
    """

    pass


class FHIRPathError(Exception):
    """
    Exception raised for errors encountered during FHIRPath expression evaluation.

    This exception is intended to signal issues specific to FHIRPath processing,
    such as invalid syntax, unsupported operations, or evaluation failures.
    """

    pass


class FhirPathWarning(Warning):
    """
    Warning raised for non-critical issues encountered during FHIRPath expression processing.

    This warning can be used to alert users to potential problems or unexpected behavior
    that do not necessarily prevent the execution of FHIRPath operations.
    """

    pass
