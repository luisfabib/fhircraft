from collections import namedtuple

import pytest

from fhircraft.fhir.path.engine.additional import GetValue
from fhircraft.fhir.path.engine.core import *
from fhircraft.fhir.path.engine.literals import Quantity
from fhircraft.fhir.path.engine.math import *

env = dict()

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
def test_addition_returns_correct_value(left, right, expected):
    resource = namedtuple("Resource", ["left", "right"])(left=left, right=right)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Addition(
        Invocation(Element("left"), GetValue()),
        Invocation(Element("right"), GetValue()),
    ).evaluate(collection, env)
    assert result == [FHIRPathCollectionItem(value=expected)]


def test_addition_string_representation():
    expression = Addition(Element("left"), Element("right"))
    assert str(expression) == "left + right"


# -------------
# Subtraction
# -------------

subtraction_cases = (
    (5, 2, 3),
    (3.2, 2.2, 1),
    (Quantity(5, "mg"), Quantity(2, "mg"), Quantity(3, "mg")),
)


@pytest.mark.parametrize("left, right, expected", subtraction_cases)
def test_subtraction_returns_correct_value(left, right, expected):
    resource = namedtuple("Resource", ["left", "right"])(left=left, right=right)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Subtraction(
        Invocation(Element("left"), GetValue()),
        Invocation(Element("right"), GetValue()),
    ).evaluate(collection, env)
    assert result == [FHIRPathCollectionItem(value=expected)]


def test_subtraction_string_representation():
    expression = Subtraction(Element("left"), Element("right"))
    assert str(expression) == "left - right"


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
def test_multiplication_returns_correct_value(left, right, expected):
    resource = namedtuple("Resource", ["left", "right"])(left=left, right=right)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Multiplication(
        Invocation(Element("left"), GetValue()),
        Invocation(Element("right"), GetValue()),
    ).evaluate(collection, env)
    result = result[0].value if len(result) == 1 else result
    assert result == expected


def test_multiplication_string_representation():
    expression = Multiplication(Element("left"), Element("right"))
    assert str(expression) == "left * right"


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
def test_division_returns_correct_value(left, right, expected):
    resource = namedtuple("Resource", ["left", "right"])(left=left, right=right)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Division(
        Invocation(Element("left"), GetValue()),
        Invocation(Element("right"), GetValue()),
    ).evaluate(collection, env)
    result = result[0].value if len(result) == 1 else result
    assert result == expected


def test_division_string_representation():
    expression = Division(Element("left"), Element("right"))
    assert str(expression) == "left / right"


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
def test_div_returns_correct_value(left, right, expected):
    resource = namedtuple("Resource", ["left", "right"])(left=left, right=right)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Div(
        Invocation(Element("left"), GetValue()),
        Invocation(Element("right"), GetValue()),
    ).evaluate(collection, env)
    result = result[0].value if len(result) == 1 else result
    assert result == expected


def test_div_string_representation():
    expression = Div(Element("left"), Element("right"))
    assert str(expression) == "left div right"


# -------------
# Mod
# -------------

mod_cases = (
    (5, 2, 1),
    (5.5, 0.7, 0.6),
)


@pytest.mark.parametrize("left, right, expected", mod_cases)
def test_mod_returns_correct_value(left, right, expected):
    resource = namedtuple("Resource", ["left", "right"])(left=left, right=right)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Mod(
        Invocation(Element("left"), GetValue()),
        Invocation(Element("right"), GetValue()),
    ).evaluate(collection, env)
    assert round(result[0].value, 4) == round(expected, 4)


def test_mod_string_representation():
    expression = Mod(Element("left"), Element("right"))
    assert str(expression) == "left mod right"


# -------------
# Abs
# -------------

abs_cases = (
    (5, 5),
    (5.5, 5.5),
    (Quantity(5, "mg"), Quantity(5, "mg")),
    (Quantity(5.5, "mg"), Quantity(5.5, "mg")),
    (-5, 5),
    (-5.5, 5.5),
    (Quantity(-5, "mg"), Quantity(5, "mg")),
    (Quantity(-5.5, "mg"), Quantity(5.5, "mg")),
)


@pytest.mark.parametrize("value, expected", abs_cases)
def test_abs_returns_correct_value(value, expected):
    resource = namedtuple("Resource", ["value"])(value=value)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Invocation(Element("value"), Abs()).evaluate(collection, env)
    assert result[0].value == expected


def test_abs_string_representation():
    expression = Invocation(Element("value"), Abs())
    assert str(expression) == "value.abs()"


# -------------
# Ceiling
# -------------

ceiling_cases = (
    (5, 5),
    (5.5, 6),
    (Quantity(5, "mg"), Quantity(5, "mg")),
    (Quantity(5.5, "mg"), Quantity(6, "mg")),
    (-5, -5),
    (-5.5, -5),
    (Quantity(-5, "mg"), Quantity(-5, "mg")),
    (Quantity(-5.5, "mg"), Quantity(-5, "mg")),
)


@pytest.mark.parametrize("value, expected", ceiling_cases)
def test_ceiling_returns_correct_value(value, expected):
    resource = namedtuple("Resource", ["value"])(value=value)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Invocation(Element("value"), Ceiling()).evaluate(collection, env)
    assert result[0].value == expected


def test_ceiling_string_representation():
    expression = Invocation(Element("value"), Ceiling())
    assert str(expression) == "value.ceiling()"


# -------------
# Exp
# -------------

exp_cases = (
    (5, 148.41316),
    (5.5, 244.69193),
    (Quantity(5, "mg"), Quantity(148.41316, "mg")),
    (Quantity(5.5, "mg"), Quantity(244.69193, "mg")),
    (-5, 0.00673795),
    (-5.5, 0.00408677),
    (Quantity(-5, "mg"), Quantity(0.00673795, "mg")),
    (Quantity(-5.5, "mg"), Quantity(0.00408677, "mg")),
)


@pytest.mark.parametrize("value, expected", exp_cases)
def test_exp_returns_correct_value(value, expected):
    resource = namedtuple("Resource", ["value"])(value=value)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Invocation(Element("value"), Exp()).evaluate(collection, env)
    if isinstance(expected, Quantity):
        assert result[0].value.value == pytest.approx(expected.value, rel=1e-5)
        assert result[0].value.unit == expected.unit
    else:
        assert result[0].value == pytest.approx(expected, rel=1e-5)


def test_exp_string_representation():
    expression = Invocation(Element("value"), Exp())
    assert str(expression) == "value.exp()"


# -------------
# Floor
# -------------

floor_cases = (
    (5, 5),
    (5.5, 5),
    (Quantity(5, "mg"), Quantity(5, "mg")),
    (Quantity(5.5, "mg"), Quantity(5, "mg")),
    (-5, -5),
    (-5.5, -6),
    (Quantity(-5, "mg"), Quantity(-5, "mg")),
    (Quantity(-5.5, "mg"), Quantity(-6, "mg")),
)


@pytest.mark.parametrize("value, expected", floor_cases)
def test_floor_returns_correct_value(value, expected):
    resource = namedtuple("Resource", ["value"])(value=value)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Invocation(Element("value"), Floor()).evaluate(collection, env)
    if isinstance(expected, Quantity):
        assert result[0].value.value == pytest.approx(expected.value, rel=1e-5)
        assert result[0].value.unit == expected.unit
    else:
        assert result[0].value == pytest.approx(expected, rel=1e-5)


def test_floor_string_representation():
    expression = Invocation(Element("value"), Floor())
    assert str(expression) == "value.floor()"


# -------------
# Ln
# -------------

ln_cases = (
    (5, 1.60943791),
    (5.5, 1.70474809),
    (Quantity(5, "mg"), Quantity(1.60943791, "mg")),
    (Quantity(5.5, "mg"), Quantity(1.70474809, "mg")),
)


@pytest.mark.parametrize("value, expected", ln_cases)
def test_ln_returns_correct_value(value, expected):
    resource = namedtuple("Resource", ["value"])(value=value)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Invocation(Element("value"), Ln()).evaluate(collection, env)
    if isinstance(expected, Quantity):
        assert result[0].value.value == pytest.approx(expected.value, rel=1e-5)
        assert result[0].value.unit == expected.unit
    else:
        assert result[0].value == pytest.approx(expected, rel=1e-5)


def test_ln_string_representation():
    expression = Invocation(Element("value"), Ln())
    assert str(expression) == "value.ln()"


# -------------
# Log
# -------------

log_cases = (
    (5, 0.698970004),
    (5.5, 0.740362689),
    (Quantity(5, "mg"), Quantity(0.698970004, "mg")),
    (Quantity(5.5, "mg"), Quantity(0.740362689, "mg")),
)


@pytest.mark.parametrize("value, expected", log_cases)
def test_log_returns_correct_value(value, expected):
    resource = namedtuple("Resource", ["value"])(value=value)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Invocation(Element("value"), Log(10)).evaluate(collection, env)
    if isinstance(expected, Quantity):
        assert result[0].value.value == pytest.approx(expected.value, rel=1e-5)
        assert result[0].value.unit == expected.unit
    else:
        assert result[0].value == pytest.approx(expected, rel=1e-5)


def test_log_string_representation():
    expression = Invocation(Element("value"), Log(10))
    assert str(expression) == "value.log(10)"


# -------------
# Power
# -------------

power_cases = (
    (5, 25),
    (5.5, 30.25),
    (Quantity(5, "mg"), Quantity(25, "mg")),
    (Quantity(5.5, "mg"), Quantity(30.25, "mg")),
    (-5, 25),
    (-5.5, 30.25),
    (Quantity(-5, "mg"), Quantity(25, "mg")),
    (Quantity(-5.5, "mg"), Quantity(30.25, "mg")),
)


@pytest.mark.parametrize("value, expected", power_cases)
def test_power_returns_correct_value(value, expected):
    resource = namedtuple("Resource", ["value"])(value=value)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Invocation(Element("value"), Power(2)).evaluate(collection, env)
    if isinstance(expected, Quantity):
        assert result[0].value.value == pytest.approx(expected.value, rel=1e-5)
        assert result[0].value.unit == expected.unit
    else:
        assert result[0].value == pytest.approx(expected, rel=1e-5)


def test_power_string_representation():
    expression = Invocation(Element("value"), Power(2))
    assert str(expression) == "value.power(2)"


# -------------
# Round
# -------------

round_cases = (
    (5, 5.0),
    (5.05, 5.0),
    (5.15, 5.2),
    (Quantity(5, "mg"), Quantity(5.0, "mg")),
    (Quantity(5.05, "mg"), Quantity(5.0, "mg")),
    (Quantity(5.15, "mg"), Quantity(5.2, "mg")),
    (-5, -5.0),
    (-5.05, -5.0),
    (-5.15, -5.2),
    (Quantity(-5, "mg"), Quantity(-5.0, "mg")),
    (Quantity(-5.05, "mg"), Quantity(-5.0, "mg")),
    (Quantity(-5.15, "mg"), Quantity(-5.2, "mg")),
)


@pytest.mark.parametrize("value, expected", round_cases)
def test_round_returns_correct_value(value, expected):
    resource = namedtuple("Resource", ["value"])(value=value)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Invocation(Element("value"), Round(1)).evaluate(collection, env)
    if isinstance(expected, Quantity):
        assert result[0].value.value == pytest.approx(expected.value, rel=1e-5)
        assert result[0].value.unit == expected.unit
    else:
        assert result[0].value == pytest.approx(expected, rel=1e-5)


def test_round_string_representation():
    expression = Invocation(Element("value"), Round(1))
    assert str(expression) == "value.round(1)"


# -------------
# Sqrt
# -------------

sqrt_cases = (
    (5, 2.236067977),
    (5.5, 2.345207879),
    (Quantity(5, "mg"), Quantity(2.236067977, "mg")),
    (Quantity(5.5, "mg"), Quantity(2.345207879, "mg")),
)


@pytest.mark.parametrize("value, expected", sqrt_cases)
def test_sqrt_returns_correct_value(value, expected):
    resource = namedtuple("Resource", ["value"])(value=value)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Invocation(Element("value"), Sqrt()).evaluate(collection, env)
    if isinstance(expected, Quantity):
        assert result[0].value.value == pytest.approx(expected.value, rel=1e-5)
        assert result[0].value.unit == expected.unit
    else:
        assert result[0].value == pytest.approx(expected, rel=1e-5)


def test_sqrt_string_representation():
    expression = Invocation(Element("value"), Sqrt())
    assert str(expression) == "value.sqrt()"


# -------------
# Truncate
# -------------

truncate_cases = (
    (5, 5),
    (5.05, 5),
    (Quantity(5, "mg"), Quantity(5, "mg")),
    (Quantity(5.05, "mg"), Quantity(5, "mg")),
    (-5, -5),
    (-5.05, -5),
    (Quantity(-5, "mg"), Quantity(-5, "mg")),
    (Quantity(-5.05, "mg"), Quantity(-5, "mg")),
)


@pytest.mark.parametrize("value, expected", truncate_cases)
def test_truncate_returns_correct_value(value, expected):
    resource = namedtuple("Resource", ["value"])(value=value)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = Invocation(Element("value"), Truncate()).evaluate(collection, env)
    if isinstance(expected, Quantity):
        assert result[0].value.value == pytest.approx(expected.value, rel=1e-5)
        assert result[0].value.unit == expected.unit
    else:
        assert result[0].value == pytest.approx(expected, rel=1e-5)


def test_truncate_string_representation():
    expression = Invocation(Element("value"), Truncate())
    assert str(expression) == "value.truncate()"
