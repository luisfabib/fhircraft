import pytest 
from collections import namedtuple
from fhircraft.fhir.path.engine.literals import Quantity
from fhircraft.fhir.path.engine.comparison import *
from fhircraft.fhir.path.engine.additional import GetValue
from fhircraft.fhir.path.engine.core import Element,  FHIRPathCollectionItem, Invocation

env = dict()

#-------------
# GreaterThan
#-------------

greater_than_cases = (
    (10, 5, True),
    (10, 5.0, True),
    ('abc', 'ABC', True),
    (Quantity(12, 'm'), Quantity(4, 'm'), True),
    # (Quantity(4, 'm'), Quantity(4, 'cm'), True), # Unit conversion not implemented yet
    ('@2018-03-01', '@2018-01-01', True),
    ('@2018-03', '@2018-03-01', False),
    ('@2018-03-01T10:30:00', '@2018-03-01T10:00:00', True),
    ('@2018-03-01T10', '@2018-03-01T10:30', False),
    ('@T10:30:00', '@T10:00:00', True),
    ('@T10', '@T10:30', False),
    ('@T10:30:00', '@T10:30:00.0', False),
)

@pytest.mark.parametrize("left, right, expected", greater_than_cases)
def test_greater_than_returns_correct_boolean(left, right, expected):
    resource = namedtuple("Resource", ["left", "right"])(left=left, right=right)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = GreaterThan(
        Invocation(Element("left"), GetValue()),
        Invocation(Element("right"), GetValue()),
    ).evaluate(collection, env)
    assert result == [FHIRPathCollectionItem(value=expected)]

def test_greaterthan_string_representation():
    expression = GreaterThan(Element("left"), Element("right"))
    assert str(expression) == "left > right"


#-------------
# LessThan
#-------------


less_than_cases = (
    (10, 5, False),
    (10, 5.0, False),
    ('abc', 'ABC', False),
    (Quantity(4, 'm'), Quantity(40, 'm'), True),
    # (Quantity(4, 'm'), Quantity(4, 'cm'), False), # Unit conversion not implemented yet
    ('@2018-03-01', '@2018-01-01', False),
    ('@2018-03-01T10:30:00', '@2018-03-01T10:00:00', False),
    ('@2018-03-01T10', '@2018-03-01T10:30', True),
    ('@T10:30:00', '@T10:00:00', False),
    ('@T10', '@T10:30', True),
)

@pytest.mark.parametrize("left, right, expected", less_than_cases)
def test_less_than_returns_correct_boolean(left, right, expected):
    resource = namedtuple("Resource", ["left", "right"])(left=left, right=right)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = LessThan(
        Invocation(Element("left"), GetValue()),
        Invocation(Element("right"), GetValue()),
    ).evaluate(collection, env)
    assert result == [FHIRPathCollectionItem(value=expected)]

def test_lessthan_string_representation():
    expression = LessThan(Element("left"), Element("right"))
    assert str(expression) == "left < right"


#----------------
# LessEqualThan
#----------------

less_equal_than_cases = (
    (10, 5, False),
    (2.5, 5.0, True),
    ('abc', 'ABC', False),
    (Quantity(4, 'm'), Quantity(4, 'm'), True),
    (Quantity(12, 'm'), Quantity(4, 'm'), False),
    # (Quantity(4, 'm'), Quantity(4, 'cm'), False), # Unit conversion not implemented yet
    ('@2018-03-01', '@2018-01-01', False),
    ('@2018-03-01T10:30:00', '@2018-03-01T10:00:00', False),
    ('@2018-03-01T10:30:00', '@2018-03-01T10:30:00.0', True),
    ('@T10:30:00', '@T10:00:00', False),
    ('@T10:30:00', '@T10:30:00.0', True),
)

@pytest.mark.parametrize("left, right, expected", less_equal_than_cases)
def test_less_equal_than_returns_correct_boolean(left, right, expected):
    resource = namedtuple("Resource", ["left", "right"])(left=left, right=right)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = LessEqualThan(
        Invocation(Element("left"), GetValue()),
        Invocation(Element("right"), GetValue()),
    ).evaluate(collection, env)
    assert result == [FHIRPathCollectionItem(value=expected)]

def test_lessequalthan_string_representation():
    expression = LessEqualThan(Element("left"), Element("right"))
    assert str(expression) == "left <= right"


#----------------
# GreaterEqualThan
#----------------

greater_equal_than_cases = (
    (10, 5, True),
    (2.5, 5.0, False),
    ('abc', 'ABC', True),
    (Quantity(4, 'm'), Quantity(4, 'm'), True),
    (Quantity(12, 'm'), Quantity(4, 'm'), True),
    # (Quantity(4, 'm'), Quantity(4, 'cm'), False), # Unit conversion not implemented yet
    ('@2018-03-01', '@2018-01-01', True),
    ('@2018-03-01T10:30:00', '@2018-03-01T10:00:00', True),
    ('@T10:30:00', '@T10:00:00', True),
)

@pytest.mark.parametrize("left, right, expected", greater_equal_than_cases)
def test_greater_equal_than_returns_correct_boolean(left, right, expected):
    resource = namedtuple("Resource", ["left", "right"])(left=left, right=right)
    collection = [FHIRPathCollectionItem(value=resource)]
    result = GreaterEqualThan(
        Invocation(Element("left"), GetValue()),
        Invocation(Element("right"), GetValue()),
    ).evaluate(collection, env)
    assert result == [FHIRPathCollectionItem(value=expected)]

def test_greater_equal_than_string_representation():
    expression = GreaterEqualThan(Element("left"), Element("right"))
    assert str(expression) == "left >= right"
