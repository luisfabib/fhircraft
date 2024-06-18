import logging
import sys
import os.path
import re
import ply.yacc

from fhircraft.fhir.path.engine import *
from fhircraft.fhir.path.lexer import FhirPathLexer
from fhircraft.utils import is_url

logger = logging.getLogger(__name__)


def parse(string):
    return FhirPathParser().parse(string)


class FhirPathParserError(Exception):
    pass

class FhirPathParser:
    """
    An LALR-parser for FHIRPath
    """

    tokens = FhirPathLexer.tokens

    def __init__(self, debug=False, lexer_class=None):
        if self.__doc__ is None:
            raise FhirPathParserError(
                'Docstrings have been removed! By design of PLY, '
            )

        self.debug = debug
        self.lexer_class = lexer_class or FhirPathLexer # Crufty but works around statefulness in PLY

        # Since PLY has some crufty aspects and dumps files, we try to keep them local
        # However, we need to derive the name of the output Python file :-/
        output_directory = os.path.dirname(__file__)
        try:
            module_name = os.path.splitext(os.path.split(__file__)[1])[0]
        except:
            module_name = __name__

        start_symbol = 'fhirpath'
        parsing_table_module = '_'.join([module_name, start_symbol, 'parsetab'])

        # Generate the parse table
        self.parser = ply.yacc.yacc(module=self,
                                    debug=self.debug,
                                    tabmodule = parsing_table_module,
                                    outputdir = output_directory,
                                    write_tables=0,
                                    start = start_symbol,
                                    errorlog = logger)

    def parse(self, string, lexer = None):
        self.string = string
        lexer = lexer or self.lexer_class()
        return self.parse_token_stream(lexer.tokenize(string))

    def parse_token_stream(self, token_iterator):
        return self.parser.parse(lexer = IteratorToTokenStream(token_iterator))

    # ===================== PLY Parser specification =====================

    precedence = [
        ('left', '.'),
        ('left', '|'),
        ('left', '&'),
    ]

    def p_error(self, t):
        if t is None:
            raise FhirPathParserError(f'FHIRPath parser error near the end of string "{self.string}"!')
        raise FhirPathParserError(f'FHIRPath parser error at {t.lineno}:{t.col} near token <{t.value}> ({t.type}): \n{self.string}\n{" "*t.col}^')

    def p_fhirpath_binop(self, p):
        """fhirpath : fhirpath '.' fhirpath
                    | fhirpath '|' fhirpath
                    | fhirpath '&' fhirpath"""
        op = p[2]

        if op == '.':
            p[0] = Child(p[1], p[3])
        elif op == '|':
            p[0] = Union(p[1], p[3])
        elif op == '&':
            p[0] = Intersect(p[1], p[3])

    def p_fhirpath_base_resource_root(self, p):
        "fhirpath : RESOURCE_BASE"
        p[0] = Root()
        
    def p_fhirpath_contextual_operator(self, p):
        """fhirpath : CONTEXTUAL_OPERATOR ID 
                    | CONTEXTUAL_OPERATOR empty """
        if p[2] is None:
            p[0] = Root()
        elif p[2] == 'this':
            p[0] = This()
        else:
            raise FhirPathParserError(f'Unknown context operator ${p[2]} at {p.lineno(1)}:{p.lexpos(1)}')
            
    def p_fhirpath_where(self, p):
        """fhirpath : fhirpath '.' WHERE '(' fhirpath '=' string ')' """
        p[0] = Child(p[1], Where(p[5], p[7]))
        
    def p_fhirpath_extension(self, p):
        """fhirpath : fhirpath '.' EXTENSION '(' url ')' """
        if not is_url(p[5]):
            FhirPathParserError(f'Invalid URL for extension() operation: {p[5]}')
        p[0] = Extension(p[1], p[5])

    def p_fhirpath_extension_element(self, p):
        """fhirpath : fhirpath '.' EXTENSION """
        p[0] = Child(p[1], Fields(p[3]))

    def p_fhirpath_last(self, p):
        """fhirpath : fhirpath '.' LAST '(' ')' """
        p[0] = Child(p[1], Index(-1))

    def p_fhirpath_first(self, p):
        """fhirpath : fhirpath '.' FIRST '(' ')' """
        p[0] = Child(p[1], Index(0))
        
    def p_fhirpath_tail(self, p):
        """fhirpath : fhirpath '.' TAIL '(' ')' """
        p[0] = Child(p[1], Slice(start=0, end=-1))

    def p_fhirpath_single(self, p):
        """fhirpath : fhirpath '.' SINGLE '(' ')' """
        p[0] = Child(p[1], Single())

    def p_fhirpath_fields(self, p):
        "fhirpath : fields_or_any"
        p[0] = Fields(*p[1])

    def p_fields_or_any(self, p):
        """fields_or_any : fields
                         | '*'    """
        if p[1] == '*':
            p[0] = ['*']
        else:
            p[0] = p[1]
        
    def p_fhirpath_idx(self, p):
        "fhirpath : '[' idx ']'"
        p[0] = p[2]

    def p_fhirpath_type_choice(self, p):
        "fhirpath : string TYPE_CHOICE"
        p[0] = TypeChoice(p[1])
        
    def p_fhirpath_slice(self, p):
        "fhirpath : '[' slice ']'"
        p[0] = p[2]
        
    def p_fields_id(self, p):
        "fields : ID"
        p[0] = [p[1]]

    def p_string_id(self, p):
        "string : ID"
        p[0] = p[1]
        
    def p_url_id(self, p):
        "url : ID"
        p[0] = p[1]

    def p_fields_comma(self, p):
        "fields : fields ',' fields"
        p[0] = p[1] + p[3]
        
    def p_fhirpath_child_idxbrackets(self, p):
        "fhirpath : fhirpath '[' idx ']'"
        p[0] = Child(p[1], p[3])

    def p_fhirpath_child_slicebrackets(self, p):
        "fhirpath : fhirpath '[' slice ']'"
        p[0] = Child(p[1], p[3])

    def p_fhirpath_parens(self, p):
        "fhirpath : '(' fhirpath ')'"
        p[0] = p[2]

    def p_idx(self, p):
        "idx : NUMBER"
        p[0] = Index(p[1])

    def p_slice_any(self, p):
        "slice : '*'"
        p[0] = Slice()

    def p_slice(self, p): # Currently does not support `step`
        """slice : maybe_int ':' maybe_int
                 | maybe_int ':' maybe_int ':' maybe_int """
        p[0] = Slice(*p[1::2])

    def p_maybe_int(self, p):
        """maybe_int : NUMBER
                     | empty"""
        p[0] = p[1]

    def p_empty(self, p):
        'empty :'
        p[0] = None

class IteratorToTokenStream:
    def __init__(self, iterator):
        self.iterator = iterator

    def token(self):
        try:
            return next(self.iterator)
        except StopIteration:
            return None
