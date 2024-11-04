from fhircraft.fhir.path.utils import _underline_error_in_fhir_path
import ply.lex

class FhirMappingLanguageLexerError(Exception):
    pass

class FhirMappingLanguageLexer:
    '''
    A Lexical analyzer for JsonPath.

    '''
    def __init__(self, debug=False):
        self.debug = debug
        if self.__doc__ is None:
            raise FhirMappingLanguageLexerError('Docstrings have been removed by design of PLY.')

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
            raise FhirMappingLanguageLexerError('Unexpected EOF in string literal or identifier')
        
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
        '.', ',', ';', ':','[', ']', '(', ')', '{', '}', '=', '+', '-', '*', '|', '/', '&', '<', '>'
    ]

    reserved_words = { 
        
        # Reserved keywords (https://build.fhir.org/mapping-language.html#reserved)
        # -------------------------------------------------------------------------------
        **{
            word: word.upper() for word in [
                'map',
                'uses',
                'as',
                'alias',
                'imports',
                'group',
                'extends',
                'default',
                'where',
                'check',
                'log',
                'let',
                'then',
                'types',
                'type',
                'first',
                'not_first',
                'last',
                'not_last',
                'only_one',
                'share',
                'single',
                'source',
                'target',
                'queried',
                'produced',
                'conceptMap',
                'prefix',
            ]
        },   
    }

    # List of token names
    tokens = list(set(reserved_words.values())) + [
        'IDENTIFIER',
        'INTEGER',
        'DECIMAL',
        'BOOLEAN',
        'DATE',
        'TIME',
        'DATETIME',
        'STRING',
        'COMMENT',
        'RIGHT_ARROW'
    ]
    
    def t_ignore_WHITESPACE(self, t):
        r'[\s]'
        if t.value=='\n':
            t.lexer.lineno += 1
            t.lexer.latest_newline = t.lexpos

    # def t_ignore_COMMENT(self, t):
    #     r'\/\*([\s\S]*?)\*\/|\/\/(.*)'
    #     for substring in ['//','/*','*/']:
    #         t.value = t.value.replace(substring,'')
    #     t.value = t.value.strip()
        
    def t_RIGHT_ARROW(self, t):
        r'->'
        return t

    def t_DATETIME(self, t):
        r'@\d{4}(?:-\d{2}(?:-\d{2})?)?T(?:\d{2}(?:\:\d{2}(?:\:\d{2}(?:.\d{3}(?:[\+|\-]\d{2}(?:\:\d{2})?)?)?)?)?)?'
        return t    
    
    def t_DATE(self, t):
        r'@\d{4}(?:-\d{2}(?:-\d{2})?)?'
        return t
    
    def t_BOOLEAN(self, t):
        r'true|false'
        return t
    
    def t_TIME(self, t):
        r'\@T\d{2}(?:\:\d{2}(?:\:\d{2}(?:\.\d{3}(?:[+|-]\d{2}(?:\:\d{2})?)?)?)?)?'
        return t
    
    def t_NUMBER(self, t):
        r'-?\d+(\.\d+)?'
        if '.' in t.value:
            t.value = float(t.value) 
            t.type = 'DECIMAL'
        else:
            t.value = int(t.value)
            t.type = 'INTEGER'
        return t

    def t_STRING(self, t):
        r'(\'([^\']*)?\')|(\"([^\"]*)?\")'
        if t.value.startswith('\'') and t.value.endswith('\''):   
            t.value = t.value.strip('\'')
        else:
            t.value = t.value.strip('\"')
        return t
    
    def t_IDENTIFIER(self, t):
        r'(?:\`[a-zA-Z][a-zA-Z0-9\-][^\`]*\`)|(?:(?:_|[a-zA-Z])[a-zA-Z0-9_]*)'
        if t.value.startswith('`') and t.value.endswith('`'):        
            t.value = t.value.strip('`') 
            t.type = 'IDENTIFIER'
        else:
            t.type = self.reserved_words.get(t.value, 'IDENTIFIER')
        return t

    def t_error_invalid_function(self, t):
        r'[a-zA-Z][a-zA-Z_0-9]*\((?:.*)?\)'
        t.value = t.value.split('(')[0]
        pos = t.lexpos - t.lexer.latest_newline
        raise FhirMappingLanguageLexerError(f'FHIRPath lexer error at {t.lexer.lineno}:{pos} - Invalid function: "{t.value}".\n{_underline_error_in_fhir_path(t.lexer.lexdata, t.value, pos)}')

    def t_error(self, t):
        raise FhirMappingLanguageLexerError(f'FHIRPath lexer error at {t.lexer.lineno}:{t.lexpos - t.lexer.latest_newline} - Unexpected character: {t.value[0]}')
    

