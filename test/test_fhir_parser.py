import pytest

from fhircraft.fhir.fhirpath import Child, Descendants, Fields, Index, Slice, Where, Extension, Single
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
    ("foo.baz", Child(Fields("foo"), Fields("baz"))),
    ("foo.baz[1]", Child(Child(Fields("foo"), Fields("baz")), Index(1))),
    ("foo.baz,bizzle", Child(Fields("foo"), Fields("baz", "bizzle"))),
    ('foo.where(bar.bizzle="test")', Where(Fields("foo"), Child(Fields("bar"), Fields("bizzle")), "test")),
    ("foo.baz", Child(Fields("foo"), Fields("baz"))),
    ("foo.baz.first()", Child(Child(Fields("foo"), Fields("baz")), Index(0))),
    ("foo.baz.last()", Child(Child(Fields("foo"), Fields("baz")), Index(-1))),
    ("foo.baz.tail()", Child(Child(Fields("foo"), Fields("baz")), Slice(0,-1))),
    ("foo.baz.single()", Child(Child(Fields("foo"), Fields("baz")), Single())),
    ('foo.extension("http://domain.org/extension")', Extension(Fields("foo"), "http://domain.org/extension")),
)


@pytest.mark.parametrize("string, expected_object", parser_test_cases)
def test_parser(string, expected_object):
    parser = FhirPathParser(lexer_class=lambda: FhirPathLexer())
    assert parser.parse(string) == expected_object