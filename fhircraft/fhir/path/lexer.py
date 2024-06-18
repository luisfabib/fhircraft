import sys
import logging

from fhircraft.fhir.path.utils import _underline_error_in_fhir_path
from fhir.resources.R4B.fhirtypesvalidators import MODEL_CLASSES as FHIR_BASE_RESOURCES
import ply.lex


class FhirPathLexerError(Exception):
    pass

class FhirPathLexer:
    '''
    A Lexical analyzer for JsonPath.

    '''
    def __init__(self, debug=False):
        self.debug = debug
        if self.__doc__ is None:
            raise FhirPathLexerError('Docstrings have been removed! By design of PLY, jsonpath-rw requires docstrings. You must not use PYTHONOPTIMIZE=2 or python -OO.')

    def tokenize(self, string):
        '''
        Maps a string to an iterator over tokens. In other words: [char] -> [token]
        '''

        new_lexer = ply.lex.lex(module=self)
        new_lexer.latest_newline = 0
        new_lexer.string_value = None
        new_lexer.input(string)

        while True:
            t = new_lexer.token()
            if t is None:
                break
            t.col = t.lexpos - new_lexer.latest_newline
            yield t

        if new_lexer.string_value is not None:
            raise FhirPathLexerError('Unexpected EOF in string literal or identifier')
        
    # ============== PLY Lexer specification ==================
    #
    # Tokenizer for FHIRpath
    #
    # =========================================================
    
    # Symbols (http://hl7.org/fhirpath/N1/#symbols)
    # -------------------------------------------------------------------------------
    # Symbols provide structure to the language and allow symbolic invocation of common 
    # operators such as addition. FHIRPath defines the following symbols:
    literals = [
        '*', '+', '-', ',', '.', '[', ']', '(', ')', ',', 
        ':', '|', '&', '=', '!', '>', '<', '{', '}', '/'
    ]

    reserved_words = { 
        
        # Funtions (http://hl7.org/fhirpath/N1/#functions)
        # -------------------------------------------------------------------------------
        **{operator: 'FUNCTION' for operator in [
            # Existence (http://hl7.org/fhirpath/N1/#existence)
            'empty', 'exists', 'all', 'allTrue', 'anyTrue', 'allFalse', 'anyFalse',
            'subsetOf', 'supersetOf', 'count', 'distinct', 'isDistinct',
            # Filtering and projection (http://hl7.org/fhirpath/N1/#filtering-and-projection)
            'where', 'select', 'repeat', 'ofType',
            # Subsetting (http://hl7.org/fhirpath/N1/#subsetting)
            'first', 'last', 'tail', 'single', 'skip', 'take', 'intersect', 'exclude',
            # Combining (http://hl7.org/fhirpath/N1/#combining)
            'union', 'combine',
            # Conversion (http://hl7.org/fhirpath/N1/#conversion)
            'iif', 'toBoolean', 'convertsToBoolean', 'toInteger', 'convertsToInteger',
            'toDate', 'convertsToDate', 'toDateTime', 'convertsToDateTime', 'toDecimal', 
            'convertsToDecimal', 'toQuantity', 'convertsToQuantity', 'toString', 'convertsToString',
            'toTime', 'convertsToTime',
            # String manipulation (http://hl7.org/fhirpath/N1/#string-manipulation)
            'indexOf', 'substring', 'startsWith', 'endsWith', 'contains', 'upper', 'lower', 'replace',
            'matches', 'replaceMatches', 'length', 'toChars',
            # Math (http://hl7.org/fhirpath/N1/#math)
            'abs', 'ceiling', 'exp', 'floor', 'ln', 'log', 'power', 'round',
            'sqrt', 'truncate',
            # Tree navigation (http://hl7.org/fhirpath/N1/#tree-navigation)
            'children', 'descendants',
            # Utility functions (http://hl7.org/fhirpath/N1/#utility-functions)
            'trace', 'now', 'timeOfDay', 'today',
            # Additional functions (https://build.fhir.org/fhirpath.html#functions)            
            #'extension',
        ]},  
        
        # Boolean logic (http://hl7.org/fhirpath/N1/#boolean-logic)
        # -------------------------------------------------------------------------------
        **{operator: 'BOOLEAN_OPERATOR' for operator in ['and','or','xor','implies']},  
        
        # Boolean (http://hl7.org/fhirpath/N1/#boolean)
        # -------------------------------------------------------------------------------
        **{operator: 'BOOLEAN' for operator in ['true','false']},  
        
        # Calendar Duration (http://hl7.org/fhirpath/N1/#boolean)
        # -------------------------------------------------------------------------------
        # For time-valued quantities, in addition to the definite duration UCUM units,
        # FHIRPath defines calendar duration keywords for calendar duration units
        **{operator: 'CALENDAR_DURATION' for operator in [
            'week','weeks','month','months','year','years','day','days',
            'hour','hours','minute','minutes','second','seconds','miliseond','miliseconds'
        ]},   
        
        #  FHIRPath Root Names (http://hl7.org/fhirpath/N1/#path-selection)
        # -------------------------------------------------------------------------------       
        # The path may start with the type of the root node            
        **{resource: 'ROOT_NODE' for resource in FHIR_BASE_RESOURCES}                  
    }

    # List of token names
    tokens = list(set(reserved_words.values())) + [
        'IDENTIFIER',
        'INTEGER',
        'DECIMAL',
        'DATE',
        'TIME',
        'CHOICE_ELEMENT',
        'STRING',
        'CONTEXTUAL_OPERATOR',
        'ENVIRONMENTAL_VARIABLE',
    ]
    
    def t_ignore_WHITESPACE(self, t):
        # Whitespace (http://hl7.org/fhirpath/N1/#whitespace)
        # -------------------------------------------------------------------------------
        # FHIRPath defines tab (\t), space ( ), line feed (\n) and carriage return (\r) as whitespace,
        # meaning they are only used to separate other tokens within the language. Any number
        # of whitespace characters can appear, and the language does not use whitespace for 
        # anything other than delimiting tokens.
        r'[\s]'
        if t.value=='\n':
            t.lexer.lineno += 1
            t.lexer.latest_newline = t.lexpos
        
    def t_ignore_COMMENT(self, t):
        # Comments (http://hl7.org/fhirpath/N1/#comments)
        # -------------------------------------------------------------------------------
        # FHIRPath defines two styles of comments, single-line, and multi-line. 
        # - A single-line comment consists of two forward slashes, followed by any 
        #   text up to the end of the line
        # - To begin a multi-line comment, the typical forward slash-asterisk token
        #   is used. The comment is closed with an asterisk-forward slash, and everything enclosed is ignored
        r'\/\*([\s\S]*?)\*\/|\/\/(.*)'
        for substring in ['//','/*','*/']:
            t.value = t.value.replace(substring,'')
        t.value = t.value.strip()
    
    def t_CHOICE_ELEMENT(self, t):
        r'(?:\`[a-zA-Z][a-zA-Z0-9\-][^\`]*\[x\]\`)|(?:(?:_|[a-zA-Z])[a-zA-Z0-9_]*\[x\])'
        t.value = t.value.replace('[x]','')
        return t
    
    def t_ENVIRONMENTAL_VARIABLE(self, t):
        # Environmental variable (http://hl7.org/fhirpath/N1/#environment-variables)
        # -------------------------------------------------------------------------------
        # A token introduced by a % refers to a value that is passed into the evaluation 
        # engine by the calling environment. 
        r'\%(\w*)?'
        return t
    
    def t_CONTEXTUAL_OPERATOR(self, t):
        # Contextual Operators (http://hl7.org/fhirpath/N1/#functions)
        # -------------------------------------------------------------------------------
        # Special elements within a funciton that refere to the input collection under evalution
        r'\$(\w*)?'
        return t
    
    def t_DATE(self, t):
        # Date (http://hl7.org/fhirpath/N1/#date)
        # -------------------------------------------------------------------------------
        # The Date type represents date and partial date values.
        # - The date literal is a subset of [ISO8601]:
        # - A date being with a @
        # - It uses the format YYYY-MM-DD format, though month and day parts are optional
        # - Months must be present if a day is present
        r'@\d{4}(?:-\d{2}(?:-\d{2})?)?'
        t.value = t.value.replace('@','')
        return t
    
    def t_TIME(self, t):
        # Time (http://hl7.org/fhirpath/N1/#time)
        # -------------------------------------------------------------------------------
        # The Time type represents time-of-day and partial time-of-day values.
        # - A time begins with a @T
        # - It uses the Thh:mm:ss.fff format
        r'@T\d{2}:\d{2}(?::\d{2}.\d{3}(.?))?'
        t.value = t.value.replace('@T','')
        return t
    
    def t_NUMBER(self, t):
        r'-?\d+(\.\d+)?'
        if '.' in t.value:
            # Decimal (http://hl7.org/fhirpath/N1/#decimal)
            # -------------------------------------------------------------------------------
            t.value = float(t.value) 
            t.type = 'DECIMAL'
        else:
            # Integer (http://hl7.org/fhirpath/N1/#integer)
            # -------------------------------------------------------------------------------
            t.value = int(t.value)
            t.type = 'INTEGER'
        return t

    def t_STRING(self, t):
        # String (http://hl7.org/fhirpath/N1/#string)
        # -------------------------------------------------------------------------------
        # The String type represents string values up to 231-1 characters in length. String 
        # literals are surrounded by single-quotes and may use \-escapes to escape quotes 
        # and represent Unicode characters 
        r'\'([^\']*)?\''
        t.value = t.value.strip('\'')
        return t
    
    def t_IDENTIFIER(self, t):
        # Identifiers (http://hl7.org/fhirpath/N1/#identifiers)
        # -------------------------------------------------------------------------------
        # Identifiers are used as labels to allow expressions to reference elements such 
        # as model types and properties. FHIRPath supports two types of identifiers, simple
        # and delimited.
        # - A simple identifier is any alphabetical character or an underscore, followed by 
        #   any number of alpha-numeric characters or underscores
        # - A delimited identifier is any sequence of characters enclosed in backticks ( ` ):
        r'(?:\`[a-zA-Z][a-zA-Z0-9\-][^\`]*\`)|(?:(?:_|[a-zA-Z])[a-zA-Z0-9_]*)'
        t.value = t.value.strip('`')
        t.type = self.reserved_words.get(t.value, 'IDENTIFIER')
        return t

    def t_error_invalid_function(self, t):
        r'[a-zA-Z][a-zA-Z_0-9]*\((?:.*)?\)'
        t.value = t.value.split('(')[0]
        pos = t.lexpos - t.lexer.latest_newline
        raise FhirPathLexerError(f'FHIRPath lexer error at {t.lexer.lineno}:{pos} - Invalid function: "{t.value}".\n{_underline_error_in_fhir_path(t.lexer.lexdata, t.value, pos)}')

    def t_error_doublequote_string(self, t):
        r'\"([^\"]*)?\"'
        pos = t.lexpos - t.lexer.latest_newline
        raise FhirPathLexerError(f'FHIRPath lexer error at {t.lexer.lineno}:{pos} - Double-quoted strings are not valid in FHIRPath: {t.value}\n{_underline_error_in_fhir_path(t.lexer.lexdata, t.value, pos)}')

    def t_error(self, t):
        raise FhirPathLexerError(f'FHIRPath lexer error at {t.lexer.lineno}:{t.lexpos - t.lexer.latest_newline} - Unexpected character: {t.value[0]}')
    
