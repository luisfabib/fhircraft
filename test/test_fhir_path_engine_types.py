from collections import namedtuple

import pytest

from fhircraft.fhir.path.engine.additional import GetValue
from fhircraft.fhir.path.engine.core import *
from fhircraft.fhir.path.engine.literals import Date, Quantity
from fhircraft.fhir.path.engine.types import *

env = dict()

# -------------
# Is
# -------------

test_cases = (
    ("ABC", "String", True),
    ("123", "String", True),
    ("", "String", True),
    (123, "String", False),
    # Integer type checking
    (12, "Integer", True),
    ("12", "Integer", True),
    (-12, "Integer", True),
    # UnsignedInt type checking
    (12, "UnsignedInt", True),
    ("12", "UnsignedInt", True),
    (0, "UnsignedInt", True),
    (-12, "UnsignedInt", False),
    ("-12", "UnsignedInt", False),
    # PositiveInt type checking
    (12, "PositiveInt", True),
    ("12", "PositiveInt", True),
    (0, "PositiveInt", False),
    (-12, "PositiveInt", False),
    ("-12", "PositiveInt", False),
    # Decimal type checking
    (23, "Decimal", True),
    (23.32, "Decimal", True),
    ("23.32", "Decimal", True),
    ("23", "Decimal", True),
    # Boolean type checking
    (True, "Boolean", True),
    ("true", "Boolean", True),
    (False, "Boolean", True),
    ("false", "Boolean", True),
    ("invalid", "Boolean", False),
    (Date("@2024"), "Date", True),
    (Quantity(12, "g"), "Quantity", True),
)


@pytest.mark.parametrize("left, type_specifier, expected", test_cases)
def test_is_returns_correct_boolean(left, type_specifier, expected):
    resource = namedtuple("Resource", ["left"])(left=left)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Is(Invocation(Element("left"), GetValue()), type_specifier).evaluate(
        collection, env
    )
    assert result[0].value == expected

def test_is_string_representation():
    expression = Is(Element('field'), 'String')
    assert str(expression) == "field is String"

@pytest.mark.parametrize("left, type_specifier, expected", test_cases)
def test_legacy_is_returns_correct_boolean(left, type_specifier, expected):
    collection = [FHIRPathCollectionItem(value=left)]
    result = LegacyIs(type_specifier).evaluate(collection, env)
    assert result[0].value == expected

def test_legacy_is_string_representation():
    expression = LegacyIs('String')
    assert str(expression) == "is(String)"

# -------------
# As
# -------------


@pytest.mark.parametrize("expected, type_specifier, equal", test_cases)
def test_as_returns_correct_boolean(expected, type_specifier, equal):
    collection = [FHIRPathCollectionItem(value=expected)]
    result = As(This(), type_specifier).evaluate(collection, env)
    assert result[0].value == expected if equal else result == []

def test_as_string_representation():
    expression = As(Element('field'), 'String')
    assert str(expression) == "field as String"

@pytest.mark.parametrize("expected, type_specifier, equal", test_cases)
def test_legacy_as_returns_correct_boolean(expected, type_specifier, equal):
    collection = [FHIRPathCollectionItem(value=expected)]
    result = LegacyAs(type_specifier).evaluate(collection, env)
    assert result[0].value == expected if equal else result == []

def test_legacy_as_string_representation():
    expression = LegacyAs('String')
    assert str(expression) == "as(String)"