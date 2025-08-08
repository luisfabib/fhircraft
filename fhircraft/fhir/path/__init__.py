import traceback
import warnings

from .engine.core import FHIRPathError, FHIRPathMixin
from .lexer import FhirPathLexerError
from .parser import FhirPathParser, FhirPathParserError


class FhirPathWarning(Warning):
    pass


try:
    fhirpath = FhirPathParser()
except Exception as e:
    print(traceback.format_exc())
    print(traceback.format_exc())
    print(traceback.format_exc())
