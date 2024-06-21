import pytest

from fhircraft.fhir.path.engine import Child, Root, Element, Index, Slice, Where, Extension, Single, TypeChoice, This, BinaryExpression
from fhircraft.fhir.path.lexer import FhirPathLexer, FhirPathLexerError
from fhircraft.fhir.path.parser import FhirPathParser, FhirPathParserError
import operator

# Format: (string, expected_object)
parser_test_cases = (
    ("foo", Element("foo")),
    ("[1]", Index(1)),
    ("[1:]", Slice(start=1)),
    ("[:]", Slice()),
    ("[*]", Slice()),
    ("[:2]", Slice(end=2)),
    ("[1:2]", Slice(start=1, end=2)),
    ("[5:-2]", Slice(start=5, end=-2)),
    ("$", Root()),
    ("$this", This()),
    ("%resource", Root()),
    ("%context", This()),
    ("parent.child", Child(Element('parent'), Element("child"))),    
    ("parent.child[1]", Child(Child(Element('parent'), Element("child")), Index(1))),    
    ("parent.where(child='string')", Child(Element('parent'), Where(BinaryExpression(Element('child'), operator.eq, 'string')))),
    ("parent.where(child=1234)", Child(Element('parent'), Where(BinaryExpression(Element('child'), operator.eq,1234)))),
    ("parent.where(child>@2024)", Child(Element('parent'), Where(BinaryExpression(Element('child'), operator.gt, '2024')))),
    ("parent.where(child=@2024-12-01)", Child(Element('parent'), Where(BinaryExpression(Element('child'), operator.eq ,'2024-12-01')))),
    ("parent.where(child=@T12:05)", Child(Element('parent'), Where(BinaryExpression(Element('child'), operator.eq, '12:05')))),
    ("parent.where(child=@T12:05)", Child(Element('parent'), Where(BinaryExpression(Element('child'), operator.eq,'12:05')))),
    ("parent.where(child & daughter)", Child(Element('parent'), Where(BinaryExpression(Element('child'), operator.and_, Element('daughter'))))),
    ("parent.extension('http://domain.org/extension')", Child(Element('parent'), Extension("http://domain.org/extension"))),
    ("parent.single()", Child(Element('parent'), Single())),    
    ("parent.first()", Child(Element('parent'), Index(0))),    
    ("parent.last()", Child(Element('parent'), Index(-1))),    
    ("parent.tail()", Child(Element('parent'), Slice(0,-1))),  
    ("parent.skip(3)", Child(Element('parent'), Slice(3,-1))),    
    ("parent.take(3)", Child(Element('parent'), Slice(0,3))),     
    ("parent.value[x]", Child(Element('parent'), TypeChoice('value'))),
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
        
    