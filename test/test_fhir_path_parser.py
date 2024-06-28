import pytest

from fhircraft.fhir.path.engine.core import *
from fhircraft.fhir.path.engine.existence import *
from fhircraft.fhir.path.engine.filtering import *
from fhircraft.fhir.path.engine.subsetting import *
from fhircraft.fhir.path.engine.combining import *
from fhircraft.fhir.path.engine.strings import *
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
    ("parent.child", Child(Element('parent'), Element("child"))),    
    ("parent.child[1]", Child(Child(Element('parent'), Element("child")), Index(1))),    
    ("parent.where(child='string')", Child(Element('parent'), Where(Operation(Element('child'), operator.eq, 'string')))),
    ("parent.where(child=1234)", Child(Element('parent'), Where(Operation(Element('child'), operator.eq,1234)))),
    ("parent.where(child>@2024)", Child(Element('parent'), Where(Operation(Element('child'), operator.gt, '2024')))),
    ("parent.where(child=@2024-12-01)", Child(Element('parent'), Where(Operation(Element('child'), operator.eq ,'2024-12-01')))),
    ("parent.where(child=@T12:05)", Child(Element('parent'), Where(Operation(Element('child'), operator.eq, '12:05')))),
    ("parent.where(child=@T12:05)", Child(Element('parent'), Where(Operation(Element('child'), operator.eq,'12:05')))),
    ("parent.where(child & daughter)", Child(Element('parent'), Where(Operation(Element('child'), operator.and_, Element('daughter'))))),
    ("parent.extension('http://domain.org/extension')", Child(Element('parent'), Extension("http://domain.org/extension"))),
    ("parent.value[x]", Child(Element('parent'), TypeChoice('value'))),
    # ----------------------------------
    # Subsetting functions
    # ----------------------------------
    ("parent.single()", Child(Element('parent'), Single())),    
    ("parent.first()", Child(Element('parent'), First())),    
    ("parent.last()", Child(Element('parent'), Last())),    
    ("parent.tail()", Child(Element('parent'), Tail())),  
    ("parent.skip(3)", Child(Element('parent'), Skip(3))),    
    ("parent.take(3)", Child(Element('parent'), Take(3))),     
    # ----------------------------------
    # Existence functions
    # ----------------------------------
    ("parent.empty()", Child(Element('parent'), Empty())),
    ("parent.exists()", Child(Element('parent'), Exists())),
    ("parent.all(parent.children)", Child(Element('parent'), All(Child(Element('parent'), Element('children'))))),
    ("parent.all($this = 'parent')", Child(Element('parent'), All(Operation(This(), operator.eq, 'parent')))),
    ("parent.allTrue()", Child(Element('parent'), AllTrue())),
    ("parent.anyTrue()", Child(Element('parent'), AnyTrue())),
    ("parent.allFalse()", Child(Element('parent'), AllFalse())),
    ("parent.anyFalse()", Child(Element('parent'), AnyFalse())),
    ("parent.subsetOf(parent.children)", Child(Element('parent'), SubsetOf(Child(Element('parent'), Element('children'))))),
    ("parent.supersetOf(parent.children)", Child(Element('parent'), SupersetOf(Child(Element('parent'), Element('children'))))),
    ("parent.count()", Child(Element('parent'), Count())),
    ("parent.distinct()", Child(Element('parent'), Distinct())),
    ("parent.isDistinct()", Child(Element('parent'), IsDistinct())),
    # ----------------------------------
    # Filtering & Projection functions
    # ----------------------------------
    ("parent.where(child='name')", Child(Element('parent'), Where(Operation(Element('child'), operator.eq, 'name')))),
    ("parent.select($this.child)", Child(Element('parent'), Select(Child(This(), Element('child'))))),
    ("parent.repeat($this.child)", Child(Element('parent'), Repeat(Child(This(), Element('child'))))),
    # ----------------------------------
    # Combining functions
    # ----------------------------------
    ("parent.combine(mother)", Child(Element('parent'), Combine(Element('mother')))),  
    ("parent.union(mother)", Child(Element('parent'), Union(Element('mother')))),  
    # ----------------------------------
    # String manipualtion functions
    # ----------------------------------
    ("parent.indexOf('John')", Child(Element('parent'), IndexOf('Lucas'))),  
    ("parent.substring(1,2)", Child(Element('parent'), Substring(1,2))),  
    ("parent.startsWith('John')", Child(Element('parent'), StartsWith('John'))),  
    ("parent.endsWith('John')", Child(Element('parent'), EndsWith('John'))),  
    ("parent.contains('John')", Child(Element('parent'), Contains('John'))),  
    ("parent.upper()", Child(Element('parent'), Upper())),  
    ("parent.lower()", Child(Element('parent'), Lower())),  
    ("parent.replace('John','James')", Child(Element('parent'), Replace('John','James'))),  
    ("parent.matches('^(?:John)')", Child(Element('parent'), Matches('^(?:John)'))),  
    ("parent.replaceMatches('^(?:John)','James')", Child(Element('parent'), ReplaceMatches('^(?:John)','James'))),  
    ("parent.length()", Child(Element('parent'), Length())),  
    ("parent.toChars()", Child(Element('parent'), ToChars())),  
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
        
    