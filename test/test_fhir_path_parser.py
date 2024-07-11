import pytest

from fhircraft.fhir.path.engine.core import *
from fhircraft.fhir.path.engine.existence import *
from fhircraft.fhir.path.engine.literals import *
from fhircraft.fhir.path.engine.filtering import *
from fhircraft.fhir.path.engine.subsetting import *
from fhircraft.fhir.path.engine.strings import *
from fhircraft.fhir.path.engine.additional import *
from fhircraft.fhir.path.engine.boolean import *
from fhircraft.fhir.path.engine.navigation import *
from fhircraft.fhir.path.engine.combining import *
from fhircraft.fhir.path.engine.conversion import *
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
    ("foo[1]", Invocation(Element("foo"), Index(1))),
    # ----------------------------------
    # Variables/Constants
    # ----------------------------------
    ("$", Root()),
    ("$this", This()),
    ("%resource", Root()),
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
    # Boolean Operators
    # ----------------------------------
    ("parent.child and mother.child", And(Invocation(Element('parent'), Element('child')), Invocation(Element('mother'), Element('child')))),  
    ("parent.child or mother.child", Or(Invocation(Element('parent'), Element('child')), Invocation(Element('mother'), Element('child')))),  
    ("parent.child xor mother.child", Xor(Invocation(Element('parent'), Element('child')), Invocation(Element('mother'), Element('child')))),  
    ("parent.child implies mother.child", Implies(Invocation(Element('parent'), Element('child')), Invocation(Element('mother'), Element('child')))),  
    ("parent.not()", Invocation(Element('parent'), Not())),  
    # ----------------------------------
    # Equality Operators
    # ----------------------------------
    ("parent.child = mother.child", Equals(Invocation(Element('parent'), Element('child')), Invocation(Element('mother'), Element('child')))),  
    ("parent.child != mother.child", NotEquals(Invocation(Element('parent'), Element('child')), Invocation(Element('mother'), Element('child')))),  
    ("parent.child ~ mother.child", Equivalent(Invocation(Element('parent'), Element('child')), Invocation(Element('mother'), Element('child')))),  
    ("parent.child !~ mother.child", NotEquivalent(Invocation(Element('parent'), Element('child')), Invocation(Element('mother'), Element('child')))),  
    # ----------------------------------
    # Comparison Operators
    # ----------------------------------
    ("parent.child >= mother.child", GreaterEqualThan(Invocation(Element('parent'), Element('child')), Invocation(Element('mother'), Element('child')))),  
    ("parent.child <= mother.child", LessEqualThan(Invocation(Element('parent'), Element('child')), Invocation(Element('mother'), Element('child')))),  
    ("parent.child > mother.child", GreaterThan(Invocation(Element('parent'), Element('child')), Invocation(Element('mother'), Element('child')))),  
    ("parent.child < mother.child", LessThan(Invocation(Element('parent'), Element('child')), Invocation(Element('mother'), Element('child')))),  
    # ----------------------------------
    # Collection Operators
    # ----------------------------------
    ("parent.child | mother.child", collection.Union(Invocation(Element('parent'), Element('child')), Invocation(Element('mother'), Element('child')))),  
    ("parent.child in mother.child", collection.In(Invocation(Element('parent'), Element('child')), Invocation(Element('mother'), Element('child')))),  
    ("parent.child contains mother.child", collection.Contains(Invocation(Element('parent'), Element('child')), Invocation(Element('mother'), Element('child')))),  
    # ----------------------------------
    # Precedence
    # ----------------------------------
    ("parent and mother implies child", Implies(And(Element('parent'), Element('mother')), Element('child'))),  
    ("parent and mother and child implies brother", Implies(And(And(Element('parent'), Element('mother')), Element('child')), Element('brother'))),  
    ("parent implies mother = child", Equals(Implies(Element('parent'), Element('mother')), Element('child'))),  
    ("parent > mother = child", Equals(GreaterThan(Element('parent'), Element('mother')), Element('child'))),  
    ("(parent > mother) = child", Equals(GreaterThan(Element('parent'), Element('mother')), Element('child'))),  
    ("parent > (mother = child)", GreaterThan(Element('parent'), Equals(Element('mother'), Element('child')))),  
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
        
    