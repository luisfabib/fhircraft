from collections import namedtuple

import pytest

from fhircraft.fhir.path.engine.additional import GetValue
from fhircraft.fhir.path.engine.core import *
from fhircraft.fhir.path.engine.equality import *
from fhircraft.fhir.path.engine.literals import *

env = dict()

# -------------
# Equals
# -------------

equals_boolean_logic_cases = (
    ("ABC", "ABC", True),
    ("ABC", "DEF", False),
    ("ABC", "abc", False),
    ("ABC", "def", False),
    (123, 123, True),
    (123, 456, False),
    (1.23, 1.23, True),
    (1.23, 4.56, False),
    (True, True, True),
    (False, False, True),
    (False, True, False),
    (Date("@2012"), Date("@2012"), True),
    (Date("@2012"), Date("@2013"), False),
    (Date("@2012-01"), Date("@2012"), []),
    (DateTime("@2012-01-01T10:30"), DateTime("@2012-01-01T10:30"), True),
    (DateTime("@2012-01-01T10:30"), DateTime("@2012-01-01T10:31"), False),
    (DateTime("@2012-01-01T10:30:12.312"), DateTime("@2012-01-01T10:30"), []),
    ("1 year", "1 year", True),
    ("1 cm", "1 m", False),
    ("ABC", [], []),
    ([], "ABC", []),
)


@pytest.mark.parametrize("left, right, expected", equals_boolean_logic_cases)
def test_equals_returns_correct_boolean(left, right, expected):
    resource = namedtuple("Resource", ["left", "right"])(left=left, right=right)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Equals(
        Invocation(Element("left"), GetValue()),
        Invocation(Element("right"), GetValue()),
    ).evaluate(collection, env)
    assert result == [FHIRPathCollectionItem(value=expected)]


def test_equals_string_representation():
    expression = Equals(Element("left"), Element("right"))
    assert str(expression) == "left == right"


@pytest.mark.parametrize("left, right, expected", equals_boolean_logic_cases)
def test_notequals_returns_correct_boolean(left, right, expected):
    resource = namedtuple("Resource", ["left", "right"])(left=left, right=right)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = NotEquals(
        Invocation(Element("left"), GetValue()),
        Invocation(Element("right"), GetValue()),
    ).evaluate(collection, env)
    assert result != [FHIRPathCollectionItem(value=expected)]


def test_notequals_string_representation():
    expression = NotEquals(Element("left"), Element("right"))
    assert str(expression) == "left != right"


# -------------
# Equivalent
# -------------

equivalent_boolean_logic_cases = (
    ("ABC", "ABC", True),
    ("ABC", "DEF", False),
    ("ABC", "abc", True),
    ("ABC", "def", False),
    (123, 123, True),
    (123, 456, False),
    (1.23, 1.23, True),
    (1.23, 1.23123, True),
    (1.23, 4.56, False),
    (1.23, 1.25123, False),
    (True, True, True),
    (False, False, True),
    (False, True, False),
    (Date("@2012"), Date("@2012"), True),
    (Date("@2012"), Date("@2013"), False),
    (Date("@2012-01"), Date("@2012"), False),
    (DateTime("@2012-01-01T10:30"), DateTime("@2012-01-01T10:30"), True),
    (DateTime("@2012-01-01T10:30"), DateTime("@2012-01-01T10:31"), False),
    (DateTime("@2012-01-01T10:30.312"), DateTime("@2012-01-01T10"), False),
    ("1 year", "1 year", True),
    ("1 cm", "1 m", False),
    ("ABC", [], False),
    ([], "ABC", False),
    ([], [], True),
    (dict(a=1, b=2), dict(b=2, a=1), True),
    (dict(a=1, b=2, id="123"), dict(b=2, a=1, id="456"), True),
    (dict(a=1, b=2, c=3), dict(b=2, a=1, id="456"), False),
)


@pytest.mark.parametrize("left, right, expected", equivalent_boolean_logic_cases)
def test_equivalent_returns_correct_boolean(left, right, expected):
    resource = namedtuple("Resource", ["left", "right"])(left=left, right=right)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Equivalent(
        Invocation(Element("left"), GetValue()),
        Invocation(Element("right"), GetValue()),
    ).evaluate(collection, env)
    assert result == [FHIRPathCollectionItem(value=expected)]


def test_equivalent_string_representation():
    expression = Equivalent(Element("left"), Element("right"))
    assert str(expression) == "left ~ right"


@pytest.mark.parametrize("left, right, expected", equivalent_boolean_logic_cases)
def test_notequivalent_returns_correct_boolean(left, right, expected):
    resource = namedtuple("Resource", ["left", "right"])(left=left, right=right)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = NotEquivalent(
        Invocation(Element("left"), GetValue()),
        Invocation(Element("right"), GetValue()),
    ).evaluate(collection, env)
    assert result != [FHIRPathCollectionItem(value=expected)]


def test_notequivalent_string_representation():
    expression = NotEquivalent(Element("left"), Element("right"))
    assert str(expression) == "left !~ right"
