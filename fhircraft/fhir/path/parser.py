import logging
import os.path
import traceback
from typing import Any

import ply.yacc

import fhircraft.fhir.path.engine.additional as additional
import fhircraft.fhir.path.engine.aggregates as aggregates
import fhircraft.fhir.path.engine.boolean as boolean
import fhircraft.fhir.path.engine.collection as collection
import fhircraft.fhir.path.engine.combining as combining
import fhircraft.fhir.path.engine.comparison as comparison
import fhircraft.fhir.path.engine.conversion as conversion
import fhircraft.fhir.path.engine.environment as environment
import fhircraft.fhir.path.engine.equality as equality
import fhircraft.fhir.path.engine.existence as existence
import fhircraft.fhir.path.engine.filtering as filtering
import fhircraft.fhir.path.engine.literals as literals
import fhircraft.fhir.path.engine.math as math
import fhircraft.fhir.path.engine.navigation as navigation
import fhircraft.fhir.path.engine.strings as strings
import fhircraft.fhir.path.engine.subsetting as subsetting
import fhircraft.fhir.path.engine.types as types
import fhircraft.fhir.path.engine.utility as utility
from fhircraft.fhir.path.engine.core import (
    Element,
    FHIRPath,
    Invocation,
    Literal,
    RootElement,
    This,
)
from fhircraft.fhir.path.exceptions import FhirPathLexerError, FhirPathParserError
from fhircraft.fhir.path.lexer import FhirPathLexer
from fhircraft.fhir.path.utils import _underline_error_in_fhir_path
from fhircraft.utils import ensure_list

logger = logging.getLogger(__name__)


def parse(string):
    return FhirPathParser().parse(string)


class FhirPathParser:
    """
    An LALR-parser for FHIRPath
    """

    tokens = FhirPathLexer.tokens

    def __init__(self, debug=False, lexer_class=None):
        if self.__doc__ is None:
            raise FhirPathParserError(
                "Docstrings have been removed! By design of PLY, "
            )

        self.debug = debug
        self.lexer_class = (
            lexer_class or FhirPathLexer
        )  # Crufty but works around statefulness in PLY

        # Since PLY has some crufty aspects and dumps files, we try to keep them local
        # However, we need to derive the name of the output Python file :-/
        output_directory = os.path.dirname(__file__)
        try:
            module_name = os.path.splitext(os.path.split(__file__)[1])[0]
        except:
            module_name = __name__

        start_symbol = "expression"
        parsing_table_module = "_".join([module_name, start_symbol, "parsetab"])

        # Generate the parse table
        self.parser = ply.yacc.yacc(
            module=self,
            debug=self.debug,
            tabmodule=parsing_table_module,
            outputdir=output_directory,
            write_tables=False,
            start=start_symbol,
            errorlog=logger,
        )

    def parse(self, string, lexer=None) -> FHIRPath | Any:
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
        return self.parser.parse(lexer=IteratorToTokenStream(token_iterator))

    # ===================== PLY Parser specification =====================
    precedence = [
        ("left", "IMPLIES"),
        ("left", "OR", "XOR"),
        ("left", "AND"),
        ("left", "IN", "CONTAINS"),
        ("left", "EQUAL", "EQUIVALENT", "NOT_EQUIVALENT", "NOT_EQUAL"),
        ("left", "GREATER_THAN", "LESS_THAN", "GREATER_EQUAL_THAN", "LESS_EQUAL_THAN"),
        ("left", "|"),
        ("left", "IS", "AS"),
        ("left", "*", "/", "DIV", "MOD"),
        ("left", "+", "-", "&"),
        ("left", "[", "]"),
        ("left", "."),
    ]

    def p_error(self, t):
        if t is None:
            raise FhirPathParserError(
                f'FHIRPath parser error near the end of string "{self.string}"!'
            )
        raise FhirPathParserError(
            f'FHIRPath parser error at {t.lineno}:{t.col} - Invalid token "{t.value}" ({t.type}):\n{_underline_error_in_fhir_path(self.string, t.value, t.col)}'
        )

    def p_fhirpath_term_expression(self, p):
        """expression : term"""
        p[0] = p[1]

    def p_fhirpath_invocation_expression(self, p):
        "expression : expression '.' invocation"
        p[0] = Invocation(p[1], p[3])

    def p_fhirpath_indexer_expression(self, p):
        "expression : expression '[' expression ']'"
        p[0] = Invocation(p[1], subsetting.Index(p[3]))

    def p_fhirpath_multiplicative_operation(self, p):
        """expression : expression '*' expression
        | expression '/' expression
        | expression DIV expression
        | expression MOD expression"""
        op = p[2]
        if op == "*":
            p[0] = math.Multiplication(p[1], p[3])
        elif op == "/":
            p[0] = math.Division(p[1], p[3])
        elif op == "div":
            p[0] = math.Div(p[1], p[3])
        elif op == "mod":
            p[0] = math.Mod(p[1], p[3])

    def p_fhirpath_additive_operation(self, p):
        """expression : expression '+' expression
        | expression '-' expression
        | expression '&' expression"""
        op = p[2]
        if op == "+":
            p[0] = math.Addition(p[1], p[3])
        elif op == "-":
            p[0] = math.Subtraction(p[1], p[3])
        elif op == "&":
            p[0] = strings.Concatenation(p[1], p[3])

    def p_fhirpath_type_operation(self, p):
        """expression : expression IS type_specifier
        | expression AS type_specifier"""
        op = p[2]
        if op == "is":
            p[0] = types.Is(p[1], p[3])
        elif op == "as":
            p[0] = types.As(p[1], p[3])

    def p_fhirpath_union_operation(self, p):
        """expression : expression '|' expression"""
        p[0] = collection.Union(p[1], p[3])

    def p_fhirpath_equality_operation(self, p):
        """expression : expression EQUAL expression
        | expression EQUIVALENT expression
        | expression NOT_EQUAL expression
        | expression NOT_EQUIVALENT expression"""
        op = p[2]
        if op == "=":
            p[0] = equality.Equals(p[1], p[3])
        elif op == "~":
            p[0] = equality.Equivalent(p[1], p[3])
        elif op == "!=":
            p[0] = equality.NotEquals(p[1], p[3])
        elif op == "!~":
            p[0] = equality.NotEquivalent(p[1], p[3])

    def p_fhirpath_inequality_operation(self, p):
        """expression : expression GREATER_THAN expression
        | expression GREATER_EQUAL_THAN expression
        | expression LESS_THAN expression
        | expression LESS_EQUAL_THAN expression"""
        op = p[2]
        if op == ">":
            p[0] = comparison.GreaterThan(p[1], p[3])
        elif op == ">=":
            p[0] = comparison.GreaterEqualThan(p[1], p[3])
        elif op == "<":
            p[0] = comparison.LessThan(p[1], p[3])
        elif op == "<=":
            p[0] = comparison.LessEqualThan(p[1], p[3])

    def p_fhirpath_membership_fhirpath_operation(self, p):
        """expression : expression IN expression
        | expression CONTAINS expression"""
        op = p[2]
        if op == "in":
            p[0] = collection.In(p[1], p[3])
        elif op == "contains":
            p[0] = collection.Contains(p[1], p[3])

    def p_fhirpath_and_operation(self, p):
        """expression : expression AND expression"""
        p[0] = boolean.And(p[1], p[3])

    def p_fhirpath_or_operation(self, p):
        """expression : expression OR expression
        | expression XOR expression"""
        op = p[2]
        if op == "or":
            p[0] = boolean.Or(p[1], p[3])
        elif op == "xor":
            p[0] = boolean.Xor(p[1], p[3])

    def p_fhirpath_implies_operation(self, p):
        """expression : expression IMPLIES expression"""
        p[0] = boolean.Implies(p[1], p[3])

    def p_fhirpath_term(self, p):
        """term : invocation
        | literal
        | constant
        | parenthesized_expression"""
        p[0] = p[1]

    def p_fhirpath_parenthesized_expression(self, p):
        """parenthesized_expression : '(' expression ')'"""
        p[0] = p[2]

    def p_fhirpath_invocation(self, p):
        """invocation : element
        | root
        | type_choice
        | function
        | contextual"""
        p[0] = p[1]

    def p_fhirpath_root(self, p):
        """root : ROOT_NODE"""
        p[0] = RootElement(p[1])

    def p_fhirpath_element(self, p):
        """element : identifier"""
        p[0] = Element(p[1])

    def p_fhirpath_typechoice_invocation(self, p):
        "type_choice : CHOICE_ELEMENT"
        p[0] = additional.TypeChoice(p[1])

    def p_fhirpath_constant(self, p):
        """constant : ENVIRONMENTAL_VARIABLE"""
        p[0] = environment.EnvironmentVariable(p[1])

    def p_fhirpath_contextual(self, p):
        """contextual : CONTEXTUAL_OPERATOR"""
        if p[1] == "$this":
            p[0] = environment.ContextualThis()
        elif p[1] == "$index":
            p[0] = environment.ContextualIndex()
        elif p[1] == "$total":
            p[0] = environment.ContextualTotal()
        else:
            raise FhirPathParserError(
                f'FHIRPath parser error at {p.lineno(1)}:{p.lexpos(1)}: Invalid contextual operator "{p[1]}".\n{_underline_error_in_fhir_path(self.string, p[1], p.lexpos(1))}'
            )

    def p_fhirpath_type_specifier(self, p):
        """type_specifier : identifier
        | ROOT_NODE"""
        p[0] = p[1]

    def p_fhirpath_type_specifier_context(self, p):
        """type_specifier : type_specifier '.' identifier"""
        p[0] = f"{p[1]}.{p[3]}"

    def p_fhirpath_function(self, p):
        """function : function_name '(' arguments ')'"""

        def check(args, function, nargs):
            if args[1] == function:
                params = ensure_list(args[3] or [])
                params = [param for param in params if param is not None]
                nprovided = len(params)
                if nprovided not in ensure_list(nargs):
                    raise FhirPathParserError(
                        f"FHIRPath parser error at {p.lineno(1)}:{p.lexpos(1)}: Function {function}() requires {nargs} arguments, but {nprovided} were provided.\n{_underline_error_in_fhir_path(self.string, function, p.lexpos(1))}"
                    )
                return True
            return False

        # -------------------------------------------------------------------------------
        # Existence
        # -------------------------------------------------------------------------------
        if check(p, "empty", nargs=0):
            p[0] = existence.Empty()
        elif check(p, "exists", nargs=[0, 1]):
            p[0] = existence.Exists(*p[3])
        elif check(p, "all", nargs=[0, 1]):
            p[0] = existence.All(*p[3])
        elif check(p, "allTrue", nargs=0):
            p[0] = existence.AllTrue()
        elif check(p, "anyTrue", nargs=0):
            p[0] = existence.AnyTrue()
        elif check(p, "allFalse", nargs=0):
            p[0] = existence.AllFalse()
        elif check(p, "anyFalse", nargs=0):
            p[0] = existence.AnyFalse()
        elif check(p, "subsetOf", nargs=1):
            p[0] = existence.SubsetOf(*p[3])
        elif check(p, "supersetOf", nargs=1):
            p[0] = existence.SupersetOf(*p[3])
        elif check(p, "count", nargs=0):
            p[0] = existence.Count()
        elif check(p, "distinct", nargs=0):
            p[0] = existence.Distinct()
        elif check(p, "isDistinct", nargs=0):
            p[0] = existence.IsDistinct()
        # -------------------------------------------------------------------------------
        # Subsetting
        # -------------------------------------------------------------------------------
        elif check(p, "where", nargs=1):
            p[0] = filtering.Where(*p[3])
        elif check(p, "select", nargs=1):
            p[0] = filtering.Select(*p[3])
        elif check(p, "repeat", nargs=1):
            p[0] = filtering.Repeat(*p[3])
        elif check(p, "ofType", nargs=1):
            p[0] = filtering.OfType(*p[3])
        # -------------------------------------------------------------------------------
        # Additional functions
        # -------------------------------------------------------------------------------
        elif check(p, "extension", nargs=1):
            p[0] = additional.Extension(*p[3])
        elif check(p, "resolve", nargs=0):
            p[0] = additional.Resolve()
        elif check(p, "hasValue", nargs=0):
            p[0] = additional.HasValue()
        elif check(p, "getValue", nargs=0):
            p[0] = additional.GetValue()
        elif check(p, "htmlChecks", nargs=0):
            p[0] = additional.HtmlChecks()
        elif check(p, "lowBoundary", nargs=0):
            p[0] = additional.LowBoundary()
        elif check(p, "highBoundary", nargs=0):
            p[0] = additional.HighBoundary()
        elif check(p, "elementDefinition", nargs=0):
            p[0] = additional.ElementDefinition()
        elif check(p, "slice", nargs=2):
            p[0] = additional.Slice(*p[3])
        elif check(p, "checkModifiers", nargs=1):
            p[0] = additional.CheckModifiers(*p[3])
        elif check(p, "conformsTo", nargs=1):
            p[0] = additional.ConformsTo(*p[3])
        elif check(p, "memberOf", nargs=1):
            p[0] = additional.MemberOf(*p[3])
        elif check(p, "subsumes", nargs=1):
            p[0] = additional.Subsumes(*p[3])
        elif check(p, "subsumedBy", nargs=1):
            p[0] = additional.SubsumedBy(*p[3])
        elif check(p, "comparable", nargs=1):
            p[0] = additional.Comparable(*p[3])
        # -------------------------------------------------------------------------------
        # Subsetting
        # -------------------------------------------------------------------------------
        elif check(p, "single", nargs=0):
            p[0] = subsetting.Single()
        elif check(p, "first", nargs=0):
            p[0] = subsetting.First()
        elif check(p, "last", nargs=0):
            p[0] = subsetting.Last()
        elif check(p, "tail", nargs=0):
            p[0] = subsetting.Tail()
        elif check(p, "skip", nargs=1):
            p[0] = subsetting.Skip(*p[3])
        elif check(p, "take", nargs=1):
            p[0] = subsetting.Take(*p[3])
        elif check(p, "intersect", nargs=1):
            p[0] = subsetting.Intersect(*p[3])
        elif check(p, "exclude", nargs=1):
            p[0] = subsetting.Exclude(*p[3])
        # -------------------------------------------------------------------------------
        # Combining
        # -------------------------------------------------------------------------------
        elif check(p, "union", nargs=1):
            p[0] = combining.Union(*p[3])
        elif check(p, "combine", nargs=1):
            p[0] = combining.Combine(*p[3])
        # -------------------------------------------------------------------------------
        # Conversion
        # -------------------------------------------------------------------------------
        elif check(p, "iif", nargs=[2, 3]):
            p[0] = conversion.Iif(*p[3])
        elif check(p, "toBoolean", nargs=0):
            p[0] = conversion.ToBoolean()
        elif check(p, "convertsToBoolean", nargs=0):
            p[0] = conversion.ConvertsToBoolean()
        elif check(p, "toInteger", nargs=0):
            p[0] = conversion.ToInteger()
        elif check(p, "convertsToInteger", nargs=0):
            p[0] = conversion.ConvertsToInteger()
        elif check(p, "toDate", nargs=0):
            p[0] = conversion.ToDate()
        elif check(p, "convertsToDate", nargs=0):
            p[0] = conversion.ConvertsToDate()
        elif check(p, "toDateTime", nargs=0):
            p[0] = conversion.ToDateTime()
        elif check(p, "convertsToDateTime", nargs=0):
            p[0] = conversion.ConvertsToDateTime()
        elif check(p, "toDecimal", nargs=0):
            p[0] = conversion.ToDecimal()
        elif check(p, "convertsToDecimal", nargs=0):
            p[0] = conversion.ConvertsToDecimal()
        elif check(p, "toQuantity", nargs=[0, 1]):
            p[0] = conversion.ToQuantity()
        elif check(p, "convertsToQuantity", nargs=[0, 1]):
            p[0] = conversion.ConvertsToQuantity()
        elif check(p, "toString", nargs=0):
            p[0] = conversion.ToString()
        elif check(p, "convertsToString", nargs=0):
            p[0] = conversion.ConvertsToString()
        elif check(p, "toTime", nargs=0):
            p[0] = conversion.ToTime()
        elif check(p, "convertsToTime", nargs=0):
            p[0] = conversion.ConvertsToTime()
        # -------------------------------------------------------------------------------
        # String manipulation
        # -------------------------------------------------------------------------------
        elif check(p, "indexOf", nargs=1):
            p[0] = strings.IndexOf(*p[3])
        elif check(p, "substring", nargs=[1, 2]):
            p[0] = strings.Substring(*p[3])
        elif check(p, "startsWith", nargs=1):
            p[0] = strings.StartsWith(*p[3])
        elif check(p, "endsWith", nargs=1):
            p[0] = strings.EndsWith(*p[3])
        elif check(p, "contains", nargs=1):
            p[0] = strings.Contains(*p[3])
        elif check(p, "upper", nargs=0):
            p[0] = strings.Upper()
        elif check(p, "lower", nargs=0):
            p[0] = strings.Lower()
        elif check(p, "replace", nargs=2):
            p[0] = strings.Replace(*p[3])
        elif check(p, "matches", nargs=1):
            p[0] = strings.Matches(*p[3])
        elif check(p, "replaceMatches", nargs=2):
            p[0] = strings.ReplaceMatches(*p[3])
        elif check(p, "length", nargs=0):
            p[0] = strings.Length()
        elif check(p, "toChars", nargs=0):
            p[0] = strings.ToChars()
        # -------------------------------------------------------------------------------
        # Math
        # -------------------------------------------------------------------------------
        elif check(p, "abs", nargs=0):
            p[0] = math.Abs()
        elif check(p, "ceiling", nargs=0):
            p[0] = math.Ceiling()
        elif check(p, "exp", nargs=0):
            p[0] = math.Exp()
        elif check(p, "floor", nargs=0):
            p[0] = math.Floor()
        elif check(p, "ln", nargs=0):
            p[0] = math.Ln()
        elif check(p, "log", nargs=1):
            p[0] = math.Log(*p[3])
        elif check(p, "power", nargs=1):
            p[0] = math.Power(*p[3])
        elif check(p, "round", nargs=1):
            p[0] = math.Round(*p[3])
        elif check(p, "sqrt", nargs=0):
            p[0] = math.Sqrt()
        elif check(p, "truncate", nargs=0):
            p[0] = math.Truncate()
        # -------------------------------------------------------------------------------
        # Tree navigation
        # -------------------------------------------------------------------------------
        elif check(p, "children", nargs=0):
            p[0] = navigation.Children()
        elif check(p, "descendants", nargs=0):
            p[0] = navigation.Descendants()
        # -------------------------------------------------------------------------------
        # Boolean functions
        # -------------------------------------------------------------------------------
        elif check(p, "not", nargs=0):
            p[0] = boolean.Not()
        # -------------------------------------------------------------------------------
        # Utility functions
        # -------------------------------------------------------------------------------
        elif check(p, "trace", nargs=[1, 2]):
            p[0] = utility.Trace(*p[3])
        elif check(p, "now", nargs=0):
            p[0] = utility.Now()
        elif check(p, "timeOfDay", nargs=0):
            p[0] = utility.TimeOfDay()
        elif check(p, "today", nargs=0):
            p[0] = utility.Today()
        # -------------------------------------------------------------------------------
        # Type functions
        # -------------------------------------------------------------------------------
        elif check(p, "is", nargs=1):
            p[0] = types.LegacyIs(*p[3])
        elif check(p, "as", nargs=1):
            p[0] = types.LegacyAs(*p[3])
        # -------------------------------------------------------------------------------
        # Aggregation functions
        # -------------------------------------------------------------------------------
        elif check(p, "aggregate", nargs=[1, 2]):
            p[0] = aggregates.Aggregate(*p[3])
        else:
            pos = self.string.find(str(p[1]))
            raise FhirPathParserError(
                f'FHIRPath parser error at {p.lineno(1)}:{pos}: Invalid function "{p[1]}".\n{_underline_error_in_fhir_path(self.string,p[1], pos)}'
            )

    def p_fhirpath_function_name(self, p):
        """function_name : identifier
        | CONTAINS
        | IN
        | AS
        | IS
        """
        p[0] = p[1]

    def p_fhirpath_function_arguments(self, p):
        """arguments : expression
        | empty"""
        p[0] = [p[1]]

    def p_fhirpath_function_arguments_list(self, p):
        """arguments : arguments ',' arguments"""
        p[0] = ensure_list(p[1]) + ensure_list(p[3])

    def p_fhirpath_identifier(self, p):
        """identifier : IDENTIFIER"""
        p[0] = p[1]

    def p_fhirpath_literal(self, p):
        """literal : number
        | boolean
        | STRING
        | date
        | time
        | datetime
        | quantity
        """
        p[0] = Literal(p[1])

    def p_fhirpath_literal_empty(self, p):
        """literal : '{' '}'"""
        p[0] = Literal([])

    def p_fhirpath_boolean(self, p):
        "boolean : BOOLEAN"
        p[0] = True if p[1] == "true" else False

    def p_fhirpath_datetime(self, p):
        "datetime : DATETIME"
        p[0] = literals.DateTime(p[1])

    def p_fhirpath_time(self, p):
        "time : TIME"
        p[0] = literals.Time(p[1])

    def p_fhirpath_date(self, p):
        "date : DATE"
        p[0] = literals.Date(p[1])

    def p_fhirpath_quantity(self, p):
        """quantity : number unit"""
        p[0] = literals.Quantity(p[1], p[2])

    def p_fhirpath_unit(self, p):
        """unit : STRING
        | CALENDAR_DURATION"""
        p[0] = p[1]

    def p_fhirpath_number(self, p):
        """number : INTEGER
        | DECIMAL"""
        p[0] = p[1]

    def p_fhirpath_empty(self, p):
        """empty :"""
        p[0] = None


class IteratorToTokenStream:

    def __init__(self, iterator):
        self.iterator = iterator

    def token(self):
        try:
            return next(self.iterator)
        except StopIteration:
            return None


try:
    fhirpath = FhirPathParser()
except Exception as e:
    print(traceback.format_exc())
