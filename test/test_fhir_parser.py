import pytest

from fhircraft.fhir.fhirpath import Child, Root, Fields, Index, Slice, Where, Extension, Single, TypeChoice
from fhircraft.fhir.lexer import FhirPathLexer
from fhircraft.fhir.parser import FhirPathParser

# Format: (string, expected_object)
parser_test_cases = (
    #
    # Atomic
    # ------
    #
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
    #
    # Nested
    # ------
    #
    ("Observation.code", Child(Root(), Fields("code"))),
    ("Observation.code[1]", Child(Child(Root(), Fields("code")), Index(1))),
    ('Observation.component.where(code.coding.code="test")', Child(Child(Root(), Fields("component")), Where(Child(Child(Fields("code"), Fields("coding")), Fields("code")), "test"))),
    ('Observation.component.where(code.coding.code="test").where(code.coding.system="test2")', Child(Child(Child(Root(), Fields("component")),Where(Child(Child(Fields("code"), Fields("coding")), Fields("code")), "test"),),Where(Child(Child(Fields("code"), Fields("coding")), Fields("system")), "test2"))),
    ("foo.baz", Child(Fields("foo"), Fields("baz"))),
    ("Observation.identifier.first().value", Child(Child(Child(Root(), Fields("identifier")), Index(0)), Fields("value"))),
    ("Observation.identifier.last().value", Child(Child(Child(Root(), Fields("identifier")), Index(-1)), Fields("value"))),
    ("Observation.identifier.tail().value", Child(Child(Child(Root(), Fields("identifier")), Slice(0,-1)), Fields("value"))),
    ("Observation.identifier.single().value", Child(Child(Child(Root(), Fields("identifier")), Single()), Fields("value"))),
    ('Observation.extension("http://domain.org/extension")', Extension(Root(), "http://domain.org/extension")),
    ("Observation.component.value[x]", Child(Child(Root(), Fields('component')), TypeChoice('value'))),
)


@pytest.mark.parametrize("string, expected_object", parser_test_cases)
def test_parser(string, expected_object):
    parser = FhirPathParser(lexer_class=lambda: FhirPathLexer())
    assert parser.parse(string) == expected_object