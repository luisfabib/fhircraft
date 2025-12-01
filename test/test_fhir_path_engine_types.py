from collections import namedtuple

import pytest

from fhircraft.fhir.path.engine.core import *
from fhircraft.fhir.path.engine.literals import Date, Quantity
from fhircraft.fhir.path.engine.types import *

env = {'%fhirRelease': "R4"}

# -------------
# Is
# -------------

test_cases = (
    ("ABC", "string", True),
    ("123", "string", True),
    ("", "string", True),
    (123, "string", False),
    # Integer type checking
    (12, "integer", True),
    ("12", "integer", True),
    (-12, "integer", True),
    # UnsignedInt type checking
    (12, "unsignedInt", True),
    ("12", "unsignedInt", True),
    (0, "unsignedInt", True),
    (-12, "unsignedInt", False),
    ("-12", "unsignedInt", False),
    # PositiveInt type checking
    (12, "positiveInt", True),
    ("12", "positiveInt", True),
    (0, "positiveInt", False),
    (-12, "positiveInt", False),
    ("-12", "positiveInt", False),
    # Decimal type checking
    (23, "decimal", True),
    (23.32, "decimal", True),
    ("23.32", "decimal", True),
    ("23", "decimal", True),
    # Boolean type checking
    (True, "boolean", True),
    ("true", "boolean", True),
    (False, "boolean", True),
    ("false", "boolean", True),
    ("invalid", "boolean", False),
    (Date("@2024"), "date", True),
    (Quantity(12, "g"), "Quantity", True),
    # Root element type checking
    (
        dict(id="123", resourceType="Observation"),
        "Observation",
        True,
    ),
    (
        dict(id="123", resourceType="Patient"),
        "Patient",
        True,
    ),
    (
        dict(id="123", resourceType="Condition"),
        "Observation",
        False,
    ),
)


@pytest.mark.filterwarnings("ignore:.*dom-6.*")
@pytest.mark.parametrize("left, type_specifier, expected", test_cases)
def test_is_returns_correct_boolean(left, type_specifier, expected):
    resource = namedtuple("Resource", ["left"])(left=left)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Is(Element("left"), TypeSpecifier(type_specifier)).evaluate(
        collection, env
    )
    assert result[0].value == expected


def test_is_returns_empty_for_empty_collection():
    result = Is(Element("left"), TypeSpecifier("string")).evaluate([], env)
    assert result == []


def test_is_string_representation():
    expression = Is(Element("field"), TypeSpecifier("string"))
    assert str(expression) == "field is string"


@pytest.mark.filterwarnings("ignore:.*dom-6.*")
@pytest.mark.parametrize("left, type_specifier, expected", test_cases)
def test_legacy_is_returns_correct_boolean(left, type_specifier, expected):
    collection = [FHIRPathCollectionItem(value=left)]
    result = LegacyIs(TypeSpecifier(type_specifier)).evaluate(collection, env)
    assert result[0].value == expected


def test_legacy_is_returns_empty_for_empty_collection():
    result = LegacyIs(TypeSpecifier("string")).evaluate([], env)
    assert result == []


def test_legacy_is_string_representation():
    expression = LegacyIs(TypeSpecifier("string"))
    assert str(expression) == "is(string)"


# -------------
# As
# -------------


@pytest.mark.filterwarnings("ignore:.*dom-6.*")
@pytest.mark.parametrize("expected, type_specifier, equal", test_cases)
def test_as_returns_correct_boolean(expected, type_specifier, equal):
    collection = [FHIRPathCollectionItem(value=expected)]
    result = As(This(), TypeSpecifier(type_specifier)).evaluate(collection, env)
    assert result[0].value == expected if equal else result == []


def test_as_returns_empty_for_empty_collection():
    result = As(This(), TypeSpecifier("string")).evaluate([], env)
    assert result == []


def test_as_string_representation():
    expression = As(Element("field"), TypeSpecifier("string"))
    assert str(expression) == "field as string"


@pytest.mark.filterwarnings("ignore:.*dom-6.*")
@pytest.mark.parametrize("expected, type_specifier, equal", test_cases)
def test_legacy_as_returns_correct_boolean(expected, type_specifier, equal):
    collection = [FHIRPathCollectionItem(value=expected)]
    result = LegacyAs(TypeSpecifier(type_specifier)).evaluate(collection, env)
    assert result[0].value == expected if equal else result == []


def test_legacy_as_returns_empty_for_empty_collection():
    result = LegacyAs(TypeSpecifier("string")).evaluate([], env)
    assert result == []


def test_legacy_as_string_representation():
    expression = LegacyAs(TypeSpecifier("string"))
    assert str(expression) == "as(string)"
