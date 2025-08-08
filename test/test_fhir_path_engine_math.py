from collections import namedtuple

import pytest

from fhircraft.fhir.path.engine.additional import GetValue
from fhircraft.fhir.path.engine.core import *
from fhircraft.fhir.path.engine.literals import Quantity
from fhircraft.fhir.path.engine.math import *

# -------------
# Addition
# -------------

addition_cases = (
    (2, 2, 4),
    (2.2, 2.2, 4.4),
    ("AB", "C", "ABC"),
    (Quantity(2, "mg"), Quantity(2, "mg"), Quantity(4, "mg")),
)


@pytest.mark.parametrize("left, right, expected", addition_cases)
def test_addition_returns_correct_logic_boolean(left, right, expected):
    resource = namedtuple("Resource", ["left", "right"])(left=left, right=right)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Addition(
        Invocation(Element("left"), GetValue()),
        Invocation(Element("right"), GetValue()),
    ).evaluate(collection)
    assert result == [FHIRPathCollectionItem(value=expected)]


# -------------
# Subtraction
# -------------

subtraction_cases = (
    (5, 2, 3),
    (3.2, 2.2, 1),
    (Quantity(5, "mg"), Quantity(2, "mg"), Quantity(3, "mg")),
)


@pytest.mark.parametrize("left, right, expected", subtraction_cases)
def test_subtraction_returns_correct_logic_boolean(left, right, expected):
    resource = namedtuple("Resource", ["left", "right"])(left=left, right=right)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Subtraction(
        Invocation(Element("left"), GetValue()),
        Invocation(Element("right"), GetValue()),
    ).evaluate(collection)
    assert result == [FHIRPathCollectionItem(value=expected)]


# -------------
# Multiplication
# -------------

multiplication_cases = (
    (2, 2, 4),
    (2.2, 2, 4.4),
    (Quantity(2, "mg"), Quantity(2, "mg"), Quantity(4, "mg*mg")),
    (Quantity(2, "mg"), Quantity(2, "L"), Quantity(4, "mg*L")),
)


@pytest.mark.parametrize("left, right, expected", multiplication_cases)
def test_multiplication_returns_correct_logic_boolean(left, right, expected):
    resource = namedtuple("Resource", ["left", "right"])(left=left, right=right)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Multiplication(
        Invocation(Element("left"), GetValue()),
        Invocation(Element("right"), GetValue()),
    ).evaluate(collection)
    result = result[0].value if len(result) == 1 else result
    assert result == expected


# -------------
# Division
# -------------

division_cases = (
    (4, 2, 2),
    (5.5, 2, 2.75),
    (5.5, 0, []),
    (Quantity(4, "mg"), Quantity(2, "mg"), Quantity(2, "1")),
    (Quantity(4, "mg"), Quantity(2, "L"), Quantity(2, "mg/L")),
)


@pytest.mark.parametrize("left, right, expected", division_cases)
def test_division_returns_correct_logic_boolean(left, right, expected):
    resource = namedtuple("Resource", ["left", "right"])(left=left, right=right)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Division(
        Invocation(Element("left"), GetValue()),
        Invocation(Element("right"), GetValue()),
    ).evaluate(collection)
    result = result[0].value if len(result) == 1 else result
    assert result == expected


# -------------
# Div
# -------------

div_cases = (
    (5, 2, 2),
    (5.5, 0.7, 7),
    (5, 0, []),
    (Quantity(4, "mg"), Quantity(2, "mg"), Quantity(2, "1")),
    (Quantity(4, "mg"), Quantity(2, "L"), Quantity(2, "mg/L")),
)


@pytest.mark.parametrize("left, right, expected", div_cases)
def test_div_returns_correct_logic_boolean(left, right, expected):
    resource = namedtuple("Resource", ["left", "right"])(left=left, right=right)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Div(
        Invocation(Element("left"), GetValue()),
        Invocation(Element("right"), GetValue()),
    ).evaluate(collection)
    result = result[0].value if len(result) == 1 else result
    assert result == expected


# -------------
# Mod
# -------------

mod_cases = (
    (5, 2, 1),
    (5.5, 0.7, 0.6),
)


@pytest.mark.parametrize("left, right, expected", mod_cases)
def test_mod_returns_correct_logic_boolean(left, right, expected):
    resource = namedtuple("Resource", ["left", "right"])(left=left, right=right)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Mod(
        Invocation(Element("left"), GetValue()),
        Invocation(Element("right"), GetValue()),
    ).evaluate(collection)
    assert round(result[0].value, 4) == round(expected, 4)
