import pytest

from fhircraft.fhir.path.engine.core import *
from fhircraft.fhir.path.engine.existence import *
from fhircraft.fhir.path.engine.filtering import *
from fhircraft.fhir.path.engine.subsetting import *
from fhircraft.fhir.path.engine.combining import *
from fhircraft.fhir.path.engine.strings import *
from fhircraft.fhir.path.engine.additional import *
from fhircraft.fhir.path.lexer import FhirPathLexer, FhirPathLexerError
from fhircraft.fhir.path.parser import FhirPathParser, FhirPathParserError
import operator

# Format: (string, expected_object)
parser_test_cases = (
    ("foo", Element("foo")),
    ("[1]", Index(1)),
    ("$", Root()),
    ("$this", This()),
    ("%resource", Root()),
    ("%context", This()),
    ("parent.child", Invocation(Element('parent'), Element("child"))),    
    ("parent.child[1]", Invocation(Invocation(Element('parent'), Element("child")), Index(1))),    
    ("parent.where(child='string')", Invocation(Element('parent'), Where(Operation(Element('child'), operator.eq, 'string')))),
    ("parent.where(child=1234)", Invocation(Element('parent'), Where(Operation(Element('child'), operator.eq,1234)))),
    ("parent.where(child>@2024)", Invocation(Element('parent'), Where(Operation(Element('child'), operator.gt, '2024')))),
    ("parent.where(child=@2024-12-01)", Invocation(Element('parent'), Where(Operation(Element('child'), operator.eq ,'2024-12-01')))),
    ("parent.where(child=@T12:05)", Invocation(Element('parent'), Where(Operation(Element('child'), operator.eq, '12:05')))),
    ("parent.where(child=@T12:05)", Invocation(Element('parent'), Where(Operation(Element('child'), operator.eq,'12:05')))),
    ("parent.where(child & daughter)", Invocation(Element('parent'), Where(Operation(Element('child'), operator.and_, Element('daughter'))))),
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
    ("parent.all($this = 'parent')", Invocation(Element('parent'), All(Operation(This(), operator.eq, 'parent')))),
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
    ("parent.where(child='name')", Invocation(Element('parent'), Where(Operation(Element('child'), operator.eq, 'name')))),
    ("parent.select($this.child)", Invocation(Element('parent'), Select(Invocation(This(), Element('child'))))),
    ("parent.repeat($this.child)", Invocation(Element('parent'), Repeat(Invocation(This(), Element('child'))))),
    # ----------------------------------
    # Combining functions
    # ----------------------------------
    ("parent.combine(mother)", Invocation(Element('parent'), Combine(Element('mother')))),  
    ("parent.union(mother)", Invocation(Element('parent'), Union(Element('mother')))),  
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
        
    