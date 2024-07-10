import logging
import sys
import os.path
import re
import ply.yacc
import operator 

from fhircraft.fhir.path.engine.core import Element, Root, This, Operation, Invocation
import fhircraft.fhir.path.engine.existence as existence
import fhircraft.fhir.path.engine.filtering as filtering
import fhircraft.fhir.path.engine.subsetting as subsetting
import fhircraft.fhir.path.engine.combining as combining
import fhircraft.fhir.path.engine.boolean as boolean
import fhircraft.fhir.path.engine.navigation as navigation
import fhircraft.fhir.path.engine.strings as strings
import fhircraft.fhir.path.engine.additional as additional
import fhircraft.fhir.path.engine.conversion as conversion
from fhircraft.fhir.path.utils import _underline_error_in_fhir_path
from fhircraft.utils import ensure_list
from fhircraft.fhir.path.lexer import FhirPathLexer, FhirPathLexerError

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

    def is_valid(self, string):
        try: 
            try:
                self.parse(string)
                return True     
            except NotImplementedError:
                return True     
        except (FhirPathParserError, FhirPathLexerError):   
            return False     

    def parse_token_stream(self, token_iterator):
        return self.parser.parse(lexer = IteratorToTokenStream(token_iterator))

    # ===================== PLY Parser specification =====================

    precedence = [
        ('left', '(', ')'),
        ('left', 'BOOLEAN_OPERATOR',
                 'TYPES_OPERATOR',
        ),
        ('left', '|',
                 '=',
                 '*',
                 '+',
                 '!',
                 '>',
                 '<',
                 '/',
        ),
        ('left', '.'),
    ]

    def p_error(self, t):
        if t is None:
            raise FhirPathParserError(f'FHIRPath parser error near the end of string "{self.string}"!')
        raise FhirPathParserError(f'FHIRPath parser error at {t.lineno}:{t.col} - Invalid token "{t.value}" ({t.type}):\n{_underline_error_in_fhir_path(self.string, t.value, t.col)}')

    def p_fhirpath_binop(self, p):
        """fhirpath : fhirpath '.' fhirpath
                    | fhirpath '|' fhirpath
                    | fhirpath BOOLEAN_OPERATOR fhirpath"""
        op = p[2]

        if op == '.':
            p[0] = Invocation(p[1], p[3])
        elif op == '|':
            p[0] = combining.Union(p[1], p[3])
        elif op == 'and':
            p[0] = boolean.And(p[1], p[3])
        elif op == 'or':
            p[0] = boolean.Or(p[1], p[3])
        elif op == 'xor':
            p[0] = boolean.Xor(p[1], p[3])
        elif op == 'implies':
            p[0] = boolean.Implies(p[1], p[3])

    def p_fhirpath_base_resource_root(self, p):
        "fhirpath : ROOT_NODE"
        p[0] = Root()
        
    def p_fhirpath_contextual_operator(self, p):
        """fhirpath : CONTEXTUAL_OPERATOR """
        if p[1] == '$':
            p[0] = Root()
        elif p[1] == '$this':
            p[0] = This()
        elif p[1] == '$index':
           raise NotImplementedError()
        elif p[1] == '$total':
           raise NotImplementedError()
        else:
            raise FhirPathParserError(f'FHIRPath parser error at {p.lineno(1)}:{p.lexpos(1)}: Invalid contextual operator "{p[1]}".\n{_underline_error_in_fhir_path(self.string, p[1], p.lexpos(1))}')
            
    def p_fhirpath_environmental_vavriable(self, p):
        """fhirpath : ENVIRONMENTAL_VARIABLE """
        if p[1] == '%resource':
            p[0] = Root()
        elif p[1] == '%context':
            p[0] = This()
        else:
            p[0] = p[1]
                          
    def p_fhirpath_segment(self, p):
        "fhirpath : IDENTIFIER"
        p[0] = Element(p[1])
        
    def p_fhirpath_in_parenthesis(self, p):
        "fhirpath : '(' fhirpath ')'"
        p[0] = p[2]

    def p_fhirpath_as_operation(self, p):
        "fhirpath : operation"
        p[0] = p[1]
        
    def p_fhirpath_idx(self, p):
        "fhirpath : '[' idx ']'"
        p[0] = p[2]

    def p_fhirpath_choice_element(self, p):
        "fhirpath : CHOICE_ELEMENT"
        p[0] = additional.TypeChoice(p[1])
       
    def p_fhirpath_child_idxbrackets(self, p):
        "fhirpath : fhirpath '[' idx ']'"
        p[0] = Invocation(p[1], p[3])


    def p_fhirpath_function(self, p):
        """fhirpath : IDENTIFIER '(' arguments ')' """
        
        def check(args, function, nargs):
            if args[1] == function:
                params = ensure_list(args[3] or [])
                params = [param for param in params if param is not None]
                nprovided = len(params)
                if nprovided not in ensure_list(nargs):
                    raise FhirPathParserError(f'FHIRPath parser error at {p.lineno(1)}:{p.lexpos(1)}: Function {function}() requires {nargs} arguments, but {nprovided} were provided.\n{_underline_error_in_fhir_path(self.string, function, p.lexpos(1))}')
                return True 
            return False
        # -------------------------------------------------------------------------------
        # Existence
        # -------------------------------------------------------------------------------
        if check(p, 'empty', nargs=0):
            p[0] = existence.Empty()
        elif check(p, 'exists', nargs=[0,1]):
            p[0] = existence.Exists(*p[3])
        elif check(p, 'all', nargs=[0,1]):
            p[0] = existence.All(*p[3])
        elif check(p, 'allTrue', nargs=0):
            p[0] = existence.AllTrue()
        elif check(p, 'anyTrue', nargs=0):
            p[0] = existence.AnyTrue()
        elif check(p, 'allFalse', nargs=0):
            p[0] = existence.AllFalse()
        elif check(p, 'anyFalse', nargs=0):
            p[0] = existence.AnyFalse()
        elif check(p, 'subsetOf', nargs=1):
            p[0] = existence.SubsetOf(*p[3])
        elif check(p, 'supersetOf', nargs=1):
            p[0] = existence.SupersetOf(*p[3])
        elif check(p, 'count', nargs=0):
            p[0] = existence.Count()
        elif check(p, 'distinct', nargs=0):
            p[0] = existence.Distinct()
        elif check(p, 'isDistinct', nargs=0):
            p[0] = existence.IsDistinct()
        # -------------------------------------------------------------------------------
        # Subsetting
        # -------------------------------------------------------------------------------
        elif check(p, 'where', nargs=1):
            p[0] = filtering.Where(*p[3])
        elif check(p, 'select', nargs=1):
            p[0] = filtering.Select(*p[3])
        elif check(p, 'repeat', nargs=1):
            p[0] = filtering.Repeat(*p[3])
        elif check(p, 'ofType', nargs=1):
            p[0] = filtering.OfType(*p[3])
        # -------------------------------------------------------------------------------
        # Additional functions
        # -------------------------------------------------------------------------------
        elif check(p, 'extension', nargs=1):
            p[0] = additional.Extension(*p[3])        
        elif check(p, 'resolve', nargs=0):
            p[0] = additional.Resolve()  
        elif check(p, 'hasValue', nargs=0):
            p[0] = additional.HasValue() 
        elif check(p, 'getValue', nargs=0):
            p[0] = additional.GetValue() 
        # -------------------------------------------------------------------------------
        # Subsetting
        # -------------------------------------------------------------------------------
        elif check(p, 'single', nargs=0):
            p[0] = subsetting.Single()
        elif check(p, 'first', nargs=0):
            p[0] = subsetting.First()
        elif check(p, 'last', nargs=0):
            p[0] = subsetting.Last()
        elif check(p, 'tail', nargs=0):
            p[0] = subsetting.Tail()
        elif check(p, 'skip', nargs=1):
            p[0] = subsetting.Skip(*p[3])
        elif check(p, 'take', nargs=1):
            p[0] = subsetting.Take(*p[3])
        elif check(p, 'intersect', nargs=1):
            p[0] = subsetting.Intersect(*p[3])
        elif check(p, 'exclude', nargs=1):
            p[0] = subsetting.Exclude(*p[3])
        # -------------------------------------------------------------------------------
        # Combining
        # -------------------------------------------------------------------------------
        elif check(p, 'union', nargs=1):
            p[0] = combining.Union(*p[3])
        elif check(p, 'combine', nargs=1):
            p[0] = combining.Combine(*p[3])
        # -------------------------------------------------------------------------------
        # Conversion
        # -------------------------------------------------------------------------------
        elif check(p, 'iif', nargs=[2,3]):
            p[0] = conversion.Iif(*p[3])
        elif check(p, 'toBoolean', nargs=0):
            p[0] = conversion.ToBoolean()
        elif check(p, 'convertsToBoolean', nargs=0):
            p[0] = conversion.ConvertsToBoolean()
        elif check(p, 'toInteger', nargs=0):
            p[0] = conversion.ToInteger()
        elif check(p, 'convertsToInteger', nargs=0):
            p[0] = conversion.ConvertsToInteger()
        elif check(p, 'toDate', nargs=0):
            p[0] = conversion.ToDate()
        elif check(p, 'convertsToDate', nargs=0):
            p[0] = conversion.ConvertsToDate()
        elif check(p, 'toDateTime', nargs=0):
            p[0] = conversion.ToDateTime()
        elif check(p, 'convertsToDateTime', nargs=0):
            p[0] = conversion.ConvertsToDateTime()
        elif check(p, 'toDecimal', nargs=0):
            p[0] = conversion.ToDecimal()
        elif check(p, 'convertsToDecimal', nargs=0):
            p[0] = conversion.ConvertsToDecimal()
        elif check(p, 'toQuantity', nargs=[0,1]):
            p[0] = conversion.ToQuantity()
        elif check(p, 'convertsToQuantity', nargs=[0,1]):
            p[0] = conversion.ConvertsToQuantity()
        elif check(p, 'toString', nargs=0):
            p[0] = conversion.ToString()
        elif check(p, 'convertsToString', nargs=0):
            p[0] = conversion.ConvertsToString()
        elif check(p, 'toTime', nargs=0):
            p[0] = conversion.ToTime()
        elif check(p, 'convertsToTime', nargs=0):
            p[0] = conversion.ConvertsToTime()
        # -------------------------------------------------------------------------------
        # String manipulation
        # -------------------------------------------------------------------------------   
        elif check(p, 'indexOf', nargs=1):
            p[0] = strings.IndexOf(*p[3]) 
        elif check(p, 'substring', nargs=(1,2)):
            p[0] = strings.Substring(*p[3]) 
        elif check(p, 'startsWith', nargs=1): 
            p[0] = strings.StartsWith(*p[3])   
        elif check(p, 'endsWith', nargs=1):
            p[0] = strings.EndsWith(*p[3])     
        elif check(p, 'contains', nargs=1):
            p[0] = strings.Contains(*p[3])   
        elif check(p, 'upper', nargs=0):
            p[0] = strings.Upper()   
        elif check(p, 'lower', nargs=0):
            p[0] = strings.Lower()   
        elif check(p, 'replace', nargs=2):
            p[0] = strings.Replace(*p[3])   
        elif check(p, 'matches', nargs=1):
            p[0] = strings.Matches(*p[3])   
        elif check(p, 'replaceMatches', nargs=2):
            p[0] = strings.ReplaceMatches(*p[3])   
        elif check(p, 'length', nargs=0):
            p[0] = strings.Length()   
        elif check(p, 'toChars', nargs=0):
            p[0] = strings.ToChars()    
        # -------------------------------------------------------------------------------
        # Math
        # -------------------------------------------------------------------------------   
        elif check(p, 'abs', nargs=0):
            raise NotImplementedError()     
        elif check(p, 'ceiling', nargs=0):
            raise NotImplementedError()     
        elif check(p, 'exp', nargs=0):
            raise NotImplementedError()     
        elif check(p, 'floor', nargs=0):
            raise NotImplementedError()     
        elif check(p, 'ln', nargs=0):
            raise NotImplementedError()     
        elif check(p, 'log', nargs=1):
            raise NotImplementedError()    
        elif check(p, 'power', nargs=1):
            raise NotImplementedError()    
        elif check(p, 'round', nargs=1):
            raise NotImplementedError()    
        elif check(p, 'sqrt', nargs=0):
            raise NotImplementedError()    
        elif check(p, 'truncate', nargs=0):
            raise NotImplementedError()     
        # -------------------------------------------------------------------------------
        # Tree navigation
        # -------------------------------------------------------------------------------   
        elif check(p, 'children', nargs=0):
            p[0] = navigation.Children()     
        elif check(p, 'descendants', nargs=0):
            p[0] = navigation.Descendants()     
        # -------------------------------------------------------------------------------
        # Boolean functions
        # -------------------------------------------------------------------------------   
        elif check(p, 'not', nargs=0):
            p[0] = boolean.Not()     
        # -------------------------------------------------------------------------------
        # Utility functions
        # -------------------------------------------------------------------------------   
        elif check(p, 'trace', nargs=2):
            raise NotImplementedError()     
        elif check(p, 'now', nargs=0):
            raise NotImplementedError()     
        elif check(p, 'timeOfDay', nargs=0):
            raise NotImplementedError()     
        elif check(p, 'today', nargs=0):
            raise NotImplementedError()     
        else:
            pos = self.string.find(p[1])
            raise FhirPathParserError(f'FHIRPath parser error at {p.lineno(1)}:{pos}: Invalid function "{p[1]}".\n{_underline_error_in_fhir_path(self.string,p[1], pos)}')


    def p_function_arguments(self, p):
        """arguments : fhirpath
                     | operation
                     | value
                     | empty """
        p[0] = [p[1]]

    def p_function_arguments_list(self, p):
        """arguments : arguments ',' arguments """
        p[0] = ensure_list(p[1]) + ensure_list(p[2])
        
    def p_operation(self, p):
        "operation : fhirpath operator righthand"
        p[0] = Operation(p[1], p[2], p[3])
            
    def p_righthand(self, p):
        """righthand : fhirpath
                     | value """
        p[0] = p[1]
        
    def p_value(self, p):
        """value : INTEGER
                 | DECIMAL
                 | STRING
                 | BOOLEAN
                 | DATE
                 | TIME
                 | datetime
                 | quantity"""
        p[0] = p[1]
        
    def p_operator(self, p):
        """operator : '*' 
                    | '/' 
                    | '+' 
                    | '-' 
                    | '|' 
                    | '&' 
                    | '=' 
                    | '~' 
                    | '!' '=' 
                    | '!' '~' 
                    | '>' 
                    | '<' 
                    | '<' '=' 
                    | '>' '=' 
                    | TYPES_OPERATOR"""
        op = ''.join(p[1:])
        # Binary Operators
        if op == '=':
            p[0] = operator.eq
        elif op == '!=':
            p[0] = operator.ne
        elif op == '>':
            p[0] = operator.gt
        elif op == '>=':
            p[0] = operator.ge
        elif op == '<':
            p[0] = operator.lt
        elif op == '<=':
            p[0] = operator.le
        elif op == '+':
            p[0] = operator.add
        elif op == '-':
            p[0] = operator.sub
        elif op == '*':
            p[0] = operator.mul
        elif op == '/':
            p[0] = operator.truediv 
        # Types Operators
        elif op == 'is':
            p[0] = operator.eq 
        else:
            raise NotImplementedError(f'Operator "{op}" not implemented')
        
                
    def p_quantity(self, p):
        """quantity : number STRING
                    | number CALENDAR_DURATION"""
        p[0] = (p[1], p[2])
        
    def p_number(self, p):
        """number : INTEGER
                  | DECIMAL"""
        p[0] = (p[1], p[2])
        
    def p_datetime(self, p):
        "datetime : DATE TIME"
        p[0] = p[1] + p[2]

    def p_idx(self, p):
        "idx : INTEGER"
        p[0] = subsetting.Index(p[1])

        
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
