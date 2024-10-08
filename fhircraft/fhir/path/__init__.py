from .parser import FhirPathParser, FhirPathParserError
from .engine.core import FHIRPathError, FHIRPathMixin 
from .lexer import FhirPathLexerError  
import traceback

try:
    fhirpath = FhirPathParser()
except Exception as e:
    print(traceback.format_exc()) 
