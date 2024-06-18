import pytest

from fhircraft.fhir.path.engine import Child, Root, Fields, Index, Slice, Where, Extension, Single, TypeChoice, This, Expression
from fhircraft.fhir.path.lexer import FhirPathLexer
from fhircraft.fhir.path.parser import FhirPathParser

# Format: (string, expected_object)
parser_test_cases = (
    ("foo", Fields("foo")),
    ("*", Fields("*")),
    ("baz,bizzle", Fields("baz", "bizzle")),
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
    ("parent.child", Child(Fields('parent'), Fields("child"))),    
    ("parent.child[1]", Child(Child(Fields('parent'), Fields("child")), Index(1))),    
    ("parent.where(child='string')", Child(Fields('parent'), Where(Expression(Fields('child'),'=', 'string')))),
    ("parent.where(child=1234)", Child(Fields('parent'), Where(Expression(Fields('child'), '=',1234)))),
    ("parent.where(child=@2024)", Child(Fields('parent'), Where(Expression(Fields('child'),'=', '2024')))),
    ("parent.where(child=@2024-12-01)", Child(Fields('parent'), Where(Expression(Fields('child'), '=','2024-12-01')))),
    ("parent.where(child=@T12:05)", Child(Fields('parent'), Where(Expression(Fields('child'),'=','12:05')))),
    ("parent.where(child=@T12:05)", Child(Fields('parent'), Where(Expression(Fields('child'),'=','12:05')))),
    ("parent.where(child=@2024)", Child(Fields('parent'), Where(Expression(Fields('child'),'=', '2024')))),
    ("parent.extension('http://domain.org/extension')", Child(Fields('parent'), Extension("http://domain.org/extension"))),
    ("parent.single()", Child(Fields('parent'), Single())),    
    ("parent.first()", Child(Fields('parent'), Index(0))),    
    ("parent.last()", Child(Fields('parent'), Index(-1))),    
    ("parent.tail()", Child(Fields('parent'), Slice(0,-1))),  
    ("parent.skip(3)", Child(Fields('parent'), Slice(3,-1))),    
    ("parent.take(3)", Child(Fields('parent'), Slice(0,3))),     
    ("parent.value[x]", Child(Fields('parent'), TypeChoice('value'))),
)


@pytest.mark.parametrize("string, expected_object", parser_test_cases)
def test_parser(string, expected_object):
    parser = FhirPathParser(lexer_class=lambda: FhirPathLexer())
    assert parser.parse(string) == expected_object