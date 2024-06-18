from .parser import FhirPathParser, FhirPathParserError
from .engine import FHIRPathError 
from .lexer import FhirPathLexerError 

try:
    fhirpath = FhirPathParser()
except Exception as e:
    print(e)
    fhirpath = None