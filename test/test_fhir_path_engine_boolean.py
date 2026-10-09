from fhircraft.fhir.path.collection import FHIRPathCollection
from collections import namedtuple

import pytest

from fhircraft.fhir.path.engine.additional import GetValue
from fhircraft.fhir.path.engine.boolean import *
from fhircraft.fhir.path.engine.core import *
from fhircraft.fhir.resources.datatypes.R4.primitive import Boolean

env = dict()


# -------------
# And
# -------------

and_boolean_logic_cases = (
    (True, True, True),
    (True, False, False),
    (True, None, []),
    (False, True, False),
    (False, False, False),
    (False, None, False),
    (None, True, []),
    (None, False, False),
    (None, None, []),
    (Boolean(value=True), True, True),
    (True, Boolean(value=False), False),
    (Boolean(value=True), Boolean(value=False), False),
)


@pytest.mark.parametrize("left, right, expected", and_boolean_logic_cases)
def test_and_returns_correct_logic_boolean(left, right, expected):
    print(left, right, expected)
    result = And(
        left=FHIRPathCollection([FHIRPathCollectionItem(left)] if left is not None else []),
        right=FHIRPathCollection([FHIRPathCollectionItem(right)] if right is not None else []),
    ).evaluate(FHIRPathCollection([]), env)
    result = result[0] if len(result) == 1 else result
    assert result == expected


def test_and_string_representation():
    expression = And(Element("left"), Element("right"))
    assert str(expression) == "left and right"


# -------------
# Or
# -------------

or_boolean_logic_cases = (
    (True, True, True),
    (True, False, True),
    (True, None, True),
    (False, True, True),
    (False, False, False),
    (False, None, []),
    (None, True, True),
    (None, False, []),
    (None, None, []),
    (Boolean(value=True), True, True),
    (True, Boolean(value=False), True),
    (Boolean(value=True), Boolean(value=False), True),
)


@pytest.mark.parametrize("left, right, expected", or_boolean_logic_cases)
def test_or_returns_correct_logic_boolean(left, right, expected):
    result = Or(
        left=FHIRPathCollection([FHIRPathCollectionItem(left)] if left is not None else []),
        right=FHIRPathCollection([FHIRPathCollectionItem(right)] if right is not None else []),
    ).evaluate(FHIRPathCollection([]), env)
    result = result[0] if len(result) == 1 else result
    assert result == expected


def test_or_string_representation():
    expression = Or(Element("left"), Element("right"))
    assert str(expression) == "left or right"


# -------------
# Xor
# -------------

xor_boolean_logic_cases = (
    (True, True, False),
    (True, False, True),
    (True, None, []),
    (False, True, True),
    (False, False, False),
    (False, None, []),
    (None, True, []),
    (None, False, []),
    (None, None, []),
    (Boolean(value=True), True, False),
    (True, Boolean(value=False), True),
    (Boolean(value=True), Boolean(value=False), True),
)


@pytest.mark.parametrize("left, right, expected", xor_boolean_logic_cases)
def test_xor_returns_correct_logic_boolean(left, right, expected):
    result = Xor(
        left=FHIRPathCollection([FHIRPathCollectionItem(left)] if left is not None else []),
        right=FHIRPathCollection([FHIRPathCollectionItem(right)] if right is not None else []),
    ).evaluate(FHIRPathCollection([]), env)
    result = result[0] if len(result) == 1 else result
    assert result == expected


def test_xor_string_representation():
    expression = Xor(Element("left"), Element("right"))
    assert str(expression) == "left xor right"


# -------------
# Implies
# -------------

implies_boolean_logic_cases = (
    (True, True, True),
    (True, False, False),
    (True, None, []),
    (False, True, True),
    (False, False, True),
    (False, None, True),
    (None, True, True),
    (None, False, []),
    (None, None, []),
    (Boolean(value=True), True, True),
    (True, Boolean(value=False), False),
    (Boolean(value=True), Boolean(value=False), False),
)


@pytest.mark.parametrize("left, right, expected", implies_boolean_logic_cases)
def test_implies_returns_correct_logic_boolean(left, right, expected):
    result = Implies(
        left=FHIRPathCollection([FHIRPathCollectionItem(left)] if left is not None else []),
        right=FHIRPathCollection([FHIRPathCollectionItem(right)] if right is not None else []),
    ).evaluate(FHIRPathCollection([]), env)
    result = result[0] if len(result) == 1 else result
    assert result == expected


def test_implies_string_representation():
    expression = Implies(Element("left"), Element("right"))
    assert str(expression) == "left implies right"


# -------------
# Not
# -------------

not_boolean_logic_cases = (
    (True, False),
    (False, True),
    (Boolean(value=True), False),
    (Boolean(value=False), True),
)


@pytest.mark.parametrize("value, expected", not_boolean_logic_cases)
def test_not_returns_correct_logic_boolean(value, expected):
    result = Not().evaluate(FHIRPathCollection([FHIRPathCollectionItem(value=value)]), env)
    result = result[0] if len(result) == 1 else result
    assert result == expected


def test_not_string_representation():
    expression = Not()
    assert str(expression) == "not()"
