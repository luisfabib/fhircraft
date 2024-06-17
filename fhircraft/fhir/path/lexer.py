import sys
import logging

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
    
    literals = ['*', '.', '[', ']', '(', ')', ',', ':', '|', '&', '=']

    reserved_words = { 
        'where': 'WHERE',
        'first': 'FIRST',
        'last': 'LAST',
        'tail': 'TAIL',
        'single': 'SINGLE',    
        'extension': 'EXTENSION',  
        **{resource: 'RESOURCE_BASE' for resource in FHIR_BASE_RESOURCES}                  
    }

    states = [ 
        ('singlequote', 'exclusive'),
        ('doublequote', 'exclusive'),
    ]

    # List of token names
    tokens = list(set(reserved_words.values())) + [
        'ID',
        'CONTEXTUAL_OPERATOR',
        'NUMBER',
        'TYPE_CHOICE',
    ]

    # Regular expression rules for simple tokens
    t_ignore = ' \t'
    t_TYPE_CHOICE = r'\[x\]'
    t_CONTEXTUAL_OPERATOR = r'\$'
    
    # Complex token definitions with actions
    def t_ID(self, t):
        r'[a-zA-Z_@][a-zA-Z0-9_@\-]*'
        t.type = self.reserved_words.get(t.value, 'ID')
        return t

    def t_NUMBER(self, t):
        r'-?\d+(\.\d+)?'
        t.value = float(t.value) if '.' in t.value else int(t.value)
        return t
    


    # Single-quoted strings
    t_singlequote_ignore = ''
    def t_singlequote(self, t):
        r"'"
        t.lexer.string_start = t.lexer.lexpos
        t.lexer.string_value = ''
        t.lexer.push_state('singlequote')

    def t_singlequote_content(self, t):
        r"[^'\\]+"
        t.lexer.string_value += t.value

    def t_singlequote_escape(self, t):
        r'\\.'
        t.lexer.string_value += t.value[1]

    def t_singlequote_end(self, t):
        r"'"
        t.value = t.lexer.string_value
        t.type = 'ID'
        t.lexer.string_value = None
        t.lexer.pop_state()
        return t

    def t_singlequote_error(self, t):
        raise FhirPathLexerError('Error on line %s, col %s while lexing singlequoted field: Unexpected character: %s ' % (t.lexer.lineno, t.lexpos - t.lexer.latest_newline, t.value[0]))


    # Double-quoted strings
    t_doublequote_ignore = ''
    def t_doublequote(self, t):
        r'"'
        t.lexer.string_start = t.lexer.lexpos
        t.lexer.string_value = ''
        t.lexer.push_state('doublequote')

    def t_doublequote_content(self, t):
        r'[^"\\]+'
        t.lexer.string_value += t.value

    def t_doublequote_escape(self, t):
        r'\\.'
        t.lexer.string_value += t.value[1]

    def t_doublequote_end(self, t):
        r'"'
        t.value = t.lexer.string_value
        t.type = 'ID'
        t.lexer.string_value = None
        t.lexer.pop_state()
        return t

    def t_doublequote_error(self, t):
        raise FhirPathLexerError('Error on line %s, col %s while lexing doublequoted field: Unexpected character: %s ' % (t.lexer.lineno, t.lexpos - t.lexer.latest_newline, t.value[0]))


    # Counting lines, handling errors
    def t_newline(self, t):
        r'\n'
        t.lexer.lineno += 1
        t.lexer.latest_newline = t.lexpos

    def t_error(self, t):
        raise FhirPathLexerError('Error on line %s, col %s: Unexpected character: %s ' % (t.lexer.lineno, t.lexpos - t.lexer.latest_newline, t.value[0]))
    

