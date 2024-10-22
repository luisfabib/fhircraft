import pytest

from fhircraft.fhir.path.engine.core import *
from fhircraft.fhir.path.engine.existence import *
from fhircraft.fhir.path.engine.literals import *
from fhircraft.fhir.path.engine.math import *
from fhircraft.fhir.path.engine.filtering import *
from fhircraft.fhir.path.engine.subsetting import *
from fhircraft.fhir.path.engine.strings import *
from fhircraft.fhir.path.engine.additional import *
from fhircraft.fhir.path.engine.boolean import *
from fhircraft.fhir.path.engine.navigation import *
from fhircraft.fhir.path.engine.combining import *
from fhircraft.fhir.path.engine.conversion import *
from fhircraft.fhir.path.engine.types import *
from fhircraft.fhir.path.engine.utility import *
from fhircraft.fhir.path.engine.equality import *
from fhircraft.fhir.path.engine.comparison import *
import fhircraft.fhir.path.engine.collection as collection
from fhircraft.fhir.path.lexer import FhirPathLexer, FhirPathLexerError
from fhircraft.fhir.path.parser import FhirPathParser, FhirPathParserError
import operator

# Format: (string, expected_object)
parser_test_cases = (
    ("foo", Element("foo")),
    ("`foo`", Element("foo")),
    ("`div`", Element("div")),
    ("foo[1]", Invocation(Element("foo"), Index(1))),
    # ----------------------------------
    # Variables/Constants
    # ----------------------------------
    ("$", Root()),
    ("$this", This()),
    ("%rootResource", Root()),
    ("%resource", Parent()),
    ("%context", This()),
    # ----------------------------------
    # Literals
    # ----------------------------------
    ("12 'mg'", Quantity(12, 'mg')),
    ("12.5 'kg'", Quantity(12.5, 'kg')),
    ("5 days", Quantity(5, 'days')),
    ("@2024-01-01", Date('@2024-01-01')),
    ("@2024-01", Date('@2024-01')),
    ("@2024", Date('@2024')),
    ('@T12:15:20.345+02:30', Time('@T12:15:20.345+02:30')),
    ('@T12:15:20.345', Time('@T12:15:20.345')),
    ('@T12:15:20', Time('@T12:15:20')),
    ('@T12:15', Time('@T12:15')),
    ('@T12', Time('@T12')),
    ('@2024-01-01T12:15:20.345+02:30', DateTime('@2024-01-01T12:15:20.345+02:30')),
    ('@2024-01-01T12:15:20.345', DateTime('@2024-01-01T12:15:20.345')),
    ('@2024-01-01T12:15', DateTime('@2024-01-01T12:15')),
    ('@2024-01-01T12', DateTime('@2024-01-01T12')),
    # ----------------------------------
    # Invocations
    # ----------------------------------
    ("parent.child", Invocation(Element('parent'), Element("child"))),   
    ("(parent.child)", Invocation(Element('parent'), Element("child"))),    
    ("parent.child[1]", Invocation(Invocation(Element('parent'), Element("child")), Index(1))),    
    ("parent.where(child = 'string')", Invocation(Element('parent'), Where(Equals(Element('child'), 'string')))),
    ("parent.where(child = 1234)", Invocation(Element('parent'), Where(Equals(Element('child'), 1234)))),
    ("parent.where(child > @2024)", Invocation(Element('parent'), Where(GreaterThan(Element('child'), Date('@2024'))))),
    ("parent.where(child = @2024-12-01)", Invocation(Element('parent'), Where(Equals(Element('child'), Date('@2024-12-01'))))),
    ("parent.where(child = @T12:05)", Invocation(Element('parent'), Where(Equals(Element('child'), Time('@T12:05'))))),
    ("parent.where(child = @T12:05)", Invocation(Element('parent'), Where(Equals(Element('child'), Time('@T12:05'))))),
    ("parent.extension('http://domain.org/extension')", Invocation(Element('parent'), Extension("http://domain.org/extension"))),
    ("parent.value[x]", Invocation(Element('parent'), TypeChoice('value'))),
    # ----------------------------------
    # Subsetting functions
    # ----------------------------------
    ("parent.single()", Invocation(Element('parent'), Single())),    
    ("parent.first()", Invocation(Element('parent'), First())),    
    ("parent.last()", Invocation(Element('parent'), Last())),    
    ("parent.tail()", Invocation(Element('parent'), Tail())),  
    ("parent.skip(3)", Invocation(Element('parent'), Skip(3))),    
    ("parent.take(3)", Invocation(Element('parent'), Take(3))),     
    # ----------------------------------
    # Existence functions
    # ----------------------------------
    ("parent.empty()", Invocation(Element('parent'), Empty())),
    ("parent.exists()", Invocation(Element('parent'), Exists())),
    ("parent.all(parent.children)", Invocation(Element('parent'), All(Invocation(Element('parent'), Element('children'))))),
    ("parent.all($this = 'parent')", Invocation(Element('parent'), All(Equals(This(), 'parent')))),
    ("parent.allTrue()", Invocation(Element('parent'), AllTrue())),
    ("parent.anyTrue()", Invocation(Element('parent'), AnyTrue())),
    ("parent.allFalse()", Invocation(Element('parent'), AllFalse())),
    ("parent.anyFalse()", Invocation(Element('parent'), AnyFalse())),
    ("parent.subsetOf(parent.children)", Invocation(Element('parent'), SubsetOf(Invocation(Element('parent'), Element('children'))))),
    ("parent.supersetOf(parent.children)", Invocation(Element('parent'), SupersetOf(Invocation(Element('parent'), Element('children'))))),
    ("parent.count()", Invocation(Element('parent'), Count())),
    ("parent.distinct()", Invocation(Element('parent'), Distinct())),
    ("parent.isDistinct()", Invocation(Element('parent'), IsDistinct())),
    # ----------------------------------
    # Filtering & Projection functions
    # ----------------------------------
    ("parent.where(child='name')", Invocation(Element('parent'), Where(Equals(Element('child'), 'name')))),
    ("parent.select($this.child)", Invocation(Element('parent'), Select(Invocation(This(), Element('child'))))),
    ("parent.repeat($this.child)", Invocation(Element('parent'), Repeat(Invocation(This(), Element('child'))))),
    # ----------------------------------
    # Combining functions
    # ----------------------------------
    ("parent.combine(mother)", Invocation(Element('parent'), Combine(Element('mother')))),  
    ("parent.union(mother)", Invocation(Element('parent'), Union(Element('mother')))),  
    # ----------------------------------
    # Type conversion functions
    # ----------------------------------
    ("parent.iif($this, 'value1', 'value2')", Invocation(Element('parent'), Iif(This(), 'value1', 'value2'))),  
    ("parent.toBoolean()", Invocation(Element('parent'), ToBoolean())),  
    ("parent.convertsToBoolean()", Invocation(Element('parent'), ConvertsToBoolean())), 
    ("parent.toInteger()", Invocation(Element('parent'), ToInteger())), 
    ("parent.convertsToInteger()", Invocation(Element('parent'), ConvertsToInteger())), 
    ("parent.toDate()", Invocation(Element('parent'), ToDate())), 
    ("parent.convertsToDate()", Invocation(Element('parent'), ConvertsToDate())), 
    ("parent.toDateTime()", Invocation(Element('parent'), ToDateTime())), 
    ("parent.convertsToDateTime()", Invocation(Element('parent'), ConvertsToDateTime())), 
    ("parent.toDecimal()", Invocation(Element('parent'), ToDecimal())), 
    ("parent.convertsToDecimal()", Invocation(Element('parent'), ConvertsToDecimal())), 
    ("parent.toQuantity()", Invocation(Element('parent'), ToQuantity())), 
    ("parent.convertsToQuantity()", Invocation(Element('parent'), ConvertsToQuantity())), 
    ("parent.toString()", Invocation(Element('parent'), ToString())), 
    ("parent.convertsToString()", Invocation(Element('parent'), ConvertsToString())), 
    ("parent.toTime()", Invocation(Element('parent'), ToTime())), 
    ("parent.convertsToTime()", Invocation(Element('parent'), ConvertsToTime())), 
    # ----------------------------------
    # String manipualtion functions
    # ----------------------------------
    ("parent.indexOf('John')", Invocation(Element('parent'), IndexOf('Lucas'))),  
    ("parent.substring(1,2)", Invocation(Element('parent'), Substring(1,2))),  
    ("parent.startsWith('John')", Invocation(Element('parent'), StartsWith('John'))),  
    ("parent.endsWith('John')", Invocation(Element('parent'), EndsWith('John'))),  
    ("parent.contains('John')", Invocation(Element('parent'), Contains('John'))),  
    ("parent.upper()", Invocation(Element('parent'), Upper())),  
    ("parent.lower()", Invocation(Element('parent'), Lower())),  
    ("parent.replace('John','James')", Invocation(Element('parent'), Replace('John','James'))),  
    ("parent.matches('^(?:John)')", Invocation(Element('parent'), Matches('^(?:John)'))),  
    ("parent.replaceMatches('^(?:John)','James')", Invocation(Element('parent'), ReplaceMatches('^(?:John)','James'))),  
    ("parent.length()", Invocation(Element('parent'), Length())),  
    ("parent.toChars()", Invocation(Element('parent'), ToChars())),  
    # ----------------------------------
    # Types legacy functions
    # ----------------------------------
    ("parent.is(String)", Invocation(Element('parent'), LegacyIs('String'))),  
    ("parent.as(String)", Invocation(Element('parent'), LegacyAs('String'))),  
    # ----------------------------------
    # Utility functions
    # ----------------------------------
    ("A.trace('id', id)", Invocation(Element('A'), Trace('id', Element('id')))),  
    ("now()", Now()),  
    ("timeOfDay()", TimeOfDay()),  
    ("today()", Today()),  
    # ----------------------------------
    # Types Operators
    # ----------------------------------
    ("A is String", Is(Element('A'), 'String')),  
    ("A is Observation", Is(Element('A'), 'Observation')),  
    ("A is System.String", Is(Element('A'), 'System.String')),  
    ("A as String", As(Element('A'), 'String')),  
    ("A as System.String", As(Element('A'), 'System.String')),  
    # ----------------------------------
    # Boolean Operators
    # ----------------------------------
    ("A and B", And(Element('A'), Element('B'))),  
    ("A or B", Or(Element('A'), Element('B'))),  
    ("A xor B", Xor(Element('A'), Element('B'))),  
    ("A implies B", Implies(Element('A'), Element('B'))),  
    ("parent.not()", Invocation(Element('parent'), Not())),  
    # ----------------------------------
    # Equality Operators
    # ----------------------------------
    ("A = B", Equals(Element('A'), Element('B'))),  
    ("A != B", NotEquals(Element('A'), Element('B'))),  
    ("A ~ B", Equivalent(Element('A'), Element('B'))),  
    ("A !~ B", NotEquivalent(Element('A'), Element('B'))),  
    # ----------------------------------
    # Comparison Operators
    # ----------------------------------
    ("A >= B", GreaterEqualThan(Element('A'), Element('B'))),  
    ("A <= B", LessEqualThan(Element('A'), Element('B'))),  
    ("A > B", GreaterThan(Element('A'), Element('B'))),  
    ("A < B", LessThan(Element('A'), Element('B'))),  
    # ----------------------------------
    # Math Operators
    # ----------------------------------
    ("A + B", Addition(Element('A'), Element('B'))),  
    ("A - B", Subtraction(Element('A'), Element('B'))),  
    ("A * B", Multiplication(Element('A'), Element('B'))),  
    ("A / B", Division(Element('A'), Element('B'))),  
    ("A div B", Div(Element('A'), Element('B'))),  
    ("A mod B", Mod(Element('A'), Element('B'))),  
    # ----------------------------------
    # Collection Operators
    # ----------------------------------
    ("A | B", collection.Union(Element('A'), Element('B'))),  
    ("A in B", collection.In(Element('A'), Element('B'))),  
    ("A contains B", collection.Contains(Element('A'), Element('B'))),  
    # ----------------------------------
    # Precedence
    # ----------------------------------
    ("A and B implies C", Implies(And(Element('A'), Element('B')), Element('C'))),  
    ("A and B and C implies D", Implies(And(And(Element('A'), Element('B')), Element('C')), Element('D'))),  
    ("A implies B = C", Implies(Element('A'), Equals(Element('B'), Element('C')))),  
    ("A > B = C", Equals(GreaterThan(Element('A'), Element('B')), Element('C'))),  
    ("(A > B) = C", Equals(GreaterThan(Element('A'), Element('B')), Element('C'))),  
    ("A > (B = C)", GreaterThan(Element('A'), Equals(Element('B'), Element('C')))),  
    ("A and B.exists(C and D) implies (E and F)", Implies(And(Element('A'), Invocation(Element('B'), Exists(And(Element('C'), Element('D'))))), And(Element('E'), Element('F')))),  
    ("B = 'b' or C = 'c'", Or(Equals(Element('B'), 'b'), Equals(Element('C'), 'c'))),  
    
)   
@pytest.mark.parametrize("string, expected_object", parser_test_cases)
def test_parser(string, expected_object):
    parser = FhirPathParser(lexer_class=lambda: FhirPathLexer())
    assert parser.parse(string) == expected_object
    
    
parser_error_cases = (
    ("*"),
    ("baz,bizzle"),
)
@pytest.mark.parametrize("string", parser_error_cases)
def test_parser_catches_invalid_syntax(string):
    with pytest.raises((FhirPathParserError, FhirPathLexerError)):
        FhirPathParser(lexer_class=lambda: FhirPathLexer()).parse(string)
        
    